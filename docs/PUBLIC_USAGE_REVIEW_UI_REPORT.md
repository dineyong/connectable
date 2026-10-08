# 공개 실사용 사례 내부 검토 UI

2026-10-08. 로컬 작업 브랜치 `research/question-corpus-foundation`, 기준 HEAD `52a8bc3`.

## 결과와 범위

기존 공개 연구 사례 PUR-001–PUR-018을 읽기 전용 목록·상세 화면으로 연결했다. 검색, 관측 항목 필터, 초기화, 빈 검색 결과, 데이터 오류, 키보드 이동, 상세 닫기와 브라우저 뒤로가기를 제공한다. 기존 목업의 색상·글꼴·구조를 재사용했다.

모든 사례는 C등급 사용자 진술이며 검토 대기다. 공식 자료 대조와 실물 검증은 수행하지 않았다. 공개 판정은 UNKNOWN, 사람 승인 골든은 0/30이다. 정상 사용 보고는 다른 구성의 호환성 승인으로 표시하지 않는다. 추가 조사, Ali 수집, 공식 catalog·판정 엔진·골든 변경, 승인 기능, 배포, 커밋과 push는 이번 작업에 포함하지 않았다.

## 파일과 데이터 흐름

- [원본 공개 연구 18건](../data/research/review/public_usage_batch_2026-10-08.jsonl)
- [검토용 매핑 18건](../data/research/review/public_usage_mapped_2026-10-08.jsonl)
- [정적 자산 생성기](../scripts/build_public_usage_review_ui.py)
- [생성된 웹 데이터](../web/review-data.js)
- [검토 페이지](../web/review.html), [스타일](../web/review.css), [동작](../web/review-app.js)
- [Python 회귀 검사](../tests/test_public_usage_review_ui.py), [브라우저 회귀 검사](../tests/e2e/review.spec.js)
- [기존 목업 진입점](../web/index.html): 메뉴·푸터에 검토 화면 링크만 추가

검증된 로컬 JSONL → Python 생성기 → 웹 정적 자산 → 목록·상세 화면 순서다. API·DB·로그인·쓰기 작업은 없다. 생성 자산에서 내부 source pointer, 행 해시와 파일시스템 경로를 제외한다. 원본 URL은 HTTPS·인증정보 없는 외부 주소만 허용하고 새 탭에는 noopener/noreferrer를 적용한다. 원문 링크 속성을 검증했으며 원문 재조사는 수행하지 않았다.

화면 출력, 신호 모드, UI 배율, 충전 보고, 클램쉘, 잠자기 복귀, 재연결을 각각 표시한다. 선택 가능한 최대 주사율·선택 설정을 실제 출력값과 구분하고 4K/FHD라는 진술에서 픽셀 수를 계산하지 않는다. 충전 보고에서 PD 협상 프로필이나 W를 추정하지 않는다. 직접 수행, 조언, 구매 계획, 제품 소개, 일시 해결과 재발, 물리 장착 간섭, 상업성 검토 메모를 구분한다. 모르는 값과 구성 범위는 UNKNOWN으로 표시한다.

## 실행과 검증

```sh
python3 -m scripts.build_public_usage_review_ui
python3 scripts/serve_mockup.py --port 8873
python3 -m unittest discover -s tests
python3 -m scripts.validate_public_usage_review
npm run test:e2e -- --workers=2
node --check web/review-app.js
git diff --check
```

- Python: 299개 통과(기존 290개 + UI 9개). v1 CSV·영어 예시·정식 v2 검증 포함.
- 검토 JSONL: 18건 통과. 원본 행 해시, C등급, UNKNOWN, 승인 0 유지.
- 브라우저: 32개 통과(기존 목업 12개 + 검토 UI 20개). 데스크톱·모바일 Chromium 153.0.8010.12.
- WCAG 자동 검사: 목록·상세에서 위반 0. 키보드, 초점 복귀, 필터 보존·초기화, 뒤로가기, 가로 넘침, 로컬 GET 요청, CSP·원본 파일 비노출 확인.
- 데이터 누락·잘못된 데이터·중첩 객체 손상은 오류 화면으로 처리하며 다른 데이터로 대체하지 않는다. HTML 주입 문자열은 문자로 표시하고 로컬 파일 URL을 차단한다.
- Codex In-app Browser에서 목록 18건, 상세, 모바일 필터와 키보드 바로가기를 직접 확인했다. 임시 모바일 viewport는 해제했다. 브라우저 콘솔 오류·경고는 관측 당시 없었다.
- 초기 테스트의 문구 오인과 다중 요소 선택 문제는 테스트를 수정했다. 실제 모바일 메뉴 숨김과 바로가기 해시 처리 문제는 UI를 수정한 뒤 전체 브라우저 검사를 다시 통과했다.

미리보기: http://127.0.0.1:8873/review.html . 자동 브라우저 검사는 별도 localhost 8874를 사용한다. 네이티브 Safari와 실제 iPhone은 검사하지 않았다.

## 보존과 검사

작업 직전 79개 파일의 SHA-256과 비교하여 기존 78개 파일은 바이트 그대로 보존됐고, `web/index.html`만 승인된 진입 링크 추가로 변경됐다. 기존 README·골든 계획의 미커밋 변경도 보존했다. v1, 영어 예시, 정식 v2, 기존 연구·매핑 18건, 공식 catalog, pilot, path 자료, 기존 목업 app/styles/cases 및 기존 테스트를 변경하지 않았다.

새 웹 데이터의 개인정보·비밀값·로컬 경로 패턴, 외부 URL, 내부 문서 링크, JSON/JS 문법과 git diff를 검사한다. 공개 원문의 개인 사용자명은 UI에 추가하지 않는다. 테스트의 가상 악성 문자열·로컬 URL은 보안 거부 검사 전용이다.

## 화면 기록

- [데스크톱 목록](screenshots/public-usage-review-desktop.png)
- [모바일 목록](screenshots/public-usage-review-mobile.png)
- [데스크톱 상세](screenshots/public-usage-detail-desktop.png)
- [모바일 상세](screenshots/public-usage-detail-mobile.png)

## 남은 한계와 최소 다음 단계

데이터는 기존 연구 요약의 매핑으로 원문 전체 재확인이나 공식 근거가 아니다. 모델/SKU/길이, OS 버전, 실제 픽셀 타이밍, PD W, 화면 수와 연결 경로에는 결측이 남는다. 정적 자산은 JSONL 변경 시 생성기를 다시 실행해야 한다. 검색·필터 결과 수는 호환성 성공률이 아니다. noindex는 인증·접근 통제가 아니며 현재 서버는 localhost에서만 제공한다.

다음 최소 작업은 이 화면으로 사람이 사례별 출처·관측 범위를 검토하고, 명확한 사례만 별도 공식 근거 대조 후보로 고르는 것이다. USER_REPORT를 공식 claim이나 승인 골든으로 자동 승격하지 않는다.
