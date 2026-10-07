# 실제 제품 9개로 연결 모델 검증

2026-10-08 · 시작 커밋 6c8dd80 · research/question-corpus-foundation.
목적은 운영 제품 DB 확장이 아니라 제안 모델의 손실과 typed capability 경계를 찾는 것이다.
공식 원문을 직접 확인한 9개 제품/제품군의 사실 29개를 별도 RESEARCH_PILOT 파일에 기록했다.
골든 승인 0/30, 공개 COMPATIBLE 판정 0건을 유지한다.

## 기준 파일

- [조사 파일](../data/official/connection_model_pilot.json): 이번 9개 조사 원본. 기존 Mac catalog에 합치지 않는다.
- [조사 파일 스키마](../schemas/connection-model-pilot.schema.json).
- [typed capability v1 스키마](../schemas/typed-capability-v1.proposed.schema.json): 이번 파일에 적용하는 구조, 운영용 정식 path 스키마 채택은 아니다.
- [검증기](../scripts/validate_connection_model_pilot.py)와 [회귀 테스트](../tests/test_connection_model_pilot.py).
- 기존 [경로 v1 제안](CONNECTION_PATH_MODEL_V1_PROPOSAL.md), [골든 계획](CONNECTION_GOLD_SET_PLAN.md)과 공식 Mac 5개는 유지한다.

## 직접 확인한 제품과 출처

전 제품 확인일 2026-10-08, 최종 검수 PENDING_HUMAN_REVIEW.
해외 자료를 한국 사양으로 간주하지 않는다. UNSPECIFIED는 문서의 지역 미기재이며 전세계 동일 사양이라는 뜻이 아니다. 이름은 원문 모델/제품군 그대로 보존했다.

| 제품·종류 | 출처·지역·등급 | 저장한 주요 사실 | 모델이 드러낸 문제 |
| --- | --- | --- | --- |
| Dell U2723QE · 모니터 | [Dell 사양](https://www.dell.com/en-gb/shop/dell-ultrasharp-27-4k-usb-c-hub-monitor-u2723qe/apd/210-bcxk/monitors-monitor-accessories) · GB · A | 패널 4K60, 영상 upstream DP 1.4 Alt Mode와 90W, downstream 15W | 같은 USB-C 모양과 서로 다른 영상/전원 역할 |
| LG 27UP850-W · 모니터 | [LG 사양](https://www.lg.com/my/monitors/ultrafine-uhd-4k-5k/27up850-w/) · MY · A | 패널 4K60, USB-C DP Alt Mode와 96W 표기 | 패널 모드와 모든 입력 포트의 모드를 동일시할 수 없음 |
| Dell G2724D · 모니터 | [Dell 사양](https://www.dell.com/en-us/shop/dell-27-gaming-monitor-g2724d/apd/210-bhxc/monitors-monitor-accessories) · US · A | DP QHD165, HDMI QHD144 | 동일 화면의 입력별 최대 주사율 분리 필요 |
| CalDigit TS4 · 독 | [CalDigit 사양](https://www.caldigit.com/thunderbolt-station-4/) · 지역 미기재 · A | 호스트에 따른 듀얼 출력, 고해상도 DSC 조건, 호스트 98W | 소스 칩·호스트/화면 DSC·공유 경로 전제 |
| Plugable UD-6950H · 독 | [Plugable 사양](https://plugable.com/products/ud-6950h/) · US · A | DisplayLink·드라이버, 최대 독립 2대 4K60, 호스트 충전 없음 | DP/HDMI 4개를 독립 4대로 계산하면 오류 |
| StarTech MST14CD122HD · 허브 | [공식 PDF](https://media.startech.com/cms/pdfs/mst14cd122hd_datasheet.pdf) · 지역 미기재 · A | MST 듀얼 4K60/DSC, macOS 비호환 표기, bus power, PD 통과 없음 | OS·MST·DSC·독 자체 전원과 호스트 충전 분리 |
| Cable Matters 201036 · 케이블 | [공식 KB 79](https://kb.cablematters.com/index.php?EntryID=79&View=entry) · 지역 미기재 · B | USB-C→DP, DSC 1.2, 조건부 8K60 | DSC 지원 표기와 encode/decode/pass-through 역할은 다름 |
| Belkin AVC002BK-BL / AVC002btBK · 어댑터 | [Belkin 사양](https://www.belkin.com/tw/en/p/usb-c-to-hdmi-charge-adapter/P-AVC002.html) · TW · A | USB-C→HDMI 4K60, 별도 USB-C 전원 입력, PD 통과 최대 60W | 영상 방향과 반대 전원 경로, PD 공급자 필요 |
| Apple Thunderbolt 4 Pro Cable 제품군 · 케이블 | [Apple 지원](https://support.apple.com/en-gb/118204) · GB · B | TB4/3·USB4 최대 40Gb/s, HBR3 영상, 전력 전달 100W | 데이터 속도를 영상 payload로 사용하면 오류; SKU/길이 미상 |

A는 제조사가 명시한 사양 섹션, B는 공식 지원 안내다. 제조사 페이지의 판매 문구·리뷰·가격은 저장하지 않았다.
Apple 케이블은 제품군 식별 PARTIAL이다. 다른 제품의 모델 표기는 EXACT이며 리비전/국가별 동일성까지 검증됐다는 뜻은 아니다.
Plugable 제품은 원문에서 단종으로 표시되지만 다양한 routing을 검증하는 조사 대상으로 유지한다. 구매 추천이 아니다.
Cable Matters KB의 갱신일은 2022-08-17이며 오래된 ‘특정 GPU만 지원’ 설명은 현재 일반 사양으로 승계하지 않았다.
Apple 지원의 게시일 2024-11-25를 기록했다. 나머지 갱신일·원문 스냅샷은 미상이다.

## 접근 실패와 제외한 정보

- Dell 공식 U2723QE 데이터시트 PDF 요청은 403. 우회·미러 복제 없이 별도로 공개된 Dell HTML 사양을 확인했다.
- LG UK 페이지는 열렸지만 필요한 상세 사양을 추출 결과에서 확인하지 못해 MY 공식 문서로 조사했다. 지역 차이를 숨기지 않는다.
- Cable Matters 판매 페이지는 최초 열림 뒤 재조회에서 timeout/오류. 실제 읽을 수 있는 공식 KB를 사용했고 검색 요약으로 보충하지 않았다.
- Dell 두 번째 USB-C upstream의 ‘data only’와 DSC 지원은 이번에 읽은 HTML에서 명시를 확인하지 못해 저장하지 않았다.
- 6K/8K 라벨을 픽셀 수로 바꾸지 않고 색 깊이·chroma·레인 수·encoding·PD 전압/전류도 추정하지 않았다.
- robots 정책에 따른 대량 자동 수집은 하지 않았다. 공개 페이지 소수 수동 열람 수준의 조회만 수행했다.

## v1이 깨진 지점과 이번 구조

기존 v1의 value_label/amount/unit만으로는 다음 관계를 기계적으로 검사할 수 없다.
현재 v1을 덮어쓰지 않고 typed facts를 별도 보존했다. 회귀 테스트는 실제 조사 payload를 기존 capability에 넣으면
unknown field로 거부됨을 확인한다. summary로만 우회 저장해서 표현됐다고 주장하지 않는다.

| 기존 한계 | 확정한 이번 typed payload | 적용 사례·남은 한계 |
| --- | --- | --- |
| 모든 해상도는 하나의 결과 값처럼 보임 | VIDEO_PROFILE.scope=PANEL/PORT/ADAPTER/SIMULTANEOUS, 픽셀 또는 원문 라벨, Hz, display_count | G2724D 입력별 165/144; 패널 모드는 전체 입력 보증 아님 |
| DSC 문자열에 주체·조건 없음 | DSC.support/version/role, VIDEO_PROFILE.requirements target·feature·version | Cable Matters 역할은 UNSPECIFIED; 지원 표기로 역할 추론 금지 |
| 전력 W가 공급·전달·통과를 혼합 | POWER_TRANSFER.mode=OFFER/PASS_THROUGH/TRANSPORT_LIMIT/NONE, watts+rating_basis, 선택 PD profiles | Apple 100W는 공급 아님; LG 96W는 원문 정격 표기이며 협상 결과 아님 |
| 영상 독과 충전 독이 혼동됨 | DEVICE_POWER.supply와 host_charger_required | bus-powered/외부 독 어댑터가 호스트 충전을 의미하지 않음 |
| 출력 포트 수가 독립 화면 수로 변환됨 | ROUTING.mechanism/max_independent_displays/driver_required/OS 조건, 선택 channel_groups | Plugable 최대 2대; 실제 DP/HDMI 쌍별 매핑은 미상이라 groups 생략 |
| 데이터 Gb/s를 영상 대역폭으로 사용 | LINK_MODE.rate_scope=AGGREGATE_DATA/PER_LANE_SIGNAL/VIDEO_PAYLOAD | Apple 40Gb/s는 aggregate data; 영상 계산 없음 |
| 변환 케이블의 역방향을 추정 | CONVERSION.from_connector/to_connector/reverse_supported/선택 active | 두 변환 장치 역방향은 UNKNOWN |
| USB-C가 곧 영상 기능처럼 보임 | PROTOCOL.interface/protocol/version/mode/support | Dell/LG DP Alt Mode는 명시된 포트 기능만 기록 |

각 property는 서로 다른 payload 정의를 갖는다. 추가 필드와 잘못된 payload 조합을 거부한다.
NONE에 watts를 넣거나 simultaneous count를 누락하거나 픽셀 width/height 한쪽만 입력하면 거부한다.
독·케이블 claim은 PENDING_HUMAN_REVIEW를 강제한다. source DIRECT_CHECK는 승인과 별개다.
DSC/링크 버전은 원문 표기이며 DP 버전으로 DSC·lane·encoding을 역추론하지 않는다.

## 아직 해결되지 않은 typed 구조

이번 8개 payload는 이 조사 파일에서 사용할 최소 구조로 확정했다. 다음 항목은 아직 계산 가능한 완성 구조가 아니다.

- 조건 일부는 원문 조건 문자열이며 host 칩·GPU·리비전·펌웨어의 실행 predicate로 아직 변환하지 않았다.
- interface 이름은 공식 위치를 구분하는 label이다. 경로 port ID와 bind하는 템플릿/인스턴스 연결은 다음 구현 대상이다.
- MST/TB 공유 자원·스트림 allocation, DisplayLink 채널 쌍·OS 권한·DRM은 미확정이다.
- 실제 PD profiles, 충전 입력/출력 방향 edge, 자체 소비·협상·동시 소비 예산은 자료가 부족하다.
- 패널/포트 타이밍은 detailed timing/blanking·색/압축 조건이 없어 대역폭 계산에 사용하지 않는다.
- SOURCE_DISPLAY_LIMIT는 기존 Mac claim에 그대로 두며 새 payload로 중복 이전하지 않았다.

따라서 typed facts를 만들었다고 경로 모델을 정식 채택하거나 엔진을 공개할 수 없다.
확장해야 할 다음 구조는 port binding + 조건 predicate + routing/shared-resource + power-flow이며
이번 사실을 억지로 ‘완전한 path’로 연결하지 않았다. 실제 조합 실험·정답은 생성하지 않았다.

## 케이블 모델 식별 정책 검증

정확한 케이블 모델이 항상 필요한지 이번 배치에서 실제 문제가 드러났다.
G2724D 동봉 USB-C→DP 케이블은 공식 목록에서 개별 모델을 확인하지 못했고,
Apple 지원 문서는 케이블 제품군 능력을 설명하지만 길이/SKU를 특정하지 않는다.
Cable Matters는 모델을 식별해도 리비전·펌웨어 조건이 남는다.

현재 정책은 완화하지 않는다. 향후 capability class는 공식 인증/제조사 근거, 길이·전력·영상 모드·리비전 범위가
동일하며 필요한 속성이 모두 증명된 경우에만 검토한다. USB-C 외형·와트·‘8K’ 라벨만으로 class를 만들지 않는다.
첫 9개로 UNKNOWN 비율을 정량 평가할 수는 없다. 정확한 경로와 요청이 바인딩돼야 비율을 측정할 수 있다.

## 검증과 결과

```sh
python3 -m unittest discover -s tests -q
python3 scripts/validate_connection_model_pilot.py
python3 -m scripts.validate_official_products
python3 scripts/validate_question_corpus.py
python3 scripts/validate_question_corpus_v2.py
```

Python 186개 PASS(기존 164 + 신규 22). 9개 제품·9개 출처·29개 typed fact 검증 PASS.
표준 라이브러리 검증기는 enum으로 서로 배타적인 8개 oneOf 분기를 명시적으로 dispatch한다.
지원하는 스키마 키워드 밖의 변경은 거부하며 범용 JSON Schema 엔진은 아니다.
구조·참조·enum·날짜·URL·property별 payload와 일부 관계만 검사한다. 공식 사실 진위·현재 유효성·사람 승인은 검사하지 않는다.
CI에 pilot 검증을 추가했다. 기존 Mac catalog·질문 v1/v2·경로 v1 제안 스키마·목업과 공개 규칙은 변경하지 않았다.
JSON 구문·문서 경로·개인정보/비밀값 패턴·diff 검수 완료. 웹 변경이 없어 브라우저 테스트 재실행은 생략했다.

다음 배치는 이번 facts와 port template을 바인딩한 3~5개 부분 경로부터 만든다.
정확한 경로·조건·근거의 사람 검수 후 골든 정답을 매기고, 그 뒤 acceptance 엔진을 구현한다.
대량 수집·공개 COMPATIBLE은 계속 보류한다.
