# 보충 공식 근거 사람 검토 준비

기준: `1990262`. 작업 브랜치: `codex/supplemental-human-review`.

## 완료 범위

[27ULD950 사람 검토 자료](CROSSOVER_PD_HUMAN_REVIEW_PACKET.md)에 원문·이미지·캡처·해시·확인 범위·미확인 조건·체크리스트와 상세/비교/필터 표시 제안을 정리했다. 모든 체크박스와 실제 검토 결과는 미작성이다.

기존 [검토 ledger](../data/review/content_reviews.json)는 원본 fact와 해당 원본 source_refs만 대상으로 한다. 새 65W 보충 assertion을 원본 fact의 승인처럼 넣는 것을 피하기 위해 [보충 ledger](../data/review/supplemental_content_reviews.json)와 [전용 스키마](../schemas/supplemental-content-review.schema.json), [검증기](../scripts/supplemental_content_review.py), [절차](SUPPLEMENTAL_CONTENT_REVIEW_PROCEDURE.md)를 분리했다. 실제 records는 0건이다. 기존 검증 기준을 완화하지 않았다.

## 기록 계약

- 배치 전체 hash, 대상 assertion ID, 관련 원본 fact hash, 캡처 hash가 모두 일치해야 한다.
- 정확한 제품 페이지와 상세 이미지 참조를 모두 기록해야 한다.
- 담당 가명·실제 날짜·결과·메모가 필요하다. 형식 검증은 담당자 신원이나 실제 사람 검토를 증명하지 않는다.
- reviewed_fields는 기존 근거에서 확인된 mode/watts/rating_basis에 한정한다. 미확인 interface는 승인할 수 없다.
- 남은 interface·power_qualifier·pd_profiles·simultaneous_budget·sku_revision·actual_host_power는 삭제할 수 없다.
- EVIDENCE_SUFFICIENT는 세 필드의 제한된 제조사 표기 근거를 확인한 편집 결과다. 공개 UNKNOWN·호환성 사용 NO, 원본과 보충 근거의 적용 보류는 유지된다.

제안 문구는 문서에만 있다. 상세/비교에는 별도 제조사 표기 65W와 검토 대기를 병기하는 방향을 제안했고, 현재 원본 숫자 셀 UNKNOWN·공급 필터 제외·공개 UNKNOWN은 그대로 유지한다. 실제 UI 연결, 사람 승인, 배포는 수행하지 않았다.

## 검증

[회귀 테스트](../tests/test_supplemental_content_review.py) 12개: 실제 빈 ledger, 정상 부분 검토 및 결과 종류, 세 hash의 stale 바인딩, 다른 assertion, 빈/중복/다른 근거, 미확인 필드 승격, 남은 조건 삭제, 부족한 부분/충족 기록, 공개 승인, 빈 검토자·메모·잘못된 날짜, 중복 ID·추가 필드, 개인정보를 검사한다. 정상·비정상 fixture의 reviewer는 테스트 전용이며 실제 검토자 기록이 아니다.

- `python3 -m unittest discover -s tests -q`: **423개 통과**, 18.576초. 기존 411개 유지.
- `python3 scripts/supplemental_content_review.py`: records0건 통과.
- `python3 scripts/crossover_pd_evidence.py`: 기존 보충 근거 통과.
- `python3 -m scripts.content_review`: 기존 원본 검토 체계 통과.
- `python3 scripts/build_site_content_v2.py --check`, `python3 web/derive-site-content.py --check`: 기존 화면·파생물 재현성 통과.
- `npm run test:e2e`: 데스크톱·모바일 **72개 통과**, 16.2초.
- 기존 파일 바이트·사용자 미커밋 문서·문서 내부 경로·민감값 패턴·`git diff --check`: 통과.
- [작업 브랜치 CI](https://github.com/dineyong/connectable/actions?query=branch%3Acodex%2Fsupplemental-human-review)는 push 후 확인하며 실제 실행 결과와 링크를 최종 응답에 기록한다.

CI에 보충 ledger 검사 명령을 추가했다. 브라우저 회귀는 화면 변경이 없는 기준 커밋의 별도 임시 복사본에서 실행해 기존 스크린샷을 덮어쓰지 않는다. 새 Python 파일은 로컬 전체 테스트와 push된 후보 CI에서 검증한다.

## 남은 승인과 다음 단계

실제 사람 검토는 아직 필요하다. 검토자는 원문과 표시 제안을 직접 대조하고 확인한 범위만 전용 ledger에 기록해야 한다. 원문 접근 실패 시 NEEDS_REVIEW를 유지한다. AI가 검토자·날짜·결과를 대신 채우지 않는다.

근거가 충분하다는 편집 검토 결과와 표시 제안 채택은 별개다. 다음 화면 적용 변경에서도 원본 fact·과거 부분 확인을 보존하고, 보충 표시가 확정 충전/호환성으로 읽히지 않는지 데스크톱·모바일 검증이 필요하다. 원본 검토 ledger는 보충 기록을 자동 합치지 않는다.

한국 SKU와 실제 충전 결과를 승인할 자료는 여전히 없다. V32UE와 LG의 기존 공백도 유지된다. 인증된 검토자·권한·서명·운영 승인 시스템은 이번 범위에 포함하지 않는다. main 병합과 공개 배포는 수행하지 않는다.
