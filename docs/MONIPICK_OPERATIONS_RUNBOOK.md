# 모니픽 운영·공개 전환 준비

> 2026-10-24 최신 상태: 사용자가 확인한 후보의 실제 공개를 승인했고 monipick.com 운영 배포·HTTPS 연결을 완료했다. [공개 결과](MONIPICK_PUBLIC_LAUNCH_REPORT_20261024.md)와 [운영 공개 기준](MONIPICK_PRODUCTION_OPERATIONS.md)을 우선한다. 광고·통계는 비활성, main은 미병합이다. 아래 승인 대기/미적용 설명은 이전 준비 단계 이력이며 후보 빌더 자체의 미승인 계약은 계속 유지한다.

기준: 2026-10-22. 통계 미도입은 사용자 결정이다. contact@monipick.com의 Gmail 전달 연결과 외부 발신 계정 원문의 INBOX 수신 확인을 완료했다. 실제 공개 승인은 대기한다. [연결·테스트 기록](MONIPICK_EMAIL_ROUTING_SETUP.md)의 최신 후속 결과를 따른다.

## 현재 기능과 운영 범위

- 모니터 검색·필터·2~3개 비교, 공식 사양/출처/조건, 외부 후기 원문 링크, 구매 가이드, 저장된 뉴스 목록을 제공한다.
- 광고·쿠팡·댓글 서버·공개 반응 집계·방문 분석 도구는 활성화하지 않는다. 자동 뉴스 수집 일정도 추가하지 않는다.
- 비교 선택은 탭 sessionStorage, 도움 반응은 브라우저 localStorage다. 이를 전체 사용자 통계·구매 인증으로 표현하지 않는다. 다른 origin으로 이동하면 기존 저장값이 자동 이전되지 않는다.
- 호스팅/Access의 운영·보안 로그는 방문 통계 스크립트와 별개다. “개인정보를 전혀 처리하지 않는다”는 포괄적인 문구를 쓰지 않는다. 공개 전 실제 로그 설정·처리 범위와 안내를 대조한다.
- 해외 공식 문서·한국 SKU 미확인·부분 검토·충돌을 그대로 표시한다. 공개 승인과 공식 사양의 검토 승인, 기기 호환성 승인, 이미지 사용권은 서로 다르다.

## 운영 이메일

[화면 안내](../web/information.html#corrections)는 실제 외부 수신을 확인한 contact@monipick.com 링크를 제공한다. 같은 Gmail의 발신/수신 중복 처리 안내는 테스트 원문 수신의 대체 증거가 아니며 다른 발신 계정의 원문 INBOX 도착으로 검증했다. 전달 대상 개인 주소는 공개 저장소에 저장하지 않는다. 전송 폼·자동 답장·도메인 주소 발신 기능은 제공하지 않는다.

정정 요청 안내에는 제품/SKU·페이지 URL·항목·공식 근거 URL과 위치를 요구하며 불필요한 개인정보를 보내지 않도록 안내했다. 처리 시간이나 자동 반영을 약속하지 않는다.

## 정정 처리 절차

1. 요청의 모델·SKU·리비전·지역이 기존 제품과 같은지 대조한다. 비슷한 이름만으로 통합하지 않는다.
2. 공식 원문과 문서 위치를 확인한다. 검색 요약이나 제3자 제안을 공식 사양으로 채택하지 않는다.
3. 불확실하면 UNKNOWN, 공식 자료끼리 다르면 CONFLICT를 유지한다. 사용자 경험은 공식 fact와 분리한다.
4. 확인한 필드와 해당 근거만 갱신한다. 전체 제품 확인일을 일괄 최신화하지 않는다.
5. 파생 파일을 재생성하고 관련 검증·회귀 테스트·CI를 확인한다. 수정 내용과 출처·범위를 기록한다.
6. 배포 권한 범위에 맞는 검수본에서 화면과 실제 응답을 확인한다. 공개 전환·운영 롤백은 별도 승인 범위에서 수행한다.

## 비활성 공개 설정 생성

```sh
python3 -m scripts.prepare_monipick_release --output /tmp/monipick-release-prep-next
```

출력은 새 경로여야 한다. 기존 폴더를 덮어쓰지 않는다. 프로그램은 네트워크 접속·DNS·배포·계정 설정 변경을 하지 않는다.

| 출력 | 용도 | 현재 적용 |
| --- | --- | --- |
| `site/` | 기존 비공개 후보: noindex, robots 전체 차단, no-store 유지 | 로컬 파일 생성만 |
| `activation-drafts/page-metadata.proposed.json` | monipick.com 기준 경로·canonical·색인 범위·원본 hash | 비활성 |
| `activation-drafts/sitemap.xml.proposed` | 안정적인 34개 주소 후보, lastmod 추정 없음 | 비활성 |
| `activation-drafts/robots.txt.proposed` | 향후 승인된 사이트맵 안내 | 비활성 |
| `activation-drafts/_headers.proposed` | CSP·프레임·nosniff·referrer·권한·일부 noindex | 비활성 |
| `activation-drafts/_redirects.proposed` | 기존 탐색 주소 두 개를 홈으로 통합하는 301안 | 비활성 |
| `manifest.json` | 파일 hash·통계 제외·운영 주소/외부 수신 검증 완료·공개/색인 승인 false | 문서 루트 밖 |

**출력 디렉터리 전체나 activation-drafts를 배포하면 안 된다.** 현재 Cloudflare 빌드는 기존 `prepare_cloudflare_preview`와 검수 브랜치만 허용하며 이 새 생성기로 바꾸지 않는다. 이 도구는 공개 전환 버튼이나 승인 우회 기능을 제공하지 않는다.

## 주소·검색 정책안

- 대표 origin 안: `https://monipick.com`. 홈 `/`, 목록 `/monitors/`, 제품 `/monitors/<id>/`, 가이드 `/guides/monitor-buying`, 자료 `/information`.
- 원본 탐색 HTML과 확장자 없는 탐색 주소는 홈으로 통합하는 안을 준비한다. www·HTTP·pages.dev의 호스트 전환은 Pages 파일 하나로 해결됐다고 가정하지 않고 공개 승인 후 도메인 설정에서 별도 검증한다.
- 34개 안정적인 주소를 사이트맵 후보로 삼는다. 필터·검색어·비교 선택 조합을 별도 페이지로 생성하지 않는다. 저장형 뉴스·10종 별도 조사·404는 초기 색인 후보에서 제외한다. 제외 페이지는 링크로 접근 가능하며 숨기거나 삭제하지 않는다.
- Pages는 `.html`을 확장자 없는 주소로 정규화하고 상위 `404.html`을 사용한다. `/* /index.html 200` 같은 포괄적인 홈 재작성은 넣지 않는다. [공식 경로 문서](https://developers.cloudflare.com/pages/configuration/serving-pages/)
- 헤더 초안은 정적 Pages용이다. 향후 Functions/Workers 응답에는 별도 적용이 필요하다. [공식 헤더 문서](https://developers.cloudflare.com/pages/configuration/headers/)
- 리다이렉트는 구체적인 기존 탐색 주소만 대상으로 한다. 공개 적용 전 실제 체인·query/hash·상세 링크·없는 경로를 다시 검사한다. [공식 리다이렉트 문서](https://developers.cloudflare.com/pages/configuration/redirects/)
- 공개 캐시는 Pages 기본 동작부터 시작하고, 이름에 hash가 없는 JS/CSS에 장기 immutable 캐시를 주지 않는다. 현재 검수의 no-store는 유지한다. [공식 캐시 안내](https://developers.cloudflare.com/pages/configuration/serving-pages/#caching-and-performance)

## 실제 공개 전환 시 필요한 별도 단계 — 이번에는 미실행

1. 운영 Gmail 전달 연결·외부 수신 검증은 완료했다. 정정 창구·운영 안내와 호스팅의 실제 로그 범위를 공개 후보에서 대조한다.
2. 검수한 공개 후보 SHA·페이지 목록·남은 미확인을 제시하고 **최종 공개 승인**을 받는다.
3. 승인 범위에서만 별도 릴리스 커밋/출력물을 확정한다. 위 초안의 metadata/robots/헤더/리다이렉트와 공개용 문구를 일관되게 적용하고 검증한다. 현재 noindex 검증기를 느슨하게 바꿔 통과시키지 않는다.
4. Cloudflare production 기준 브랜치·빌드 명령·출력 경로를 명시적으로 설정하고 도메인·HTTPS·대표 호스트 이동을 검사한다. 기존 Access 검수본은 계속 보호한다. main 병합은 공개 승인과 별도의 Git 작업이다.
5. 실제 운영 origin의 200/404/헤더/모바일/내부 경로/색인 정책과 비공개 연구 파일 미노출을 재검사한다. 검수 호스트나 로컬 성공으로 대신하지 않는다.
6. 검색 도구 소유 확인·사이트맵 제출·수집·색인 결과를 구분해 기록한다. 색인/순위/AI 인용을 보장하지 않는다.

## 되돌리기 준비

이번 기준 코드와 CI는 Git 이력으로 고정하고, 향후 운영 배포 ID·SHA·시각·파일 manifest를 별도 기록한다. 이번에는 운영 배포가 없으므로 “실제 롤백 성공”을 주장하지 않는다. 공개 후 결함이 생기면 승인 범위의 Pages 배포 복원으로 대응하며 원본 데이터나 관련 없는 변경을 reset/강제 push로 되돌리지 않는다.

남은 사용자 결정: 최종 공개 승인. 사진·남은 SKU·댓글·광고·실시간 뉴스는 첫 공개의 추가 필수 조건으로 늘리지 않는다.

## 공개용 빌드 후속 준비 · 2026-10-23

[공개용 빌드 가이드](MONIPICK_PUBLIC_BUILD_GUIDE.md)가 공개 형식 출력과 전환안의 최신 기준이다. 기존 prepare_monipick_release의 비활성 초안과 보호 후보 계약은 보존한다. 새 build_monipick_public_candidate는 별도 로컬 출력에 metadata/문구/사이트맵/헤더/redirect를 적용하지만 승인 flag를 해제하거나 Cloudflare 설정을 변경하지 않는다. 실제 도메인 연결·운영 배포·검색 제출은 최종 승인까지 보류한다. 비공개 검수에는 기존 prepare_cloudflare_preview만 사용한다.
