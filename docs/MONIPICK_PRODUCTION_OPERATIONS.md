# 모니픽 운영 공개 기준

2026-10-24 사용자가 확인한 화면·문구로 monipick.com의 실제 공개와 도메인·HTTPS 연결을 승인했다. 광고·통계 비활성, main 미병합, 기존 데이터·한국 SKU 불확실성·호환성 UNKNOWN은 유지한다. 이전 문서의 최종 공개 승인 대기는 이번 승인 범위에서만 해소한다. 외부 검색 도구 제출, 광고/제휴, 새 수집 기능을 승인한 것이 아니다.

## 고정한 공개 범위

[승인 기록](../deploy/monipick-public-release.json)의 파일 inventory fingerprint가 검수한 후보 9afa091의 61개 파일을 고정한다. 공개 빌더는 여기에 맞지 않는 UI/데이터/파일 변경을 거부한다. 배포 문서 루트는 site/뿐이다. 승인 기록·manifest·원본 조사·검토 기록은 문서 루트 밖에 둔다. 공개 승인과 제품 사실/호환성 승인은 별개다.

기존 build_monipick_public_candidate는 계속 미승인 후보를 만들고, [새 분기 빌더](../scripts/build_monipick_cloudflare.py)가 승인된 내용일 때만 운영 manifest를 별도로 기록한다. 빌더 자체는 파일 생성만 하며 Cloudflare/DNS를 호출하지 않는다.

- 운영 branch: codex/monipick-production. main과 병합하지 않는다.
- 검수 branch: codex/monipick-private-preview. 기존 Access 보호·noindex 유지.
- 설정한 공통 출력: cloudflare-build/site.
- production에서는 build_monipick_cloudflare, private-preview에서는 기존 prepare_cloudflare_preview --include-http-check, 그 외 branch에서는 exit 1이다.
- 최초 운영 배포를 위해서만 운영 자동 배포를 켜고, 첫 정상 배포가 완료되면 다시 Disabled로 둔다. 향후 변경은 별도 검증·운영 절차에 따른다.

## 승인 파일의 재현성

사이트맵 XML 선언이 macOS/Python 3.9의 UTF-8과 Linux/Python 3.12의 utf-8로 달라 첫 CI의 승인 hash 검사가 실패했다. 승인 hash를 변경하거나 검사를 완화하지 않고, XML 직렬화에 UTF-8 표기를 명시해 사용자가 확인한 원래 바이트로 고정했다. locale 표기를 바꿔도 결과가 같은 회귀 테스트를 추가했다.

공개 작업 도중 로컬 카드 디자인 파일의 새 미커밋 변경을 발견했다. 그 변경을 덮어쓰거나 이번 릴리스에 포함하지 않는다. Git의 승인된 커밋을 별도 임시 폴더로 내보내 검증하고 Cloudflare도 같은 Git 커밋에서 빌드한다. 현재 작업 트리의 다른 사용자 작업을 임의 배포하지 않는다.

## 도메인과 보안

monipick.com의 웹사이트용 apex CNAME @ → monipick.pages.dev만 추가했다. 메일 MX/SPF/DKIM은 보존한다. HTTPS는 Cloudflare의 인증서 발급·검증 상태와 실제 인증서 검증을 함께 확인한다. 기존 preview Access를 해제하지 않는다. www·pages.dev의 대표 주소 처리는 실제 적용 여부를 공개 보고서에서 구분한다.

운영 검증은 도메인의 실제 200/404, canonical/robots/sitemap, CSP/nosniff/frame/referrer/permissions/cache, JS/CSS와 제품 경로, 모바일·검색·비교·상세를 포함한다. Access 로그인 응답·로컬 성공으로 대신하지 않는다. 공개 뒤 실제 배포 ID/SHA/검증 결과를 별도 보고서에 기록한다.

첫 공개에는 이전 운영 배포가 없다. 정상 배포 ID와 manifest를 이후 복원 기준점으로 보존한다. 다음 배포부터는 이력상의 검증된 운영 배포로 되돌리는 절차를 사용한다. 원본 데이터 reset·강제 push·관계없는 변경의 삭제는 하지 않는다.
