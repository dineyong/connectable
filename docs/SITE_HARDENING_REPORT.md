# 사이트 목업 추가 보강과 리뷰 준비

2026-10-07, 사용자 추가 진행 요청에 따른 작업. 기준 시작 커밋 `554e0c1`.

## 반영한 변경

- [3차 마이그레이션](QUESTION_CORPUS_V2_MIGRATION_BATCH_3_REPORT.md)으로 20건 이전 완료. 사이트 파생 사례 자산 재생성.
- 입력 변경 시 오래된 결과를 제거하여 이전 기기·칩 조건이 현재 입력 결과로 보이지 않게 수정.
- 입력 오류 aria-invalid와 오류 안내 연결, 초점 이동, 검색 결과 수 라이브 안내, 본문 바로가기.
- 상세 창 접근 가능한 제목·Escape 닫기·원래 카드 초점 복귀.
- 원문 링크 HTTPS 제한, 사용자 입력 HTML 이스케이프 회귀 검사.
- 페이지 noindex/nofollow, 외부 Google Fonts 요청 제거, 시스템 글꼴로 오프라인 표시.
- [전용 로컬 서버](../scripts/serve_mockup.py): 웹 루트만 노출, 디렉터리 목록 차단, CSP·nosniff·no-referrer·DENY·no-store 헤더.
- 읽기 어려웠던 보조 텍스트·배지·그림 설명의 명암 대비 수정. 디자인 구조는 유지.
- [브라우저 테스트](../tests/e2e/mockup.spec.js)와 잠금 파일, 코드 정렬 도구 추가. 생성 cases.js는 정렬하지 않고 생성기로만 변경.
- [GitHub Actions](../.github/workflows/validate.yml)에 데이터/Python/브라우저 검사 등록. 외부 배포나 main merge는 없음.

## 전체 흐름 검증

`vercel:verification` 스킬의 원본→응답→브라우저 방식으로 검수했다.
현재 데이터 흐름은 JSONL→Python 파생 생성→정적 JS 응답→카드/검색/상세 화면이다.
입력 흐름은 브라우저 폼→미확인 체크리스트이며 API·DB·외부 판정 호출은 없다.

| 경계 | 검증 |
| --- | --- |
| 원본→파생 | Python 재생성 바이트·ID·결과·관측·URL 일치 검사 |
| 서버→브라우저 | 실제 Chromium 페이지 HTTP 200·자산 실행·보안 헤더 확인 |
| 입력→결과 | 누락 필드·미확인 상태·충전 요청·입력 변경 시 이전 결과 제거 |
| 파생→사례 화면 | 검색·필터·더 보기·빈 결과·상세 원문 링크 |
| 키보드·접근성 | 상세 제목·Escape·초점 복귀·axe WCAG 2 A/AA 및 2.1 AA 태그 검사 |
| 악의적 입력 | img/onerror 문자열은 텍스트이며 이미지 DOM이 생성되지 않음 |
| 화면 폭 | 데스크톱 및 iPhone 13 크기 Chromium에서 가로 넘침 없음 |

Python 131개 PASS(기존 126개 + 마지막 배치 5개). Playwright 6개 흐름 × 데스크톱/모바일 = 12개 PASS.
초기 axe 검사에서 낮은 글자 대비가 발견됐고 실제 스타일을 수정하여 페이지와 상세 창 위반 0건으로 재검사했다.
규칙을 비활성화하거나 대비 검사를 제외하지 않았다. 모바일은 Chromium의 크기·터치 에뮬레이션이며 실제 iOS Safari 검수는 아니다.
자동 axe 통과가 모든 접근성 준수나 저시력 사용자 검수를 보장하지 않는다.

## 다시 실행

```sh
python3 scripts/build_mockup_cases.py
python3 -m unittest discover -s tests -q
python3 scripts/validate_question_corpus_v2.py
npm ci
npx playwright install chromium
npm run test:e2e
python3 scripts/serve_mockup.py
```

미리보기는 http://127.0.0.1:8873 이다. e2e 전용 서버는 8874이며 테스트가 자동 실행·종료한다.
테스트용 Node 의존성만 추가했으며 사용자 화면에는 프레임워크·빌드 서버·npm 의존성이 없다.
폰트 삭제로 이전 스크린샷과 글꼴 모양은 달라질 수 있다. 원문은 새 창 HTTPS 링크로만 열며 로컬 폼 값을 보내지 않는다.

## 코드 리뷰 범위와 다음 작업

클로드 리뷰는 README·DECISIONS부터 읽고 web/·scripts/build_mockup_cases.py·scripts/serve_mockup.py·tests/·playwright.config.js·워크플로를 확인한다.
입력값 처리, CSP, 초점·알림·모바일, 원문과 관측 출처, 결과 표현의 오해 가능성, 테스트의 실질적 검증을 우선한다.

추가 80건 수집, 공식 사양 데이터 및 판정 규칙, 실제 Safari/Firefox, 공개 배포 환경 헤더는 미완료다.
외부 배포·계정·결제·제휴·공식 제조사 사양 추정은 수행하지 않았다. 현 사이트는 운영 호환 판정 서비스가 아닌 조사 기반 목업이다.
생산용 도메인과 인프라를 선택한 뒤 별도 실제 배포 검수가 필요하다.

[최신 브라우저 검수 화면](screenshots/connectable-hardened.png)을 보존했다.
