# 모니픽 구조화 데이터·공유 이미지·파비콘 운영 반영

2026-10-24. 사용자: 로컬 8886 검토본 그대로 운영 반영 및 모바일 재확인 승인.

## 배포 범위와 보존

검토 commit `99762c055366822627ed47f664437e48f2feac27`의 산출물 69개와 승인된 운영 빌드 파일의 바이트·목록이 완전히 일치함을 확인했습니다. 별도 `deploy/monipick-brand-release.json`에 검토 commit, 기존 SEO fingerprint, 새 fingerprint와 이번 승인을 연결했습니다. 이전 공개·콘텐츠·SEO 승인 검증을 모두 유지하고 새 변경도 바이트 일치 검증을 통과해야 빌드됩니다.

WebSite 1개, WebPage 34개, BreadcrumbList 30개를 추가했습니다. 공유 이미지는 공통 1200×630 PNG이며 SVG/PNG/ICO 파비콘과 Apple touch icon을 연결했습니다. 제품 가격·별점·리뷰·Product/Offer schema는 추가하지 않았습니다. 본문·제품 설명·내부 링크·CSS/JS·canonical·robots·사이트맵·보안 정책은 기존 검토본을 보존했습니다. 광고·방문 통계 OFF, main 미병합, preview 보호를 유지합니다.

[승인 manifest](assets/brand-release-20261024/release-manifest.json)

## 검증 기록

배포 승인 관련 집중 테스트 12개 및 이전 콘텐츠 승인 회귀 4개 통과. 첫 CI는 이전 테스트의 최상위 reviewed commit 기대값이 SEO 승인에 고정되어 한 건 실패했습니다. 최상위 값은 이번 승인 commit을 검증하고 별도 SEO baseline도 검증하도록 테스트를 수정했습니다. 앱·이미지·검토 산출물은 이 수정으로 변경하지 않았습니다.

운영 검증 및 최종 배포 결과는 아래 후속 기록에 추가합니다. 검토 단계의 로컬 결과와 운영 URL 결과를 구분합니다.

## 운영 반영 완료

- 서비스: https://monipick.com/
- 운영 소스: `d09c2048812097c240d50c5e782cbca4a921d771`.
- Cloudflare 배포: `817d0c30-578a-4493-810f-52a7f06655b4`, Production, success, monipick.com alias 확인. 화면 시각 2026-10-24 13:46 KST, 소요 24초.
- 배포 전 동일 소스 [CI 40063370988](https://github.com/dineyong/connectable/actions/runs/40063370988) success. Python 690개, 브라우저 212+10+14=236개 통과.

## 실제 도메인 검증

[HTTP 증거](assets/brand-release-20261024/http-results.json): **64개 응답 모두 검토본과 바이트 일치**. 404 문서, 중복 원본 monitor-v3.html, _headers/_redirects 및 네이버 확인 파일은 이 64개 검사에서 제외했습니다. 소유확인 파일은 승인 빌드 69개 inventory에 보존됩니다.

- 운영 HTML 내 WebSite 1개·WebPage 34개·BreadcrumbList 30개가 JSON으로 파싱되고 승인한 canonical/제목/설명/화면 경로와 일치합니다. noindex 페이지의 schema 제외 범위를 유지했습니다.
- 공통 공유 이미지의 실제 HTTPS URL, OG/Twitter 태그, 이미지 크기 1200×630을 확인했습니다.
- SVG·PNG48/192·ICO·Apple180 아이콘 링크 및 실제 이미지 응답을 확인했습니다. 루트 favicon.ico도 정상 응답했습니다.

[브라우저 증거](assets/brand-release-20261024/browser-results.json): 홈·Dell 제품 상세·구매 가이드 × 1280/390/320px **9개 조합**에서 검토본과 스크린샷 픽셀 동일, 가로 넘침 0, pageerror/console.error 0. 각 화면에서 JSON-LD 파싱 및 공유 이미지/아이콘 HTTP 200과 image MIME, 공유 이미지 실제 디코딩 크기를 확인했습니다. Chromium 모바일 에뮬레이션 결과이며 실물 iPhone Safari 검증을 뜻하지 않습니다.

[모바일 상세](assets/brand-release-20261024/detail-390.png), [PC 상세](assets/brand-release-20261024/detail-1280.png). 모바일 캡처를 직접 열어 기존 디자인·제품 설명 보존을 확인했습니다.

[호스트 격리](assets/brand-release-20261024/host-isolation.json): 새 배포 고유 URL 및 기존 preview alias는 비인증 요청에서 Access 로그인 302, 기본 pages.dev는 noindex,nofollow 유지. Cloudflare 설정의 Automatic deployments Disabled를 배포 후 확인했습니다. preview branch, Access, DNS, 환경 변수/secret은 변경하지 않았습니다. main SHA `c58dee5f3d1222d49e598dddbac5c8c6a7b4b8f0` 유지, 운영 push는 fast-forward입니다.

카카오·검색엔진의 외부 캐시 갱신, Google 검색 아이콘/사이트명 채택 및 색인·순위 변화는 이번 서버·브라우저 정상 적용 검증과 별개입니다. 재색인/사이트맵 재제출 요청은 하지 않았습니다.

운영 push로 실행된 동일 SHA의 [후속 CI 40063659000](https://github.com/dineyong/connectable/actions/runs/40063659000)도 최종 success를 확인했습니다. 후속 증거/문서 commit은 서비스 파일을 변경하지 않으며 자동 배포 Disabled 상태를 유지합니다.
