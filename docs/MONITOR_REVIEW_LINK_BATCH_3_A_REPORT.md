# 외부 후기 링크 배치 3 — 조사 세션 A

확인일: 2026-10-12. 배치 2에서 보류한 ASUS PA279CRV·PA248QV·VA24EHF, Dell U2724D·U2724DE 5종을 제한된 검색과 공개 원문 직접 확인으로 재조사했다. [기존 조사](MONITOR_REVIEW_LINK_BATCH_2_A_REPORT.md)와 [플랫폼 계약](MONITOR_REVIEW_LINK_PLATFORM_REPORT.md)을 유지한다. 제품 원본·UI·승인 상태는 이 조사 세션에서 변경하지 않았다. 최종 기준 원본은 [후기 링크 데이터](../data/research/monitor-review-links.json)이며 임시 후보 파일은 기준 원본이 아니다.

## 확인한 후보

| 모델 | 공개 원문 | 확인 범위 | 광고·제휴 | 포함 근거 및 제한 |
|---|---|---|---|---|
| PA279CRV | [Parka Blogs](https://www.parkablogs.com/index.php/content/review-asus-proart-pa279crv-4k-27-inch-display) | 제목·제품 대여·직접 조작 및 측정·사용 본문 | PRESENT | 영어 리뷰. 싱가포르 대여 제품, 실제 측정·반사·스탠드 관측 명시. 댓글에서 측정 설정 이견이 있어 수치 자체는 이관하지 않음. |
| PA248QV | [영상](https://www.youtube.com/watch?v=KCxgIK6Cg7E) | watch 제목·펼친 게시자 설명·챕터 | UNKNOWN | 스페인어. 자체 시험과 개봉·첫 인상·편집 예제 명시. 협찬 없음으로 단정하지 않음. |
| VA24EHF | [Can Buy or Not](https://www.canbuyornot.com/reviews/pc/asus-va24ehf-eye-care-gaming-monitor-review-price/) | 제목·책상 사용·조립·OSD 설정·시험 본문 | PRESENT | 영어. ASUS 리뷰 제품 제공과 구매 링크 명시. 단순 제품 소개와 구분되는 본인 시험 경험 확인. |
| U2724D | [영상](https://www.youtube.com/watch?v=EU9ckzIwnMw) | watch 제목·펼친 설명·직접 제작 챕터 | PRESENT | 영어. 정확 모델과 연결·메뉴·밝기·화면 챕터, 링크 수수료 고지 확인. 자동 생성 요약은 제외. |
| U2724DE | [두 모델 초기 인상 영상](https://www.youtube.com/watch?v=zeiJtjJBKdE) | watch 제목·펼친 게시자 설명 | UNKNOWN | 영어. U2724DE/U2724D 초기 인상으로 명시, DE 연결 기능과 조합 항목 구분. 두 모델을 함께 다루며 단독 심층 리뷰로 소개하지 않음. 동일 URL을 D 모델에 중복 등록하지 않음. |

5종 후보 5개: YouTube 3개, 블로그형 전문 리뷰 2개. 광고·제휴 맥락 PRESENT 3개, UNKNOWN 2개. 지역 SKU 동일성과 호환성 승인 근거로 사용하지 않는다. 전문 리뷰라는 분류는 독립적인 내용의 정확도 인증을 뜻하지 않는다.

## 제외·보류 자료

- [Gamedaim VA24EHF](https://gamedaim.com/review/asus-va24ehf/)는 공개 본문을 직접 확인했다. 본인 사용 경험은 있으나 VA24EF/VA24HE 등 표기가 섞여 있고 수치 오타가 있다. 더 명확한 Can Buy or Not 원문을 확보해 이 링크는 채택하지 않았다. 오타를 고쳐서 사실로 저장하지 않았다.
- [Think Different U2724DE](https://www.thinkdifferent.blog/reviews/dell-ultrasharp-u2724de-27-qhd-thunderbolt/)도 직접 열었다. 이번 배치에서는 본인 시험 범위를 명확하게 확인한 영상 후보를 우선하여 이 글은 포함하지 않았다.
- 검색에서 발견된 광고성 추천·판매 가이드·다른 모델 자료는 검색 제목이나 요약만으로 채택하지 않았다. 기존 배치에서 제외한 PA279CRV FAQ와 U2724D 혼합 가이드를 재사용하지 않았다.

## 원문 접근과 표현 경계

YouTube 2건(PA248QV, Dell 두 모델 초기 인상)의 web 원문 열람에서 내부 오류가 발생했다. 로그인·CAPTCHA 차단은 아니어서 일반 공개 브라우저 watch 페이지로 직접 열고 게시자 설명을 펼쳐 확인했다. U2724D 단독 영상도 공개 브라우저로 확인했다. 영상 전체 시청이나 실측 재현으로 주장하지 않는다. 자동 요약과 타인 댓글은 포함 근거가 아니다. 브라우저의 자동 더빙·번역 표시를 원본 언어로 혼동하지 않는다.

공개 전문 리뷰 두 글에서는 본문 중 실제 사용·시험 항목만 포함 근거로 삼았으며, 사양표·점수·추천·측정 수치를 사이트 공식 사실에 추가하지 않았다. 작성자명·닉네임·이메일·전화번호를 데이터에 저장하지 않았고 원문·사진·썸네일을 복제하지 않았다. 구매 링크를 따라가거나 영상 댓글·구독·좋아요를 변경하지 않았다. 접근 제한 우회와 대량 수집은 수행하지 않았다.

새 창 처리·데이터 계약 검증·전체 테스트·GitHub CI는 통합 세션에서 실행한다. 이 보고서는 5개 공개 원문의 모델 연결과 실제 후기 성격을 확인한 조사 기록이다.
