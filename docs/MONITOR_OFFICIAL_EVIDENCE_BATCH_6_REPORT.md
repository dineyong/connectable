# 모니터 공식 근거 후속 배치 6

2026-10-11 · `codex/monitor-purpose-design` · 기준 `221d072`.

## 조사 범위와 결과

확인 가능한 근거만 보완했다. 전체 결측을 채우거나 한국 SKU 동일성을 추정하는 작업은 하지 않았다.

| 제품 | 직접 확인한 공식 근거 | 반영 | 남은 불확실성 |
|---|---|---|---|
| Modern MD271UL | [한국어 V1.1 설명서](https://download.msi.com/archive/mnu_exe/monitor/Modern_MD271ULv1.1_Korean.pdf) 인쇄12·17쪽 | Adaptive-Sync 지원 fact 추가; 무게 충돌 메모 | VRR 범위·한국 SKU·소비전력 |
| M27Q rev.1.0 | [정확한 리비전 공식 소개](https://www.gigabyte.com/Monitor/M27Q-rev-10), Key Features | Adaptive-Sync 지원 fact 추가 | rev.2.0와 동일시하지 않음; VRR 범위·한국 SKU |
| M28U | [한국 공식 모델 페이지](https://www.gigabyte.com/kr/Monitor/M28U), 하단 지역별 차이 경고 | 출처·확인 범위 메모 | 정확한 판매 SKU·PD·USB-C 영상 모드·국내 보증 |
| M32U | [한국 공식 모델 페이지](https://www.gigabyte.com/kr/Monitor/M32U), 하단 지역별 차이 경고 | 출처·확인 범위 메모 | 정확한 판매 SKU·PD·USB-C 영상 모드·국내 보증 |

MD271UL 설명서의 Net 5.3kg/Gross 7.4kg는 기존 공식 웹 값 5.75kg/7.35kg와 다르다. 원인을 확정할 근거가 없어 기존 무게 fact를 유지하고 `CONFLICT_REVIEW`에 기록했다. 한국어 문서 또는 한국 공식 소개의 존재만으로 한국 판매 SKU를 승인하지 않는다.

## 데이터와 회귀 검증

공식 원본에 사실2개와 출처3개를 추가하고 확인 메모를 보강했다. `vrr` 결측2개만 제거했다. 기존 모든 fact·출처·메모, 다른26종 제품 객체, 모델·지역·리비전 값은 보존했다. intake의 해당 원본 파일 해시만 갱신했다.

신규 `tests/test_monitor_research_followup.py` 3개 테스트는 반영 전 실패했다. 반영 후 통과했으며 다음 경계를 검사한다.

- 지원 여부를 VRR 범위나 SKU 승인으로 승격하지 않음.
- 무게 충돌을 표시하면서 원래 수치 및 소비전력 결측 보존.
- 한국 제품 페이지 추가가 PD·영상 모드·국내 판매 SKU 승인이 아님.

공식 데이터 및 intake 검증 통과. 통합 세션에서 파생 데이터 재생성과 Python·브라우저 전체 테스트 및 CI 결과를 기록한다.

## 남은 위험과 수집 기준

국내 유통 SKU·국내 보증·입력별 VRR 범위는 추가 공식 근거가 필요하다. 결측276개를 전부 해소하는 것을 출시 필수 조건으로 보지 않는다. 새 근거가 없는 필드는 미확인으로 보존하고 반복 조사를 보류할 수 있다. 기존 충돌은 해소로 처리하지 않았다. 공개 호환성 승인, main 병합, 배포는 진행하지 않는다.
