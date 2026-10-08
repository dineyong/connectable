# P1 수정 독립 검증 및 통합 준비

확인일: 2026-10-09.
검증 대상: `codex/p1-data-trust-fix`, **`4f51e0f8d4b13b4b7a393f6746a70cea0f775072`**.
수정 전 대조: `57dbf2c0a9aed2da85c5f64d674fd737189ee09e`.
보고서 브랜치: `codex/p1-fix-independent-review`.

## 판단

**원래 P1 재현 두 건은 해결됨을 확인했다. 다만 모든 입력·생성 경로의 신뢰성이 완결됐다고 승인하지 않으며 main 병합은 보류를 권고한다.** 기존 정상 데이터는 모두 통과했고 370개 Python·66개 브라우저 테스트도 통과했다. 새로 확인한 빈틈은 URL 인코딩 검사, 단계 간 리다이렉트 메타데이터 처리, 개별 fact 출처의 모델 범위, 파생 링크의 SKU 승격 상태 검사다.

이번 검토는 같은 코드 작성 세션에서 기존 테스트와 별개 입력·전후 커밋 스냅샷을 대조한 검토다. 다른 사람의 독립 승인이나 실물 호환성 검증으로 해석하지 않는다. 코드·데이터·기존 테스트를 수정하지 않았고 새 회귀 테스트도 저장소에 추가하지 않았다. 재현은 메모리 복사, mock 및 임시 폴더에서만 수행했다.

## 1. 수정 전후 차이

[직전 수정 보고서](P1_DATA_TRUST_FIX_REPORT.md) 및 실제 diff를 대조했다.

- `07197a0`: 공통 모델명 대응 및 URL 권위 검사, batch/full/public 검증 경로 연결, 회귀 테스트.
- `53004d1`: 공식 도메인 내부의 미등록 사용자 게시판 제외.
- `4f51e0f`: 결과 보고서.

[build_site_content_v2.py](../scripts/build_site_content_v2.py)는 node·reported_model·대상 제품 모델을 함께 검사하고, 제품 근거의 제조사 URL을 검사한다. [site_content_validation.py](../scripts/site_content_validation.py)는 monitor_ids 및 monitor_links의 DISPLAY node를 대상 모델과 대조하고 모니터 출처 URL을 검사한다. [validate_official_spec_review.py](../scripts/validate_official_spec_review.py)도 공통 URL 규칙을 사용한다.

[data_trust.py](../scripts/data_trust.py)의 대응표는 기존에 확인된 세 제조사 포함 모델명만 인정한다. 미등록 별칭·SKU를 추정해 자동 동일시하지 않는다. URL은 hostname 전체 일치, 등록 경로, HTTPS/포트, 제한 query, 기록된 redirect_chain/final_url을 검사한다. 원문 내용이나 최신 HTTP 목적지를 증명하는 검사와 구별한다.

## 2. 원래 결함별 수정 확인

수정 전 `57dbf2c`를 별도 폴더에 풀어 두 재현을 각각 새 정상 fixture로 다시 실행했다. 두 입력 모두 ACCEPTED였다. 수정 후에는 아래처럼 거부됐다.

| 재현·경로 | 4f51e0f 결과 |
|---|---|
| 후기 node와 reported_model을 함께 OTHER-MODEL로 변경, batch 검증 | MANUAL_REVIEW ValueError |
| 같은 공동 변경, 전체 content 검증 | target model not established by display node |
| 같은 공동 변경, 실제 JS projection 복사 검증 | 같은 오류로 거부 |
| batch 제조사 출처를 example.com으로 변경 | UNKNOWN 제조사 권위 오류 |
| full/public 모니터 출처를 비제조사 URL로 변경 | 거부. 기존 14개 회귀 검사에서도 확인 |
| 공식 재검토 근거를 미등록 Dell 하위 도메인으로 변경 | UNKNOWN 오류 |
| 정상 batch·full/public 콘텐츠·공식 재검토 | PASS |

모델명이 다른 DISPLAY node를 그대로 붙이는 원래 입력은 관련 세 검증 경로에서 차단된다. 내부 review 화면과 legacy 사례 화면은 공식 제품 ID 연결을 갖지 않는 별도 projection이므로 동일한 모델 join 검사 대상은 아니다. 코퍼스의 사용자 모델 표기는 관측 원본이며 이 검사로 제품 사양 승인으로 승격하지 않는다.

## 3. URL 경계 검사 결과

| 입력 유형 | 결과 및 해석 |
|---|---|
| www.dell.com.evil.example, userinfo 위장, 다른 제조사 도메인 | UNKNOWN, 거부 |
| HTTP, 포트444, 인코딩된 dot segment, /support/redirect | UNKNOWN, 거부 |
| 정상 HTTPS :443, 기존 공식 제품·지원·문서 URL | 허용 범위 검사 통과 |
| 기록된 외부 redirect chain / final_url | helper 직접 호출 시 거부 |
| %00 / %0A / %0D 경로 및 raw DEL | **OFFICIAL_URL_SCOPE**, 아래 IR-01 |
| 5회 인코딩한 외부 URL을 language query에 삽입 | **OFFICIAL_URL_SCOPE**, 아래 IR-02 |
| language=%ZZ, 빈 query 구분자 | 허용됨. malformed query/파싱 정규화 경계 검사 부족 |
| 정상 LG 모델 URL에 utm_source 또는 #specifications 추가 | UNKNOWN. 추적 query·fragment를 허용하지 않는 의도된 보수적 정책 |

기존 저장 공식 URL은 모두 통과한다. 추적값·anchor나 미등록 호스트를 가진 URL을 UNKNOWN으로 돌리는 것은 사양이 거짓이라는 판정이 아니다. 새 정상 공식 경로까지 폭넓게 허용한다는 보장은 없다. 근거 위치를 별도 location에 두고 canonical URL을 검토해야 한다. 이번 검토는 공격 형태 URL을 외부 서버로 요청하지 않았다.

### IR-01 — P2: 디코딩된 제어문자 및 raw DEL의 검사 누락

위치: data_trust.py 59–69행. raw 입력의 C0·공백을 검사한 뒤 path를 디코딩하지만 디코딩된 C0를 다시 거부하지 않는다. DEL은 raw 검사에도 포함되지 않는다.

재현:

```python
from scripts.data_trust import official_url_status
for suffix in ('%00', '%0A', '%0D', chr(127)):
    print(official_url_status('https://www.dell.com/support/spec' + suffix, 'Dell'))
# 네 입력 모두 OFFICIAL_URL_SCOPE
```

외부 호스트로 이동한 증거는 아니다. 파서·요청·브라우저 단계마다 다르게 다뤄질 수 있는 입력을 신뢰 범위로 인정하는 계약 빈틈이다. raw/decoded path의 제어문자 및 malformed escape를 일관되게 처리하는 음성 회귀 검사가 필요하다.

### IR-02 — P2: query 디코딩 횟수 한계로 외부 URL 표기 검사 회피

위치: data_trust.py 73–89행. parse_qsl 이후 세 번만 디코딩한다. Dell language 값은 의미상 언어 코드인지 검사하지 않는다.

재현:

```python
from urllib.parse import quote
from scripts.data_trust import official_url_status
v = 'https://evil.example'
for _ in range(5):
    v = quote(v, safe='')
print(official_url_status('https://www.dell.com/support/spec?language=' + v, 'Dell'))
# OFFICIAL_URL_SCOPE
```

실제 Dell endpoint가 이 값을 리다이렉트 목적지로 사용했다는 증거는 없다. **외부 URL 형태를 배제한다는 검사 자체의 회피**만 확인했다. 무제한 디코딩 대신 허용 query 값의 좁은 자료형/형식을 확정하고, 미해결 중첩 인코딩을 UNKNOWN으로 처리하는 수정이 적절하다.

### IR-03 — P2: 생성기 단독 경로에서 원본의 redirect 메타데이터가 누락됨

위치: build_site_content_v2.py 23–26, 29–41행. reference()는 url/title/date/file/ID만 복사한다. pilot 원본은 생성 전에 공통 require_official_source에 전달되지 않는다.

재현은 원본 파일을 변경하지 않는 mock이다.

```python
import copy
from unittest.mock import patch
from scripts import build_site_content_v2 as b
from scripts.data_trust import require_official_source
pilot = b.read(b.INPUTS[0])
s = next(s for s in pilot['sources'] if s['source_id'] == 'SRC-dell-u2723qe')
s['final_url'] = 'https://evil.example/spec'
# require_official_source(s, 'Dell', 'raw')는 ValueError
read = b.read
with patch.object(b, 'read', side_effect=lambda p:
                  copy.deepcopy(pilot) if p == b.INPUTS[0] else read(p)):
    result = b.build()  # 통과
assert 'final_url' not in result['monitors'][0]['source_refs'][0]
```

**중요한 상위 방어:** 같은 변형을 `validate_connection_model_pilot.validate(pilot)`에 넣으면 `$.sources[0].final_url: unknown field`로 거부된다. 현재 pilot Schema는 final_url을 허용하지 않는다. 따라서 모든 원본 검사까지 실행한 전체 CI를 이 입력이 통과했다고 주장할 수 없다. 현재 원본에서 실제 외부 리다이렉트가 기록됐다는 발견도 아니다.

발견 내용은 생성기를 단독 호출하면 지원하지 않는 메타데이터를 거부하지 않고 버린다는 점이다. source_file 조회 역시 original URL만 대조한다. 수정은 원본 envelope 검증을 생성 전에 강제하거나, 허용하는 체인 자료형을 별도로 설계한 뒤 검증 전에 누락시키지 않는 방향이어야 한다. 현재 Schema를 몰래 완화하거나 가짜 체인을 원본에 추가하면 안 된다.

### IR-04 — P2: 같은 제조사의 다른 제품 문서를 fact 근거로 붙일 수 있음

제조사 권위와 제품별 근거 범위는 별개다. validate_content는 local source ID와 URL·파일 관계를 검사하지만 그 source가 해당 모델 fact를 설명하는지 검사하지 않는다.

재현:

```python
import copy
from scripts.build_site_content_v2 import build
from scripts.site_content_validation import validate_content
x = build()
# 기존 실제 G2724D 공식 record를 U2723QE의 source 목록에 추가
s = copy.deepcopy(x['monitors'][2]['source_refs'][0])
x['monitors'][0]['source_refs'].append(s)
x['monitors'][0]['features'][0]['source_refs'] = [s['record_id']]
validate_content(x)  # 통과
```

두 URL 모두 Dell이고 source_file의 실제 record/URL에도 일치하므로 호스트 검사로 해결되지 않는다. 현재 정상 생성기가 이 잘못된 연결을 만들지는 않으며 build --check는 임의 수정된 산출물과 정상 재생성 값의 차이를 감지할 수 있다. **단독 content/projection 검증을 충분한 제품 근거 승인으로 쓰면 안 되는 이유**다. 원본 product/fact/source binding 또는 동등한 model_scope 검사를 요구하는 회귀가 필요하다.

## 4. 남은 P2와 통합 전 필수 여부

| 항목 | 영향 | 통합 기준 권고 |
|---|---|---|
| IR-01/02 URL 정규화/인코딩 | 좁은 URL 정책에도 malformed/숨은 외부 표기가 통과 | 검증 계약 보강 후 통합 권고. 외부 redirect exploit으로 과장하지 않음 |
| IR-03 생성기 원본 검증 경계 | 단독 생성과 전체 upstream 검사의 방어 수준 차이 | 생성 전 원본 검증 또는 의존 검증 실행을 필수 gate로 명시 |
| IR-04 fact 모델 출처 범위 | 제조사만 같으면 잘못된 제품 근거가 붙을 수 있음 | content 단독 승인을 허용하지 않고 binding/재생성 gate 확정 |
| public_status/protocol mode·SKU 상태 | 형식 통과와 공개 승인 보류가 다르게 적용될 수 있음 | 현재 보류 상태를 입력/파생에서도 거부 검사하기 전 품질 승인 보류 |
| 수동 문장 및 부분 검토 승격 | MANUAL_REVIEW 문장과 Cross 공급 필터의 의미 차이 | 연구용 UNKNOWN 원본 유지 가능. 공개 콘텐츠 승격 전 필수 |
| LG RATED/UP_TO·지역 SKU | 기존MY96W RATED와 별도LV96W UP_TO가 분리됨 | 값을 임의 통일하지 않음. 공개 적용·표시 승격 전에 검토 |
| 실시간 redirect 확인 | 오프라인 helper로 최신 HTTP 목적지 증명 불가 | 지금 엔진/네트워크 기능 확대 불필요. 향후 수집 절차에 최종 목적지 기록 필수 |
| CI 및 미커밋 문서 | codex branch push에 CI trigger 없음; 최신 README/GP 문서 로컬만 존재 | 통합 PR checks 실행과 문서 소유자 검토 필수 |

SKU 상태 재현도 수행했다. 정상 첫 monitor_link의 `variant_match='EXACT_SKU'`, `match_scope='SKU'`로 바꿔 validate_content에 전달하면 통과한다. batch 검증은 MODEL_ONLY/UNKNOWN을 요구하므로 동일하지 않은 상태 경계다. 실제 현재 링크는 계속 MODEL_ONLY/UNKNOWN이며 공개 SKU 승인으로 바뀌지 않았다.

공개 UNKNOWN·사람 승인 골든0은 보존된다. 테스트 개수로 공식 원문의 진실, 사용자 관측의 재현성, 지역 SKU 동일성, 실물 호환 성공을 계산할 수 없다.

## 5. 실제 전체 테스트와 정상 회귀

검증 커밋을 git archive로 저장소 밖에 풀고 전체 테스트를 재실행했다. 브라우저 캡처는 임시 폴더에서 생성해 기존 목업/스크린샷에 쓰지 않았다. 동일 package-lock 의존성·Chromium 설치를 사용했다.

- `python3 -m unittest discover -s tests -q`: **370 PASS**, 4.604초. v1 CSV·영어 예시·v2 JSONL도 PASS.
- `npm run test:e2e`: **66 PASS**, 26.5초. desktop/mobile Chromium이며 실제 Safari/실물 검증이 아니다.
- `python3 scripts/build_site_content_v2.py --check`: PASS.
- `python3 scripts/validate_official_spec_review.py`: PASS, 모델 범위10·부분검토2.
- `python3 scripts/path_instance_v1.py --check`: PASS, 내부후보5·승인0.

정상 6모니터·38기록·3가이드, 네 기존 모델 연결, 10 공식 재검토 assertion은 유지됐다. 기존 370개 테스트에는 위 새 IR 사례가 포함되지 않아 전체 PASS와 검수 빈틈 발견은 모순되지 않는다. 새 입력을 지속 회귀 테스트로 추가하는 작업은 승인된 다음 수정 배치에서 진행해야 한다.

임시 실행 로그: `/tmp/connectable-p1-review-python.log`, `/tmp/connectable-p1-review-e2e.log`. 추가 probe 결과: `/tmp/connectable-p1-independent-probes.json`. 임시 파일은 지속 근거가 아니므로 재현 절차와 결과를 이 보고서에도 기록했다.

## 6. main과 통합 위험

원격 heads 조회 시 main은 `c58dee5f3d1222d49e598dddbac5c8c6a7b4b8f0`, P1 branch는 `4f51e0f8d4b13b4b7a393f6746a70cea0f775072`이며 로컬 tip과 일치했다. main은 검증 대상의 조상이며 `git rev-list --left-right --count main...4f51e0f`는 **0 / 41**이다.

main 대비 **155파일, 58,341줄 추가, 2줄 삭제**의 누적 변경이다. 큰 수에는 데이터·archive·파생 콘텐츠가 포함돼 코드 위험을 줄 수와 동일시하지 않는다. P1만 반영하는 작은 diff가 아니라 이전 조사·사이트·검증 작업 전체가 통합되는 것이다.

기술적으로 fast-forward가 가능하며 현재 주요 작업 브랜치의 선행 변경은 모두 포함돼 있다. 선행 브랜치를 다시 cherry-pick할 필요가 없다. 하지만 다음이 위험이다.

- 생성/원본 검증을 따로 실행하며 어느 단계가 승인 기준인지 불명확해지는 문제.
- 생성 JSON·JS의 의미가 맞아도 출처 truth와 모델 scope를 보증하지 못하는 문제.
- 현재 로컬 README·DECISIONS 변경 및 GP 검토 문서와 원격 기준의 차이.
- workflow는 research branch push와 pull_request에만 실행되므로 현재 codex push 성공은 CI 성공 증거가 아님.
- Git merge 성공과 공개 운영/사양 정확성 승인 혼동.

**main 병합 판단: 기술적 YES, 품질 승인 보류.** 원래 P1은 차단됐지만 위 추가 검증 경계 및 보류 상태 gate를 보강하거나 통합 후보의 필수 검증 조건으로 확정한 뒤 고정 SHA를 재검토해야 한다. 모든 미확인 사양을 숫자로 채우거나 실시간 네트워크 기능을 구현해야 연구용 기준을 통합할 수 있다는 뜻은 아니다. 미확인/부분 검토 상태 보존은 계속 필요하다.

권장 순서: IR 입력 회귀 작성 → URL 입력 계약 보강 → 생성 전 원본 검증/binding 확정 → public/SKU 보류 gate 및 CI 확인 → 소유 문서 정리 → 통합 후보 고정 SHA 전체 재검증 → 사용자 main 승인 검토. 이번 단계에서는 어떠한 수정·main 병합·공개 배포도 하지 않았다.

## 7. 보존 및 보고서 Git 기록

작업 시작 시 기존 추적 파일과 로컬 문서 hash를 저장했다. 사용자 README·DECISIONS 수정 및 미추적 통합 감사/GP 문서는 그대로 보존하고 커밋에서 제외한다. 이번 branch diff에는 이 보고서만 포함한다. 최종 보존·내부 경로 검사 결과는 아래 기록한다. 보고서 commit/push는 현재 별도 branch에만 수행하며 main과 P1 수정 branch를 변경하지 않는다.

최종 검사: 기존 파일 **164개 모두 SHA-256 일치**, 내부 로컬 링크 **5개 존재**, `git diff --check` 통과. 새 산출물은 이 보고서 한 파일이다.
