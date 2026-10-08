# 사이트 표시 콘텐츠 v2 구축 보고서

2026-10-08 · research/question-corpus-foundation · 데이터·콘텐츠 담당.

## 결과와 범위

최초 빈 계약 파일을 만든 뒤 `data/site/content-v2.json`을 기존 로컬 근거만으로 재생성했다. 공식 연구 pilot에서 모델 식별이 확인된 모니터 3개(Dell U2723QE, LG 27UP850-W, Dell G2724D), 공개 review 검토 자료 18건과 정식 v2 공개 코퍼스 20건의 연결 기록 38건, 구매 전 확인 가이드 3개를 담는다. 38건은 서로 다른 연구 레코드 수이며 고유 사용자·독립 사건 수나 성공률이 아니다. 질문·문제 기록도 포함하므로 화면에서는 ‘연결 기록/공개 자료 편집 요약’으로 설명한다.

기존 official/products.json도 읽고 해시를 기록하지만 Mac 사양을 모니터 기능으로 합치지 않는다. 원래 raw review 18건은 해시 추적용 입력으로 읽고, 표시 관측은 의미 교정이 반영된 mapped 자료를 사용한다. 신규 웹 조사, 대량 수집, 공식 판정, 상품 추천, 사진 생성, 가격·평점·통계·구매 링크를 추가하지 않았다. 과거 공식 출처의 확인일을 보존하며 이번 작업의 새 원문 확인일로 바꾸지 않는다.

## 화면 계약

최상위 필수 키는 `schema_version`(문자열 "2"), `generated_on`(자료 파생일), `monitors`, `reviews`, `guides`, `disclosures`다. 추가 `provenance`는 입력 상대 경로와 SHA-256을 담는다. 생성일은 원문·실물 확인일이 아니다.

모든 콘텐츠는 안정적인 `id`, `title`, `source_refs`, `review_status`를 갖는다. source_refs는 객체 배열이며 `url`, `title`, `checked_on`, `published_on`, `source_file`, `record_id`를 제공한다. 공개 날짜가 입력에 없으면 UNKNOWN이다. source_file은 로컬 근거 추적용이며 사이트 서버에서 연구 원본을 공개할 필요는 없다.

- monitors: 기존 product ID를 그대로 쓴다. `display_model`, `manufacturer`, `region`, `identity_status`, `features`, `missing_fields`를 제공한다. features는 공식 fact의 요약·payload·조건·출처ID·검토상태를 보존하고 `basis=MANUFACTURER_SPEC`를 붙인다. 내부 source ID는 해당 모니터 source_refs의 record_id로 추적한다. 패널·포트별 영상 능력과 공급 전력을 실제 Mac 출력·수전 결과로 전환하지 않는다. 지역은 원래 GB/MY/US이며 국내 변형을 확인한 의미가 아니다.
- reviews: PUR/UQ ID를 그대로 쓴다. `macbook_display_name`, `reported_monitor_models`, `monitor_ids`, `connection_summary`(문자열 배열), `configurations`, `observations`, `functional_observations`, `missing_fields`, `commercial_context`를 제공한다. 노드·포트·시도·근거와 구성별 결론도 보존하므로 구성/관측의 로컬 ID를 같은 레코드 안에서 해석한다. connection_summary는 구성에 연결된 근거 요약이며 완전한 경로 문자열이 아니다. `functional_observations`는 PUR에만 존재하며 UQ는 빈 배열이다. UQ 상세에서는 observations를 사용한다.
- 후기 모델 연결은 공식 display_model과 공개 노드 display_model의 완전 일치만 허용한다. 현재 38건은 모두 monitor_ids가 빈 배열이다. LG의 비슷한 모델 접미사나 다른 Dell 제품을 자동 연결하지 않는다. 원문 모델 표기는 reported_monitor_models에서 확인한다. 후기에만 등장한 표시명을 공식 확인 모니터 카드로 만들지 않는다.
- `semantic_review`는 PUR의 AI 원문 의미검수 이력을 보존한다. UQ는 UNVERIFIED다. `reported_outcome`은 기존 사용자 기록의 결과이며 공개 호환 판정이 아니다. 모든 public_status는 UNKNOWN, usable_for_compatibility는 NO다.
- guides: `body`는 문단 문자열 배열, `related_monitor_ids`, `related_review_ids`는 내부 링크용 배열이다. `basis=EDITORIAL_CHECKLIST`, `review_status=NEEDS_REVIEW`이며 구매 추천·호환 승인 글이 아니다. 공식 pilot와 기존 사용자 기록을 함께 출처로 제공한다.
- disclosures는 editorial/compatibility/advertising/affiliate 문자열이다. 현재 광고·제휴는 준비 단계다. 사진·가격·평점·구매URL의 UNKNOWN 값은 실제 자산/링크로 렌더링하지 않는다.

원문 전체, 댓글 원문, 닉네임, 비공개 사용자 대화는 편입하지 않는다. 제조사 기능, 사용자 관측, 후기 원문의 판매·제휴·광고 맥락을 별도 필드로 유지한다. 기존 NEEDS_REVIEW/PENDING_HUMAN_REVIEW를 사람 승인으로 승격하지 않는다. 공개 판정 UNKNOWN과 승인 골든 0/30은 유지된다. 화면용 파생 JS가 필요하면 화면 담당이 이 JSON에서 생성한다.

## 재생성과 검증

```sh
python3 scripts/build_site_content_v2.py
python3 scripts/build_site_content_v2.py --check
python3 -m unittest tests.test_site_content_v2 -v
python3 -m unittest discover -s tests -q
```

추가 검사 4개와 전체 Python 313개가 통과했다. 바이트 일치 재생성, 입력 read-only/해시 보존, 콘텐츠 ID 중복·관련 ID·출처 파일/URL, 38건의 공개 접근 여부·관측 및 광고 맥락 무변형, 공식 fact 무변형, 공개 UNKNOWN, 민감 패턴/개인 식별 필드 미포함을 검사했다. 기존 테스트도 통과했다. 네트워크·브라우저 검증은 이 데이터 담당 범위에 포함하지 않는다.

변경은 data/site/, 이 보고서, scripts/build_site_content_v2.py, tests/test_site_content_v2.py에만 한정했다. 기존 연구·official·schema·테스트·문서를 쓰거나 삭제하지 않았다. Git index 변경·commit·push·브랜치 변경·main merge·배포를 수행하지 않았다. 작업 시작 시 존재하던 미커밋 변경은 다른 세션 소유로 보존했다.
