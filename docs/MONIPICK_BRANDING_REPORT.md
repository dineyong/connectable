# 모니픽 이름·비공개 검수 안내·메타데이터 정리

기준일: 2026-10-22. 작업 브랜치: `codex/monipick-cloudflare-preparation`.
기준 커밋: `7f7918f`, 구현 커밋: `ea01a29`.

## 적용 범위

- 현재 검수 후보의 HTML 37개: 탐색, 뉴스, 안내, 404, 구매 가이드, 10종 보강 자료, 모니터 목록, 제품 상세 30개.
- 로고 텍스트·본문·푸터·문서 제목의 Connectable 표기를 **모니픽**으로 변경했다.
- 과거 연구 문서·기존 사이트/관리 화면·archive·저장소/폴더 이름은 일괄 변경하지 않았다. 기존 사용자 변경이 있는 README/DECISIONS는 그대로 보존했다. 이번 서비스 표시명의 기준은 이 보고서와 현재 검수 화면이며 과거 문서의 Connectable은 프로젝트 이력이다.
- `connectable-v3-comparison`, 도움 반응 저장 키, JS 전역 이름과 데이터 ID를 유지했다. 서비스 이름 변경 때문에 사용자의 기존 브라우저 선택이나 원본 참조를 초기화하지 않는다.

## 문구와 메타데이터

- ‘로컬 미리보기’ → **비공개 검수 중**. 공개·사람 검수 완료로 오인할 표현은 넣지 않았다.
- ‘로컬 시연’·‘로컬 검토용’ 등 환경 설명을 정리하고, 사양 범위·미확인·광고 미활성 등의 실제 안내는 유지했다.
- 404의 “실제 호스팅 404는 공개 전 확인” 문구를 삭제하고 주소 확인·검색 안내로 바꿨다. 이전 원격 검수에서 실제 404를 확인한 기록은 보존했다.
- 페이지별 title/description과 Open Graph/Twitter title/description을 일치시켰다. `og:site_name=모니픽`, `og:locale=ko_KR`, `og:type=website`를 적용했다.
- 생성 문서에는 [메타데이터 함수](../scripts/site_branding.py)를 사용한다. 모델명을 메타 태그에 넣을 때 HTML 이스케이프한다. 기존 [제품 문서 생성기](../scripts/build_monitor_pages_v3.py)와 [보강 문서 생성기](../scripts/build_monitor10_review.py)를 갱신하고 결과를 재생성했다.
- 정식 도메인 canonical·og:url·sitemap·가격/별점/후기 구조화 데이터를 추가하지 않았다. 문서 noindex/nofollow, Cloudflare 헤더·robots 및 Access 보호를 유지했다. 공유 메타데이터를 넣었다고 공개 공유 미리보기나 검색 색인이 활성화된 것은 아니다.
- 미확인/충돌·해외 공식 문서와 한국 SKU·PD와 소비전력·반응의 브라우저 저장·뉴스의 저장 목록 안내를 유지했다. ‘로컬 디밍’ 같은 제품 사양 용어도 바꾸지 않았다.

## 검증

| 검사 | 결과 |
| --- | --- |
| 변경 전 Python 전체 | 623개 통과 |
| 변경 후 Python 전체 | 626개 통과 |
| 관련 Python 묶음 | 40개 통과 |
| 데스크톱·모바일 브라우저 전체 | 224개 통과; 보존한 사용자 미커밋 테스트 14개 포함 |
| 현재 HTML 37개 | 이름·제목·설명·공유 메타데이터 일치, 이전 문구 제거, noindex/도메인 보류 검사 통과 |
| 내부 HTML/자산 경로 | `python3 scripts/validate_local_site.py` 통과 |
| 정적 문서 재현성 | 제품 30개·10종 보강 페이지 생성 결과 일치 |
| Cloudflare 후보 | 61개 파일 생성 통과; 검수 점검 파일은 opt-in만 포함 |
| 보존 | 모든 data/schema 및 기존 사용자 변경 4개 SHA-256 일치 |
| 사양·후기 보존 | 30개 제품의 사양 표·미확인 목록/원본 메모·외부 후기 section이 기존 HEAD와 바이트 일치 |
| 개인정보·비밀값·diff | 변경 소스 이메일/토큰 패턴 검사 및 `git diff --check` 통과 |

추가한 [Python 테스트](../tests/test_site_branding.py)는 현재 HTML 전체, 메타데이터 이스케이프, 저장 키/불확실성 안내 보존을 검사한다. [브라우저 테스트](../tests/e2e/site-branding.spec.js)는 8개 대표 경로에서 로고·제목·메타데이터·공개 보류·가로 넘침을 데스크톱/모바일로 확인한다. 기존 출시 후보 테스트는 변경된 안내 영역 이름에 맞춰 선택자만 갱신했다.

테스트 명령:

```sh
python3 -m unittest discover -s tests -q
python3 -m unittest tests.test_site_branding tests.test_monitor_pages_v3 tests.test_monitor10_review tests.test_prepare_launch_preview tests.test_prepare_cloudflare_preview -q
npm run test:e2e -- --workers=2
python3 scripts/validate_local_site.py
python3 -m scripts.prepare_cloudflare_preview --output /tmp/monipick-branding-preview-20261022 --include-http-check
```

자동 생성된 기존 테스트 캡처 2개만 실행 전 Git 내용으로 복원했다. 사용자 수정 파일이나 원본은 복원 대상에 넣지 않았다. 첫 로컬 화면 확인은 꺼져 있는 8875 서버 때문에 접속 실패했으며, 검수 서버 8876에서 다시 열어 실제 화면을 확인했다.

## 공개 보류와 남은 항목

- main 병합, production 배포, DNS/Custom domain 연결, 검색 색인·광고·제휴·유료 플랜 활성화는 하지 않는다.
- 제품 실제 사진 사용권, 한국 SKU와 남은 공식 문서 충돌, 공개 반응 서버, 뉴스 수집 운영 등은 이번 이름 변경의 완료 범위가 아니다.
- 공개 승인이 나면 도메인·canonical·색인 정책·공개용 안내·캐시 정책을 별도 검수한다. 현재 비공개 안내를 삭제하고 바로 공개해도 된다는 뜻은 아니다.

## 보호된 원격 검수

- 배포 소스: `ea01a29cb07048217acef25f010deaa787c779b7`. Cloudflare Preview `3afd8034-c0fb-43fe-b73e-7cb2fb35de0a`, success, 2026-10-22 02:00 KST, 45초를 대시보드에서 확인했다.
- [변경된 검수 사이트](https://3afd8034.monipick.pages.dev/): 모니픽 로고·title·description·og:site_name을 실제 인증된 DOM에서 확인했다. [메인 화면 캡처](assets/monipick-branding-20261022/desktop.jpg)는 이 호스트의 CSS 폭 1265px 화면이다.
- [인증된 실제 응답](assets/monipick-branding-20261022/http-results.json): 정상 경로 7개 HTTP 200, 없는 주소 2개 HTTP 404, noindex/nosniff/frame/referrer/permissions/cache 6개 정책 모두 **9/9 통과**. Access 로그인 응답으로 대신하지 않았다.
- [익명 차단 결과](assets/monipick-branding-20261022/anonymous-access.json): 고정 URL과 실제 alias 각각 root·JS·제품 상세 모두 **6/6 HTTP 302 → Access 로그인**. 인증 쿼리·쿠키·토큰을 저장하지 않았다.
- production 자동 배포 paused 및 `No production deployment yet`를 재확인했고, 기본 monipick.pages.dev root는 HTTP 404다. 설정 권한·보호 정책·DNS·도메인 연결은 변경하지 않았다.
- 원격 화면은 검증된 Git 커밋 기반이다. 로컬 사용자 미커밋 테스트 14개는 보존하되 CI에 임의 포함하지 않아 CI 브라우저 수는 로컬과 다르다.
- 구현 커밋의 [검수 브랜치 CI](https://github.com/dineyong/connectable/actions/runs/39639732430)와 [준비 브랜치 CI](https://github.com/dineyong/connectable/actions/runs/39639717207)는 모두 success를 확인했다. 검수 CI 로그에서 Python **626개**, 브라우저 **210개** 통과를 직접 확인했다. 로컬 224개와의 14개 차이는 위의 보존한 미커밋 테스트다.
