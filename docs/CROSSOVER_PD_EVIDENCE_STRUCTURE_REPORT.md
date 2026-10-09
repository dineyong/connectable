# 크로스오버 PD 공식 이미지 근거 구조화

확인일: 2026-10-09. 기준 커밋: `9a2739e`.
작업 브랜치: `codex/crossover-pd-evidence`. main 병합·공개 배포 없음.

## 결과와 적용 범위

[후속 조사](OFFICIAL_GAP_FOLLOWUP_REPORT.md)에서 직접 확인한 크로스오버 27ULD950의 PD 65W 표시를 [별도 근거 배치](../data/official/crossover_pd_followup_2026-10-09.json)에 기록했다. [전용 스키마](../schemas/crossover-pd-evidence.schema.json)는 이 한 배치의 제한된 계약이며 정식 제품 catalog나 범용 공식 이미지 스키마를 대체하지 않는다.

| 구분 | 기존 원본 | 새 보충 근거 |
|---|---|---|
| 연결 | `crossover-27uld950:site-2` | `related_fact_id`와 원본 전체 fact SHA-256 |
| 전력 | UNKNOWN, 상품명 PD65 | 제조사 기능 표의 65W |
| 의미 | PRODUCT_LABEL_ONLY | MANUFACTURER_STATED, 연결기기 충전 OFFER |
| 공급 포트 | UNKNOWN | UNKNOWN |
| 최대·정격 qualifier | 확인 없음 | 확인 없음; UP_TO/RATED 승격 금지 |
| 적용 | 기존 화면과 역사적 부분 확인 | SUPPLEMENTAL_EVIDENCE, NOT_APPLIED |
| 승인 | 공개 UNKNOWN | PENDING_HUMAN_REVIEW, 공개 UNKNOWN, 호환성 사용 NO |

`confirmed_fields`는 과거 에이전트가 원문에서 읽은 표기의 범위다. 사람 승인, 한국 판매 SKU 동일성 승인, 특정 Mac 실제 충전 결과가 아니다. 원본 payload와 새 보충 payload가 다르므로 역사적 재확인 검증기의 동등성 규칙을 완화하지 않고 별도 검증기로 분리했다. 숫자가 확보됐다는 이유로 원본을 변경하거나 공급 필터에 넣지 않는다.

## 출처·시간·참조 계약

- 공식 제품 페이지: [27ULD950](https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757).
- 페이지에서 확인한 두 번째 상세 이미지: [공식 이미지](https://www.crosslcd.co.kr/data/editor/2411/047dd0567fcc29d7226521dd0b0f9f78_1732598597_5708.jpg).
- 위치: 이미지 앞부분 편의 특별기능 표의 PD 65W 칸.
- [최소 구간 캡처](evidence/crossover-27uld950-pd65-followup.jpg)의 기존 바이트를 SHA-256으로 연결한다. 원본 전체 이미지를 추가 저장하지 않았다.
- DIRECT_CHECK와 2026-10-09는 이전 조사에서 실제 확인한 시간·방법을 계승한다. 이번 구조화 작업을 별도의 재접속이나 사람 확인으로 기록하지 않았다.

제품 ID → 정확한 모델 → 기존 fact/hash → 기존 fact가 인용한 공식 제품 페이지 → 직접 관찰한 이미지 URL → 로컬 캡처/hash → 보충 assertion을 검사한다. 로컬 객체 ID 중복·빈 근거·깨진 참조·추가 필드·잘못된 날짜·개인정보 패턴도 거부한다.

공식 이미지 URL은 기존 일반 공식 route 자동 승인 대상이 아니다. [검증기](../scripts/crossover_pd_evidence.py)는 기존 제품 페이지 정책을 유지하고, 이미 관찰한 제품 페이지/이미지 URL의 정확한 조합만 제한적으로 허용한다. 같은 제조사 호스트의 임의 이미지, 다른 상품 ID, 유사 도메인, URL 변형은 허용하지 않는다. 이미지 경로 전반의 allowlist는 확장하지 않았다.

캡처 경로는 기존 발췌 파일로 한정하며 경로 탈출·절대 경로·심볼릭 링크·바이트 해시 불일치를 거부한다. 원본 데이터도 기존 검증을 통과해야 하고 원본 fact가 달라지면 검토를 다시 해야 한다. 네트워크 요청이나 리다이렉트 자동 추적은 수행하지 않는다.

## 검증

[회귀 테스트](../tests/test_crossover_pd_evidence.py) 19개를 추가했다. 계약 적용 전 임시 무검증 구현에서 16개 테스트를 실행해 부정 입력 19개 실패를 확인했고, 실제 검증 구현 후 모든 테스트가 통과했다. 이는 새 계약의 거부 동작 검증이며 기존 운영 검증기에 동일한 결함이 있었다는 주장은 아니다.

- `python3 -m unittest discover -s tests -q`: 411개 통과, 19.349초. 기존 392개 유지.
- `python3 scripts/crossover_pd_evidence.py`: 통과.
- `python3 scripts/validate_official_spec_review.py`: 기존 assertion 10개·부분 확인 2개 통과.
- `python3 -m scripts.content_review`: 기존 공개 보류 검토 체계 통과.
- `python3 scripts/build_site_content_v2.py --check`, `python3 web/derive-site-content.py --check`: 원본·파생 화면 재현성 통과.
- `npm run test:e2e`: 데스크톱·모바일 합계 72개 통과, 52.1초.
- 문서 내부 경로·민감값 패턴·`git diff --check`: 통과. 테스트의 이메일은 거부 검사용 가상 문자열이다.
- [작업 브랜치 CI](https://github.com/dineyong/connectable/actions?query=branch%3Acodex%2Fcrossover-pd-evidence): push 후 실행하며 최종 응답에서 해당 실행의 실제 성공 여부와 링크를 보고한다.

브라우저 테스트는 Git 기준선과 이번 변경만 복사한 임시 디렉터리에서 실행해 저장소의 기존 스크린샷을 덮어쓰지 않는다. CI에도 별도 검증 명령을 추가했다. 원본 사양·코퍼스·후기·화면·과거 검토 배치·검토 ledger·사용자 미커밋 문서는 모두 보존한다.

## 남은 위험과 다음 단계

1. 오프라인 검증은 직접 확인 당시의 기록을 연결할 뿐, 현재 웹 페이지의 이미지 포함 관계·리다이렉트·문구의 진실성을 새로 증명하지 않는다. 캡처와 기록을 함께 위조하면 사람이 원문을 대조해야 한다. 해시는 일치 검사이며 출처 인증 서명이 아니다.
2. 전압·전류 profile, 최대/정격 qualifier, 정확한 공급 포트와 동시 소비 예산, 세부 SKU/revision, 실제 호스트 수전은 미확인이다.
3. 이 제한된 배치는 다른 제품 이미지의 자동 수집·승인에 재사용할 범용 정책이 아니다. 새 근거는 별도 검토가 필요하다.
4. V32UE 숫자 사양과 LG 한국 SKU/전력 qualifier 공백은 이번에 해결하거나 변경하지 않았다.
5. 다음 단계는 사람이 이 보충 근거의 확인 범위를 검토하고 화면에 어떻게 별도로 표시할지 결정하는 것이다. 기존 원본·역사 배치의 조용한 승격이나 자동 공개 승인은 하지 않는다.

최종 커밋은 이 보고서를 포함하는 Git 이력에서 확인한다.
