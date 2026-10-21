# 모니픽 Cloudflare 설정 준비 · 2026-10-22

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
