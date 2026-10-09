# 사람 검토 및 통합 후보 준비

작성일: 2026-10-09. 작업 브랜치: `codex/human-review-preparation`.
코드·데이터 고정 기준: `f391080f3d74da60c2effd13a9bdcaa969b8218c`.
이번 변경은 검토 문서 두 개뿐이며 승인 기록·원본·화면·검증기 변경은 없다.

## 준비한 검토 자료

[제품별 사람 검토 자료](HUMAN_CONTENT_REVIEW_PACKET.md)에 모니터6종·fact29개를 정리했다. 원본 요약, typed payload, 기존 재확인 필드, 미확인 필드, 공식 URL/문서 위치/기존 확인일, 원본 fact hash, 연결 연구 기록을 함께 제공한다. 체크박스·검토 메모는 작성 전 상태다.

가장 먼저 확인할 대상은 V32UE 픽셀/Hz 미확인, 27ULD950 PD65 표기와 실제 공급 사양 구분, LG RATED/UP_TO 및 지역 SKU, 검토 보류 표시다. 확인 없는 부분은 그대로 보류하며 제조사 원문을 이번에 새로 확인했다고 기록하지 않았다. 화면 테스트 통과를 공식 제품 정확도 또는 사람이 검토했다는 증거로 쓰지 않는다.

## Git 관계

2026-10-09 `git fetch origin` 후 확인했다. 원격 content-review-display는 고정 후보와 동일하며 origin/main은 후보의 조상이다.

| 기존 작업 브랜치 | tip | f391080에 포함 |
|---|---|---|
| codex/data-validation-hardening | fb1382b | 예 |
| codex/product-semantic-validation | 90136e8 | 예 |
| codex/official-spec-manual-review | 57dbf2c | 예 |
| codex/p1-data-trust-fix | 4f51e0f | 예 |
| codex/p1-fix-independent-review | 199c146 | 예 |
| codex/p2-validation-boundaries | f879b03 | 예 |
| codex/content-review-display | f391080 | 예 |

main의 tip 및 공통 조상은 `c58dee5f3d1222d49e598dddbac5c8c6a7b4b8f0`. main 대비 f391080의 좌/우 독립 커밋 수는 **0/51**, 변경 경로는 **168개**다. 이는 이번 문서 변경 수가 아니라 연구·목업·검증 전체의 누적 통합 범위다. 기존 변경 누락 여부는 위 tip의 조상 관계로 확인했으며 모든 커밋의 기능 정확도를 새로 외부 감사한 것은 아니다.

이전 브랜치들을 다시 순서대로 병합하거나 각각 cherry-pick할 필요는 없다. f391080에 앞선 작업이 모두 포함되어 있다. 현재 main 기준으로는 분기 충돌 없이 fast-forward 관계지만, 향후 main/다른 작업 변경이 생기면 재검증해야 한다.

## 권장 통합 절차

1. 고정 코드 후보와 [검토 자료](HUMAN_CONTENT_REVIEW_PACKET.md)를 제품별로 사람 검토한다. [수동 검토 절차](CONTENT_REVIEW_PROCEDURE.md)에 따라 확인한 사실만 기록한다. 실제 담당자가 작성하지 않은 reviewer/date/result를 만들지 않는다.
2. 사용자 미커밋 README/DECISIONS/GP 관련 문서와 로컬 통합 감사 보고서는 현재 코드 후보에 포함하지 않았다. 소유자가 별도로 변경 내용을 검토하고 채택할 부분을 결정한다. 단순히 `git add .`로 섞지 않는다.
3. 기존 판정 원본과 공개 보류 정책, 데이터·후기·archive 보존을 누적 diff에서 확인한다. 연구 스키마/판정 상태와 사이트 방향 변경을 구분한다.
4. 사용자 통합 승인 후 하나의 최종 후보에 대한 PR을 만들고 required CI와 리뷰 정책을 확인한다. [전체 코드 비교](https://github.com/dineyong/connectable/compare/c58dee5...f391080)를 기준으로 검토 단위를 나눈다. PR 생성/병합은 이번에 수행하지 않았다.
5. 검토 중 코드·데이터 수정이 발생하면 대상 hash·표시용 파생물·전체 Python/브라우저/CI를 다시 확인한다. 사람 검토 기록을 추가해도 공개 UNKNOWN과 호환성 사용 NO는 유지한다.
6. main 통합 승인과 콘텐츠 공개/운영 승인은 구분한다. 광고·제휴·서비스 배포는 별도 검수·승인 이후 단계다.

## 자동 검증 재실행

고정 후보를 `git archive f391080`으로 저장소 밖 임시 디렉터리에 풀어 실행했다. 기존 작업 트리·스크린샷을 덮어쓰지 않는다.

- `python3 -m unittest discover -s tests -q`: **392개 통과**, 49.032초.
- `npm run test:e2e`: **72개 통과**, 35.3초. 데스크톱/모바일 Chromium.
- 기준 후보의 [GitHub CI](https://github.com/dineyong/connectable/actions/runs/37857141777): SUCCESS 확인.
- 신규 검토 문서의 로컬 링크 및 29개 fact hash/source ID 대조: 통과.
- 기존 파일·사용자 문서 보존, `git diff --check`, 추가 문서의 자격증명/연락처 패턴 검사: 통과.

이번 문서 후보의 원격 CI 링크는 완료 응답에서 제공한다. 문서가 추가되어도 테스트 수가 늘지는 않으며 새 기능 구현이 아니다.

## 현재 결정과 남은 사항

**기술적 검토 자료 준비 완료 / 사람 검토 미완료 / main 통합 미승인 / 공개 미승인.** 실제 검토 ledger는 빈 records이며 모든 체크박스는 미확인이다.

실제 담당자가 공식 근거와 화면의 표현을 확인해야 한다. 지역 SKU 동일성·실물 출력·PD 협상·LG 정격/최대의 적용 범위는 여전히 미확인이다. 자료 접근 실패 시 검토를 보류하고 이유를 기록한다. 파일 기반 기록은 인증된 승인 시스템이 아니며 담당자 신원/권한·저장소 리뷰 보호 설정은 추후 운영 단계의 과제다.

다음으로 필요한 사람 결정은 제품별 편집 검토 결과와 최종 통합 후보의 승인 여부다. 검토자가 별도 공식 근거로 새로운 필드를 확인한 경우 기존 역사 배치를 바꾸지 말고 새 근거 배치로 처리한다.
