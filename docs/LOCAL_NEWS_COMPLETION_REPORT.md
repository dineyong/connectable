# 테크 소식 로컬 완성도 보강

2026-10-13 · `codex/monitor-purpose-design` · 기준 커밋 `bb8b899`.

## 처리한 작업

1. 기존 RSS 두 곳에만 robots.txt 확인 후 한 차례 요청했다. 두 응답 모두 성공했다. 새 출처, 예약 실행, 상시 프로세스, 유료 API 또는 계정 키는 추가하지 않았다.
2. 이전 [30건 스냅샷](../data/news/archive/tech_news_20261010.json)을 바이트 그대로 보존한 뒤 [현재 목록](../data/news/tech_news.json)과 [파생 JS](../web/tech-news-data.js)를 갱신했다. 현재 목록도 30건(삼성 20, Windows 10)으로 제한했다. 기존 목록 대비 신규 URL은 3개다. RSS의 제목·발행 시각·URL만 사용하며 기사 본문·이미지·작성자 정보는 저장하지 않는다.
3. 화면에서 출처의 마지막 요청 시각과 마지막 성공 시각, 개별 항목의 RSS 확인 시각을 구분한다. 확인 시각은 RSS 메타데이터 확인이며 기사 본문 확인이나 공개 승인 시각을 의미하지 않는다.
4. 신제품 발표 검증기가 잘못된 입력을 일관되게 거부하도록 보강했다. 출처 등록이 안 된 행, 잘못된 배열/객체, 비문자 식별자는 `ValueError`로 거부한다. 공식 호스트라도 `..`/`.` 경로, 제어문자 또는 잘못된 포트가 있는 URL을 거부한다.
5. 발표 화면에서 null 항목이 다른 정상 항목 표시까지 중단하던 경로를 막았다. 원문 링크의 새 창/탭 및 `noopener noreferrer`를 유지한다.

## 실제 요청과 공식 원문

| 출처 | 요청 결과 | 마지막 시도 / 성공 | 자료 처리 |
| --- | --- | --- | --- |
| [삼성전자 뉴스룸 RSS](https://news.samsung.com/kr/feed) | 성공 · RSS 215,515바이트 | 2026-10-13 21:31:16 한국 시간 | 제목 기반 분류, 기사 본문 미저장 |
| [Windows Blog RSS](https://blogs.windows.com/feed/) | 성공 · RSS 184,099바이트 | 2026-10-13 21:31:16 한국 시간 | 영어 제목 원문 유지, 번역 미생성 |
| [BenQ 한국 모니터 출시 발표](https://www.benq.com/ko-kr/news/products/benq-launches-ex271qmzqmqp.html) | 웹 원문 재열람 성공 | 2026-10-13 | 제목·게시일·모델 세 가지가 기존 발표 기록과 일치 |

BenQ 원문 위치는 제목과 게시일 및 신제품 3종 소개 문단이다. 원문은 EX271QMZ·EX271QM·EX271QP를 구분한다. 이번 재열람으로 제품별 사양 데이터나 판매 상태를 추가하지 않았다. [기존 신제품 발표 2건](../data/news/product_announcements.json)은 그대로 보존했다. Apple 발표의 최신 판매 상태는 이번에 재확인하지 않았으며 예약 가능 상태로 표시하지 않는다.

이전 RSS 파일 SHA-256은 `c90ac5b6dafc45a194f9e2f47d491e35af42d510965b7b394e2e3c5571dbede3`이다. 이 값과 일치하는 보존 검사를 테스트에 추가했다. 10월 10일 마지막 시도에 삼성 출처가 STALE이었던 이전 기록도 아카이브에 남는다. 현재 OK는 이번 RSS 요청 성공을 의미하며 향후 접속 성공을 보장하지 않는다.

## 재현 및 검증

기준 커밋의 검증기를 별도 메모리 네임스페이스에 읽어 아래 입력을 실행한 뒤 수정본과 비교했다. 테스트용 URL은 실제 뉴스 데이터에 넣지 않았다.

| 입력 | 수정 전 | 수정 후 |
| --- | --- | --- |
| 발표 배열의 null 항목 | TypeError | ValueError로 거부 |
| 미등록 source_id | KeyError | ValueError로 거부 |
| 허용 제조사 호스트의 `products/../x` 경로 | 통과 | 거부 |
| 허용 제조사 URL 끝의 DEL 제어문자 | 통과 | 거부 |
| 기존 정상 발표 2건 | 통과 | 계속 통과 · 파생 JS 변경 없음 |

- `python3 -m unittest tests.test_product_news tests.test_tech_news -q`: **25개 통과**, 신규 회귀 4개 포함.
- `python3 scripts/product_news.py --check`: 통과.
- `python3 scripts/tech_news.py --check`: 현재 30건 통과.
- `python3 -m py_compile scripts/product_news.py`: 통과.
- 브라우저 회귀는 확인 시각의 구분과 malformed 발표 격리 2개를 추가했다. 서브세션에서는 브라우저 서버를 띄우지 않았으며 전체 Python/데스크톱·모바일 및 CI 결과는 통합 보고서에 기록한다.

## 남은 경계와 결정

- 독립 언론 출처, 네이버 검색 API, 운영 스케줄러, 공개 배포는 여전히 미연동이다. API 사용 설정과 출처 이용 조건·운영 정책은 별도 승인 범위다.
- 공개 RSS 제공이 상업적 재사용 조건 전체를 승인한다는 의미는 아니다. 현재 `public_status=UNKNOWN`, `PENDING_PUBLICATION_REVIEW`, `noindex,nofollow`를 유지한다.
- 저장된 발표 일정은 현재 재고·판매처 혜택·사전예약 진행 여부가 아니다. 날짜가 지난다는 이유로 브라우저에서 상태를 자동 승격하지 않는다.
- RSS 제목 기반 분류와 공식 발표 본문 확인을 분리한다. 뉴스가 모니터 공식 사양이나 추천·호환성 판정 근거로 자동 전환되지 않는다.
- 이번 보강에는 사용자 결정이 필요한 신규 운영 변경이 없다. 다음 갱신에서도 이전 자료를 보존하고 결과를 검토해야 한다. 현재 아카이브는 이번 수동 갱신의 보존 기록이며 자동 아카이브 운영을 구현했다는 의미가 아니다.

## 변경 파일

- [발표 검증기](../scripts/product_news.py)
- [뉴스 원본](../data/news/tech_news.json), [이전 스냅샷](../data/news/archive/tech_news_20261010.json), [파생 JS](../web/tech-news-data.js)
- [RSS 화면 스크립트](../web/tech-news.js), [발표 화면 스크립트](../web/product-news.js)
- [발표 단위 테스트](../tests/test_product_news.py), [RSS 단위 테스트](../tests/test_tech_news.py), [브라우저 회귀](../tests/e2e/tech-news-design.spec.js)
- 이 보고서. 원본 제품 사양·질문 코퍼스·README·DECISIONS 및 기존 사용자 수정 파일은 이 세션에서 변경하지 않았다.
