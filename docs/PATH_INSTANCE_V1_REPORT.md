# Path Instance v1 내부 실행 및 검토 보고서

작성일: 2026-10-08. 기존 stress pilot은 사용자 검토로 통과했다.
이번 결과는 운영 엔진 채택이나 새로운 골든 5건의 사람 승인에 해당하지 않는다.

## 파일과 기준

- [경로 인스턴스](../data/rules/path_instances_v1.json): 계획 구성 5건의 기준 원본
- [인스턴스 스키마](../schemas/path-instance-v1.schema.json): 이번 내부 검토 슬라이스만 검증
- [검증 및 내부 평가](../scripts/path_instance_v1.py)
- [회귀 테스트](../tests/test_path_instance_v1.py)
- [5건 검토 자료](PATH_INSTANCE_GOLD_BATCH_1_REVIEW.md): 포트·edge·조건·claim URL·해시

기존 [경로 모델 제안](CONNECTION_PATH_MODEL_V1_PROPOSAL.md), Mac catalog,
별도 pilot, 사용자 코퍼스는 보존한다. 이번 인스턴스 스키마는 기존 제안의 대체나
정식 공개 판정 스키마가 아니다. 제품별 claim은 기존 두 공식 자료 원본을 참조한다.

## 포트 바인딩

포트는 기기 로컬 ID를 가진다. 커넥터·claim 참조·식별 범위를 별도로 기록한다.
`PORT_CLASS_MEMBER`는 공식 자료가 보장하는 포트 종류의 한 구성원을 선택했다는 뜻이며,
기기 좌우 위치나 TB1 실크 인쇄 위치가 검증됐다는 뜻이 아니다. 정확한 위치가 필요한
경로는 추가 근거가 필요하다. `DOCUMENTED_PORT`도 claim 소유 제품만 검사하며 공식
포트 위치 템플릿에 대한 완전한 대조는 아직 구현하지 않았다.

USB-C 커넥터 자체로 영상 능력을 부여하지 않는다. PHYSICAL은 기기간 접속,
INTERNAL_ROUTING은 같은 기기 내부 영상 전달을 나타낸다. 변환 claim 방향과
포트별 HDMI/DP 프로파일을 검증한다. 내부 edge는 계획상의 기능 경로이며
칩셋 배선이나 실제 사용 성공을 새로 관측한 사실이 아니다.

## 최소 predicate

EQ / NEQ / VERSION_GTE와 제한된 context key만 지원한다.
사실에 포함된 OS 제외, macOS 최소 버전, 드라이버 필수, 덮개/내장 화면/전원,
DSC 조건에서만 predicate를 만들 수 있다. 다른 제품 조건과 근거 없는 조건을 거부한다.
세 값 TRUE / FALSE / UNKNOWN을 유지한다. 14.10과 14.3을 수치로 비교하며
미상 또는 비정규 버전은 UNKNOWN이다. 현재 OS_VERSION_GTE는 macOS 자료에 근거한
범위에서만 사용한다. GPU·revision·firmware와 임의 논리 조합은 추가하지 않았다.

## 독 routing과 동시성

물리 출력 포트 수와 독립 스트림 한도는 다르다. resource는 공식 ROUTING claim의
aggregate 한도를 참조하고, 해당 출력 뒤의 목표 화면만 집계한다.
한도 이내는 성공 보증이 아니다. 선택한 포트 쌍의 채널 매핑, MST/TB 공유 대역폭,
색상·DSC 협상은 아직 검증되지 않았다. CHANNEL_MAPPING_KNOWN 입력을 거부한다.
단일 포트의 최대 주사율을 동시 구성 보증으로 합성하지 않는다.

## PD 최소 흐름

영상 edge와 별도로 전력 방향을 기록한다. OFFER / PASS_THROUGH /
TRANSPORT_LIMIT / REQUIREMENT_UNKNOWN을 구분한다. 서로 다른 기기 사이 전력 edge는
실제 계획 접속 edge가 있어야 한다. 케이블 내부 역방향 전달은 영상 방향과 독립이다.
Dell 90W 공급과 Apple 케이블 100W 상한에서 기록 상한 90W를 표시하지만
Mac 수전·협상·전원 장치·독 자체 소비가 미확정이므로 충전 결과는 UNKNOWN이다.
Belkin 60W pass-through는 실제 제공 전원이나 충전량이 아니다.

현재 상한은 인스턴스에 기록된 한도들의 최솟값을 표시하는 진단값이다.
다중 전원 분기·예산·전력 경로의 완전한 연속성/주기 검증과 USB-PD 협상은
구현하지 않았다. 해당 진단값으로 충전 가능 여부나 공급 능력을 승인하면 안 된다.

## 실행 결과와 골든 승인

| ID | 계획 | 구분 | 내부 후보 | 공개 |
|---|---|---|---|---|
| PI-001 | GP-02 | Air M1 → USB-C/DP 어댑터 → Dell DP | UNKNOWN | UNKNOWN |
| PI-002 | GP-03 | Air M1 → Belkin → 미상 HDMI 케이블 → Dell HDMI | UNKNOWN | UNKNOWN |
| PI-003 | GP-07 | Air M2 → PARTIAL TB4 케이블 → Dell USB-C, PD 흐름 | UNKNOWN | UNKNOWN |
| PI-004 | GP-06 | Air M1 → DisplayLink 독 → 미상 DP 케이블 → Dell 2대 | UNKNOWN | UNKNOWN |
| PI-005 | GP-25 | Air M1 → MST 허브 → 미상 HDMI 케이블 → Dell 2대 | INCOMPATIBLE | UNKNOWN |

PI-005는 공식 macOS 제외 조건과 Air M1 네이티브 출력 수 제약이 각각 충돌한다.
PI-004는 DisplayLink라 네이티브 화면 수 규칙을 적용하지 않는다. 드라이버가 미상이고
케이블·채널 배정도 미확정이다. 케이블 식별 기준은 완화하지 않았다.

검토안과 실행 결과가 5건 일치해도 acceptance 5/5로 계산하지 않는다.
골든은 **검토용 바인딩 5건 / 사람 승인 0/30**이다. 기존 30개 계획의 정답 칸은
비워둔다. 사용자 이전 pilot 통과 승인으로 이번 새 조합 승인을 대신하지 않는다.

## 검증

```sh
python3 -m unittest discover -s tests -q
python3 scripts/validate_question_corpus.py
python3 scripts/validate_question_corpus_v2.py
python3 -m scripts.validate_official_products
python3 scripts/validate_connection_model_pilot.py
python3 scripts/path_instance_v1.py --check
python3 scripts/path_instance_v1.py
```

Python 총 216개 통과(기존 186 + 신규 30). v1/v2·catalog·pilot·경로 검증 통과.
참조 무결성, 중복 ID, 변환 방향, 포트별 프로파일, 영상 순환,
물리 포트 중복 접속, 드라이버/OS 미상, 전력 모드 혼동, 접속 없는 전력 흐름을 검사한다.
요청·근거 해시와 규칙 버전을 반환하며 검토안의 예상 결과는 평가 입력에서 제외한다.
문서 로컬 경로·JSON 구문·개인정보/비밀 패턴·diff를 추가 점검한다.
기존 데이터 및 사이트 파일은 변경하지 않았다. UI 변경이 없으므로 브라우저 테스트는 재실행하지 않았다.

## 남은 범위와 다음 순서

1. 사람에게 5건의 근거/조건/UNKNOWN 이유와 독립 기대 결과를 검토받는다.
2. 정확한 포트 위치·채널 배정이 필요한 사례를 선별하고 근거를 보충한다.
3. 동일 capability class를 케이블 식별 대체로 허용할지는 골든 UNKNOWN 분포를 보고 결정한다.
4. timing·색상·lane·encoding·DSC·공유 대역폭·PD 예산은 명시적 추가 근거 후 확장한다.

공개 COMPATIBLE, 대량 제품 수집, 사용자 질문 추가 수집, main merge는 하지 않았다.


GP-02/03 연결은 확보된 Dell G2724D를 사용하는 QHD60 축소 변형이다.
원래 계획의 4K60 충족 또는 해당 골든 시나리오 완료로 계산하지 않는다.
원래 목표의 최종 승인에는 별도의 4K 화면·포트 근거 바인딩이 필요하다.
