# 모니픽 검색 도구 등록 — 2026-10-24

## 승인 및 보존 범위

사용자가 Google/Naver 사이트 등록과 사이트맵 제출을 승인했다. 광고·통계는 비활성 유지한다. main 병합, UI 변경, 별도 수집 기능, 계정 권한 확대는 하지 않는다. 현재 작업 브랜치는 codex/monipick-production이며 기준 HEAD는 f1cf0c0d402c9a559a14a017f11c26a528b63b3e이다. 기존 미커밋 사용자 작업은 수정하거나 배포하지 않았다.

## Google Search Console — 완료

- 기존 로그인 계정에서 중복 속성이 없음을 확인하고 도메인 속성 monipick.com을 등록했다.
- Cloudflare DNS에 소유권 확인용 TXT 레코드 하나만 추가했다. Google에 Cloudflare 계정 접근 권한을 위임하는 자동 인증은 사용하지 않았다.
- 기존 웹 CNAME, MX, SPF, DKIM은 보존했다. TXT 레코드는 소유권 유지용이므로 삭제하지 않는다.
- DNS 저장 직후 첫 인증은 전파 지연으로 실패했다. 이후 공개 DNS에 레코드가 확인됐고 Google 소유권 확인이 완료됐다.
- https://monipick.com/sitemap.xml 을 한 번 제출했다.
- 최초 목록은 가져올 수 없음/0개였으나 상세 페이지의 최종 결과는 **사이트맵 처리 완료 / 발견된 페이지 34 / 동영상 0**이었다. 중복 재제출하지 않았다.
- [실제 처리 완료 화면](assets/monipick-search-20261024/google-sitemap.png)
- 검색 색인 및 검색 결과 노출 완료는 확인되지 않았다. 사이트맵 처리 성공과 개별 URL 색인 성공은 다르다.

## Naver Search Advisor — 소유확인 및 사이트맵 제출 완료

사용자가 직접 로그인한 뒤 기존 사이트 목록에 monipick.com이 없음을 확인했다. https://monipick.com 등록 절차에서 공식 HTML 확인 파일을 다운로드했다. 공식 파일 한 개만 정식 운영 빌더의 별도 search_verification_files로 추가한다. 기존 61개 승인 파일 fingerprint는 변경하지 않는다. 확인 파일 배포 후 소유확인 버튼을 눌렀으며 보안문자(CAPTCHA) 대화상자가 나타났다. 사용자에게 직접 입력·확인을 요청했고 이후 등록 목록 및 해당 사이트 관리 화면에 접근할 수 있음을 확인했다. 소유확인이 완료됐다. 사이트맵 제출 화면은 비어 있었으므로 https://monipick.com/sitemap.xml 을 제출했다. 제출된 사이트맵 목록에 sitemap.xml / 26.10.24 12:05:36이 표시됨을 확인했다. Naver의 개별 URL 수집·색인·검색 노출 완료는 아직 확인하지 않았다. 비밀번호·인증 코드는 저장하지 않는다. CAPTCHA가 요구되면 사용자에게 알린다.

## 현재 사이트 확인

- 기본 curl 요청으로 홈페이지, robots.txt, sitemap.xml 모두 실제 HTTP 200 확인.
- robots.txt: User-agent * / Allow / 및 정식 사이트맵 URL 확인.
- 사이트맵 XML 파싱 정상, URL 34개·중복 0개.
- 홈페이지 응답에 Google Analytics, Tag Manager, AdSense, Cloudflare Web Analytics 스크립트 도메인 없음. 이번 작업에서 광고·통계를 활성화하지 않았다.
- Python urllib 기본 요청은 HTTP 403이었다. 일반 curl 성공 또는 사이트맵 처리 성공을 모든 클라이언트/모든 페이지의 수집 성공으로 확대하지 않는다. Google은 이번 사이트맵 34개를 실제 처리했다. Naver 수집 성공 여부는 로그인·제출 후 별도 확인이 필요하다.
- Google 등록 때는 코드·배포 변경이 없었다. 이후 Naver 확인 파일 추가를 위해 아래 범위만 변경·검증·배포했다. 기존 제품 데이터·화면·광고·통계 설정은 변경하지 않았다.

## 다음 단계

1. Google/Naver 등록과 사이트맵 제출은 완료됐다.
2. Google/Naver의 실제 색인 보고서를 추후 확인한다. 즉시 노출이나 일정 기간 내 노출을 보장하지 않는다.

## 공식 안내

- [Google 사이트맵 보고서](https://support.google.com/webmasters/answer/7451001?hl=ko)
- [Google 소유권 확인](https://support.google.com/webmasters/answer/9008080?hl=ko)
- [Naver 사이트 등록 및 소유확인](https://searchadvisor.naver.com/guide/faq-start-register)
- [Naver 사이트맵 제출](https://searchadvisor.naver.com/guide/request-feed)

## Naver 확인 파일 배포 계약

공식 다운로드 파일 바이트를 그대로 보존한다. 배포 기록 deploy/monipick-search-verification.json은 문서 루트 밖에 두고, 고정된 파일명과 내용 하나만 허용한다. 임의 경로·다른 원점·변형된 내용·미승인 상태를 거부한다. 파일은 sitemap에 추가하지 않고 보호된 preview에도 추가하지 않는다. 운영 빌드 manifest의 files는 전체 62개를 포함하고 search_verification_files는 추가 파일 한 개의 hash를 별도로 기록한다. 원래 approved_content_fingerprint는 추가 파일을 제외한 61개에 계속 적용한다.

## 배포·검증 결과

- 구현 커밋: 85ee23f9b6897768fb6b0f11ce1feb31f79cc787 (codex/monipick-production), 원격 push 완료.
- Cloudflare 운영 배포: e250fc88-bc64-45ab-a739-92229e4e34b3 / 위 SHA / success.
- Cloudflare 빌드 로그: 기존 자산 59개 재사용, 새 파일 1개 업로드. 설정 파일 2개는 업로드 자산과 별도다.
- 확인 파일의 .html 요청은 Pages 기본 동작으로 확장자 없는 동일 경로에 308 후 200 응답한다. 최종 본문은 공식 다운로드 파일과 바이트 일치한다. 인증 우회·스크립트 리다이렉트는 없다. 보안문자 완료 후 Naver의 소유확인 성공과 사이트 관리 접근을 확인했다.
- 자동 운영 배포는 이번 업로드를 위해서만 켰고, 완료 후 Disabled로 복구했다. Preview branch/Access 설정은 변경하지 않았다.
- 기존 공개 파일 61개 승인 fingerprint df71388fbe44404e224592f13096cf862970076366af35fd1bee1eb053723bf0 유지. 사용자 미커밋 변경을 제외한 Git 원본을 임시 폴더에 내보내 검증했다.
- 새 테스트 4개: 정확한 파일·원본 보존·광고/통계 OFF, preview 미포함, 미승인/잘못된 원점/경로/본문 거부, 승인 파일 누락 시 빌드 거부. 변경 전 3개 오류/1개 통과, 구현 후 전체 4개 통과.
- 기존 운영 테스트 7개 포함 관련 테스트 총 11개 통과. 기존 운영 테스트의 fingerprint 비교는 별도 승인된 확인 파일만 제외한 동일 61개에 적용하며, 추가 테스트에서 공식 확인 파일 바이트를 독립 검증한다.
- 깨끗한 Git 원본에서 python3 -m unittest discover -s tests -q: **659개 통과**.
- 실제 운영 URL 60개: 실패 0. 기존 바이트/정상 200/없는 경로 404/HTTPS/CSP/nosniff/frame/referrer/permissions/cache/광고·통계 비활성 확인. 운영 안내의 기존 Cloudflare 이메일 보호 변환만 정규화 비교하는 이전 검증을 유지했다.
- [구현 CI](https://github.com/dineyong/connectable/actions/runs/40054923555): **success**. 전체 Python 및 브라우저·공개 CSP 검사가 통과했다. 문서/증거 후속 커밋은 이 구현 SHA와 별도로 기록한다.

## 최종 확인

- Google 도메인 소유확인 및 사이트맵 처리 완료: 34개 발견.
- Naver 사이트 소유확인 완료 및 사이트맵 접수 완료. [접수 화면](assets/monipick-search-20261024/naver-sitemap.png).
- 입력란의 도메인 표기가 접두어로 보였으나 실제로는 전체 URL을 요구했다. 처음 상대 경로 입력은 형식 오류로 거부됐고 등록되지 않았다. 전체 URL로 수정해 한 번 접수했다.
- 사용자가 추가로 인증할 부분 없음. 별도 방문 통계/광고 활성화, main 병합 없음. 검색 결과 노출까지 완료됐다는 의미는 아니다.
