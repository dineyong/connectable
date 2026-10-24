# 승인한 제품 설명·내부 링크 운영 반영

## 승인 범위

사용자는 2026-10-24 후보 89dd4ec의 시안을 운영에 반영하고 화면·링크·404·보안 헤더·GitHub/CI를 확인하도록 승인했다. 광고·통계 비활성, main 미병합, 기존 사용자 미커밋 변경과 원본 데이터 보존을 유지한다. 제품 사진/쿠팡 상품 연결/뉴스 자동 수집 등 다른 로컬 작업은 포함하지 않는다.

후보 구현과 시안은 [후보 보고서](MONIPICK_CONTENT_POLISH_REPORT_20261024.md)에 보존한다. 후보 빌더는 계속 미승인 후보만 만들고, 기존 운영 빌더의 승인 계층에서 별도 사용자 승인 기록을 검증한 뒤에만 공개 파일을 만든다. 후보 파일 바이트는 승인한 89dd4ec와 동일하다.

## 운영 승인 계약

- 이전 공개 기준 61개 fingerprint: df71388fbe44404e224592f13096cf862970076366af35fd1bee1eb053723bf0.
- 이번 후보 61개 fingerprint: 6acf6558d60a38b86d4560133a3c4f112bf225e9702603f1b9b7a5eddb478728.
- 별도 deploy/monipick-content-release.json에서 이번 승인·후보·이전 기준·새 fingerprint·광고/통계/main 보류를 함께 고정한다. 이전 승인 기록은 덮어쓰지 않는다.
- 기존 61개 기준도 계속 검증하고, 그로부터 결정적으로 생성한 후보와 새 승인 fingerprint를 대조한다. 승인 기록 부재·변형·다른 원점·다른 후보·새 본문/CSS·광고/통계/main 활성화는 거부한다.
- Naver 확인 파일 1개는 기존 별도 승인으로 보존하며 전체 파일 inventory는 62개다.
- API 서버/키/쿠팡 활성화 설정은 변경하지 않는다. 기존 Functions는 그대로 배포되고 제품 연결 gate는 유지한다.

## 변경 및 검증

대표 3종의 설명·메타 설명·근거/주의사항·구매 가이드 연결, 내부 링크 168곳 및 자료 대화상자 링크, 설명 영역 CSS, 3종 접근성 안내 이름만 후보대로 반영한다. 원본 data/official·data/research·schemas·web은 수정하지 않는다.

신규 승인 테스트 3개: 실제 승인 후보만 운영 빌드, 승인 누락·변형·광고/통계/main 활성화 거부, 임의 CSS 추가 거부. 기존 후보와 검수본의 승인 보류를 해제하지 않는다.

배포 SHA·ID·CI·실제 검증은 실행 후 아래 기록한다.

## Cloudflare 자동 삽입 발견 및 차단

실제 브라우저에서는 Cloudflare beacon.min.js가 DOM에 삽입돼 있었다. 기본 curl 검사에서는 나타나지 않았다. 따라서 ‘원본에 분석 코드 없음’ 또는 기본 HTTP 바이트 검사만으로 실제 브라우저의 통계 비활성을 확정할 수 없다. 이번 배포 전부터 존재했는지·실제로 전송됐는지·CSP 차단됐는지는 별도이며 이번 관측으로 과거 수집 여부를 단정하지 않는다.

Pages Metrics의 Web Analytics는 disabled였고 계정 Web Analytics 목록에는 다른 프로젝트만 등록돼 있었다. 다른 프로젝트의 설정을 변경하거나 데이터를 삭제하지 않았다. 사용자 통계 OFF 지시를 확실히 적용하기 위해 공식 문서가 설명하는 public, no-transform 캐시 지시를 추가한다. 기존 max-age=0, must-revalidate는 유지한다. 공개된 운영 이메일과 보안 CSP를 바꾸지 않는다. 보안 정책을 완화해 beacon을 허용하지 않는다.

공식 근거: [Cloudflare Web Analytics 자동 삽입과 no-transform](https://developers.cloudflare.com/web-analytics/get-started/), [RUM beacon](https://developers.cloudflare.com/speed/observatory/rum-beacon/). 이것은 사이트 전면 디자인 변경이 아니라 사용자가 명시한 통계 비활성을 위한 응답 정책이다.

시각적 후보 89dd4ec의 61개 fingerprint는 위 6acf…이며, 통계 OFF 조건을 위해 _headers의 Cache-Control을 별도 규칙으로 추가했던 중간 fingerprint는 70eaba02874115d5cdfd30ca122653dc481b3caf7e5b3a4272194ff17b29cff6다. 이 중간 버전의 규칙 충돌을 아래와 같이 수정했다. 승인 기록에 범위와 새 fingerprint를 함께 기록한다. 디자인·제품 데이터·출처는 그대로다. 새 배포 후 실제 브라우저에서 삽입 부재를 다시 확인한다.

## 실패 발견·수정 및 최종 결과

### 보안 헤더 규칙 충돌

중간 배포 5063c26 / f71401e7-e287-465b-847d-b8d441eb8faf에서 두 번째 /* 규칙이 첫 번째 규칙을 덮어써 CSP·frame·permissions 헤더가 누락됐다. 로컬 smoke 서버는 여러 헤더 규칙을 합쳐 검사했으므로 이 플랫폼 동작 차이를 놓쳤다. 실제 운영 60개 검사를 통해 발견했고 성공으로 숨기지 않았다. [수정 전 검사](assets/content-release-20261024/header-override-before-fix.json)를 보존한다.

3bb2e69에서 Cache-Control을 기존 전역 규칙 내부로 합쳤다. 전역 규칙이 정확히 하나이며 같은 규칙에 no-transform과 모든 보안 헤더가 존재해야 한다는 회귀 테스트를 추가했다. 기존 검증 기준을 완화하지 않았다. 최종 61개 승인 fingerprint는 **665042d51aecd72c2ff51249c6c6be0ea30313860e9abea28cc691be48c7e8a8**이다. 최종 [manifest](assets/content-release-20261024/manifest.json)를 보존한다.

### 도메인 RUM 비활성

정상 페이지의 no-transform만으로는 Pages가 별도 처리하는 404 응답의 삽입까지 막지 못했다. monipick.com → Speed → Real user monitoring에서 Disable completely → Disable RUM을 적용해 **RUM is currently disabled for this zone** 상태를 확인했다. 이 변경은 사용자 통계 OFF 지시 범위이며 다른 도메인 통계와 Cloudflare 보안 로그/Access/WAF는 변경하지 않았다. 설정 직후 404에 삽입 흔적이 잠시 남았으나 전파 후 새로운 404 요청에서는 script 0개·브라우저 error 0개를 확인했다. [RUM OFF 화면](assets/content-release-20261024/rum-disabled.png).

### 배포와 실제 운영 검수

- 운영 브랜치: codex/monipick-production. 작업 브랜치의 승인 범위만 fast-forward했고 main 병합·변경·강제 push 없음.
- 최종 배포 SHA: **3bb2e698dd1a6f8f95fbcdbc893ac94ee6fe0998**.
- 최종 Cloudflare 배포 ID: **0de0a5ed-db87-473b-b48e-bd655e114e63**. monipick.com에서 새 설명과 최종 헤더 확인.
- 실제 운영 URL 60개: **실패 0**, 58개 정상 200·2개 실제 404, HTTPS 인증서·CSP/nosniff/DENY/referrer/permissions/cache·canonical/robots 확인. 모든 비교 대상 파일의 응답 본문이 승인한 최종 빌드와 바이트 일치했다. [최종 HTTP 결과](assets/content-release-20261024/http-final.json).
- 기존 사이트맵 34개, 공식 원본·질문 코퍼스·후기·UNKNOWN/CONFLICT·한국 SKU 및 호환성 보류 유지. Naver 확인 파일 유지. 검수 배포는 비인증 302 보호 유지.
- 실제 브라우저: 대표 3종 설명·근거·주의사항 및 canonical, 가이드 최종 주소/usb-c anchor, 홈 모델 검색(각 1개 결과)·2종 비교·한국 SKU 미확인 유지 확인. 정상 페이지 및 마지막 404에서 통계 스크립트 없음. 최종 확인한 브라우저 error/warn 없음.
- 390×844 모바일: innerWidth 390 / scrollWidth 375, 넘침 없음. viewport 복원했다. [데스크톱](assets/content-release-20261024/desktop.png), [모바일](assets/content-release-20261024/mobile.png), [404](assets/content-release-20261024/404.png).
- 쿠팡 제품 API는 계속 503 INTEGRATION_NOT_ENABLED 및 no-store다. 키·상품 이미지·제휴 링크·광고를 활성화하거나 인증 경로를 새로 호출하지 않았다.
- 자동 운영 배포는 최종 업로드 후 다시 Disabled로 복구했다. 도메인/DNS/HTTPS/Access/메일은 변경하지 않았다.

### 테스트·GitHub

- 배포 승인 추가 시 로컬 Python 전체 668개 통과, 최종 헤더 규칙 테스트 추가 후 관련 21개 통과.
- [최종 운영 SHA CI 40059491054](https://github.com/dineyong/connectable/actions/runs/40059491054): **success**. Python **669개**, 기존 브라우저 **212개**, 공개 CSP **10개**, 새 후보 **14개**(브라우저 합계 **236개**)가 통과했다.
- 첫 내용 배포 51437bb의 CI 40059012079도 success였다. 중간 5063c26 CI는 후속 수정 push로 cancelled이며 성공으로 표시하지 않는다.
- 원래 dirty 사용자 파일과 미추적 작업은 보존했다. 원본 data/research·data/official·schemas·web/은 Git diff에서 변경 없음.
- 후속 문서·증거 커밋은 배포 SHA와 분리한다. 코드 변경이 없어 전체 검사를 중복 실행하지 않도록 해당 문서 커밋에만 [skip ci]를 사용한다. 자동 운영 배포 Disabled이므로 문서 push로 다시 배포하지 않는다.

현재 남은 필수 사용자 조치는 없다. 대표 3종 외의 제품 설명 확대, 실제 검색 색인 보고서 관찰, 브랜드 공유 이미지 등은 후속 작업이며 이번 공개 반영의 필수 조건으로 추가하지 않는다.

## 최종 검수 갱신 — 재방문 자산 캐시

위 3bb2e69는 보안 헤더 복구 기준점이다. 이후 실제 기존 방문 브라우저에서는 과거 CSS가 캐시돼 새 설명 영역에 흰색 배경/패딩이 적용되지 않는 것을 발견했다. 일반 새로고침만으로 해소됐다고 가정하지 않고, 5bf48c9에서 변경된 두 자산의 href/src에 내용 hash query를 추가했다. 새 CSS/JS 내용이 바뀌면 버전이 결정적으로 갱신된다. 제품 URL·canonical·sitemap·근거값·디자인 자체는 바꾸지 않는다. 신규 회귀 테스트에서 CSS/JS의 실제 hash와 문서의 버전 주소가 일치함을 검사한다.

- **최종 운영 SHA: 5bf48c973507fd343261ed1db997d2e90fd4911b**.
- **최종 배포: dd03fd26-9bef-40ff-8692-db8e614e98c4**.
- **최종 61개 승인 fingerprint: 0e1e72327bf45dd03ec6901a487a7ef3141009ad1c1920742f1a90c35821e732**. 위 manifest/http-final/화면 증거를 이 버전으로 갱신했다.
- 실제 브라우저 CSS 주소 monitor-detail-v3.css?v=38ff42df7eb5, 홈 JS monitor-v3.js?v=b844006ea60f 확인.
- 데스크톱 computed background rgb(255,255,255)/padding 24px, 390px 모바일 background rgb(255,255,255)/padding 18px, scrollWidth 375 확인. 이전 잘못된/작게 캡처된 이미지도 최종 화면으로 교체해 직접 열람했다.
- 최종 배포 HTTP 60개 재검사: 실패 0. 최종 404 및 홈·제품의 실제 DOM에서 Cloudflare beacon 없음 확인. RUM OFF 및 자동 운영 배포 Disabled 유지.
- 관련 회귀 22개 통과. [최종 운영 CI 40060034062](https://github.com/dineyong/connectable/actions/runs/40060034062)는 **success**. Python **670개**, 기존 브라우저 212개 + 공개 CSP 10개 + 새 후보 14개, 합계 **236개** 통과했다.
