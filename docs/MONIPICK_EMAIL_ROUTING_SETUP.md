# 모니픽 무료 운영 이메일 연결 준비

기준일: 2026-10-22. 작업 브랜치 `codex/monipick-cloudflare-preparation`.

## 실제 연결 후속 결과 · 2026-10-22

이 절이 아래 준비 당시 기록보다 최신이다. 사용자 지정 Gmail이 Cloudflare에서 이미 Verified였으므로 인증 요청을 중복 발송하지 않았다. 전달 대상의 실제 개인 주소는 공개 저장소에 저장하지 않는다.

- monipick.com의 Email Routing Activate를 수행해 메일용 MX 3개·SPF/DKIM TXT를 적용했다. 공개 DNS에서도 MX 3개와 SPF/DKIM 존재를 확인했다. 웹사이트용 DNS/Custom domain·Pages production·Access·색인·유료 플랜은 변경하지 않았다.
- `contact@monipick.com` → 사용자 지정 인증 Gmail 규칙 한 개를 저장하고 **Active**를 확인했다. Catch-all은 Disabled 유지다. 도메인 Overview는 확인 시 Syncing 표시였으므로 규칙 Active와 동기화 표시를 혼동하지 않는다.
- 연결된 Gmail에서 수신 주소로 테스트 메일 한 건을 발송했다. 확인 번호는 `MP-20261023-001`이며 번호의 날짜 문자열은 실제 발송일의 근거로 쓰지 않는다. 실제 발송은 2026-10-22 14:36:57 UTC다.
- 테스트 원문은 Gmail에서 SENT로만 확인됐고, 별도로 Cloudflare의 Gmail 중복 처리 안내 메일이 **INBOX에 도착**했다. 원문을 받은 것으로 대신 처리하지 않는다. 이 안내는 같은 계정에서 보낸 메일은 Gmail이 중복으로 숨길 수 있으므로 다른 발신 계정으로 시험하도록 설명한다.
- Cloudflare Activity log에서 해당 고유 제목의 원래 테스트 건이 `Forwarded`로 처리된 것을 추가 확인했다. 이는 전달 처리 증거이며 원문이 Gmail INBOX에 별도로 표시됐다는 증거와는 다르다.
- 사용자에게 다른 이메일에서 ‘모니픽 외부 수신 테스트’ 제목으로 보내도록 요청했다. 외부 테스트 원문·전달 로그 확인 전까지 `ROUTING_CONFIGURED_DELIVERY_TEST_PENDING` 및 공개 보류를 유지한다. 단순 발송 성공이나 DNS 등록을 실제 원문 수신 완료로 승격하지 않는다.
- 관련 Python 17개·내부 경로 검증 및 운영 안내 브라우저 회귀를 실행한다. 새 토큰·Workers·유료 발송 기능을 만들지 않았다. 원본 데이터와 사용자 변경은 보존한다.

## 아래 내용은 연결 전 준비 이력

## 확정과 대기 상태

- 사용자 확정 운영 주소: **contact@monipick.com**.
- 사용자가 별도 운영 Gmail을 만들 예정이다. 전달 대상 주소는 미제공이며 기존 계정 이메일을 임의 재사용하지 않았다.
- 주소 선택과 수신 개통을 분리했다. 공개 준비 manifest의 contact_email은 확정 주소, contact_delivery_status는 `PENDING_DESTINATION_VERIFICATION`, 공개 전 조건은 `CONTACT_ROUTING_PENDING` 및 `FINAL_PUBLICATION_APPROVAL_PENDING`이다.
- 사이트 안내에는 운영 주소와 연결 준비 중 상태를 표시하며 mailto/접수 폼을 아직 제공하지 않는다. 수신 성공·문의 접수 시작·실제 공개로 표시하지 않는다.

## Cloudflare에서 직접 확인한 상태

- monipick.com 도메인과 Free 표시를 확인했다. 다른 도메인 설정은 변경하지 않았다.
- Email Routing 목록에 monipick.com이 아직 등록돼 있지 않았고 공개 DNS 조회에서도 MX 응답이 없었다. 이 조회만으로 전파 상태나 향후 수신 성공을 보장하지 않는다.
- Email → Email Routing → Onboard Domain에서 monipick.com을 선택하고 **Verify DNS records** 화면까지 이동했다.
- 화면에는 route1/route2/route3.mx.cloudflare.net 대상 MX 3개와 SPF/DKIM TXT 2개 추가안이 표시됐다. 현재 우선순위/인증 키를 임의 하드코딩하지 않고 실제 활성화 시 화면 값을 사용한다.
- 최종 **Activate는 누르지 않았다.** Gmail 미제공 상태에서 메일 라우팅·MX/TXT를 활성화하거나, 잘못된 전달 대상·catch-all·폐기 규칙을 만들지 않았다. DNS 레코드 생성·메일 발송·대상 주소 인증·수신 시험은 미실행이다.
- 사이트 DNS/Custom domain·Pages production·Access·색인·광고·유료 플랜·Workers·토큰·권한은 변경하지 않았다. 현재 설정 탭은 재개용으로 유지했다.

## Gmail을 받은 뒤 순서

1. 사용자가 운영 Gmail 주소를 알려준다. 비밀번호나 인증 코드를 채팅에 보내지 않는다.
2. Cloudflare에 전달 대상 주소를 등록한다. 사용자가 해당 Gmail에서 Cloudflare 인증 메일을 열어 인증을 완료한다. 인증 완료 전 수신 가능으로 표시하지 않는다.
3. 도메인 온보딩/DNS 변경안을 다시 확인하고 메일용 레코드만 적용한다. 기존 MX/SPF가 새로 생겼다면 덮어쓰지 않고 충돌을 먼저 검토한다. 화면 흐름에 따라 도메인 활성화와 대상 인증 순서는 달라질 수 있으나 최종 규칙은 인증된 대상만 사용한다.
4. `contact` → 해당 인증된 Gmail로 전달하는 규칙 한 개만 만든다. catch-all은 기본 비활성 방향이며 다른 도메인의 규칙을 건드리지 않는다.
5. 전달 대상 Gmail과 다른 발신 계정으로 테스트 메일을 보내고 실제 수신/스팸함을 확인한다. 메일 전송은 사용자 지시 범위에서 수행하며 임의로 다른 사람에게 보내지 않는다.
6. 성공을 확인한 뒤에만 수신 상태·사이트 안내·공개 준비 조건을 갱신한다. 웹사이트 공개는 별도 최종 승인까지 보류한다.

## 무료 범위와 발신 한계

Cloudflare Email Routing의 무료 전달을 사용한다. 별도 Email Workers 처리·유료 발송 기능은 설정하지 않는다. 도메인 주소로 일반 사용자에게 답장하는 기능은 이번 수신 전달 설정과 다르며 구현하지 않는다. Gmail로 일반 답장할 경우 Gmail 주소가 상대에게 표시될 수 있음을 운영자가 확인해야 한다.

[공식 연결 절차](https://developers.cloudflare.com/email-service/get-started/route-emails/) · [공식 무료/유료 범위](https://developers.cloudflare.com/email-service/platform/pricing/)

## 코드 검증과 Git

확정 주소가 수신 완료로 자동 승격되지 않도록 준비 생성기와 테스트를 갱신했다. 관련 Python 17개·데스크톱/모바일 브라우저 4개 및 기존 내부 경로 검사를 통과했다. 기존 data/schema·미확인 사양·사용자 변경은 보존한다. GitHub CI 결과는 본 커밋의 checks를 기준으로 확인하며 완료 응답에 실제 실행 URL을 기록한다. 사이트 실제 공개와 기존 비공개 검수 배포 갱신은 하지 않는다.
