# 모니픽 공개용 빌드와 비공개 검수 분리

> 2026-10-24 최신 상태: 사용자가 확인한 후보의 실제 공개를 승인했고 monipick.com 운영 배포·HTTPS 연결을 완료했다. [공개 결과](MONIPICK_PUBLIC_LAUNCH_REPORT_20261024.md)와 [운영 공개 기준](MONIPICK_PRODUCTION_OPERATIONS.md)을 우선한다. 광고·통계는 비활성, main은 미병합이다. 아래 승인 대기/미적용 설명은 이전 준비 단계 이력이며 후보 빌더 자체의 미승인 계약은 계속 유지한다.

기준일: 2026-10-23. 공개 승인·도메인 연결·색인·광고는 보류한다. [기존 운영 절차서](MONIPICK_OPERATIONS_RUNBOOK.md)의 공개 전환 절차와 함께 사용한다.

## 현재 기준 도구

| 도구 | 출력 | 허용 범위 |
| --- | --- | --- |
| [prepare_cloudflare_preview](../scripts/prepare_cloudflare_preview.py) | 원본 검수 문구, noindex, Disallow, no-store | Access가 확인된 비공개 검수 배포 |
| [prepare_monipick_release](../scripts/prepare_monipick_release.py) | 보호 후보 + 문서 루트 밖 비활성 초안 | 이전 준비 이력·회귀 계약 유지 |
| [build_monipick_public_candidate](../scripts/build_monipick_public_candidate.py) | 공개 형식 metadata/문구/헤더가 반영된 별도 후보 | **로컬 생성·검증만**, 실제 업로드 승인 아님 |

`web/` 원본은 그대로 noindex와 비공개 문구를 유지한다. 실제 공개용 변환의 기준은 새 빌더다. 기존 proposed 파일을 수작업으로 복사해 두 번째 기준 원본을 만들지 않는다. 기존 생성기는 역사적 준비와 테스트를 위해 보존한다.

## 공개 형식 후보 생성·검증

```sh
python3 -m scripts.build_monipick_public_candidate --output /tmp/monipick-public-candidate-next
python3 -m scripts.build_monipick_public_candidate --output /tmp/monipick-public-candidate-next --check
python3 -m scripts.serve_monipick_candidate --output /tmp/monipick-public-candidate-next --port 8876
```

출력은 새 디렉터리여야 한다. site/만 향후 배포 문서 루트 후보다. manifest.json은 그 밖에 두며 공개 승인 false·색인 승인 false·FINAL_PUBLICATION_APPROVAL_PENDING을 유지한다. 빌더에는 업로드·DNS·토큰·승인 해제 옵션이 없다.

**파일에는 실제 공개 시 필요한 index/canonical/Allow 설정이 들어 있다.** 따라서 비공개 검수에 이 디렉터리를 잘못 연결하면 안 된다. 현재 Cloudflare 빌드 명령을 이 도구로 교체하지 않았다. noindex는 접근 제어가 아니며 Access 보호를 해제하지 않는다.

37개 원본 HTML에서 경로별 robots·canonical·og:url과 검수 전용 문구만 변환하고 홈 복사까지 HTML 38개를 만든다. JS/CSS·제품 데이터·공식 출처·확인일·한국 SKU·UNKNOWN/CONFLICT·수동 검토 상태는 원본 그대로다. 제품 사실의 승인·호환성 판정을 생성하지 않는다.

사이트맵 34개, 나머지 뉴스/보강 자료/404 noindex, 루트 404.html, 정확한 홈 리다이렉트 두 개, CSP/nosniff/frame/referrer/permissions를 반영한다. 일반 Pages 캐시를 사용하고 장기 immutable·추가 추적기를 넣지 않는다. 사용자 선택 조건의 query/hash별 URL은 사이트맵으로 늘리지 않는다.

운영 안내에서는 Cloudflare Pages의 정적 제공, 호스팅 접속·보안 처리 가능성과 사이트 분석 도구의 차이, Cloudflare Email Routing → 운영 Gmail의 문의 처리 경로를 설명한다. 보존 기간이나 로그 미수집을 임의 보장하지 않는다. 개인정보가 없는 사이트라고 주장하지 않는다. 원본 검수 페이지의 수신 테스트 내부 안내는 공개 출력에서 제외한다.

## 검증 범위

[Python 회귀](../tests/test_monipick_public_candidate.py)는 예상 원본 변환 전체와 모든 파일 hash/inventory를 대조한다. manifest 하나만 신뢰하지 않는다. 잘못된 metadata·허가 flag·변조된 데이터·누락 파일·예상 밖 파일·symlink·잘못된 JSON을 거부한다.

[HTTP 회귀](../tests/test_serve_monipick_candidate.py)는 루프백 실제 200/404, 정적 파일과 리다이렉트/헤더, 내부 파일 차단을 검사한다. [별도 Playwright 설정](../playwright.release.config.js)의 데스크톱·모바일 테스트는 공개 후보의 CSP를 실제 HTTP 응답에 적용하고 검색·비교·상세·출처·사이트맵·뉴스를 검사한다.

```sh
python3 -m unittest tests.test_monipick_public_candidate tests.test_serve_monipick_candidate -q
npx playwright test --config playwright.release.config.js --workers=2
```

테스트 서버는 127.0.0.1에만 바인딩한다. 정적 경로·헤더·redirect의 제한된 smoke 서버이며 Cloudflare CDN/Access/HTTPS/자동 canonical redirect/캐시의 완전한 에뮬레이터가 아니다. 실제 배포 검증을 대신하지 않는다. 기존 원본 검수용 validate_local_site의 noindex 계약을 완화하지 않았다.

## Cloudflare 전환안 — 미적용

현재 실제 설정은 유지한다.

- production branch: codex/monipick-cloudflare-preparation, Automatic deployments Disabled.
- 검수 branch: codex/monipick-private-preview.
- 현재 빌드 명령은 해당 검수 branch에서만 prepare_cloudflare_preview를 실행하고 그 외 branch에서는 exit 1이다.
- 출력: cloudflare-preview/site. Access는 *.monipick.pages.dev에서 소유자 한 명만 허용한다.

최종 공개 승인 **후** 별도 릴리스 SHA를 고정하고 production branch/빌드 명령/출력 루트를 운영 설정에서 명시적으로 전환한다. 공개 빌드 명령 후보는 `python3 -m scripts.build_monipick_public_candidate --output cloudflare-public-candidate`, 출력 후보는 `cloudflare-public-candidate/site`다. 현재 설정에는 입력하지 않았다. 승인 이후에도 검수 branch의 보호 빌드 분기는 유지하고, main 병합 여부는 별도다.

도메인·HTTPS·대표 host·www/HTTP/pages.dev 이동은 이 `_redirects` 두 줄만으로 완료되지 않는다. DNS나 Custom domain은 이번에 만들지 않는다. 실제 운영 배포 후 200/404/CSP/캐시/색인/모바일을 확인한 뒤 검색 제출 여부를 별도로 결정한다. 유료 플랜, Workers, 분석 도구, 광고/제휴 활성화는 포함하지 않는다.

Cloudflare 공식 문서: [정적 경로·404·캐시](https://developers.cloudflare.com/pages/configuration/serving-pages/), [헤더 규칙](https://developers.cloudflare.com/pages/configuration/headers/), [리다이렉트](https://developers.cloudflare.com/pages/configuration/redirects/). 2026-10-23 확인. Functions를 추가하면 정적 헤더·redirect 적용 범위를 다시 검토한다.
