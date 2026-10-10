# 공식 모니터 사양 확대 조사

확인일: 2026-10-10. 상태: 내부 연구 / public_status UNKNOWN. 기준: README, PRODUCT_DIRECTION_V3.md, MONITOR_COMPARISON_V3_ROADMAP.md 및 이번 공식 조사 위임.

목표30종 중 **30종, 제조사8곳, 제품별 공식 원문30개, 근거별 fact 637개**를 확보했다. 30종의 모든 필드가 완성됐다는 뜻은 아니다. 검색 결과는 문서 탐색에만 사용했고, 저장 사실은 직접 열어 확인한 공식 제품 사양 또는 제조사 PDF에서 추출했다. 원문 전체, 리뷰 작성자, 닉네임, 개인 연락처는 저장하지 않았다. 공개 배포·한국 SKU 승인·물리 테스트·추천 순위는 수행하지 않았다.

기존6종 중 모델 수준 재확인은 MSI MD271UL→공식 표기 Modern MD271UL **1종**이다. 해당 기록은 origin=EXISTING_MODEL_NEW_DIRECT_CHECK이며 모든 값은 이번 직접 확인에서 새로 작성했다. 기존 사실의 단순 재사용은0종, 기존 목록에 없던 모델29종이다. 27UP850K-W는 기존27UP850-W와 자동 동치가 아니다. 기존 data/official과 data/site 파일은 수정하지 않았다.

## 값과 범위 해석

- width/height는 패널의 기본 픽셀 해상도다. active_area는 실표시 영역mm이며 dimensions는 케이스/스탠드 크기다. 객체에 축 이름·단위·스탠드 유무를 명시했다.
- 입력 개수/버전은 hdmi/displayport/usb_c 객체로, 포트별 프로파일은 input_profile 및 scope로 분리했다. scan frequency는 input_vertical_frequency이며 특정 해상도 타이밍 검증과 다르다.
- response 문자열은 GtG, MPRT, Faster 등을 보존한다. 서로 다른 측정법의 단순 성능 순위로 사용하지 않는다. 색역%는 원문 표기와 표준을 보존하고, 면적·채도 값을 커버리지로 재해석하지 않는다.
- 공급 PD, 다운스트림 충전, 모니터 소비전력, 외장 어댑터 DC 출력을 합치지 않았다. 공급 전력은 실제 노트북 충전 관측이 아니다.
- missing_fields는 조사 범위에서 확보하지 못한 필드이며 미지원이 아니다. 객체 내부 null도 결측 목록에 별도 기록했다. 명시적 No/대시는 문맥상 미지원으로 확인된 경우만 false로 기록했다.
- EXACT_DOCUMENT_MODEL은 문서에 적힌 모델 일치다. 한국 SKU 동일성은 전부 UNKNOWN이다. 해외 보증은 해당 국가 범위이고 한국 보증으로 사용하지 않는다.
- typical/native 표기는 정격(rated)의 뜻이 아니므로 밝기·대비 51개 fact의 qualifier를 MANUFACTURER_STATED로 보존했다. 이번 배치 RATED 사실은0개다.
- ASUS/Gigabyte 치수·무게 Esti.는 객체 estimate_status=MANUFACTURER_ESTIMATE로 표시했다. 제조사가 제공한 추정 수치이며 조사자가 계산한 추정치는0개다. 다른 제조사 값은 manufacturer figures로 유지하고 정격·계산값으로 승격하지 않았다.
- 스탠드·무게·포트 및 일부 기본 사양의 문서 오류 가능성이 남는다. 의심 항목은 주석과 결측으로 분리했다. 화면용 파생 전 사람이 원문을 재검토해야 한다.

## 모델별 coverage와 공식 URL

사실 수는 필드/범위별 레코드 수이며 독립 문서 수나 사람 검토 수가 아니다. 아래 결측에 추가로 모든 모델의 한국 SKU·한국 보증·동시 입력 조건·물리 테스트가 미확인이다.

| 제조사 / 정확한 문서 모델 | 지역 | fact 수 | 모델별 미확보 필드 | 직접 확인 원문 |
|---|---|---:|---|---|
| ASUS PA279CRV | US | 26 | kvm | [공식 문서](https://www.asus.com/us/displays-desktops/monitors/proart/proart-display-pa279crv/techspec/) |
| ASUS VG27AQ | US | 21 | usb_c, pd_supply, usb_hub, kvm, pip, pbp, warranty | [공식 문서](https://www.asus.com/us/displays-desktops/monitors/tuf-gaming/tuf-gaming-vg27aq/techspec/) |
| ASUS XG27AQDMG | US | 17 | size, refresh, brightness_typical, contrast_native, response, color_gamut, usb_c, pd_supply, kvm, pip, pbp | [공식 문서](https://rog.asus.com/us/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/spec/) |
| ASUS PG32UCDM | US | 19 | panel, refresh, brightness_typical, contrast_native, response, color_gamut, kvm, pip, pbp | [공식 문서](https://rog.asus.com/us/monitors/27-to-31-5-inches/rog-swift-oled-pg32ucdm/spec/) |
| ASUS PA278QV | SG | 19 | hdr, usb_c, pd_supply, kvm, pip, pbp | [공식 문서](https://www.asus.com/sg/displays-desktops/monitors/proart/proart-display-pa278qv/techspec/) |
| ASUS PA248QV | US | 19 | hdr, usb_c, pd_supply, kvm, pip, pbp | [공식 문서](https://www.asus.com/us/displays-desktops/monitors/proart/proart-display-pa248qv/techspec/) |
| ASUS VA24EHF | Global | 16 | color_gamut, hdr, displayport, usb_c, pd_supply, usb_hub, kvm, pip, pbp, warranty | [공식 문서](https://www.asus.com/displays-desktops/monitors/eye-care/va24ehf/techspec/) |
| BenQ PD2705U | CA | 25 | vrr, warranty | [공식 문서](https://www.benq.com/en-ca/monitor/creative-pro/pd2705u/spec.html) |
| BenQ PD2725U | CA | 25 | usb_c, vrr, warranty | [공식 문서](https://www.benq.com/en-ca/monitor/creative-pro/pd2725u/spec.html) |
| BenQ EX2710Q | CA | 21 | usb_c, pd_supply, kvm, pip, pbp, warranty | [공식 문서](https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html) |
| BenQ GW2790QT | CA | 22 | hdr, kvm, pip, pbp, vrr, warranty | [공식 문서](https://www.benq.com/en-ca/monitor/home/gw2790qt/spec.html) |
| BenQ GW2490 | US | 17 | hdr, usb_c, pd_supply, usb_hub, kvm, pip, pbp, vrr, warranty | [공식 문서](https://www.benq.com/en-us/monitor/home/gw2490/spec.html) |
| LG 27GP850-B | ES | 14 | hdr, usb_c, pd_supply, usb_hub, kvm, pip, pbp, stand, vesa, dimensions, weight, warranty, hdmi.version, displayport.version | [공식 문서](https://www.lg.com/es/monitores/monitores-ultragear-gaming/27gp850-b/) |
| LG 27GR83Q-B | GB | 15 | brightness_typical, usb_c, pd_supply, power_consumption, kvm, pip, pbp, vesa, dimensions, warranty, hdmi.version | [공식 문서](https://www.lg.com/uk/monitors/gaming/27gr83q-b/) |
| LG 27GS95QE-B | GB | 18 | usb_c, pd_supply, power_consumption, kvm, pip, pbp, warranty, hdmi.count | [공식 문서](https://www.lg.com/uk/monitors/gaming/27gs95qe-b/) |
| LG 32GS95UE-B | CA | 19 | usb_c, pd_supply, power_consumption, kvm, pip, pbp, warranty, hdmi.version | [공식 문서](https://www.lg.com/ca_en/monitors/gaming/32gs95ue-b/) |
| LG 27UP850K-W | GB | 20 | power_consumption, kvm, pip, pbp, vrr, warranty, hdmi.version | [공식 문서](https://www.lg.com/uk/monitors/uhd-4k-5k/27up850k-w/) |
| LG 34WQ75C-B.AUS | US | 25 | pip, vrr, hdmi.version, displayport.version | [공식 문서](https://www.lg.com/us/support/products/documents/34WQ75C_Spec_Sheet.pdf) |
| MSI Modern MD271UL | Global | 19 | brightness_typical, hdr, power_consumption, usb_hub, kvm, pip, pbp, vrr, vesa, warranty | [공식 문서](https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL/Specification) |
| MSI MAG 274QRF QD E2 | Global | 26 | power_consumption, kvm, warranty | [공식 문서](https://www.msi.com/Monitor/MAG-274QRF-QD-E2/Specification) |
| MSI MPG 321URX QD-OLED | Global | 25 | power_consumption, kvm, pip, pbp | [공식 문서](https://www.msi.com/Monitor/MPG-321URX-QD-OLED/Specification) |
| Gigabyte M27Q rev.1.0 | Global | 22 | pd_supply, vrr, warranty, usb_c.video_mode | [공식 문서](https://www.gigabyte.com/Monitor/M27Q-rev-10/sp) |
| Gigabyte M28U | Global | 22 | pd_supply, pip, pbp, vrr, warranty, usb_c.video_mode | [공식 문서](https://www.gigabyte.com/Monitor/M28U/sp) |
| Gigabyte M32U | Global | 24 | pd_supply, vrr, warranty, usb_c.video_mode | [공식 문서](https://www.gigabyte.com/Monitor/M32U/sp) |
| AOC Q27G3XMN | US | 18 | brightness_typical, usb_c, pd_supply, usb_hub, kvm, pip, pbp, dimensions, warranty | [공식 문서](https://www.aoc.com/us/gaming/monitors/q27g3xmn) |
| Samsung S32CG554EU (LS32CG554EUXEN) | DE | 23 | color_gamut, pd_supply, kvm, hdmi.version | [공식 문서](https://images.samsung.com/is/content/samsung/assets/de/display/pdf/Datenblatt_Monitor_LS32CG554EUXEN.pdf) |
| Samsung S65UC (LS34C650UEEXXY) | AU | 26 | color_gamut, warranty, usb_c.video_mode | [공식 문서](https://www.samsung.com/au/monitors/high-resolution/viewfinity-s6-s65uc-34-inch-ultra-wqhd-ls34c650ueexxy/) |
| Dell U2724D | US | 22 | kvm, vrr, dimensions, weight, warranty | [공식 문서](https://www.dell.com/en-us/shop/dell-ultrasharp-27-monitor-u2724d/apd/210-bksf/monitors-monitor-accessories) |
| Dell U2724DE | US | 28 | vrr | [공식 문서](https://www.dell.com/en-us/shop/dell-ultrasharp-27-thunderbolt-hub-monitor-u2724de/apd/210-bksj/monitors-monitor-accessories) |
| Dell AW3225QF | US | 24 | brightness_typical, contrast_native, pd_supply, kvm, pip, pbp, weight | [공식 문서](https://www.dell.com/en-us/shop/alienware-32-4k-qd-oled-gaming-monitor-aw3225qf/apd/210-blmq/computer-monitors) |

## 보존한 조건과 의심 항목

- ASUS VG27AQ: 패널165Hz, HDMI 수직 입력 범위 최대144Hz. XG27AQDMG는 DP40–240Hz와 HDMI40–144Hz 범위만 확보해 패널 주사율 필드를 추측으로 채우지 않았다.
- ASUS PG32UCDM: 원문 추출에서 패널 종류·일반 밝기·기본 대비·응답 시간·패널 주사율 행이 빠졌다. DP/USB-C 수평 범위510~501kHz는 역전된 표기여서 정규화하지 않았다. 최대 HDR1000과 Dolby Vision, 포트·PD·보증은 별도로 확보했다.
- MSI MAG274QRF QD E2: DP/USB-C QHD180Hz, HDMI QHD144Hz. MPG321URX는 포트별 UHD240Hz, USB-C PD90W. KVM을 이번 spec에서 찾지 못해 기능을 추정하지 않았다.
- Gigabyte M28U/M32U: HDMI UHD144Hz의4:4:4는 DSC 조건, 대안은4:2:0이다. PS5/Xbox SeriesX의 UHD120Hz4:2:0 각주를 유지했다. M27Q는 rev.1.0만 조사했다.
- Samsung S65UC: PBP에서100Hz 사용 불가. sRGB Coverage1.15는 단위 해석 불명확해 색역 수치로 채우지 않았다. HAS PIVOT이라는 스탠드 이름만으로 피벗 범위를 만들지 않았다.
- Dell U2724D: 요약 RJ45 Yes와 상세 포트 목록이 불일치해 LAN 기능을 저장하지 않았다. U2724DE의 영상 TB4 upstream90W, TB4 downstream15W, USB-C downstream15W는 각각 다른 출력이다. USB-C data-only upstream을 영상 포트로 취급하지 않았다.
- Dell AW3225QF: USB-C는 downstream/BC1.2이며 USB-C 영상 입력이나 노트북 PD 근거가 아니다.1000nit 밝기는 표기 조건이 없어 typical로 바꾸지 않았고, dynamic contrast를 native contrast로 바꾸지 않았다.
- AOC Q27G3XMN: 미국 공식 페이지 HDMI1개 표기를 유지했다. 크기 WxHxD 라벨과 실제 나열 순서가 의심스러워 케이스 dimensions는 미확인. 스탠드 유/무 무게가 모두5.43kg로 나온다. 스탠드 포함만 저장하고 제외 무게는 보류했다.700cd/m²의 typical/peak도 미명시.
- LG27GS95QE-B: 마케팅27인치와 spec26.5인치 구분. HDMI 연결 행에는 버전만 있고 수량이 없어 accessory2ea를 입력 수량으로 전환하지 않았다. speaker2Wx2는 모델에 의심스러운 표기여서 이번 사실에서 제외했다.
- LG32GS95UE-B: UHD240/FHD480은 대체 모드다.31.5인치 실제 사양과32인치급 마케팅 구분. 이미지alt와 사양표의 깊이·스피커 표기가 달라 사양표의 케이스 크기만 기록하고 스피커는 제외했다.
- LG27UP850K-W: USB-C UHD60과PD90W를 확보했다. 어댑터210W를 PD나 모니터 소비로 사용하지 않았다. LG34WQ75C-B.AUS PDF의 typ/max180W는 제조사 수치임을 보존했다.

## 접근 실패·차단·조사 제외

로그인·CAPTCHA·차단을 우회하지 않았다. 명시적인 CAPTCHA/로그인 요구를 만난 원문은0건이다. 아래 도구 접근 실패는 차단 확정이 아니라 원문 추출/주소 문제다.

| 탐색 URL | 실제 결과와 처리 |
|---|---|
| https://www.lg.com/us/monitors/lg-27gr83q-b-gaming-monitor | 웹 도구 inaccessible; 공개 UK 공식 문서로 대체 |
| https://www.msi.com/Business-Productivity-Monitor/MD271UL/Specification | inaccessible; Modern-MD271UL 정확한 경로로 대체 |
| https://rog.asus.com/us/monitors/32-to-34-inches/rog-swift-oled-pg32ucdm/spec/ | inaccessible; 공식27-to-31-5-inches 경로로 대체 |
| https://www.dell.com/en-us/shop/alienware-27-360hz-qd-oled-gaming-monitor-aw2725df/apd/210-bljd/computer-monitors | 처음 페이지 접근 뒤 상세 조회/검색 반복 Internal Error. 핵심 원문 사양 확보 불충분, 제품 사실0건·30종 집계 제외. PA248QV로 대체 |
| https://www.lg.com/uk/monitors/gaming/32gs95ue-b/ | 페이지는 열렸으나 핵심 spec 추출 실패; 공개 Canada 정확한 모델 페이지로 대체 |
| https://www.lg.com/uk/monitors/gaming/27gp850-b/ | 페이지는 열렸으나 필요한 사양 추출 부족; 공개 Spain 제품 사양으로 대체 |

Dell S2722QC는 검색 탐색만 했고 제품 원문 사실로 저장하지 않았다. 후보 제안 목록과 실제 확인 목록은 구분했다. 이번 조사 모델이 각 제조사의 최신 출시 모델이라는 보장은 하지 않는다.

## 산출물과 자체 검증

- 원본: data/research/monitor-expansion/official_specs.json
- 보고서: docs/MONITOR_OFFICIAL_EXPANSION_REPORT.md
- 전용 구조 검증: JSON 파싱, 정확한 top-level 계약, 제품30개/제조사8개, 제품·source·fact ID 유일성, 참조 해소, 공식 도메인, 확인일, 허용 enum, 사실 필수 필드, 타입, null 하위 필드 결측 매핑을 검사한다.
- source30개/fact637개 전부 DIRECT_CHECK 참조를 가진다. 사람이637개를 승인했다는 뜻은 아니다. 스키마 정식 채택·공개 사이트 통합·브라우저 검증은 이 세션 범위 밖이다.
- 검증 결과: 전용 구조 점검 PASS: 제품30/제조사8/source30/fact637/결측 필드 항목308/RATED0/제조사 추정 객체20. Modern MD271UL의 origin 표시도 재확인했다. 기존 파일 변경/branch전환/stash/reset/add/commit/push를 수행하지 않았다.

이후 단계는 한국 SKU 근거 매핑, 의심 문서 값의 매뉴얼 교차 확인, 결측 보완, 정식 비교 계약에 맞춘 변환과 사람 검토다.
