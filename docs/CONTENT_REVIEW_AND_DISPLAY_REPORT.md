# 검증 상태 표시 및 수동 검토 체계

작업일: 2026-10-09. 기준: `codex/p2-validation-boundaries`의 `f879b03`.
작업 브랜치: `codex/content-review-display`.
기준 커밋의 [GitHub CI](https://github.com/dineyong/connectable/actions/runs/37856262157)는 SUCCESS를 확인했다.

## 변경 및 승인 범위

원본 사양·후기·catalog·공식 재확인 배치를 수정하지 않았다. 화면의 검토 정보는 기존 공식 재확인 배치에서 읽기 전용으로 파생한다. 원본 요약·typed payload를 보존하며 원본에 없는 픽셀·Hz·공급 전력·한국 SKU 동일성을 채우지 않는다.

공개 UNKNOWN, 후기 호환성 사용 NO, 사람 검토 대기 정책은 유지된다. 수동 검토 체계는 파일 기반 기록이며 실제 공개 승인·인증 관리자 UI·자동 배포 기능이 아니다. 현재 실제 검토 기록은 **0건**이다.

## 부분 검증 표시

[표시용 생성기](../web/derive-site-content.py)는 [기존 재확인 배치](../data/official/spec_manual_review_2026-10-09.json)를 기존 검증기로 먼저 검사한 뒤 각 fact에 field_review를 붙인다. 재확인 기록이 없는 fact에는 PENDING_HUMAN_REVIEW와 별도 재확인 없음이 표시된다.

| 대상 | 확인 범위 | 유지한 미확인 범위 |
|---|---|---|
| 주연테크 V32UE 해상도 | resolution_label: 4K UHD | width·height·refresh_hz 숫자 |
| 크로스오버 27ULD950 충전 | label: PD65 제품명 | watts·interface·mode |
| Dell 재확인 기존 fact | 배치의 verified_fields에 지정된 모델 범위 | 한국 SKU 일치 및 실제 연결 결과 |
| 기타 기존 fact | 원본 공식 표기, 사람 검토 대기 | 별도 재확인 없음 |

[화면](../web/site-v2.js)의 제품 상세와 비교 셀은 동일 featureHTML 함수를 사용한다. MANUAL_REVIEW·UNKNOWN·PENDING_HUMAN_REVIEW를 호환 승인과 구분하며 각 확인/미확인 필드와 재확인 지역·문서 위치·날짜를 표시한다. 근거 정보가 누락되면 재확인 완료라고 표시하지 않는다. 원본의 전체 문장을 유지하고 검증 범위를 함께 표시하므로 자연어 요약을 새 사실로 해석하지 않는다.

공식 공급 기능 필터는 OFFER뿐 아니라 숫자 watts와 알려진 interface를 요구하며, 부분 확인에서 해당 기능의 핵심 필드가 미확인이라면 제외한다. 크로스오버 PD65는 제품명만 확인된 상태이므로 공급 기능 필터에서 제외된다. 제품 자체나 PD65 기록을 삭제하지 않으며 상세·비교에서 확인할 수 있다. 일반 사양 종류 필터는 자료 탐색용이며 확인 완료나 호환 승인을 뜻하지 않는다.

## LG 전력 및 지역

LG 27UP850-W의 기존 96W RATED payload는 변경하지 않았다. 상세와 비교에서 **정격 (RATED)**으로 표시한다. 기존 공식 재확인 배치의 라트비아 자료 `SR-LG-PD`는 **최대 상한 (UP_TO) 96W**, 지역 LV, 공식 URL, 확인일, 문서 위치를 별도 블록에 표시한다.

숫자가 같아도 두 주장을 합치지 않는다. 별도 근거는 기존 사양 대체가 아니며 한국 판매 SKU 적용은 UNKNOWN이다. 별도 지역 assertion을 한국 제품 기능 필터의 새로운 근거로 사용하지 않는다. 이번에 공식 원문을 새로 조사한 것이 아니라 기존에 확인한 근거의 범위를 정확히 표시한 것이다.

## 최소 수동 검토 체계

- [Schema](../schemas/content-review.schema.json)
- [빈 검토 기록](../data/review/content_reviews.json)
- [검증기 및 표시 파생 코드](../scripts/content_review.py)
- [검토 절차](CONTENT_REVIEW_PROCEDURE.md)

기록은 정확한 target_fact_id·전체 target_sha256·reviewer_id·reviewed_on·result·해당 fact의 공식 source_refs·notes를 요구한다. 검토자는 실명 대신 내부 가명 식별자를 사용한다. target hash가 바뀌거나 다른 fact의 근거가 연결되면 거부한다. 빈 담당자·날짜 오류·근거 누락·중복 ID·미등록 필드를 거부한다. site 원본도 기존 검증기로 검사한다.

result는 NEEDS_REVIEW/PARTIALLY_VERIFIED/EVIDENCE_SUFFICIENT/REJECTED만 허용한다. EVIDENCE_SUFFICIENT도 편집 검토 결과이며 실제 공개 승인이 아니다. APPROVED·COMPATIBLE·usable_for_compatibility YES는 거부한다. ledger는 화면 필드 확인 결과나 원본 상태를 자동 승격하지 않는다. 실제 담당자가 기록한 사실은 코드만으로 증명할 수 없으므로 저장소 리뷰와 권한 관리가 필요하다.

## 테스트 및 수정 과정

- 전체 Python: **392개 통과** (기존386 + 신규6), 17.964초.
- 전체 브라우저: **72개 통과** (기존66 + 신규3 시나리오 × desktop/mobile), 25.5초. Chromium 기준.
- Python 명령: `python3 -m unittest discover -s tests -q`.
- 브라우저 명령: `npm run test:e2e`.
- `python3 scripts/build_site_content_v2.py --check`: 통과. 원본 site JSON 변화 없음.
- `python3 web/derive-site-content.py --check`: 통과. 새 표시용 JS 재현 가능.
- `python3 -m scripts.content_review`: 통과. 실제 기록0건, 공개 승인 보류.

신규 Python 테스트는 부분 필드 범위·payload/문장 보존·RATED/UP_TO 분리·빈 ledger·정상 비승인 기록·근거/날짜/담당자/해시 오류·중복 ID·미등록 필드·부분 검증 승격 거부를 검사한다. 브라우저는 두 부분 검증 표시, 공급 필터 제외, LG 상세/비교와 지역 표시, 검토 metadata가 없을 때 미확인 표시를 확인한다. 기존 66개 기능·접근성·링크·출처 검사는 유지했다.

초기 전체 Python 실행에서 임시 파생물 검사 fixture가 신규 schema 디렉터리를 복사하지 않아 기존 stale-asset 테스트 1건이 실패했다. fixture에 schemas 복사를 추가한 뒤 전체 392개를 다시 실행해 통과했다. 검사 기준을 완화하거나 실패 테스트를 삭제하지 않았다. 기존 공급 기능 필터 테스트의 기대값은 숫자·단자 확인 조건에 맞게 변경했으며 별도 음성 브라우저 검사로 크로스오버 제외를 확인한다.

## 보존 및 변경 파일

작업 전 SHA-256 manifest 170개 경로를 비교했다. 기존 변경은 workflow, 테스트2개, 표시용 생성기, 표시용 JS 자산, 화면 JS의 6개 파일뿐이다. 원본 data/site/content-v2.json·공식 자료·코퍼스·rules·schemas 원본·후기·archive·기존 CSS/HTML·원본 스크린샷 및 사용자 README/DECISIONS와 미커밋 문서는 보존됐다.

- 신규: content_review.py, content-review.schema.json, content_reviews.json, CONTENT_REVIEW_PROCEDURE.md, Python/E2E 테스트 각1개, 본 보고서.
- 수정: web/derive-site-content.py, web/site-content-v2.js, web/site-v2.js, tests/test_projection_check.py, tests/e2e/site-v2.spec.js, .github/workflows/validate.yml.

내부 문서 경로 검사와 `git diff --check`를 통과했다. 변경 diff의 자격증명·연락처 패턴 검사에서 발견 사항이 없었고 직접 diff도 검토했다.

화면의 정보 표시와 파생 자산은 목표에 따라 변경했지만 전체 UI 재설계는 하지 않았다. 기존 모니터6개·연구 기록38개·가이드3개는 유지한다. 브라우저 테스트가 생성한 기존 스크린샷은 작업 전 바이트로 보존했다.

## 커밋 및 원격 CI

- `add1236`: 비승인 검토 기록·Schema·절차·검증기·Python 회귀.
- `b359972`: 부분 확인/LG 화면·필터·표시 파생·브라우저 회귀·CI gate.
- [코드 후보 GitHub CI](https://github.com/dineyong/connectable/actions/runs/37856961724): **SUCCESS**. `b359972e8bd0f00123cb1c8b43541242e3d850e5`에서 Python392개(14.789초), 브라우저72개(25.9초) 및 모든 데이터·파생물·검토 ledger gate 통과.
- 최종 보고서 커밋은 Git 이력과 완료 응답에 기록한다. main 병합·공개 배포는 하지 않는다.

## 남은 위험과 후속 작업

실제 검토자 기록과 별도 사람 승인은 아직 없다. 파일 검증은 공식 문서 진실성·검토자 신원·물리 연결 성공을 증명하지 않는다. 지역 SKU 동일성, LG 정격과 최대 값의 적용 범위, PD 협상/실수전, 실물 및 Chromium 이외 브라우저 검증은 미확인이다.

검토 상태와 필드 이름이 늘어 상세/비교가 길어졌다. 향후 사용자 읽기 검토로 문구·정보 밀도를 조정하되 근거 범위를 숨기지 않아야 한다. 공개 승격은 별도 정책과 권한·사람 검토가 필요하다. 부분 확인 기록에 새로운 필드를 추가하려면 역사적 배치를 덮어쓰지 말고 새 근거 배치를 마련한다.
