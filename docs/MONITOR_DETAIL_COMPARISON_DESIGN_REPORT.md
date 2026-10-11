# 상세·비교 화면 디자인 통일

- 작업일: 2026-10-11
- 브랜치: `codex/monitor-purpose-design`
- 시작 커밋: `5fc7ccf01b3ce3f56612925b71855358cdc93062`
- 최종 커밋은 이 문서를 포함한 Git 커밋으로 식별한다.

## 변경

승인된 용도부터 메인 디자인의 연녹색·진녹색 스타일을 제품 상세 모달, 독립 상세 페이지 30개, 비교 모달에 적용했다. 모바일 상세는 항목별 카드로 표시하고 값·조건·근거 라벨을 유지한다. 비교표는 항목명과 헤더를 고정하고 가로 이동 안내를 제공한다. 출처 링크, 미확인 안내, 조건 차이 표시, 로컬 반응은 유지한다.

원본 조사 데이터, 수치, 지역 SKU 상태, 공개 승인 상태와 필터 로직은 변경하지 않았다. 독립 상세 HTML의 변경은 data-label과 접근성 설명뿐이다. 기존 다른 작업의 README, DECISIONS, content-review 테스트, site-v2.js 변경은 포함하지 않는다.

## 검증

- `python3 -m unittest discover -s tests -q`: 520 통과, 48.192초.
- `npm run test:e2e`: 로컬 140 통과, 41.0초.
- 새 반응형 테스트: 상세 근거 보존·가로 넘침·고정 비교 항목·출처·미확인·차이 토글, 데스크톱과 모바일 4개 통과.
- 로컬 140개에는 기존 미커밋 content-review 테스트 14개가 포함된다. 이 커밋은 해당 변경을 포함하지 않으므로 원격은 126개가 예상된다.
- `python3 scripts/build_monitor_pages_v3.py --check`: 30개 일치.
- `git diff --check`: 통과.
- `git diff -- data`: 변경 없음.
- 브라우저에서 데스크톱 상세·비교 및 390px 모바일 상세를 직접 확인했다.

## 검수 이미지

- [데스크톱 상세](screenshots/monitor-detail-purpose-desktop.png)
- [모바일 상세](screenshots/monitor-detail-purpose-mobile.png)
- [데스크톱 비교](screenshots/monitor-compare-purpose-desktop.png)

## 남은 작업

구조화된 복합 값 일부는 아직 JSON 형태로 표시된다. 다음 단계에서 값·단위·조건을 보존하는 사용자용 표현을 설계할 수 있다. 실제 제품 이미지의 사용 권한 및 지역 SKU 확인, 실제 댓글 저장은 이번 작업에 포함하지 않았다. 로컬 8875 정적 미리보기이며 공개 배포·main 병합은 하지 않았다. 뉴스 자동 갱신은 이 미리보기 서버에서 실행하지 않는다.
