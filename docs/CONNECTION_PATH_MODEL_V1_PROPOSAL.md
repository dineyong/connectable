# Connection / Port / Capability / Path v1 제안

2026-10-08 · PROPOSED. 사용자 제공 검토 의견에 따른 설계안.

## 적용 범위와 기준 파일

[제안 스키마](../schemas/connection-path-v1.proposed.schema.json)는 공식 catalog를 대체하지 않는 설계 검증용이다.
현재 공식 기준은 [products.json](../data/official/products.json)와 [공식 스키마](../schemas/official-products.schema.json)다.
질문 코퍼스의 topology는 사용자 관측을 기록하며 이 모델의 공식 capability를 자동 생성하지 않는다.
새 스키마를 정식으로 채택하거나 기존 제품을 전부 변환하지 않았다. 웹사이트·공개 판정 엔진에도 연결하지 않는다.

공식 Mac 동시 출력 프로파일은 앞으로 SOURCE_DISPLAY_LIMIT capability에 연결하되 기존 claim_id를 유지한다.
‘6K 60Hz’를 DP 버전·링크 대역폭·DSC·색 깊이 값으로 역산하지 않는다.

## 객체와 참조

| 객체 | 역할 | 핵심 필드 |
| --- | --- | --- |
| devices | 경로 안의 개별 물리 장치 인스턴스 | id, kind, identity_status, 선택 product_ref |
| ports | 장치 인스턴스의 특정 단자 | device_id, connector, video_direction, power_role, capability_refs |
| capabilities | 공식 claim에 연결한 개별 능력·제약 후보 | subject_id, property, claim_refs, 조건, source_status, review_status |
| edges | 장치 간 배선 또는 장치 내부 영상 경로 | from_port, to_port, kind, protocol, output_method, capability_refs |
| paths | 소스에서 여러 화면으로 이어지는 구성과 목표 | source_device_id, edge_ids, display_targets, context, topology_completeness |

객체 ID는 문서 안에서 전역 고유하다. product_ref는 기존 불변 product ID다.
같은 모니터 두 대는 서로 다른 device ID로 만들고 동일 product_ref를 사용할 수 있다.
포트는 인스턴스에 속한다. 향후 제품 포트 템플릿을 별도 catalog에 만들고 인스턴스화할 때 claim 참조를 보존한다.
현재 제안은 제품 포트 템플릿 catalog까지 구현한 것이 아니다.

케이블도 SOURCE→CABLE→DISPLAY처럼 장치 인스턴스로 표현한다. 케이블 양 끝 포트와 내부 edge를 두어
케이블 능력이 생략되지 않게 한다. 변환 어댑터의 내부 edge는 방향과 변환 claim을 가진다.
독은 upstream input에서 각 downstream output으로 INTERNAL_ROUTING edge를 갖는다.
분기가 있다고 독립 영상 스트림 두 개가 생긴다고 판단하지 않는다. ROUTING claim에서 MST/SST/DisplayLink,
호스트 OS 조건, 공유 자원을 추가로 확인한다.

PHYSICAL edge는 서로 다른 장치 사이, INTERNAL_ROUTING은 같은 장치 안에만 허용한다.
영상 경로는 소스→디스플레이 방향이다. PD 흐름은 영상과 반대일 수 있으므로 power_role을 별도 필드로 둔다.
USB_C는 물리 단자이며 protocol과 별개다. Thunderbolt는 connector 값으로 사용하지 않는다.
UNKNOWN connector/protocol/output_method는 구조상 허용하지만 긍정 판정 근거가 아니다.
부분 경로는 PARTIAL/UNKNOWN으로 보존한다. COMPLETE는 모든 목표 화면에 구조적 도달 경로가 있다는 의미만 가진다.

## Capability와 확장 경계

property는 PROTOCOL, LINK_MODE, VIDEO_PROFILE, DSC, POWER_OFFER, POWER_REQUIREMENT,
ROUTING, SOURCE_DISPLAY_LIMIT이다. subject_id는 device/port/edge 중 하나를 참조한다.
공식 claim_refs는 필수이며 source_status와 review_status를 별도로 둔다.

현재 value_label은 공식 문구의 요약으로 계산 입력이 아니다. 선택 amount/unit 역시 명시된 값만 기록한다.
조건은 공식 문구를 보존하는 문자열 목록이다. 문자열을 파싱해서 실행 규칙으로 사용하지 않는다.
아직 픽셀 타이밍·링크 레인·encoding·DSC 협상·MST 스트림 공유·PD 프로파일의 계산 가능한 세부 스키마는 없다.
따라서 이 부분은 스키마 채택 전 소수 실제 제품을 수집하며 확정해야 한다.
‘확장 공간’이라는 이유로 자유 JSON 필드를 열어두지 않고 property별 typed payload를 후속 버전에서 명시한다.

목표 display_targets는 픽셀 width/height, 주사율, 색 깊이·chroma·HDR·DSC 요구를 별도로 보존한다.
미상 값은 생략/UNKNOWN이며 임의 기본 8bit·RGB로 채우지 않는다.
목표 수와 모니터 인스턴스 수는 독립 확장 수와 다를 수 있다. independent_external_count는 요청값이며 성공 관측 수가 아니다.
미러링 그룹 모델은 이 제안에서 미구현이며 미러링 판정은 UNKNOWN이다.

## 상태 분리와 공개 승인

다음 판정 결과 계약은 문서 제안이다. 실행 엔진은 아직 없다.

| 상태 축 | 허용값 | 의미 |
| --- | --- | --- |
| source_status | DIRECT_CHECK / UNAVAILABLE / STALE / CONFLICT / UNKNOWN | 원문 확인·유효성. A/B 신뢰등급이나 claim 승인과 별개 |
| review_status | PENDING_HUMAN_REVIEW / APPROVED / REJECTED | 지정 검토자의 사실·적용 조건 검수 |
| rule_status | NOT_IMPLEMENTED / INSUFFICIENT_DATA / CONFLICT / SUPPORTED / CONTRADICTED | 경로에 대한 실행 규칙의 근거·적용 결과 |
| public_status | 기존 7개 판정 코드 | 공개할 수 있는 최종 결과 |

결과에는 대상 path ID·요청 해시·catalog/rule 버전·확인일·적용 rule/claim ID·누락 필드·충돌 ID·사유를 남긴다.
승인 기록은 reviewer 내부 식별자·일시·검수한 데이터 해시를 가져야 한다. 개인정보를 공개 결과에 포함하지 않는다.
같은 claim이 바뀌면 이전 승인을 새 값에 재사용하지 않는다.

COMPATIBLE 승인 조건:

1. 소스·케이블·중간 장치·화면과 사용 포트가 정확히 식별되고 전체 경로가 확인됨.
2. 필요한 OS·덮개·전원·드라이버·영상 모드 조건이 확인됨.
3. 각 경로 구간과 독 내부 공유/분기의 공식 claim이 존재하며 사람 검수 승인됨.
4. 요청 화면 수·해상도·주사율·관련 색/DSC/충전 조건을 실행 규칙이 모두 다룸.
5. 해당 규칙의 골든·결측·충돌 테스트가 승인되고 통과함.
6. 근거가 최신이며 미해결 충돌이 없음.

핵심 근거가 부족하면 UNKNOWN. 조건이 필수인데 현재 충족 여부가 미상이면 UNKNOWN이며 조건 목록을 표시한다.
CONDITIONAL은 조건을 충족하면 가능하다는 공식 경로 근거가 모두 검수된 경우에만 허용한다.
LIMITED는 낮은 프로파일이 실제로 지원된다는 검수 근거가 필요하다. 목표 불충족만으로 LIMITED를 만들지 않는다.
VERIFIED_COMPATIBLE은 별도 독립 실사용 검수까지 필요하며 현 단계에서 생성하지 않는다.

INCOMPATIBLE은 요청을 막는 명시적 제한과 그 제한의 적용 전제가 증명되어야 한다.
자료 부재는 미지원 근거가 아니다. 전체 경로 결측이 있어도 정확히 식별된 소스의 화면 수 제한처럼
독립적으로 성립하는 제한을 발견할 수 있지만 공개 부정 판정에는 요청 범위(NATIVE/DisplayLink 등),
검수·규칙 적용 조건·대체 경로 범위를 명확히 해야 한다. 현재 count candidate를 자동 공개 승격하지 않는다.
공식 claim 충돌은 CONFLICT이며 최신 글을 임의 우선하지 않는다.

사용자 사례는 case/configuration/observation ID와 별도 비교 기록으로 연결한다.
공식 판정과 동일/유사 구성 사용자 보고를 병렬로 보여주고 단일 사례로 공식 capability를 변경하지 않는다.
일치 모델 문자열만으로 ‘동일 구성’ 표시를 만들지 않는다.

## 다음 구현 단위

1. 제안 구조로 대표 모니터 3~5개·독/허브 3~5개·소수 케이블/어댑터의 공식 포트·경로 사실을 수집.
2. property별 typed payload, OS·드라이버 조건, 공유 자원·PD 흐름을 실제 자료로 확정.
3. [골든 조합 계획](CONNECTION_GOLD_SET_PLAN.md)의 30개 시나리오에 정확한 제품·경로·근거를 바인딩.
4. 지정 검토자가 기대 결과를 매긴 뒤 엔진과 독립적인 정답 원본으로 동결.
5. source→path→rule→result를 연결한 내부 판정기 구현, 골든·결측·충돌 acceptance suite 통과.
6. 공개 승인 계약 구현 후 목업에 연결. 대량 수집은 구조 안정 후 진행.

## 이번 검증과 한계

[구조 검증기](../scripts/validate_connection_path_proposal.py)와 [테스트](../tests/test_connection_path_proposal.py)를 추가했다.
Python 164개 PASS(기존 154 + 구조 회귀 10). 공식 데이터·코퍼스는 변경하지 않았다.
테스트의 test-* ID는 합성 구조 fixture이며 실제 사례·제품·호환성 정답으로 저장하지 않는다.
검증기는 ID·참조·장치 내부 경로·COMPLETE 도달 여부를 확인한다.
claim_ref의 실제 catalog 존재·적용성, 방향별 프로토콜 협상, cycle/중복 스트림·PD 흐름·승인은 아직 검증하지 않는다.
이 검사 통과는 topology 구조의 일부 무결성일 뿐 물리 연결이나 호환성 통과가 아니다.
브라우저 변경이 없어 e2e는 재실행하지 않았다. 문서 경로·JSON 구문·diff·원본 무변경을 확인했다.
