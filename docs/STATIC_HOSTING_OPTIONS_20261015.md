# 정적 호스팅 후보 조사 · 2026-10-15

상태: 공식 공개 문서 조사와 기술 적합성 검토. 계정 등록·구매·카드 설정·Git 연동·업로드·배포·DNS 변경을 수행하지 않았다. 도메인은 사용자 결정이며 실제 공개는 보류다. 가격·한도·조건은 계약 시 다시 확인한다.

## 기술 후보 비교

| 후보 | 직접 확인한 공식 안내 | 현재 사이트에 대한 판단 |
| --- | --- | --- |
| Cloudflare Pages | [Free 한도](https://developers.cloudflare.com/pages/platform/limits/): 월 500빌드, 사이트 20,000파일, 파일당 25MiB. [미리보기 접근 정책](https://developers.cloudflare.com/pages/configuration/preview-deployments/): 기본 미리보기 URL 공개, Access 설정 가능. preview 보호는 기본 pages.dev와 custom domain을 자동 보호하지 않음 | 단순 HTML/CSS/JS 정적 후보의 우선 기술 검토 대상. 현재 55파일의 초기 후보는 이 파일 수 한도 이하. 플랫폼·계정 약관/상업 사용·실제 비용 승인까지 완료했다는 뜻은 아님 |
| Netlify | [Credit-based plans](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/): Free 월 300credits, hard limit·auto recharge 없음. 문서상 password protection/basic authentication headers는 Pro에 명시 | 대안. 트래픽뿐 아니라 빌드 등 크레딧 사용을 확인해야 함. 무료 플랜의 접근 제한 미리보기 기능을 가정하지 않음. 상업 사용 계약은 별도 최종 확인 |
| Vercel | [Hobby 공식 안내](https://vercel.com/docs/plans/hobby): 개인·비상업 용도로 제한 | 광고·제휴 수익화를 목적으로 한 사이트의 운영을 Hobby 무료 플랜으로 추천하지 않음. 유료 플랜이 필요하면 예산 승인 후 재검토 |

추천은 **정적 파일 유지 + Cloudflare Pages 조건 우선 검토**다. 특정 호스트 확정이나 무료 영구 운영 보장은 아니다. 서버·DB·이미지 변환·공개 반응 집계·API를 첫 출시에서 제외하면 초기 구조를 단순하게 유지할 수 있다.

## 접근 제한과 자동 배포 경계

현재 작업 브랜치를 호스팅 Git 연동에 연결하면 push가 배포를 일으킬 수 있다. 이번에는 GitHub CI까지만 유지하며 호스팅 integration을 만들지 않는다. 공개 전에는 모든 도메인·기본 배포 URL·고유 preview URL·브랜치 별칭을 확인해 인증되지 않은 접근이 차단되는지 검사한다. noindex는 접근 통제가 아니다. preview 정책 하나를 켰다는 이유만으로 production URL도 보호됐다고 보고하지 않는다.

[Cloudflare Serving Pages](https://developers.cloudflare.com/pages/configuration/serving-pages/)는 404.html이 없는 경우 SPA 처리 경로를 설명한다. 존재하지 않는 제품 URL이 정상 페이지 200으로 바뀌지 않도록 실제 호스팅에서 404 상태와 응답을 확인해야 한다. 로컬에 작성한 404.html 템플릿은 호스트의 실제 반환 상태를 보증하지 않는다.

## 도메인 결정 후 실행할 준비

1. 사용자 소유 도메인과 정확한 월 비용 상한 확인. 도메인 구매·갱신 비용, 세금, 환율, 유료 부가 기능은 미정으로 둔다.
2. 후보 호스트의 상업 사용·접근 제한·기본 URL 보호·보안 헤더·404·비용 상한을 계정 조건과 함께 확인한다.
3. 최종 커밋의 별도 미리보기 패키지만 올릴 수 있게 출력 폴더를 지정한다. 저장소 전체나 기존 `web/` 전체를 공개하지 않는다.
4. 접근 제한 확인 후 실제 헤더·404·정적 HTML·자산·모바일 동선을 검수한다.
5. 사용자 최종 공개 승인 전 DNS·색인·광고·자동 production 배포를 활성화하지 않는다.

[최신 준비 기준](FIRST_RELEASE_PREPARATION.md) · [공개 전 인계 체크리스트](PUBLIC_RELEASE_HANDOFF_CHECKLIST.md)
