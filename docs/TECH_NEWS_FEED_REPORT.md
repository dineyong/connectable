# 테크 소식 RSS 시제품 보고서

2026-10-10. 로컬 검토용이며 공개 상태 UNKNOWN, 기사별 PENDING_PUBLICATION_REVIEW다.

## 확보 및 화면

공개 RSS 두 곳에서 제목·원문 URL·발행 시각·확인 시각 30건을 확보했다. 전문·이미지·작성자 정보는 수집하지 않았다.

- [삼성전자 뉴스룸 RSS](https://news.samsung.com/kr/feed): 한국어 제조사 발표 20건. 최초 직접 요청 성공 이후 갱신 실패로 STALE이며 기존 제목과 최초 확인 시각을 보존했다.
- [Windows Blog RSS](https://blogs.windows.com/feed/): 영어 제조사 발표 10건, 마지막 요청 OK.

[JSON 원본](../data/news/tech_news.json), [파생 JS](../web/tech-news-data.js), [화면](../web/tech-news.html)을 분리한다. 모니터/디스플레이 필터는 제목 키워드 기반이며 본문 내용 판정이 아니다. 화면에 제조사 발표·언어·발행 시각·출처 갱신 실패를 구분하고 안전한 원문 링크로 안내한다. 홈에 테크 소식 링크를 추가했다. 기존 모니터 탐색·후기 데이터는 변경하지 않았다.

## 수집과 이용 경계

[삼성 robots](https://news.samsung.com/robots.txt), [Windows robots](https://blogs.windows.com/robots.txt)를 요청마다 먼저 확인한다. 최초 공개 요청에서 접근 가능했으며 후속 robots HTTP 오류도 실패로 처리한다. 로그인·CAPTCHA·차단 우회는 하지 않는다. 요청은 두 고정 RSS와 해당 robots에 한정한다. 리다이렉트는 따라가지 않으며 TLS·호스트·포트·크기·시간 제한을 적용한다. XML entity/DOCTYPE·NUL을 거부하고 HTML 오류 페이지는 RSS로 채택하지 않는다.

[Ars RSS 안내](https://arstechnica.com/rss-feeds/)도 검토했으나 재배포·캐싱 이용 조건과 robots 검토가 필요하여 활성 출처에서 제외했다. RSS 공개 제공이 광고 수익 사이트의 재사용 권리 전체를 승인한다는 의미는 아니다. 공개 전 발행처 조건·허용 범위·삭제 요청 절차를 별도 검토한다. 뉴스룸만 있는 현재 구성은 독립 뉴스 전체를 대표하지 않는다. 번역이나 AI 요약은 생성하지 않는다.

## 자동 갱신의 실제 범위

```sh
python3 scripts/serve_tech_news_preview.py --port 8875
```

위 서버가 실행되는 동안 15분마다 RSS를 확인한다. 커밋 원본은 읽기만 하고 `.runtime-tech-news.json`의 Git 무시 캐시를 갱신한다. 프로세스가 종료되면 자동 확인도 중지된다. 브라우저 목록 다시 보기 버튼으로 최신 캐시를 읽는다. 공개 서버·상시 스케줄러·실시간 푸시·배포는 설정하지 않았다. 기본 첫 갱신은 시작 15분 후다. 따라서 “실시간 운영 완료”로 보고하지 않는다.

```sh
python3 scripts/tech_news.py --check
python3 -m unittest tests.test_tech_news -q
```

수동 `python3 scripts/tech_news.py`는 저장소 스냅샷을 갱신하므로 변경을 검토 후 커밋한다. 운영 반복 갱신에는 로컬 서버의 무시 캐시를 사용한다. 실패한 출처는 이전 목록을 유지하고 최종 성공 시각을 새 시각으로 꾸미지 않는다.

## 검증과 남은 작업

16개 Python 회귀 테스트로 RSS/Atom, 링크·날짜·크기·entity 거부, 실패/빈 응답 보존, 승인 보류, 파생 JS 일치를 검사한다. 브라우저 세 시나리오를 데스크톱/모바일에서 실행해 필터·출처 상태·텍스트 삽입·악성 링크 제외·접근성/가로 넘침을 검증한다. 전체 결과는 [배치 보고서](MONITOR_RESEARCH_NEWS_BATCH_REPORT.md)에 기록한다.

추가 독립 한국어 매체의 허용 RSS, 뉴스 보존 기간, 공개 수집 정책, 장애 알림, 예약 실행·페이지 자동 갱신과 중복 URL 정규화의 확장은 남아 있다. 지금은 뉴스 읽기 보조 화면의 시제품이다.
