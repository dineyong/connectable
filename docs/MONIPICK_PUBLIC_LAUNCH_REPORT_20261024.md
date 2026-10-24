# 모니픽 실제 공개 결과 — 2026-10-24 KST

## 결과

**https://monipick.com/ 실제 공개와 HTTPS 연결을 완료했다.** 사용자가 확인한 화면/문구의 원본 파일 inventory를 고정해 배포했다. 광고·쿠팡·방문 통계는 활성화하지 않았고 main과 병합하지 않았다. 새 기능/원본 사양/호환성 승인도 추가하지 않았다.

- 운영 branch: `codex/monipick-production`.
- 실제 운영 소스 SHA: `be36d2d9bde5b0b8073d286975a52fb0931ca9d0`.
- 실제 배포 ID: `1d64511e-ded0-4fc0-81f4-4a135a4faff3`.
- 배포 고유 주소: `https://1d64511e.monipick.pages.dev/` (기존 wildcard Access 보호 범위). 공개 서비스 주소는 monipick.com이다.
- Cloudflare Deployments에서 운영 환경·브랜치·SHA·ID를 대조하고 Custom domains에서 monipick.com **Active / SSL enabled**를 확인했다.
- 최초 운영 배포를 위해서만 자동 운영 배포를 켰으며, 성공 후 **Automatic deployments Disabled**로 복구했다. 후속 문서 push가 운영 화면을 자동 교체하지 않는다.

[승인 범위](../deploy/monipick-public-release.json), [운영 절차](MONIPICK_PRODUCTION_OPERATIONS.md), [실제 배포 manifest](assets/monipick-launch-20261024/release-manifest.json)를 기준으로 관리한다. 준비/검수 branch는 그대로 보존한다.

## 승인과 빌드 분리

사용자는 2026-10-24 화면·문구 확인 후 실제 공개, 도메인·HTTPS 연결을 명시적으로 승인했다. 광고·통계 비활성과 main 미병합은 명시 조건이다. 이를 monipick.com의 현재 비교 사이트 61개 파일로 한정했다.

[분기 빌더](../scripts/build_monipick_cloudflare.py)는 검수 branch에서 기존 보호 빌더를 사용하고, 운영 branch에서만 사용자 검수 파일 hash inventory의 fingerprint를 확인한다. 다른 branch와 다른 내용은 거부한다. 실제 서버에 올리는 것은 site/뿐이며 manifest/승인 기록/원본 연구/내부 검토 파일은 포함하지 않는다. 기존 미승인 candidate/preview 빌더의 false 정책을 해제하거나 검증기를 완화하지 않았다.

고정 fingerprint: `df71388fbe44404e224592f13096cf862970076366af35fd1bee1eb053723bf0`.

Cloudflare 빌드 설정은 다음 분기를 사용하고 출력은 cloudflare-build/site다.

```sh
if [ "$CF_PAGES_BRANCH" = "codex/monipick-production" ]; then
  python3 -m scripts.build_monipick_cloudflare --output cloudflare-build
elif [ "$CF_PAGES_BRANCH" = "codex/monipick-private-preview" ]; then
  python3 -m scripts.prepare_cloudflare_preview --output cloudflare-build --include-http-check
else
  exit 1
fi
```

검수 branch에는 새 운영 빌더가 없어도 기존 보호 빌더로 빌드할 수 있다. 현재 검수 배포 bd395c6b/9afa091은 그대로다. Access 정책을 제거하거나 범위를 축소하지 않았다.

## 도메인·HTTPS·분리

- 웹사이트용 CNAME `@ → monipick.pages.dev`만 추가했다. 메일용 MX 3개/SPF/DKIM은 삭제하거나 덮어쓰지 않았다. 공개 MX에서 기존 route1/2/3을 확인했다.
- `http://monipick.com/`은 HTTPS로 301 이동한다. 실제 HTTPS 요청은 인증서 검증을 끄지 않았으며 curl ssl_verify_result 0이다.
- `/monitor-v3.html?q=4k`는 `/?q=4k`로 301, `/information.html`은 `/information`으로 308 이동한다.
- monipick.pages.dev의 운영 사본은 200이지만 `X-Robots-Tag: noindex, nofollow`와 monipick.com canonical을 유지한다. pages.dev → 사용자 도메인 301 규칙은 별도로 만들지 않았다.
- www.monipick.com 별칭은 이번에 추가하지 않았다. 대표 서비스 주소는 https://monipick.com 이다.
- 기존 검수 고유 호스트와 branch alias는 비인증 요청에서 계속 Access 로그인 302다.
- `/_headers`, `/manifest.json`, `/data/research/user_questions.csv`는 실제 404다. 공개 서버에서 내부 파일을 읽을 수 있는 것으로 표시하지 않는다.

[호스트·리다이렉트·격리 결과](assets/monipick-launch-20261024/host-and-isolation.json).

## 운영 주소의 실제 검증

[HTTP 결과 60개](assets/monipick-launch-20261024/http-results.json)는 정상 URL 58개와 없는 경로 2개다. HTML 37개 canonical 경로와 JS/CSS/robots/sitemap 등 정적 URL 21개를 검사했다. 복사된 홈 파일 중복 경로와 제공하지 않는 Pages 설정 파일은 이 수량에 포함하지 않는다.

| 항목 | 결과 |
| --- | --- |
| 실제 정상 URL | 58개 200 |
| 없는 루트/제품 하위 경로 | 2개 실제 404 및 올바른 오류 본문 |
| HTTPS 인증서 검증 | 60개 모두 성공 |
| CSP | script-src self, 외부 실행 허용/unsafe-inline 추가 없음 |
| nosniff / frame / referrer / permissions | 60개 모두 설정 일치 |
| 캐시 | Cloudflare 기본 public max-age=0, must-revalidate; 장기 immutable 미적용 |
| canonical / robots | 홈·제품·가이드 정상, 뉴스/보강/404 제외 유지 |
| sitemap | 34개 URL; 가짜 lastmod 없음 |
| 광고·분석 스크립트 | 검사한 HTML에서 주요 광고·분석 도메인/Cloudflare Analytics beacon 없음 |
| UI 동작 | 모델 검색, 두 제품 비교, 상세·미확인 표시, 외부 링크 안전 속성, 운영 이메일 확인 |
| 브라우저 오류 | 실제 운영 브라우저에서 확인한 warning/error 로그 없음 |

서비스 HTML과 정적 파일을 승인한 빌드 바이트와 대조했다. 운영 안내 한 곳은 Cloudflare의 기본 Email Address Obfuscation이 이메일 링크와 보호용 decode 스크립트를 변환한다. 원본 raw body hash 불일치를 숨기지 않고 결과에 exact_body_match=false로 기록했다. 해당 이메일 변환만 정확히 복원하면 승인 바이트와 일치하며, 브라우저에서 contact@monipick.com과 mailto 링크가 정상 복원됨을 확인했다. 이 스크립트는 방문 분석이 아니며, 전역 보호 설정을 임의 해제하지 않았다. [Cloudflare 공식 설명](https://developers.cloudflare.com/waf/tools/scrape-shield/email-address-obfuscation/).

처음 임시 HTTP 검증 스크립트의 정적 자산 URL에 선행 슬래시가 빠져 검사 요청이 실패했다. 앱 결함과 분리해 스크립트를 수정하고 올바른 URL 60개로 다시 실행했다. 최종 결과에 실패는 없다. 사이트맵 CI 실패와 함께 아래에 실패 이력을 보존한다.

화면 증거: [데스크톱](assets/monipick-launch-20261024/desktop.jpg), [비교](assets/monipick-launch-20261024/compare.jpg), [모바일](assets/monipick-launch-20261024/mobile.jpg), [운영 안내](assets/monipick-launch-20261024/information.jpg), [404](assets/monipick-launch-20261024/404.jpg).
모바일 viewport는 390×844, DOM innerWidth 390/scrollWidth 375였다. 검수 후 viewport를 원복했다. 실제 iOS Safari 전수 검수로 표현하지 않는다.

## 테스트와 실패 처리

- 새 운영 분기 테스트 6개와 locale 재현 테스트 1개를 추가했다.
- Git 커밋을 별도 임시 폴더로 내보낸 깨끗한 릴리스 원본에서 Python **655개 통과**.
- [수정 후 CI 40049876141](https://github.com/dineyong/connectable/actions/runs/40049876141) success.
- [실제 배포 SHA의 CI 40050181672](https://github.com/dineyong/connectable/actions/runs/40050181672) success. 전체 Python과 기존 데스크톱/모바일, 공개 CSP 테스트를 포함한다.
- 기존 커밋된 브라우저 212개 + 공개 후보 10개 검사 계약을 유지했다. 사용자 미커밋 테스트 14개를 임의 포함하지 않았다.
- 문서·증거 후속 커밋은 같은 운영 branch에 기록하되 자동 운영 배포 Disabled 상태를 유지한다. 후속 CI 결과는 완료 응답에 실제 실행 링크로 남긴다.

[첫 CI 40049684325](https://github.com/dineyong/connectable/actions/runs/40049684325)는 승인 fingerprint 불일치로 실패했다. XML 선언이 로컬 Python 3.9/locale의 UTF-8과 CI Python 3.12의 utf-8로 달랐기 때문이다. 승인 fingerprint나 검증 기준을 바꾸지 않고, 사이트맵 직렬화 인코딩을 명시하여 검수한 원래 바이트로 고정했다. locale을 바꿔도 결과가 같은 테스트가 통과한다. 실패한 실행은 삭제하거나 통과로 바꾸지 않았다.

작업 중 다른 로컬 작업이 monitor-purpose.css/monitor-v3.js/site-v2.css/site-v2.js와 archive에 미커밋 변경을 추가했다. 기존 사용자 변경과 함께 그대로 보존하고 커밋·배포에서 제외했다. 그 작업 트리에서 승인 hash 검사가 거부된 결과는 정상이며, 이를 통과시키기 위해 승인 목록을 갱신하지 않았다. Git의 승인된 원본을 빌드한 Cloudflare 및 깨끗한 임시 폴더 결과로 검증했다. 원본 data/schema는 변경하지 않았고 main SHA도 실행 전후 같다.

## 운영 기준점과 남은 범위

현재 정상 배포 `1d64511e` / `be36d2d`와 manifest가 첫 운영 복원 기준이다. 이전 운영 배포는 없으므로 과거 운영 배포로의 롤백을 시험했다고 주장하지 않는다. 향후 수정은 별도 branch·검수·승인된 변경 범위를 따르고, 원본 데이터 reset이나 강제 push로 처리하지 않는다.

광고·쿠팡·통계, 댓글/공개 반응 서버, 제품 사진, 실시간 뉴스 자동 갱신은 미활성이다. 한국 SKU/일부 미확인/공식 충돌/사람 검토/호환성 보류도 그대로다. 이를 해소했다고 표시하지 않는다. 검색 도구 사이트 등록·사이트맵 제출은 이번에 수행하지 않았으며, robots/sitemap 공개가 실제 검색 색인 완료를 뜻하지 않는다.
