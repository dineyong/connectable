# 연결 판정 골든 조합 계획

2026-10-08 · DRAFT. 다음 표는 수집·검수 시나리오 30개이며 승인된 gold set이 아니다.
실제 제품·포트·케이블·독 모델과 공식 claim을 바인딩하기 전 기대 결과를 입력하지 않는다.
GPT가 만든 답을 사람 정답으로 취급하지 않는다. 현재 30/30 정확도는 측정할 수 없다.

| 계획 ID | 검수 시나리오 | 목표 검증 |
| --- | --- | --- |
| GP-01 | M1 Air USB-C 직결 4K60 | 직결 포트·영상·PD 분리 |
| GP-02 | M1 Air USB-C→DP 4K60 | 케이블 양 끝·변환 방향 |
| GP-03 | M1 Air USB-C→HDMI 4K60 | 어댑터 출력 프로파일 |
| GP-04 | M1 Air 독 HDMI 4K60 | 독 입력과 내부 경로 |
| GP-05 | M1 Air 네이티브 외장 2대·내장 ON | 소스 제한 적용 범위 |
| GP-06 | M1 Air DisplayLink 외장 2대 | 네이티브 제한 오용 방지 |
| GP-07 | M2 Air USB-C 직결 | 모델 세대 분리 |
| GP-08 | M2 Air 독 USB-C 출력 | USB 데이터 전용 출력 가능성 |
| GP-09 | M2 Air HDMI 고주사율 목표 | 공식 프로파일 부족 처리 |
| GP-10 | M1 Pro TB 독 외장 2대 | 독 스트림·OS 제약 |
| GP-11 | M1 Pro HDMI 직접 4K60 | 포트별 공식 한계 |
| GP-12 | M1 Pro HDMI 직접 4K120 목표 | 명시적 포트 제한 |
| GP-13 | M1 Pro 네이티브 외장 3대·내장 ON | 소스 수 제한 |
| GP-14 | M1 Max 6K 3대 + 4K 1대 | 이질적인 동시 그룹 |
| GP-15 | M1 Max 6K 4대 목표 | 그룹 평탄화 방지 |
| GP-16 | M1 Max 외장 5대·내장 ON | 수 제한과 출력 방식 |
| GP-17 | M3 Air 내장 ON 외장 1대 | 열린 구성 |
| GP-18 | M3 Air 내장 ON 외장 2대 | 닫힌 조건 오용 방지 |
| GP-19 | M3 Air CLOSED 외장 2대·요구 조건 충족 | 조건부 경로 |
| GP-20 | M3 Air CLOSED macOS 14.3 미만 | OS 전제 |
| GP-21 | M3 Air CLOSED OS 미상 | UNKNOWN 보존 |
| GP-22 | M3 Air CLOSED 전원 미상 | 전원 전제 누락 |
| GP-23 | USB-C 단자가 있으나 영상 기능 미상 | 커넥터로 기능 추정 금지 |
| GP-24 | 독 듀얼 출력 복제/확장 미상 | 포트 수와 스트림 수 분리 |
| GP-25 | MST 경로 macOS | OS·라우팅 claim 필요 |
| GP-26 | PD 모니터 출력과 소스 요구가 확인된 경로 | 영상과 충전 방향 분리 |
| GP-27 | PD 전력 부족 목표 | 충전/방전 조건 공식 근거 |
| GP-28 | 케이블 정체 미상 | 결측 UNKNOWN |
| GP-29 | 독 모델 또는 DisplayLink 여부 미상 | 결측 UNKNOWN |
| GP-30 | 같은 모델·조건 공식 claim 충돌 | CONFLICT 보존 |

각 계획의 기대 결과는 비워 둔다. 이름에 ‘제한’이 있어도 공식 검수 전 정답을 확정하지 않는다.
소스 식별 미상·포트 미상·목표 타이밍 미상·OS 미상·색/DSC 조건 미상은 위 30개에서 별도 mutation 테스트로 생성한다.
mutations는 실제 성공·실패 사례 수에 포함하지 않는다. 핵심 결측 시 긍정 결과를 내지 않아야 한다.

## 승인될 gold record 계약

- gold_id, 실제 request/path, 요청 해시, catalog/rule version.
- expected public/candidate/rule status와 사유, 적용 범위 및 필수 조건.
- supporting claim IDs, 원문 URL·확인일, 인간 검수 상태·일시·검수 데이터 해시.
- case/configuration/observation 참조는 보조 근거로 분리.
- 미검수는 PLANNED 또는 PENDING_REVIEW, 승인된 정답만 acceptance 계산에 포함.
- engine 출력에서 expected를 역생성하지 않는다. 정답 변경 시 사유·근거·영향 tests 기록.

첫 공개 기준은 승인된 기본 조합 30/30 일치와 핵심 결측 UNKNOWN, 충돌 CONFLICT,
공개 승인 gate 회귀 통과다. 30개 통과가 미검수 제품·조합까지 보장하지는 않는다.
현재 승인된 gold record는 0건이다.


## 최초 경로 검토 배치

[5건 검토 자료](PATH_INSTANCE_GOLD_BATCH_1_REVIEW.md)에 GP-02/03/07/06/25의
기능 경로를 바인딩했다. GP-02/03은 현재 확보된 Dell G2724D의 QHD60 목표를
사용하는 축소 검증 변형이며, 기존 계획의 4K60 시나리오를 충족했다고 계산하지 않는다.
추후 정확한 4K 제품/포트 근거로 별도 경로를 만들어 원래 시나리오를 검증해야 한다.
계획 정답과 사람 승인 칸은 계속 미기록이다. **승인 0/30**.
