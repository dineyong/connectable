# 모니픽 최신 비공개 검수본·공개용 빌드 준비

기준일: 2026-10-23 KST. 브랜치 `codex/monipick-cloudflare-preparation`.
구현/검수 배포 SHA: `9afa091b7a8d7eea5799a308e5f213a7caa93af3`.

## 완료 범위

최신 운영 이메일 안내를 포함한 비공개 검수 배포를 갱신했다. 별도로 공개 형식 빌더·검증기·루프백 HTTP 서버·회귀 테스트·CI 검사를 추가했다. 공개용 파일과 비공개 검수 원본을 분리했다. **monipick.com 공개·DNS/Custom domain 연결·운영 빌드 명령 변경·색인/광고·Access 변경·main 병합은 하지 않았다.**

이번 작업은 [이전 최종 감사](MONIPICK_FINAL_PREPUBLICATION_AUDIT_20261023.md)의 최신 검수본 갱신과 공개용 출력/검증 미구현 문제를 해결한다. 실제 운영 origin 검수와 최종 공개 승인은 아직 남아 있다.

## 변경 파일

- [공개 형식 빌더·검증기](../scripts/build_monipick_public_candidate.py): 원본 검수 검증을 먼저 통과한 뒤 별도 출력에 경로별 canonical/robots/og:url, 공개 문구, 운영 안내, 사이트맵·헤더·redirect를 적용한다. 파일은 공개 형식이지만 manifest의 배포/공개/색인 승인과 통계 활성화는 모두 false다. 출력만 만들며 네트워크·배포·DNS·승인 해제 기능은 없다.
- [루프백 HTTP 서버](../scripts/serve_monipick_candidate.py): 생성된 후보와 실제 CSP 헤더로 검색/비교/정적 경로/404를 테스트한다. 127.0.0.1에만 바인딩하며 Cloudflare CDN/Access/TLS의 에뮬레이터를 주장하지 않는다.
- [빌더 회귀](../tests/test_monipick_public_candidate.py), [HTTP 회귀](../tests/test_serve_monipick_candidate.py): 총 15개 Python 테스트 추가.
- [공개 후보 Playwright 검사](../tests/release-e2e/public-candidate.spec.js), [별도 설정](../playwright.release.config.js): 데스크톱·모바일 10개. 기존 검수용 e2e/noindex 계약은 유지했다.
- [CI](../.github/workflows/validate.yml): 공개 형식의 로컬 빌드와 CSP 브라우저 검증 추가. 업로드/배포 단계·추가 권한은 없다.
- [공개용 빌드 가이드](MONIPICK_PUBLIC_BUILD_GUIDE.md), [운영 절차서](MONIPICK_OPERATIONS_RUNBOOK.md): 도구의 기준과 미적용 Cloudflare 전환안을 기록했다.
- 이 보고서와 [검수 증거](assets/monipick-public-prep-20261023/): 기존 데이터와 목업을 변경하지 않는 별도 기록이다.

## 빌드 계약

공개 후보는 파일 61개·HTML 38개이며 안정적인 사이트맵 URL 34개다. 뉴스/보강 자료/404는 noindex를 유지한다. canonical은 monipick.com 경로를 사용하고 필터 query/hash를 색인 주소로 늘리지 않는다. 근거 확인일이나 lastmod를 빌드 날짜로 조작하지 않는다.

검수 전용 문구를 변환하되 제조사 조건·지역·한국 SKU 미확인·부분 검토·UNKNOWN/CONFLICT는 그대로다. JS/CSS/표시 데이터는 원본과 바이트가 같으며 사용자 후기·공식 사양·호환성 승인을 통합하지 않는다. 운영 안내에는 실제 사용 중인 Pages·Email Routing·운영 Gmail과 브라우저 저장 범위를 설명하고 보존 기간·로그 미수집을 추정하지 않는다.

검증기는 명시한 inventory와 모든 출력 바이트/hash를 원본의 결정적 변환과 대조한다. 변조된 manifest만으로 데이터나 승인 상태를 통과시킬 수 없다. 잘못된 canonical/robots/헤더, 예상 밖 파일, 데이터 변경, 누락 파일, symlink, 잘못된 JSON과 승인 flag 승격을 거부한다. 기존 폴더는 덮어쓰지 않는다.

기존 prepare_monipick_release와 proposed 초안은 이전 준비 계약으로 보존한다. 실제 공개 형식 변환의 기준 도구는 새 빌더이며 초안을 수작업으로 두 번째 원본처럼 편집하지 않는다. 원본 web/은 계속 noindex·검수 문구다. 공개 형식 산출물 자체에는 index/Allow 설정이 있으므로 승인 전 업로드하지 않는다.

## 최신 비공개 배포

- 검수 branch: `codex/monipick-private-preview`.
- 이전 ea01a29에서 9afa091로 **fast-forward push**했다. 강제 push나 이력 수정은 없다.
- 배포 ID: `bd395c6b-0fa2-42f5-bf0f-b93cff946045`.
- [고유 검수 URL](https://bd395c6b.monipick.pages.dev/).
- alias: <https://codex-monipick-private-previ.monipick.pages.dev/>.
- Cloudflare Deployments 화면에서 정확한 SHA와 URL을 대조했다. 운영 branch의 같은 SHA는 skipped/No deployment available이며 Production Automatic deployments paused, No production deployment yet 상태다.

배포 전 Settings에서 검수 branch만 prepare_cloudflare_preview를 실행하는 조건과 출력 cloudflare-preview/site, 운영 자동 배포 Disabled를 확인했다. Access 앱 *.monipick.pages.dev의 소유자 이메일 하나 Allow 규칙을 확인하고 변경하지 않았다. 검수 배포에는 공개 형식 빌더를 연결하지 않았다.

새 고유 호스트와 alias 각각 홈·JS·제품·운영 안내 GET 4개, 총 **8/8**이 비인증 요청에서 Access 로그인 호스트로 302 이동했다. [비인증 검사 결과](assets/monipick-public-prep-20261023/anonymous-access.json)에 상태와 redirect 호스트만 저장했다. 인증 query·쿠키·개인 이메일은 저장하지 않았다.

기존 허용 계정으로 인증 후 홈·검색·2개 제품 비교·최신 contact 메일 링크/수신 완료 안내를 직접 확인했다. [실제 HTTP 검사](assets/monipick-public-prep-20261023/http-results.json)는 **9/9 통과**다. 정상 경로 7개 200, 루트/제품 아래 없는 경로 2개 404와 올바른 오류 본문을 확인했다. noindex/nosniff/DENY/referrer/permissions/no-store도 9개 모두 일치했다. 로그인 응답을 앱 응답으로 계산하지 않았다.

[데스크톱](assets/monipick-public-prep-20261023/private-desktop.jpg), [비교](assets/monipick-public-prep-20261023/private-compare.jpg), [운영 안내](assets/monipick-public-prep-20261023/private-information.jpg), [모바일](assets/monipick-public-prep-20261023/private-mobile.jpg) 화면을 저장했다. 모바일 override는 390×844이고 DOM에서 innerWidth 390/scrollWidth 375를 확인했으며 종료 전 viewport 설정을 복구했다. 실물 iOS Safari 검증은 아니다.

기본 monipick.pages.dev는 404, monipick.com의 웹 요청은 DNS 해석 불가를 확인했다. 이메일 MX/TXT와 웹사이트 DNS를 혼동하지 않는다. 메일 수신 연결은 유지했고 새 외부 수신 테스트 메일은 보내지 않았다.

## 테스트 결과

| 검증 | 결과 |
| --- | --- |
| Python 전체 | 648개 통과, 약 63초; 기존 633 + 새 15 |
| 기존 데스크톱·모바일 전체 | 로컬 226개 통과, 약 1.4분 |
| 새 공개 후보 데스크톱·모바일 | 10개 통과, 약 9.7초 |
| 원본 검수 메타데이터/경로 | validate_local_site 통과 |
| 정적 제품 페이지 | 30개 재생성 check 통과 |
| 보호 후보 | 기존 생성기 61개 파일 생성 통과(HTTP 진단 2개 포함) |
| 공개 후보 | 61개 생성 및 독립 --check 통과; 진단/원본 연구/manifest 미포함 |
| 원본·사용자 변경 | data/schema와 사용자 수정 4개를 포함한 44개 파일 hash 일치 |
| 개인정보·비밀값·추적기 | 공개 후보에서 개인 Gmail/대표 secret 패턴/주요 광고·분석 도메인 일치 없음 |
| 내부 문서 경로·diff | 변경 문서 상대 링크·git diff --check 통과 |

공개 후보 브라우저 검사에서 처음 2개가 카드의 담기 버튼과 비교함의 빼기 버튼을 동시에 선택해 실패했다. 테스트 locator를 제품 카드로 한정한 뒤 10개가 통과했다. 제품 구현이나 검증 기준을 완화한 것이 아니다. 신규 단위 테스트는 빌더 추가 전 모듈 부재로 실패했고 구현 후 잘못된 입력 거부를 포함해 통과했다. 기존 unittest의 임시 파생 파일 변조 테스트가 출력하는 FAIL 문구는 최종 OK/exit 0과 구분한다.

검증 명령:

```sh
python3 -m unittest discover -s tests -q
npm run test:e2e -- --workers=2
npx playwright test --config playwright.release.config.js --workers=2
python3 scripts/validate_local_site.py
python3 -m scripts.build_monitor_pages_v3 --check
python3 -m scripts.build_monipick_public_candidate --output /tmp/monipick-public-candidate-20261023 --check
```

9afa091의 두 CI 모두 success:
[준비 branch 39863282509](https://github.com/dineyong/connectable/actions/runs/39863282509),
[검수 branch 39863286572](https://github.com/dineyong/connectable/actions/runs/39863286572).
CI 브라우저는 기존 커밋된 212개 + 공개 후보 10개다. 로컬 226개에는 기존 사용자 미커밋 테스트 14개가 있으므로 숫자가 다르다. 보고서 후속 커밋은 준비 branch에만 push하며 실행 결과를 완료 응답에 기록한다. 그 커밋은 배포 소스의 화면/코드를 변경하지 않는다.

## 남은 확인과 공개 경계

사용자가 확인할 부분은 두 가지다.

1. 최신 검수본에서 검색·비교·상세와 모바일 사용 흐름을 수락한다. 공개용 문구를 볼 경우 로컬 후보 http://127.0.0.1:8876/ 및 /information에서 확인할 수 있다. 이 서버는 해당 컴퓨터에서만 접근 가능하다.
2. 검증한 릴리스 SHA/범위에 대해 실제 공개 여부를 별도로 승인한다. 이번에 승인 요청·자동 공개를 실행하지 않는다.

승인 이후에만 운영 build branch/command/output, Custom domain·HTTPS·대표 호스트를 설정하고 운영 origin에서 200/404/CSP/캐시/색인 상태를 다시 검증한다. 현재 성공은 실제 monipick.com 운영 성공의 대체 증거가 아니다. Cloudflare 자동 URL 정규화·CDN·TLS·Access와 웹 로그의 실제 운영 범위는 전환 단계에서 확인한다.

[████████░] 준비 체크포인트 완료, 실제 공개 승인·운영 origin 검증 대기. 작업량 백분율이 아니다. 남은 SKU 조사, 제품 사진, 댓글, 통계·광고·제휴·실시간 뉴스는 첫 공개 선행 조건으로 추가하지 않았다. 기존 원본/사용자 변경과 미추적 문서는 보존했으며 테스트가 생성한 캡처 2개만 실행 전 Git 내용으로 복원했다.
