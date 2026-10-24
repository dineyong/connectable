# 모니픽 나머지 모니터 설명 보강 — 2026-10-24

## 범위 및 공개 경계

- 기준: `codex/monipick-production`의 `cc2f4f7`(운영 코드 `5bf48c9`). 작업 브랜치: `codex/monipick-summary-expansion`.
- 나머지 27종에 설명·메타 설명을 추가한 **별도 검토 후보**다. 기존 3종과 합쳐 30종이다.
- 승인된 흰색 설명 블록을 사용한다. 원본 사양·후기·필터·비교 기능은 변경하지 않았다.
- 기존에 검증한 공식 기록을 재사용했다. 제조사 페이지를 이번에 새로 직접 확인했다고 기록하거나 확인일을 갱신하지 않았다.
- 값·단위·qualifier·scope·출처와 모델/지역/variant 상태를 설명에 연결한다. 미확인·충돌을 해소한 것으로 취급하지 않는다.
- 실제 운영 배포·공개 승인 fingerprint·Cloudflare 설정·main은 변경하지 않는다. 운영본은 기존 3종 설명이며 확장 후보는 30종이다. 광고·통계 비활성 유지.

## 보강 내용과 근거

모든 모델에 화면·패널, 주사율 표기 종류, 모델별 포트/기능 설명을 제공한다. 최대 주사율은 모든 입력의 동일한 출력이나 동시 사용을 보장하지 않는다. 문장 아래 공식 출처와 **기존 확인일**을 표시하며 새 창으로 연결한다.

한국 SKU 동일성·입력별 동시 사용 조건·실물 연결 결과는 27종 모두 미확인 상태다. 아래 링크는 기존에 기록된 공식 근거이며 현재 재접속 성공을 주장하지 않는다.

| 모델 | 문서 지역 | 핵심 설명 / 남겨둔 제한 | 공식 자료 · 기존 확인일 |
|---|---|---|---|
| ASUS VG27AQ | US | HDMI 2.0 2개와 DisplayPort 1.2 1개가 기록돼 있습니다. 입력 포트가 다르면 가능한 영상 조건도 따로 확인하세요. | [2026-10-10](https://www.asus.com/us/displays-desktops/monitors/tuf-gaming/tuf-gaming-vg27aq/techspec/) |
| ASUS XG27AQDMG | US | DisplayPort 1.4의 DSC 표기와 HDMI 2.0 2개가 기록돼 있습니다. DSC 표기를 연결 기기의 실제 협상 성공으로 해석하지 않습니다. | [2026-10-10](https://rog.asus.com/us/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/spec/)<br>[2026-10-11](https://rog.asus.com/us/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/) |
| ASUS PG32UCDM | US | USB-C DP Alt Mode, PD 공급 전력 90W와 KVM 지원이 표기돼 있습니다. 실제 충전량이나 모든 기기에서의 KVM 동작을 보장하는 값은 아닙니다. | [2026-10-10](https://rog.asus.com/us/monitors/27-to-31-5-inches/rog-swift-oled-pg32ucdm/spec/)<br>[2026-10-11](https://rog.asus.com/us/monitors/27-to-31-5-inches/rog-swift-oled-pg32ucdm/) |
| ASUS PA278QV | SG | 스탠드는 높이 150mm 조절과 피벗이 표기돼 있습니다. HDMI 1.4와 DisplayPort 1.2가 기록돼 있으며 USB-C 지원은 미확인입니다. | [2026-10-10](https://www.asus.com/sg/displays-desktops/monitors/proart/proart-display-pa278qv/techspec/) |
| ASUS PA248QV | US | 스탠드 높이 130mm 조절과 피벗, HDMI 1.4·DisplayPort 1.2 입력이 기록돼 있습니다. USB-C 지원은 미확인입니다. | [2026-10-10](https://www.asus.com/us/displays-desktops/monitors/proart/proart-display-pa248qv/techspec/) |
| ASUS VA24EHF | Global | HDMI 1.4 1개가 기록돼 있습니다. 스탠드의 높이 조절은 지원하지 않는 것으로 명시돼 있어 기울기 조절과 구분해야 합니다. | [2026-10-10](https://www.asus.com/displays-desktops/monitors/eye-care/va24ehf/techspec/) |
| BenQ PD2705U | CA | USB-C 업스트림에 DP Alt Mode·데이터 기능과 PD 공급 전력 65W가 표기돼 있습니다. KVM 지원도 기록돼 있지만 실제 조합별 동작은 따로 확인해야 합니다. | [2026-10-10](https://www.benq.com/en-ca/monitor/creative-pro/pd2705u/spec.html) |
| BenQ PD2725U | CA | Thunderbolt 3 업스트림·다운스트림 각 1개가 기록돼 있습니다. PD 65W는 업스트림 기준이며 다운스트림의 15W 표기와 구분합니다. | [2026-10-10](https://www.benq.com/en-ca/monitor/creative-pro/pd2725u/spec.html) |
| BenQ EX2710Q | CA | HDMI 2.0 2개와 DisplayPort 1.4 입력 1개가 기록돼 있습니다. HDR10·DisplayHDR400 표기는 실제 HDR 화질의 실측 평가가 아닙니다. | [2026-10-10](https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html) |
| BenQ GW2790QT | CA | USB-C 업스트림에 DP Alt Mode·데이터 기능과 PD 공급 전력 65W가 표기돼 있습니다. 실제 충전 여부는 연결 기기와 케이블 조건도 확인해야 합니다. | [2026-10-10](https://www.benq.com/en-ca/monitor/home/gw2790qt/spec.html) |
| BenQ GW2490 | US | HDMI 1.4 2개와 DisplayPort 1.2 입력 1개가 기록돼 있습니다. USB-C와 PD 공급 지원 여부는 아직 확인하지 못했습니다. | [2026-10-10](https://www.benq.com/en-us/monitor/home/gw2490/spec.html) |
| LG 27GP850-B | ES | HDMI 2.0 2개와 DisplayPort 1.4 1개가 기록돼 있습니다. USB-C는 공식 기록에서 미지원으로 명시돼 있으며 단순 미확인과 구분합니다. | [2026-10-10](https://www.lg.com/es/monitores/monitores-ultragear-gaming/27gp850-b/)<br>[2026-10-11](https://www.lg.com/es/monitores/monitores-ultragear-gaming/27gp850-b/) |
| LG 27GR83Q-B | GB | DisplayPort 1.4의 DSC 표기와 HDMI 2개가 기록돼 있습니다. HDMI 버전은 미확인이므로 포트 수만으로 규격이나 가능한 주사율을 판단하지 않습니다. | [2026-10-10](https://www.lg.com/uk/monitors/gaming/27gr83q-b/) |
| LG 27GS95QE-B | GB | HDMI 2.1과 DSC가 표기된 DisplayPort 1.4 입력이 기록돼 있습니다. HDMI 포트 수는 미확인으로 남겨두고, HDR 표기를 실측 성능으로 바꾸지 않습니다. | [2026-10-10](https://www.lg.com/uk/monitors/gaming/27gs95qe-b/) |
| LG 32GS95UE-B | CA | 듀얼 모드는 3840×2160 최대 240Hz와 1920×1080 최대 480Hz의 대안 모드로 기록돼 있습니다. 4K 480Hz나 두 모드의 동시 출력으로 합치지 않습니다. | [2026-10-10](https://www.lg.com/ca_en/monitors/gaming/32gs95ue-b/) |
| LG 27UP850K-W | GB | DisplayPort 1.4 1개와 HDMI 2개가 기록돼 있습니다. HDMI 버전은 미확인이며 PD 전력은 공식 표기 충돌이 남아 있어 이 요약에서 확정하지 않습니다. | [2026-10-10](https://www.lg.com/uk/monitors/uhd-4k-5k/27up850k-w/) |
| LG 34WQ75C-B.AUS | US | KVM 지원과 USB-C의 데이터 기능이 기록돼 있습니다. USB-C 데이터 표기만으로 영상 모드를 확정하지 않으며, HDMI·DisplayPort 버전도 미확인입니다. | [2026-10-10](https://www.lg.com/us/support/products/documents/34WQ75C_Spec_Sheet.pdf) |
| MSI MAG 274QRF QD E2 | Global | USB-C DP alt, PD 공급 전력 65W와 KVM 지원이 표기돼 있습니다. 색역·포장 중량의 공식 표기 충돌은 별도 안내에 유지합니다. | [2026-10-10](https://www.msi.com/Monitor/MAG-274QRF-QD-E2/Specification)<br>[2026-10-11](https://www.msi.com/Monitor/MAG-274QRF-QD-E2) |
| MSI MPG 321URX QD-OLED | Global | USB-C DP alt, PD 공급 전력 90W와 KVM 지원이 표기돼 있습니다. HDMI 2.1 2개도 기록돼 있지만 모든 연결의 동시 동작을 보장하지 않습니다. | [2026-10-10](https://www.msi.com/Monitor/MPG-321URX-QD-OLED/Specification)<br>[2026-10-11](https://www.msi.com/Monitor/MPG-321URX-QD-OLED) |
| Gigabyte M27Q rev.1.0 | Global | 기록된 제품은 M27Q rev.1.0입니다. KVM 지원과 USB-C 1개가 기록돼 있지만 USB-C 영상 모드·PD 공급 전력은 미확인입니다. 다른 리비전으로 사양을 옮기지 않습니다. | [2026-10-10](https://www.gigabyte.com/Monitor/M27Q-rev-10/sp) |
| Gigabyte M28U | Global | HDMI 2.1 2개, DSC가 표기된 DisplayPort 1.4 1개와 KVM 지원이 기록돼 있습니다. USB-C 영상 모드·PD 공급 전력은 미확인입니다. | [2026-10-10](https://www.gigabyte.com/Monitor/M28U/sp) |
| Gigabyte M32U | Global | HDMI 2.1 2개, DSC가 표기된 DisplayPort 1.4 1개와 KVM 지원이 기록돼 있습니다. USB-C 영상 모드·PD 공급 전력은 미확인입니다. | [2026-10-10](https://www.gigabyte.com/Monitor/M32U/sp) |
| AOC Q27G3XMN | US | 로컬 디밍 336개 구역과 DisplayHDR1000 표기가 기록돼 있습니다. 구역 수나 인증 표기만으로 실제 HDR 화질을 평가하지 않습니다. | [2026-10-10](https://www.aoc.com/us/gaming/monitors/q27g3xmn) |
| Samsung S32CG554EU (LS32CG554EUXEN) | DE | 기록된 지역 모델은 LS32CG554EUXEN입니다. DisplayPort 1.2 1개가 있으며 USB-C는 공식 기록에서 미지원입니다. HDMI 버전은 미확인입니다. | [2026-10-10](https://images.samsung.com/is/content/samsung/assets/de/display/pdf/Datenblatt_Monitor_LS32CG554EUXEN.pdf) |
| Samsung S65UC (LS34C650UEEXXY) | AU | 기록된 지역 모델은 LS34C650UEEXXY입니다. KVM과 PD 공급 전력 90W가 표기돼 있으나 USB-C 영상 모드는 미확인입니다. 한국 판매 SKU로 동일시하지 않습니다. | [2026-10-10](https://www.samsung.com/au/monitors/high-resolution/viewfinity-s6-s65uc-34-inch-ultra-wqhd-ls34c650ueexxy/) |
| Dell U2724D | US | USB-C 업스트림은 데이터 전용입니다. HDMI의 2.1 표기에는 TMDS 조건이 함께 기록돼 있어 FRL 지원으로 확장 해석하지 않습니다. | [2026-10-10](https://www.dell.com/en-us/shop/dell-ultrasharp-27-monitor-u2724d/apd/210-bksf/monitors-monitor-accessories) |
| Dell AW3225QF | US | HDMI 2.1 2개에 FRL·eARC 1개가, DisplayPort 1.4에는 DSC가 표기돼 있습니다. USB-C는 다운스트림 표기이며 노트북 영상 입력으로 해석하지 않습니다. | [2026-10-10](https://www.dell.com/en-us/shop/alienware-32-4k-qd-oled-gaming-monitor-aw3225qf/apd/210-blmq/computer-monitors) |

## 보존한 구분

- BenQ PD2725U: 업스트림 PD 65W와 다운스트림 15W를 분리한다.
- LG 32GS95UE-B: 4K 240Hz / FHD 480Hz는 대안 모드다. 4K 480Hz나 동시 출력으로 합치지 않는다.
- LG 27UP850K-W: 90W/96W 충돌을 유지하며 요약에 확정 PD claim을 만들지 않는다. 원래 사양표·충돌 안내는 보존한다.
- MSI MAG 274QRF QD E2: 색역·포장 중량 충돌을 남긴다.
- Dell U2724D: USB-C 데이터 전용, HDMI TMDS를 FRL 지원으로 확대하지 않는다. AW3225QF의 USB-C 다운스트림도 영상 입력으로 바꾸지 않는다.
- Gigabyte 리비전, Samsung 지역 SKU, 해외 공식 문서 지역을 유지한다. USB-C 미지원과 미확인도 구분한다.

## 구현 및 검증 구조

- `data/editorial/monitor-summary-expansion.json`: 27종의 편집 문장·사실·출처·미확인·충돌·제품 식별 상태 바인딩.
- `scripts/prepare_monipick_summary_expansion.py`: 기존 3종 후보 위에 27종만 추가한다. manifest는 공개·배포·색인·광고·통계 권한을 부여하지 않는다.
- 공유 렌더러는 입력 파일 지정과 확장 바인딩을 지원한다. 기본 3종 출력은 바이트 그대로 보존한다.
- 값·단위·qualifier·scope·출처, 제품/지역/variant, 충돌/미확인 변경과 후보 변조·추가 파일·symlink·승인 플래그 변경을 거부하는지 검사한다.
- 브라우저에서 30종 설명, 출처 날짜·새 창, 원래 사양표, 모바일 가로 넘침, 충돌/지역/대안 모드 페이지 접근성을 검사한다.
- 초기 브라우저 2건은 테스트가 내부 영문 `CONFLICT`를 기대해 실패했다. 기존 한국어 “충돌이 해소된 것으로 해석하지 마세요”를 검사하도록 수정했다. 데이터나 경고는 바꾸지 않았다.
- 병렬로 실행한 서로 다른 Playwright 설정이 같은 결과 폴더를 정리하여 trace 파일 ENOENT가 확장 검사 2건·기존 검사 4건에서 발생했다. 두 검사 모두 결과 폴더를 별도로 지정해 재실행했다. CI의 테스트 단계는 순차 실행한다.

## 실행 결과

| 검사 | 결과 |
|---|---|
| `python3 -m unittest discover -s tests -q` | **679 통과**, 174.513초. 기존 670 + 신규 9 |
| `npm run test:e2e -- --workers=2 --output /tmp/monipick-original-test-results` | **212 통과** |
| `npx playwright test --config playwright.release.config.js --workers=2` | **10 통과** |
| `npx playwright test --config playwright.content.config.js --workers=2 --output /tmp/monipick-content-test-results` | **14 통과** |
| `npx playwright test --config playwright.summary.config.js --workers=2 --output /tmp/monipick-summary-test-results` | **18 통과** (기존 14를 확장 후보에서 재검증 + 신규 4) |
| 공식 모니터 검증, v3 생성·제품 문서 `--check` | 통과, 30종 |
| 승인된 운영 빌드 재생성 | 통과, 기존 fingerprint 유지. 업로드 없음 |
| 확장 후보 manifest·전체 파일 hash·승인 보류 | 통과 |
| 원본 `data/research`, `data/official`, `schemas`, `web`, `deploy` diff | 변경 없음 |
| 신규 편집·코드·보고서의 개인정보/비밀값 패턴 | 발견 없음 (패턴 검사 한계 있음) |
| README/신규 보고서 내부 문서 경로와 `git diff --check` | 통과 |

브라우저 합계 254회 실행이다. 서로 다른 후보에서 기존 동작을 반복 확인한 수치로, 고유 기능 수를 뜻하지 않는다. 실행 로그 중 `FAIL: stale/missing derived files`는 기존 음성 테스트의 의도된 출력이며 전체 Python 결과는 OK다. 테스트가 생성한 기존 스크린샷 2개는 원래 바이트로 복원하여 커밋하지 않았다.

화면은 1440px 데스크톱과 390px 모바일에서 직접 캡처하여 확인했다. 설명 블록 배경은 흰색, padding은 각각 24px/18px이고 가로 넘침이 없었다.

이전 운영 코드 `5bf48c9`의 CI [40060034062](https://github.com/dineyong/connectable/actions/runs/40060034062)는 성공 상태임을 확인했다. 이번 브랜치 원격 CI는 push 후 별도 기록한다.

## 로컬 검토

```sh
python3 -m scripts.serve_monipick_summary_expansion --port 8898
```

검토 URL: <http://127.0.0.1:8898/monitors/lg-32gs95ue-b/>. 루프백 검토본이며 Cloudflare 운영 배포가 아니다.

## 남은 위험

- 자연어 문장의 모든 의미를 기계적으로 증명하지는 않는다. 편집 검토와 공식 근거 확인이 계속 필요하다.
- 기존 확인일 이후 제조사 문서가 바뀌었을 수 있다. 이번 작업은 새 공식 조사나 한국 판매 SKU 확인 완료를 의미하지 않는다.
- 원본 사양표의 제한/충돌은 그대로 노출한다. 설명이 추가됐다고 호환성·화질·충전 실측을 승인하지 않는다.
- 이 브랜치를 운영 브랜치에 그대로 fast-forward해도 기존 배포 빌더는 승인된 3종을 출력한다. 27종 공개는 후보 검토·fingerprint 승인과 배포 검증이 별도로 필요하다.

## 관련 문서

- [기존 3종 설명 보강](MONIPICK_CONTENT_POLISH_REPORT_20261024.md)
- [기존 운영 배포 검증](MONIPICK_CONTENT_RELEASE_REPORT_20261024.md)
- [공식 기록 원본](../data/research/monitor-expansion/official_specs.json)
- [27종 편집 원본](../data/editorial/monitor-summary-expansion.json)
