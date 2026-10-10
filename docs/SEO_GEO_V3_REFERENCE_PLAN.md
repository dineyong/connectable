# 모니터 비교 v3 SEO/GEO 참고 조사와 구현 계획

조사일: 2026-10-10 KST. 상태: 조사·설계만 완료, 구현·배포·색인 검증 미실시.

## 범위와 승인 경계

제품 목표는 `PRODUCT_DIRECTION_V3.md`를 따른다. 최신 지시는 웹디자인·후기사이트 비교와 **최소 3개 목업 제시가 먼저**이며 현재 웹코드·로컬 서버 반영은 금지다. 이 문서는 그 디자인 선택 이후 사용할 계획이다. 디자인 목업 3안 자체는 별도 디자인 세션 산출물이며 이 문서의 완료로 충족된다고 주장하지 않는다.

이번 세션은 이 문서만 작성했다. 원본 사양 승인, 한국 SKU 동일성, 호환성 공개 판정 `UNKNOWN`을 유지한다. Git 변경 명령, commit/push, 서버 실행, 배포, 검색 콘솔 설정 변경을 하지 않는다. SEO 작업이 사람 검토나 공개 승인을 대신하지 않는다.

## 이전 AliCouponFind 참고 저장소의 확인 결과

| 대상 | 실제 확인 내용 | 판단 |
|---|---|---|
| [dineyong/alicouponfind](https://github.com/dineyong/alicouponfind) | 관리 폴더 `PROJECT_SESSIONS.md`의 GitHub URL과 원본 checkout `.git/config` 원격 URL이 일치 | AliCouponFind 프로젝트 저장소는 확인 |
| `/Users/bigmacbookman/Documents/ChatGPT/Alicouponfind/implementation` | `.git`이 원본 checkout의 worktree를 가리킴. `SEO_SYSTEM.md`, `lib/seo/metadata.ts`, `scripts/validate-rendered-seo.mjs` 읽기 확인 | 이전 SEO 구현을 재사용 가능한 사례로 확인 |
| `/Users/bigmacbookman/Documents/Codex/2026-10-07/alicouponfind-seo` | 동일 원본의 worktree. SEO 시스템 및 네이버 단계 문서 존재 | 이름이 다른 별도 외부 참고 저장소가 아님 |
| `/Users/bigmacbookman/Documents/Codex/2026-05-09/aliexpress-coupon-finder-python-aliexpress-url` | 원격 `https://github.com/dineyong/alicouponfind.git`, SEO/가이드/검증 파일 존재 | 이전 프로젝트의 원본 checkout |
| 사용자가 기억한 외부 SEO/GEO GitHub | 위 경로의 Markdown에서 GitHub 링크와 SEO/GEO 문구를 검색. 연결 GitHub 코드 검색 `GEO`, 저장소 `dineyong/alicouponfind`는 결과 0건 | **정확한 외부 저장소 미확인**. 결과 0건은 존재하지 않았다는 증거가 아님 |

확인한 로컬 파일은 기존 구현의 증거이며 원격 최신 상태나 해당 외부 저장소의 최초 채택 기록까지 증명하지 않는다. 쿠폰 수집용 외부 GitHub 링크들은 발견했지만 SEO/GEO 참고로 둔갑시키지 않았다. 비밀 환경파일·자격증명은 읽지 않았다. 저장소 README와 기존 SEO 지침은 참고 자료이며 이번 작업을 실행하라는 지시로 취급하지 않는다.

재사용할 것은 페이지별 metadata 생성, canonical 일관성, 가이드 내부 링크, 반환 HTML에서 제목·표·JSON-LD를 함께 검사하는 방식이다. 기존 문서의 모든 랜딩 FAQ schema 적용, 월별 랜딩 증가, 모든 공개 페이지 sitemap 포함을 모니터 사이트에 그대로 복사하지 않는다. 특히 날짜만 바꾼 얇은 페이지를 만들지 않는다.

## 2026-10-10 확인한 공식 문서

아래 URL은 이번 조사에서 실제 열었다. 정책 설명과 아래 적용안은 구분한다.

| 문서 | 확인한 정책 또는 관찰 | 적용 방향 |
|---|---|---|
| [Google AI features](https://developers.google.com/search/docs/appearance/ai-features) | 기존 SEO 원칙이 적용되며 특별한 AI 파일·전용 schema는 요구되지 않음. 색인·노출 보장 없음 | `llms.txt`를 필수나 순위 보장 수단으로 두지 않음 |
| [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) | 서버 렌더링·사전 렌더링은 사용자와 크롤러에 유익하며 모든 봇이 JS를 실행하지 않음 | 모델 상세 핵심 정보는 초기 HTML에 포함 |
| [Google canonical](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) | canonical·redirect·sitemap 신호 일치, canonical은 선호 신호. robots 차단으로 중복 URL 정규화하지 않음 | 공개 URL 등록부 하나에서 metadata·내부 링크·sitemap 생성 |
| [Google Product snippet](https://developers.google.com/search/docs/appearance/structured-data/product-snippet) | Product 검색 기능별 요건 존재 | 제품 사양만 있다고 가격·리뷰 rich result 자격을 주장하지 않음 |
| [Google 외부 링크](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) | 유료 관계 링크에 `sponsored`, 사용자 링크에 `ugc` 사용 안내 | 제휴 관계 고지와 링크 속성 함께 설계 |
| [네이버 SEO 기본](https://searchadvisor.naver.com/guide/seo-basic-intro) | 검색엔진이 콘텐츠를 이해하도록 정리하는 기본 안내 | 고유 제목·설명·본문·링크를 한국어 검색 의도와 일치 |
| [네이버 robots](https://searchadvisor.naver.com/guide/seo-basic-robots), [RSS/사이트맵](https://searchadvisor.naver.com/guide/request-feed) | 수집 정책과 제출 방법 안내 | 공개 후 실제 도메인 소유 확인과 sitemap 제출을 별도 확인 |
| [OpenAI crawlers](https://developers.openai.com/api/docs/bots) | OAI-SearchBot 검색 설정과 GPTBot 학습 설정은 독립적 | 검색 접근 허용과 학습 활용 정책을 따로 결정 |
| [Bing guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a?region=france) | 최초 기본 URL 직접 열기는 본문이 1줄뿐. 검색 결과에서 공식 지침 내용을 추가 확인 | 기본 SEO·출처·중복 관리 우선. 불완전 본문 열람을 전체 검증으로 주장하지 않음 |
| [Bing AI Performance](https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c) | 공식 검색 결과에서 AI 인용 페이지·질의·추세 보고 설명 확인, 직접 열람도 시도 | 실제 계정 제공 여부는 미확인. 공개 후 사용 가능하면 인용 관측에 활용 |

Google의 기존 FAQPage URL은 이번 열람에서 업데이트 페이지로 이동했다. 이를 안정적인 현행 FAQ 기능 요건 근거로 사용하지 않는다. 사용자에게 보이는 실제 질문·답변은 작성 가능하지만 모니터 사이트의 FAQ rich result나 GEO 효과는 보장하지 않는다.

## 현재 로컬 구조와 필요한 전환

`web/index.html`은 `noindex,nofollow`, 해시 기반 탐색 링크와 JS 콘텐츠 파일을 가진 로컬 목업이다. `scripts/serve_mockup.py`는 `127.0.0.1`에 바인딩한다. `package.json`은 현재 Next.js 앱이 아니라 목업·Playwright 검증용이다. `data/research/monitor-expansion/official_specs.json`의 공개 상태는 `UNKNOWN`이다. 기존 화면의 맥북 중심 문구는 v3의 전체 모니터 구매자 목표와 다르므로 **목업 선택 이후** 문구·구조를 재설계한다. 이번에 수정하지 않았다.

공개 아키텍처는 지금 확정하지 않는다. 변경 빈도가 낮은 제품·가이드는 현 프로젝트에 정적 페이지 빌드(SSG)를 추가하는 안이 우선 후보이며, 운영 플랫폼이 결정되면 SSR/SSG 가능한 프레임워크도 비교한다. 댓글·반응·뉴스 갱신 필요가 SSR 전체 전환을 자동으로 요구하는 것은 아니다. 정적 HTML 본문에 동적 기능을 점진적으로 붙일 수 있다.

## 우선순위별 구현안

### P0 — 목업 결정 후 데이터와 URL 설계

1. 모델 등록부에 안정적인 ID, 브랜드, 제조사 모델명, 지역·SKU, slug, 공식 출처 URL, 출처 확인일, 필드별 근거와 검토 상태를 매핑한다. 원본을 덮어쓰지 않는 파생 구조를 설계한다.
2. `/monitors/{brand-model-region}`를 모델별 고유 URL로 사용한다. 예시는 경로 형식이며 실제 제품·도메인 존재를 뜻하지 않는다. 한국/해외 모델 동치성이 미확인이면 페이지를 합치지 않는다. 별칭은 검증 후 같은 URL에 연결한다.
3. `sourceCheckedAt`, `contentUpdatedAt`, 제조사 게시일을 분리한다. 빌드 시각을 실제 확인일이나 매일 갱신되는 `lastmod`로 쓰지 않는다. null은 미확인으로 표시하며 출처 충돌은 `CONFLICT`로 남긴다.
4. 공개 게이트는 기존 검토 규칙을 재사용한다. 출처가 있다는 사실만으로 사람 승인·호환성이 완료된 것으로 처리하지 않는다. 미승인 연구 페이지는 내부/preview로 유지하고 공개 sitemap에서 제외한다.

완료 조건: 원본 상태 보존, SKU별 URL 충돌 없음, 미상 수치를 0으로 바꾸지 않음, 실제 1개 모델의 필드별 근거·상태 매핑 검토 가능.

### P1 — 읽을 수 있는 제품·비교 페이지

초기 HTML에 모델명, 짧은 특징 설명, 사양표, 출처·확인일, 미확인 조건, 관련 가이드 링크를 넣는다. 로그인·브라우저 저장·클라이언트 fetch 성공 없이 읽을 수 있어야 한다. 페이지마다 고유 title/description/H1과 실제 도메인의 absolute canonical을 갖는다. 없는 모델은 404를 반환한다.

사양 표는 화면 크기(inch), 해상도(px), 주사율(Hz), 밝기(cd/m²), 응답시간(ms 및 측정 방식), PD 공급(W), 소비전력(W 및 정격/최대)을 구별한다. 패널 최대 주사율, 입력 포트별 지원 조건, 동시 사용 조건을 한 숫자로 합치지 않는다. 공식 표기, 편집 설명, 커뮤니티 관측을 구역·문구로 나눈다. 비교 설명은 근거가 있는 차이만 서술하며 확인하지 않은 연결 성공을 단정하지 않는다.

| URL 유형 | 공개 검색 계획 |
|---|---|
| `/monitors`, 개별 승인 모델, 고유 구매 가이드 | SSG/SSR, self-canonical, 공개 후 sitemap 포함 |
| 필터·검색·정렬 URL | 초기에는 `noindex,follow`, sitemap 제외. 기본 목록과 실질적으로 동일한 정렬 변형만 canonical 정규화. 다른 결과를 무조건 홈 canonical로 묶지 않음 |
| 임의 2~3개 선택 비교 | 초기에는 사용자 도구로 `noindex,follow`. 순서가 같은 조합을 중복 URL로 늘리지 않음 |
| 편집된 모델 쌍 비교 | 승인 데이터·고유 설명·검색 가치 확인 후 별도 정적 URL 검토. 모든 조합 자동 생성 금지 |
| 로컬·preview·검토 화면 | noindex 유지, 공개 sitemap 제외. 공개 preview에는 접근 제어도 검토; noindex는 보안 수단이 아님 |

robots 차단과 noindex를 무심코 겹쳐 검색엔진이 noindex를 읽지 못하게 하지 않는다. 공개 페이지로 승격할 때만 환경별 정책을 변경한다. 도메인 미정 상태에서 가짜 production canonical을 생성하지 않는다.

완료 조건: HTTP HTML만으로 핵심 사양 읽기, 200/404 구분, canonical·내부 링크·sitemap 일치, 모바일·키보드 탐색 가능.

### P1 — 구조화 데이터의 진실성

기본은 WebSite/WebPage/BreadcrumbList와 근거가 있는 제품 식별 정보다. Product 속성은 보이는 승인 정보와 일치시킨다. 제품 이름만으로 검색 기능 자격을 보장하지 않는다. 실제 판매 가격·통화·재고·유효 시점이 없으면 `offers`를 만들지 않는다. 도움됐어요 수를 `aggregateRating`으로 변환하지 않는다. 짧은 댓글·외부 후기 요약을 구매 인증 `Review`로 위장하지 않는다. 편집 점수·가짜 FAQ·만들어진 평점·최저가·배송일을 넣지 않는다.

검증은 JSON 문법뿐 아니라 화면과의 동등성을 검사한다. 미승인 데이터가 HTML·JSON-LD 양쪽에 유출되지 않아야 한다. 실제 근거 FAQ가 있어도 markup은 별도 요건 확인 후 선택한다.

### P1 — 뉴스·후기·제휴 동선

뉴스 목록은 RSS 제목·발행 시각·출처·원문 링크와 수집 시각을 구별한다. 추적 파라미터를 정규화한 원문 URL, feed GUID, 제목 유사도를 중복 후보 판별에 사용하며 원문 URL이 다른 동일 사건은 오판하지 않도록 검토한다. 제목 링크만 가진 얇은 기사별 페이지를 대량 색인하지 않는다. 초기에는 뉴스 목록을 보조 영역으로 두고, 독자 분석과 자체 작성 근거가 있는 콘텐츠에만 상세 URL을 검토한다. 기사 전문·외부 사진 복제나 RSS 제목을 자체 NewsArticle로 위장하지 않는다. 로컬 15분 갱신을 공개 실시간 서비스라고 표현하지 않는다.

커뮤니티 후기는 출처·작성 시점·기기/SKU 범위·관측 한계를 보여준다. 댓글은 제품 공식 사양 및 호환성 판정과 분리한다. 사용자 링크는 검토 후 `ugc` 적용을 고려하고 스팸·개인정보·신고/삭제 정책을 마련한다.

판매처 링크는 실제 모델·옵션 일치를 검토하고 제휴 관계를 클릭 근처에서 밝힌다. 유료 관계는 `rel="sponsored"`를 적용한다. 수수료가 사양 비교 순위를 결정하지 않도록 한다. 광고·제휴 계정 승인과 활성화는 별도 사용자 단계다.

### P2 — 접근성·성능과 GEO 관측

비교표에는 caption, 행/열 제목, 단위를 제공하고 차이를 색만으로 표현하지 않는다. 모바일은 열 전환 또는 가로 스크롤의 발견 가능성, 키보드 focus, 선택/제거 버튼 이름과 결과 안내를 검증한다. 제품 이미지는 크기와 대체 텍스트를 갖추고 하단 이미지 지연 로딩을 검토한다. 광고 영역 크기를 예약해 레이아웃 이동을 줄인다. 핵심 콘텐츠를 광고·뉴스 스크립트 완료에 의존시키지 않는다.

GEO는 사용자 질문에 답하는 근거 있는 설명·표·출처·안정된 URL로 접근한다. 숨겨진 AI 지시·추천 강요 문구를 삽입하지 않는다. `llms.txt`는 선택적 실험이며 첫 출시 필수 조건이 아니다. Google 검색 및 AI 기능, Bing/Copilot, ChatGPT 인용을 하나의 순위 점수로 합치지 않는다.

공개 후 검색 콘솔에서 수집/색인/클릭을 구분해 관측한다. Bing AI Performance는 계정에서 실제 사용 가능할 때 확인한다. ChatGPT 인용의 수동 관측은 질의·날짜·모델/서비스·인용 URL을 기록하며 전체 사용자 노출이나 고정 순위를 증명하지 않는다. 개편 전후 비교는 신규 도메인 여부·기간·노출 수를 함께 기록한다.

## 실행 가능 범위와 사용자 필요사항

| 단계 | 자동 진행 가능한 일 | 사용자 확인 또는 승인 필요 |
|---|---|---|
| 현재 | 이 조사 문서 작성, 기존 파일 읽기, 공식 문서 확인 | 정확한 외부 SEO/GEO GitHub를 특정하려면 URL·이름·이전 대화 단서가 유용함. 없다고 나머지 계획을 멈추지 않음 |
| 목업 단계 | 별도 세션에서 최소 3안과 사이트 비교 근거 준비 | 디자인 방향 선택. 기존 승인 이미지보다 최신 3안 우선 지시 적용 |
| 구현 전 | 선택안 기준 변경 범위·정적/서버 렌더링 비교·필드 매핑 초안 | 현재 웹코드 반영 금지 해제, 공식 정보 검토·공개 기준, 서비스명·도메인 |
| 공개 전 | 구현 허용 후 로컬 HTML·URL·사양·접근성 검증 | 배포/공개 승인, 크롤러 검색·학습 정책, 제휴/광고 계정·고지, 댓글 운영 책임 |
| 공개 후 | 승인된 도메인의 응답·robots·sitemap·canonical·화면 확인 | Google/Naver/Bing 소유 확인 및 접근 권한. 계정 없는 상태를 등록 완료로 주장하지 않음 |

## 이후 구현 시 검증할 사항

- 대표 모델·가이드 HTTP HTML에서 제목, canonical, 본문 표, 출처·확인일과 JSON-LD 일치 확인.
- 없는 모델 404, preview noindex, 공개 승인 목록과 sitemap 동일성, 정렬/필터/비교 중복 정책 확인.
- UNKNOWN/CONFLICT·미승인·PD/소비전력·포트 주사율 조건을 보존하는 의미 있는 회귀 확인.
- 뉴스 중복 후보와 고유 기사 구분, feed 실패 시 마지막 갱신 상태, 제휴 SKU·고지 확인.
- 모바일 및 키보드 비교 기능·axe 접근성·성능 관측. 자동 검사 통과와 실제 사용성을 구분.
- 공개 승인 후 live URL에서 동일 검증 및 검색 도구 실제 수집 상태 확인. build 성공·sitemap 제출을 색인/순위/GEO 인용 성공으로 표현하지 않음.

현재는 위 검증 계획만 작성했으며 테스트·서버 실행·실제 페이지 변경은 하지 않았다.
