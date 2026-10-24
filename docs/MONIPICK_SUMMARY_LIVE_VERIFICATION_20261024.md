# 27종 설명 운영 반영 요청 — 최신 운영본 재검증

2026-10-24 KST. 요청: 나머지 27종 설명 운영 반영, 미확인·충돌 유지, 광고/통계 OFF, main 미병합, 화면·링크·404·보안 헤더·CI 확인.

## 최종 기준 및 동시 작업 처리

작업 중 원격 운영 브랜치가 별도 SEO 작업에 의해 먼저 갱신된 것을 확인했다. 강제 push하거나 새 운영 내용을 과거 후보로 덮어쓰지 않았다.

- 기존 이 채팅 후보: `26d2a66` / `codex/monipick-summary-expansion` — 27종 각각 3개 claim. 이 후보는 이력 그대로 보존한다.
- 먼저 완료된 최신 운영 후보: `6b933d1cae75f64ae84ea096b1274ab50597c2d9` — 30종 설명·탐색 경로·가이드/정정 링크.
- 실제 운영 코드: **`efa63c177be2c371cf6e8d3d37492aec8ccee517`**.
- 운영 remote 최신 문서 commit: `220e831fbfaa37ef442d47e82d9025c0052acf9c`.
- 실제 Cloudflare 배포: **`12f2f5ab-2701-46b6-a431-81bde2ffb89a`**, Production, monipick.com alias, success. 대시보드에서 SHA·alias·성공·배포 시각 13:22 KST/19초를 직접 재확인했다.
- 승인 콘텐츠 fingerprint: **`e7849b28dbecdd9ca86c85fd6ead9565f39b1419986722345dffd160c4d3673c`**. 네이버 확인 파일을 포함한 inventory 62개.

운영본과 이전 8898 후보는 바이트가 같지 않다. 최신 운영본은 별도 [SEO 승인·배포 기록](SEO_GEO_RELEASE_20261024.md)에 따른 30종 설명 판이다. 이 요청의 목적을 이미 충족하는 최신 공개 내용을 검증하여 유지했고, 중복 배포나 충돌 병합을 하지 않았다.

이 채팅에서 준비한 `c17a50f`(codex/monipick-summary-release)는 원격 운영 브랜치가 앞서 있어 push가 정상 거부됐으며 공개되지 않았다. 자동 배포를 잠시 켰다가 원격 차이를 확인한 즉시 다시 Disabled로 저장했다. 현재 운영 빌드·원본·승인 기록을 변경하거나 새 원격 승인 파일을 추가하지 않았다. main은 `c58dee5f3d1222d49e598dddbac5c8c6a7b4b8f0` 유지다.

## 이번에 직접 실행한 HTTP 및 링크 검사

[HTTP 원시 결과](assets/summary-live-verification-20261024/http-results.json), [검사 분류](assets/summary-live-verification-20261024/classification.json).

- HTTPS 요청 **61개**: 정상 200 **59개**, 임의의 루트/제품 경로 실제 404 **2개**.
- 61개 모두 최신 승인 빌드와 응답 본문 바이트 일치. 30종 제품 모두 요약 1구역 확인.
- 내부 링크 **428개 출현**의 대상과 fragment 검사: 오류 **0**. 고유 링크 수 또는 외부 제조사 사이트 전수 재접속을 뜻하지 않는다.
- 전체 응답의 CSP/nosniff/DENY/referrer/permissions 값 검사 통과. HTTPS 인증서 검증을 우회하지 않았다.
- 정상 문서 canonical·robots와 승인된 메타 설명 대조 통과. 실제 404 문서는 `noindex,follow`다.
- 기존 사양표·출처·확인일·한국 SKU 미확인·충돌 안내를 보존한 빌드와 일치했다. 원본 `data/research`, `data/official`, `schemas`, `web` 및 기존 공개/3종 승인 기록은 기준 cc2f4f7 대비 변경 없음.

### 캐시 검사 결과를 성공으로 숨기지 않음

추가한 엄격 검사에서는 모든 응답에 `no-transform`까지 요구했다. **59/61 통과**, 실제 404 두 건은 `missing_no_transform`으로 기록됐다. 두 응답의 실제 Cache-Control은 **no-store**이고, 상태·본문·주요 보안 헤더는 모두 정상이다. 원시 실패를 보존하며 캐시 정책 차이로 별도 분류했다. 앱이나 검사 기준을 바꿔 오류를 없애지 않았다. 404의 실제 브라우저 DOM에도 script가 없었다.

## 이번 실제 브라우저 검사

[브라우저 기록](assets/summary-live-verification-20261024/browser-results.json), [데스크톱](assets/summary-live-verification-20261024/desktop.png), [모바일](assets/summary-live-verification-20261024/mobile.png), [요약 구역](assets/summary-live-verification-20261024/summary-desktop.png), [404 모바일](assets/summary-live-verification-20261024/404-mobile.png).

- LG 32GS95UE-B: 4K 240Hz와 FHD 480Hz를 구분하고, 한국 SKU 미확인·공식 근거·기존 확인일 유지 확인.
- LG 27UP850K-W: 90W/96W 충돌 안내 유지. 요약은 기존 90W 기록을 기술하며 충돌이 해결됐음을 뜻하지 않는다.
- MSI MAG 274QRF QD E2: 색역 및 포장 중량 충돌 안내 유지.
- Samsung LS34C650UEEXXY: AU 문서 지역과 USB-C 영상 모드 미확인 유지.
- Dell U2724D: USB-C 데이터 전용과 HDMI TMDS 조건 유지.
- 데스크톱 1280px 및 모바일 390px에서 가로 넘침 없음. 설명 블록 흰색, padding 각각 24px/18px 확인. 모바일의 탐색 경로는 세로로 배치된다. 전체 브라우저·기기 인증이나 접근성 완전 검수를 의미하지 않는다.
- 모바일에서 USB-C 가이드 #usb-c, 사양 비교표 #comparison, 자료 정정 #corrections 링크를 실제 클릭하여 최종 주소·앵커 확인.
- 홈 모델 검색 `32GS95UE-B` → 1종 확인. 검색값은 복구했고 기존 비교함 선택은 바꾸지 않았다.
- 홈·제품·404의 검사한 DOM에 외부 광고/분석 script 및 iframe 없음. 제품/404는 script 0개, 홈은 기존 자체 JS만 존재. 확인한 콘솔 error/warn 없음.
- 임시 viewport를 reset했다. 최종 브라우저는 실제 운영 제품 설명 URL을 보여준다.

## 광고·통계 및 검수 호스트

[호스트·상품 gate 확인](assets/summary-live-verification-20261024/host-and-product-gate.json).

- 정확한 서버 모델 ID로 상품 API를 조회해 **503 INTEGRATION_NOT_ENABLED**, `private, no-store, max-age=0` 확인. 활성화 플래그·키·사이트/광고 설정은 변경하지 않았다. 처음 사용한 비정규 모델 ID는 UNKNOWN_MODEL을 반환했고 정확한 ID로 재확인했다.
- 검수 고유 URL·기존 preview alias·기본 pages.dev의 이번 비인증 HTTP 요청은 **403**이었다. 이전 보고서의 302/로그인·noindex 상태를 이번 요청에서도 확인했다고 주장하지 않는다. 현재 요청에서 콘텐츠가 노출되지는 않았으나 Access 로그인 경로/기본 호스트의 noindex는 이 결과만으로 재확정할 수 없다. 이를 우회하려고 로그인·WAF·Access를 변경하지 않았다.
- Cloudflare 자동 운영 배포는 **Disabled**로 복구된 상태를 직접 확인했다. 도메인/DNS/HTTPS/메일/Access/환경변수/secret/RUM 설정은 변경하지 않았다.

## 테스트 및 GitHub

- 최신 운영 SHA의 [CI 40062034540](https://github.com/dineyong/connectable/actions/runs/40062034540): **success**, head `efa63c1` 일치.
- CI 로그 직접 확인: Python **680개**, 브라우저 **212 + 10 + 14 = 236개** 통과.
- 이번 로컬 재실행: `python3 -m unittest tests.test_monipick_seo_review tests.test_monipick_seo_release tests.test_monipick_content_release tests.test_monipick_cloudflare_build -q` → **21개 통과**.
- 최신 운영 빌드 재생성 통과. 코드가 바뀌지 않아 전체 테스트/배포를 중복 실행하지 않았다.
- 이 검수의 보고서·증거만 `codex/monipick-summary-live-verification`에 별도 commit/push한다. 사용자 dirty 체크아웃은 보존한다. main 병합·강제 push 없음.

## 판단

**실제 monipick.com에 30종 설명이 반영되어 있고, 이번 요청의 필수 운영 검증은 통과했다.** 캐시 검사 차이와 검수 호스트 403의 확인 한계는 위에 남긴다. 새로운 사양 확인·한국 SKU 동일성 승인·실측/호환성 보장·검색 색인 효과를 의미하지 않는다. 현재 이 작업을 마치기 위한 추가 사용자 결정은 없다.
