# 모니픽 Cloudflare 설정 준비 · 2026-10-22

## 표시명 후속 정리 · 2026-10-22

사용자 지시로 현재 화면 표시명을 **모니픽**으로 바꾸고 로컬 환경 문구와 페이지별 메타데이터를 정리했다. [브랜딩 결과 보고서](MONIPICK_BRANDING_REPORT.md)가 이 변경의 기준이다. 아래의 Connectable/로컬 문구가 남았다는 내용은 이전 검수 당시 이력이며 해당 표시 정리는 후속 작업에서 완료했다. 비공개 접근 제한·noindex·한국 SKU와 사양 불확실성·실제 공개 보류는 유지한다.

## 인증된 원격 검수 완료 · 2026-10-22

이 절이 아래 대기 기록보다 최신이다. 사용자 Access 로그인 후 실제 응답과 화면을 확인했다. **비공개 검수 통과이며 공개 승인이나 제품 사양의 추가 인증은 아니다.**

### 검수 대상과 보호 범위

- 최종 소스: `89763ffd8dbcbe9dedae6a8b5fe7d96555ecdd6a`, 검수 브랜치 `codex/monipick-private-preview`.
- [고정 검수 URL](https://66e184bf.monipick.pages.dev/), deployment `66e184bf-aacb-4cdc-8049-3e9ad0512831`. Cloudflare 상세에서 Preview/success, 2026-10-22 01:48 KST, 21초를 확인했다.
- 실제 alias는 `codex-monipick-private-previ.monipick.pages.dev`다. 이전에 전체 브랜치명을 변환해 추정했던 주소와 다르므로 실제 alias를 다시 검사했다. 배포 식별은 변경 가능한 alias 대신 고정 URL과 SHA를 사용한다.
- 고정 URL과 실제 alias 각각 root, 점검 HTML, JS 데이터, 제품 상세, 없는 경로에 비인증 GET을 보냈다. **10/10 HTTP 302 → Access 로그인 호스트**로 차단됐다. [비인증 결과](assets/cloudflare-review-20261022/anonymous-access.json)에는 상태와 로그인 호스트만 기록하고 인증 쿼리·토큰·이메일은 저장하지 않았다.
- Access의 `*.monipick.pages.dev` 소유자 이메일 1개 허용 정책을 유지했다. production 자동 배포 Disabled/paused, 목록 `No production deployment yet`, 기본 `monipick.pages.dev/` HTTP 404를 재확인했다. monipick.com 연결·DNS·main·색인·광고·제휴·유료 플랜은 변경하지 않았다.

### 화면과 HTTP 검증

| 항목 | 결과 | 실제 확인 |
| --- | --- | --- |
| 기본 화면 | 통과 | 모니터 30종·브랜드 8개 표시 |
| 용도 선택 | 통과 | 문서·사무 11종, 별도 결과 버튼; 선택 즉시 목록으로 이동하지 않음 |
| 검색·브랜드 | 통과 | PA279CRV 1종, ASUS 7종 |
| 비교 | 통과 | PA279CRV/PG32UCDM 비교 열림, Escape 닫기, 선택 유지 |
| 미확인/지역/조건 | 통과 | US 기준·한국 SKU 미확인, 미확인 값, PD 96W/90W 및 PG32UCDM 기본 65W·OSD 90W 조건 유지 |
| 직접 제품 상세 | 통과 | `/monitors/asus-pa279crv/` 제목·공식 출처·지역 불확실성 표시 |
| 뉴스·가이드 | 통과 | 실제 내용 표시; `.html` 진입 시 확장자 없는 주소로 정상 이동 |
| 실제 정상 응답 | 통과 | root, JS, CSS, 목록, 제품, 가이드, 뉴스 7개 HTTP 200 |
| 실제 없는 경로 | 통과 | root 하위 및 제품 하위 2개 HTTP 404, 전용 404 문구 표시 |
| 보안 헤더 | 통과 | 아래 6개 정책을 9개 응답 모두에서 확인 |
| 인증 없는 접근 | 통과 | 고정 URL/실제 alias의 HTML·JS·상세·없는 주소 10개 모두 Access 302 |

[인증된 실제 HTTP 결과](assets/cloudflare-review-20261022/http-results.json)는 로그인 응답이 아닌 애플리케이션 응답이다. 각 경로에서 다음을 확인했다.

- `X-Robots-Tag: noindex, nofollow, noarchive`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- `Cache-Control: no-store`

일반 브라우저 도구가 인증된 HTTP 헤더를 제공하지 않아, [옵트인 점검 HTML](../scripts/preview_http_check.html)과 [JS](../scripts/preview_http_check.js)를 비공개 후보에만 추가했다. 고정된 같은 origin 경로만 GET하고 인증값·쿠키를 읽거나 출력하지 않는다. `redirect:error`로 Access 로그인 응답을 성공으로 오인하지 않는다. 초기 점검은 가이드/뉴스의 `.html` 정규화 이동을 요청 오류로 표시했으며, 일반 화면에서 최종 주소를 확인한 뒤 점검 대상만 정규화 주소로 수정했다. 최종 **9/9 PASS**다. 실제 사이트 경로나 UI를 바꿔 오류를 숨긴 것이 아니다.

기본 생성에는 점검 파일이 포함되지 않고 `--include-http-check`에서만 포함된다. 원격 조건부 명령도 검수 브랜치에서만 이 옵션을 사용한다. 그 밖의 브랜치는 `exit 1`이다. 점검 파일은 공개 후보에서 계속 제외해야 한다. noindex/robots는 Access 인증의 대체 수단이 아니다.

### 화면 증거와 검수 범위

- [최종 메인 화면](assets/cloudflare-review-20261022/desktop.jpg): 66e184bf, 측정 CSS 폭 1265px.
- [모바일 화면](assets/cloudflare-review-20261022/mobile.jpg): b0bd1ac3, 측정 CSS 폭/scrollWidth 모두 375px. 가로 넘침 없음.
- [비교 화면](assets/cloudflare-review-20261022/compare.jpg): b0bd1ac3, 중간 폭 화면.
- [실제 404 화면](assets/cloudflare-review-20261022/404.jpg): ac86f2ca.
- [최종 HTTP 점검 화면](assets/cloudflare-review-20261022/http-check.jpg): 66e184bf.

주요 검색·비교·모바일 조작은 사용자가 인증한 b0bd1ac3에서 수행했다. 017997b→89763ff 사이 `web/`, `data/`, `schemas/`의 커밋 차이는 0임을 검사했다. 최종 호스트에서도 메인 화면과 HTTP 점검을 다시 확인했다. 캡처마다 실제 호스트를 구분하며 모든 기기·브라우저의 완전한 기능 검수로 확대 해석하지 않는다. 최종 점검/메인 탭에서 수집된 warn/error 콘솔 로그는 없었다. 모든 경로의 전체 네트워크·외부 링크·사양 진위를 검사했다는 뜻은 아니다.

### 테스트와 보존

- `node --check scripts/preview_http_check.js`: 통과.
- `python3 -m unittest tests.test_prepare_cloudflare_preview -q`: 7개 통과. 기본 후보에서 점검 파일 제외, 옵트인 포함 및 manifest/CSP를 검사한다.
- `python3 -m unittest discover -s tests -q`: 로컬 **623개 통과**. 의도적인 비정상 입력의 FAIL 출력은 테스트 결과 실패가 아니며 최종 exit 0/OK를 확인했다.
- ecacb31 [검수 CI](https://github.com/dineyong/connectable/actions/runs/39637251565): Python **623개**, 브라우저 **208개** 통과. 준비 브랜치 CI도 success.
- 최종 89763ff [검수 CI](https://github.com/dineyong/connectable/actions/runs/39638086903): success. Python 623개·브라우저 208개 통과. 최종 변경은 점검 경로 2개의 `.html` 확장자 제거뿐이다.
- `git diff --check`: 통과. 기존 사용자 수정 README/DECISIONS/content-review.spec.js/site-v2.js와 미추적 문서는 보존했다. 제품·코퍼스·목업 원본 변경 없음.
- 새 근거에는 개인 계정·이메일·인증 쿠키·토큰·비밀값을 저장하지 않았다. 문서 상대 경로와 JSON 파싱을 검사했다.
- 후속 확인 자동화 `automation-4`는 검수가 완료돼 삭제했다. 현재 채팅은 보존했다.

### 남은 위험과 공개 전 작업

1. 화면/문서 제목은 아직 Connectable이며 로컬 미리보기·로컬 시연 문구가 남아 있다. 모니픽 브랜딩과 공개 문구/메타데이터는 별도 변경·검수해야 한다. 특히 404의 “실제 호스팅 404는 공개 전 별도 확인” 문구는 이번 실제 확인 이후 갱신 대상이다.
2. 한국 SKU 미확인·해외 지역 공식 문서·충돌·부분 검증을 유지했다. 이번 배포 검수가 제품 전체 사양/호환성 승인을 뜻하지 않는다.
3. 뉴스는 저장 목록이고 자동 실시간 수집을 보장하지 않는다. 이모지 반응은 로컬 저장이며 공개 집계가 아니다.
4. 기본 pages.dev와 custom domain은 현재 Access wildcard 대상이 아니다. 실제 공개는 별도 승인 후 production 구성·도메인·색인 정책을 검수해야 한다. 수동 콘솔 배포까지 막는 절대적 권한 경계는 아니다.
5. 이번 점검은 익명 차단과 허용 계정 성공을 검사했다. 다른 계정으로 로그인하는 부정 접근 테스트는 수행하지 않았다. 헤더 확인은 열거한 정책 범위이며 종합 보안 감사가 아니다.

## 자동 후속 검수 · 2026-10-22 01:26 KST

아래 인증 후 준비 기록보다 이 절의 실제 수신 결과가 최신이다.

- GitHub 공식 summary API는 Webhook 지연 incident를 여전히 investigating으로 반환했다. 전면 복구됐다고 판단하지 않는다. 다만 Cloudflare에는 두 개의 **Preview 성공 배포가 도착**했다.
- 검수 기준은 `017997b0daba402f1d6e448db520e3b057a85894`, deployment `b0bd1ac3-dea5-475a-8fec-b365b27bbc82`, 고유 URL [b0bd1ac3.monipick.pages.dev](https://b0bd1ac3.monipick.pages.dev/)이다. 상세 화면에서 Preview, success, 한국 시각 00:41, 빌드 15초를 직접 확인했다. 로그에서 조건부 빌드, 59파일 후보 검사, header rule 1개 파싱, 자산 58파일 업로드를 확인했다. `_headers`는 제어 파일이므로 후보 파일 수와 업로드 자산 수는 다르다.
- 지연 전달된 이전 커밋 c55b9d3의 Preview `69d8c37e`도 존재한다. out-of-order 전달 가능성을 고려해 브랜치 alias만 최신 소스의 증거로 쓰지 않고 위 고유 URL을 검수 대상으로 고정한다. 두 커밋 간 사이트 코드/데이터는 같다.
- 두 고유 URL과 검수 alias 각각의 root, JS 데이터, 목록, 존재하지 않는 경로 및 ASUS PA279CRV 상세 직접 경로를 비인증 curl로 확인했다. 전부 HTTP 302로 Access 로그인 호스트에 이동했다. origin의 404나 성공 응답으로 해석하지 않는다.
- 기본 monipick.pages.dev root는 현재 HTTP 404다. 운영 배포 목록은 `No production deployment yet`이며 실제 production 콘텐츠가 생겼다는 증거가 없다. DNS/Custom domain 연결과 공개 전환은 하지 않았다.
- [검수 커밋 CI](https://github.com/dineyong/connectable/actions/runs/39626621911)는 success다. 기존 코드가 바뀌지 않아 전체 테스트를 다시 실행하지 않았다.
- **남은 사용자 조치:** 고유 URL을 열면 Cloudflare Access가 별도의 이메일 로그인 코드를 요구한다. Cloudflare 대시보드 로그인과 이 사이트의 Access 세션은 별개다. 로그인 창만 열었으며 이메일/코드 입력·코드 발송·메일함 열람·토큰 생성·인증 우회를 하지 않았다. 사용자에게 계정 이메일로 직접 로그인하도록 안내한다.
- 인증된 화면·검색/비교/상세 동선, 실제 origin 200/404, 실제 자산 응답 보안 헤더는 아직 확인 불가다. 로컬 테스트나 Access 로그인 응답으로 통과 처리하지 않는다. 사용자가 Access 로그인한 뒤 비공개 검수를 계속한다.

## 인증 후 설정 진행 · 2026-10-22

아래 내용은 본문의 최초 준비 기록 이후 수행한 후속 설정이다. 이전의 미생성·권한 대기 표기는 당시 상태이며 이 절이 현재 진행 상태다.

- 사용자 직접 인증 후 GitHub 연동 완료를 확인했다. 허용된 저장소 목록에는 connectable 하나가 표시됐다.
- Git integration 방식으로 `monipick` Pages 프로젝트를 생성했다. 초기 빌드 명령은 `exit 1`, 출력은 `cloudflare-preview/site`로 지정했다. 기존 작업 커밋 `c55b9d3`을 clone한 뒤 실패하도록 의도한 설정이며 실제 서비스 결함이나 테스트 실패를 숨기는 목적이 아니다. 프로젝트 화면에서 `No production deployment yet`, `No deployment available`을 확인했다.
- Production branch는 `codex/monipick-cloudflare-preparation`이며 자동 production 배포를 Disabled로 저장했다. main은 사용하지 않는다.
- Pages의 Restrict previews를 적용했다. Access 앱은 `*.monipick.pages.dev`를 보호하며 정책의 Include Emails는 현재 소유자 계정 이메일 하나다. 주소 자체는 보고서에 저장하지 않는다. 다른 사용자·도메인·Everyone·Bypass를 추가하지 않았다.
- 인증 없는 curl 요청에서 검수용 alias의 `/`, `/monitor-v3-data.js`, `/monitors/`, `/not-a-real-product`가 모두 HTTP 302로 `monipick-pages.cloudflareaccess.com` 로그인으로 이동했다. 이는 업로드 전 접근 장벽 확인이며 배포 후 실제 자산 보호를 다시 확인해야 한다. 초기 Python urllib 확인은 curl과 다른 403 응답을 반환해 결론 근거로 쓰지 않았다.
- 기본 `monipick.pages.dev`는 같은 경로에서 522를 반환했다. 서비스 정상 응답이나 Access 보호 성공으로 해석하지 않는다. **기본 주소는 Access 보호 범위 밖이므로 실제 콘텐츠를 production으로 배포하지 않는다.**
- 빌드 명령을 다음 조건식으로 변경했다. Preview 자동 배포는 아래 브랜치 하나만 포함하는 Custom branches로 제한했다. PR build comments도 Disabled로 저장했다.

```sh
if [ "$CF_PAGES_BRANCH" = "codex/monipick-private-preview" ]; then python3 -m scripts.prepare_cloudflare_preview --output cloudflare-preview; else exit 1; fi
```

- [공식 빌드 문서](https://developers.cloudflare.com/pages/configuration/build-configuration/)의 `CF_PAGES_BRANCH`를 사용한다. 로컬 격리 검사에서 main, production 기준 브랜치, 임의 다른 브랜치는 모두 exit 1로 중단되고 출력 폴더가 생기지 않았다. 이 검사는 원격 콘솔 권한 자체를 잠그는 보안 경계는 아니다.
- `codex/monipick-private-preview`에 검증 커밋을 push해 인증이 필요한 preview 환경만 준비 중이다. 실제 공개 도메인 연결, main merge, 색인·광고·쿠팡·유료 플랜·Workers/D1 생성은 수행하지 않았다.
- Cloudflare 대시보드가 GitHub push event 연동 저하 안내를 표시했다. 안내 표시를 특정 장애 원인의 확정 증거로 취급하지 않으며, 빌드 수신/실행/완료는 별도로 확인한다.
- 준비 코드 [GitHub CI 39624161587](https://github.com/dineyong/connectable/actions/runs/39624161587)는 성공했다. 로그 기준 Python 621개·브라우저 208개 통과다. 로컬 222개와의 차이는 보존한 미커밋 사용자 테스트 14개다. 사용자 변경을 임의 포함해 CI 숫자를 맞추지 않았다.

인증된 원격 화면, 실제 호스트의 헤더·404·asset 검수 결과는 검수 배포 완료 뒤 아래 후속 기록에 추가한다. 현재 로컬 테스트 통과를 원격 서비스 전체 검수 완료로 승격하지 않는다.

### 후속 확인과 외부 대기 상태

- `017997b`(본 설정 기록만 추가한 커밋)을 검수 브랜치에 push했다. 원격 브랜치 SHA를 다시 확인했다. 코드/데이터/화면의 기준은 CI 성공한 c55b9d3과 동일하다.
- Pages 설정을 새로 불러와 Custom branches 포함값이 `codex/monipick-private-preview` 하나이며 production 자동 배포는 꺼져 있음을 재확인했다. 출력 폴더, 조건부 명령, Access 제한이 저장된 상태다.
- [GitHub 공식 상태](https://www.githubstatus.com/)를 직접 열어 `Delays for Pull Requests and Webhook deliveries` 미해결 공지와 Webhooks Degraded Performance를 확인했다. 공지 시작은 2026-10-21 14:52 UTC(한국 2026-10-21 23:52)다. 특정 push의 미전달 원인을 개별 추적한 것은 아니지만 외부 연동 지연과 일치한다.
- 최종 확인 당시 Pages 목록에는 초기 차단 빌드 한 건과 `No production deployment yet`만 보였다. 검수 브랜치의 원격 빌드 시작·성공, 인증된 사이트 화면, 실자산 헤더, origin 404는 **아직 확인 불가**다. 본문의 로컬 성공 결과로 대체하지 않는다.
- 초기 차단 빌드의 Cloudflare Pages GitHub check는 failure다. 사전에 `exit 1`로 지정한 공개 보류 장치의 예상 결과로 기록하며 GitHub 테스트 실패로 섞지 않는다. 이를 성공 배포로 표시하거나 삭제하지 않았다.
- 검수 브랜치 push로 생긴 추가 GitHub Actions 실행은 대기/실행 중 상태였다. c55b9d3의 최초 CI 성공 결과는 위 링크에서 확인했다. 문서만 바뀐 후속 커밋의 미완료 CI를 통과로 표기하지 않는다.
- 검수 브랜치가 나중에 빌드되더라도 wildcard Access 로그인 제한 안에서만 제공되도록 설정했다. 본 도메인 연결·기본 주소 production 콘텐츠 업로드는 보류다. 정기 감시나 자동 공개 전환은 만들지 않았다.

다음 확인은 Pages가 받은 검수 deployment의 정확한 SHA/고유 URL부터 시작한다. 고유 URL과 alias의 HTML·JS·제품 직접 경로가 인증 없이 노출되지 않는지 재검사하고, 허용 계정으로 화면·200/404·헤더를 확인한 뒤 사용자에게 최종 공개 전 결과를 제시한다. 권한 승인 추가나 유료 플랜 선택은 현재 필요하지 않다. 외부 지연을 해결하려고 저장소 권한을 넓히거나 production 배포를 켜지 않는다.

## 결정과 실제 상태

사용자는 monipick.com 구매를 알렸고 모니픽 호스팅을 Cloudflare로 선택했다. Vercel Pro는 보류한다. 이번 지시는 Cloudflare 설정을 이어가되 **실제 공개 전에 검수 결과를 먼저 제시**하는 것이다. 알리쿠폰파인드의 호스팅·Railway·DNS는 이 작업 대상이 아니다.

- 기준 HEAD: `6fd8ccf2ea83677b27e123a612b860219bd33dbf`.
- 작업 브랜치: `codex/monipick-cloudflare-preparation`.
- 계정 대시보드 로그인과 monipick.com 도메인 목록 항목을 직접 확인했다. DNS·등록자·청구 정보를 변경하지 않았다.
- Pages 생성 및 GitHub 연결 화면까지 확인했다. GitHub 설치는 기존에 연결되어 있지 않았다. `Only select repositories`에서 `dineyong/connectable` 하나를 선택했으나 **Install & Authorize는 누르지 않았다**.
- 실제 Pages 프로젝트 생성, Git 연동 승인, 파일 업로드, 배포, 도메인 연결, Workers/D1 생성, 결제, 광고·색인 활성화는 수행하지 않았다.

## 추가한 로컬 준비물

[후보 생성기](../scripts/prepare_cloudflare_preview.py)는 [기존 생성기](../scripts/prepare_launch_preview.py)를 호출해 검증된 화면 파일만 복사한다. 원본 web/data/schema나 기존 목업을 변경하지 않는다. 추가된 [테스트](../tests/test_prepare_cloudflare_preview.py)는 검색 차단 헤더, 기존 경로 보존, 원본 보존, manifest 해시 및 미배포·접근제어 미검증 상태를 검사한다.

```sh
python3 -m scripts.prepare_cloudflare_preview --output /tmp/monipick-cloudflare-preview-20261022
```

- 이번 생성 결과: `site/` 아래 59개 파일. 기존 후보 57개 + `_headers` + `robots.txt`.
- 원본 v3 화면을 후보의 index.html로 복사하고 30개 제품 상세와 404.html을 유지한다. 연구 원본, 기존 관리 화면, manifest는 문서 루트에서 제외한다.
- `_headers`: 전 경로 X-Robots-Tag(noindex/nofollow/noarchive), nosniff, 프레임 차단, referrer policy, 카메라/마이크/위치 비허용, 검토 중 no-store.
- `robots.txt`: 전체 크롤링 비허용. **robots/noindex는 비공개 인증 수단이 아니다.**
- manifest의 `deployment_authorized=false`, `domain=null`을 유지하며 `access_control_verified=false`, `requires_access_control_before_upload=true`를 명시한다. 도메인 구매가 곧 업로드 승인으로 해석되지 않는다.
- 현재 화면의 Connectable 표기는 그대로다. 모니픽 명칭·메타데이터·운영 도메인 정합성은 공개 전 별도 확인 대상으로 남긴다. 과거 코퍼스/제품 식별자까지 일괄 변경하지 않는다.

## 준비한 Pages 설정안 — 원격 적용 전

| 항목 | 설정안 |
| --- | --- |
| 제품 | Cloudflare Pages, 정적 사이트 |
| 프로젝트명 | monipick 후보, 이름 가용성은 생성 시 확인 |
| 저장소 | dineyong/connectable만 허용 |
| 프레임워크 | None |
| 저장소 루트 | 루트 |
| 빌드 명령 | `python3 -m scripts.prepare_cloudflare_preview --output cloudflare-preview` |
| 배포 출력 폴더 | `cloudflare-preview/site`만 지정, 저장소 전체 또는 web 전체 금지 |
| 기준 브랜치 | 검수한 작업 커밋을 명시하고 선택. main의 과거 화면을 자동 배포하지 않음 |
| 비밀키 | 첫 정적 후보에는 필요 없음 |
| Workers/Railway/D1 | 이번 단계에서 불필요·미생성 |
| 도메인 | monipick.com 구매 확인. DNS/Custom domain 연결 보류 |
| 자동 배포 | 공개 승인 전 활성화하지 않음. Git 연결의 첫 배포도 공개 가능성을 먼저 검사 |

빌드 명령의 출력은 새 디렉터리여야 한다. 로컬 재실행은 다른 출력 경로를 사용한다. Cloudflare 캐시가 출력 폴더를 재사용한다면 임의 삭제로 덮어쓰지 않고 빌드/캐시 구성을 점검한다. 위 설정안은 호스트 빌드 성공이나 원격 헤더 적용 결과가 아니다.

## 공개 차단 및 권한 경계

1. GitHub 화면의 Cloudflare Workers and Pages 앱은 metadata 읽기와 administration/checks/code/deployments/pull requests 읽기·쓰기를 요청한다. 선택 범위는 connectable 하나지만 저장소 권한의 신규 부여이므로 사용자 확인 전 승인하지 않는다. 알리쿠폰파인드 등 다른 저장소를 선택하지 않는다.
2. [공식 미리보기 문서](https://developers.cloudflare.com/pages/configuration/preview-deployments/)에 따르면 preview URL은 기본 공개다. Pages의 preview Access 옵션만으로 기본 `<project>.pages.dev`와 custom domain이 보호되지 않는다.
3. 원격 검수본을 올리기 전 필요한 URL 전부의 접근 통제 방식을 정하고 적용한다. 가능하면 비어 있는 프로젝트/차단용 초기 구성에서 설정하고 인증 없는 접근을 먼저 검증한다. 초기 Git 배포가 실제 후보를 공개한다면 누르지 않는다.
4. 보호되지 않은 상태로 후보를 잠깐 공개한 뒤 Access를 켜는 방식은 사용하지 않는다. Git 연결과 원격 검수본 업로드는 자동 production 배포나 최종 공개 승인과 구분한다.
5. 인증 없는 요청에서 root·고유 preview·브랜치 alias·직접 제품/자산 URL이 노출되지 않는지 확인한다. 로그인한 검수자는 해당 페이지를 열 수 있어야 한다. 실제 200/404·보안 헤더·모바일 검수 후 결과를 사용자에게 제시한다.
6. 최종 공개 승인 이후에만 DNS 연결·정식 canonical/sitemap·색인 정책·공개 캐시 정책을 준비한다. 이번 후보의 no-store/robots 차단은 정식 운영용 최종 SEO 설정이 아니다.

[Pages 헤더 문서](https://developers.cloudflare.com/pages/configuration/headers/) 기준 정적 응답용 파일을 준비했지만 호스트에서 적용됐다고 주장하지 않는다. 향후 Functions/Workers를 붙이면 헤더와 인증의 적용 범위를 다시 검증해야 한다. [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/) 프로젝트는 나중에 같은 프로젝트를 Git integration으로 전환할 수 없으므로, 편의를 위해 임의로 생성하지 않았다.

## 검수 실행 결과

| 검사 | 결과 |
| --- | --- |
| 변경 전 Python 전체 | 616개 통과 |
| 새 후보 생성기 테스트 | 5개 통과 |
| 변경 후 Python 전체 | 621개 통과, 29.084초 |
| 데스크톱·모바일 브라우저 전체 | 222개 통과, 약 1.2분. 기존 사용자 작성 테스트 14개 포함 |
| 로컬 HTML/내부 경로/공개 보류 검사 | 통과 |
| Cloudflare 로컬 후보 생성 | 59파일, 업로드 없음 |
| 실제 Cloudflare 빌드·HTTP·인증·404·CI | 원격 단계 미실행/아직 확인하지 않음 |

실행 명령: `python3 -m unittest discover -s tests -q`, `npm run test:e2e -- --workers=2`, `python3 scripts/validate_local_site.py`, `python3 -m scripts.prepare_cloudflare_preview --output /tmp/monipick-cloudflare-preview-20261022`, `git diff --check`.

Python 비정상 입력 테스트 중 출력되는 `FAIL: stale/missing derived files`는 의도적으로 손상된 임시 입력이 거부되는 로그다. 테스트 전체 종료 상태로 통과 여부를 판단했다. 첫 준비 턴에서 존재하지 않는 `tests.test_validate_local_site`를 포함한 명령이 ImportError로 실패했으며 올바른 `tests.test_local_site` 17개와 패키지 11개를 다시 실행해 통과했다. 이번 변경 후 전체 621개 테스트도 종료 코드 0으로 통과했다.

## 보존 및 다음 단계

기존 사용자 변경 4개(README, DECISIONS, content-review.spec.js, site-v2.js)와 기존 미추적 문서 6개는 작업 전 상태를 보존하고 커밋에 포함하지 않는다. 브라우저 검사가 다시 생성한 mobile 캡처 한 개만 실행 전 Git 내용으로 되돌렸다. 기존 원본과 표시 데이터, 실제 화면 코드는 수정하지 않았다. 최종 Git diff에서 이번 변경은 생성기·테스트·본 보고서만 포함한다.

다음 실제 조작은 GitHub의 저장소 한정 권한 승인이다. 승인 후 Pages 생성/빌드 설정과 인증 경계를 이어서 확인한다. 최종 공개·DNS 전환은 사용자 검수 이후로 유지한다. 원격 환경에서 차단을 보장할 수 없으면 업로드하지 않고 구체적인 제한을 보고한다.
