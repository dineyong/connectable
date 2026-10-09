# 제품별 사람 검토 자료 — 1차

작성일: 2026-10-09. 고정 코드/데이터 기준: `f391080`. 사람 검토 **미완료**. 이 문서는 검토 준비 자료이며 공식 원문을 이번에 새로 확인한 결과나 승인 기록이 아니다.

원본 자료는 바꾸지 않았다. 모든 체크박스는 미확인으로 남긴다. 검토자는 [절차](CONTENT_REVIEW_PROCEDURE.md)에 따라 실제로 확인한 대상만 별도 [검토 기록](../data/review/content_reviews.json)에 기록한다. AI가 대신 사람 검토자나 검토 완료 날짜를 입력하지 않는다.

## 먼저 확인할 항목

- [ ] V32UE: 4K UHD 표기 확인과 숫자 픽셀·Hz 미확인을 구분했는가?
- [ ] 27ULD950: PD65 제품명만으로 65W 공급을 확정하지 않으며 공급 기능 필터에서 제외되는가?
- [ ] LG: 기존 정격 RATED와 LV 최대 UP_TO를 별도로 표시하고 한국 SKU는 UNKNOWN인가?
- [ ] 모든 제품: 기능 표기와 실제 Mac 연결 결과, 사용자 후기와 공식 사양을 구분하는가?
- [ ] 검토 기록이 없어도 화면이 승인 완료처럼 보이지 않는가?

화면 확인: 로컬 `http://127.0.0.1:8873/#monitors`에서 제품 상세를 열고, 아래 제품 두 개씩 비교한다. 서버가 없으면 `python3 scripts/serve_mockup.py`로 실행한다. 공식 페이지 접근 실패/로그인/차단은 우회하지 않고 검토 메모에 기록한다.

## 제품별 근거·필드·검토 대상

### Dell U2723QE

제품 ID: `product:dell-u2723qe` · 원본 지역: `GB` · 공개 `UNKNOWN` · 사람 검토 `PENDING_HUMAN_REVIEW`.

원본 공식 출처:

- `SRC-dell-u2723qe` — [Dell UltraSharp 27 4K USB-C Hub Monitor - U2723QE](https://www.dell.com/en-gb/shop/dell-ultrasharp-27-4k-usb-c-hub-monitor-u2723qe/apd/210-bcxk/monitors-monitor-accessories) · 기존 확인일 2026-10-08 · 원본 `data/official/connection_model_pilot.json`

| fact / 원본 문장 | typed 값 | 기존 재확인 범위 | 미확인·검토 대기 필드 |
|---|---|---|---|
| `dell-u2723qe:1`: 패널 기본 해상도 3840×2160 60Hz | scope=PANEL; width=3840; height=2160; refresh_hz=60; interface=UNKNOWN | VERIFIED_MODEL_SCOPE: scope / width / height / refresh_hz | interface |
| `dell-u2723qe:2`: 영상용 USB-C upstream은 DP 1.4 Alt Mode | interface=USB_C_VIDEO_UPSTREAM; protocol=DISPLAYPORT; version=1.4; mode=ALT_MODE; support=SUPPORTED | VERIFIED_MODEL_SCOPE: interface / protocol / version / mode / support | 없음 |
| `dell-u2723qe:3`: 영상용 USB-C upstream에서 최대 90W 공급 | mode=OFFER; interface=USB_C_VIDEO_UPSTREAM; watts=90; rating_basis=UP_TO | VERIFIED_MODEL_SCOPE: mode / interface / watts / rating_basis | 없음 |
| `dell-u2723qe:4`: USB-C downstream은 최대 15W 충전 | mode=OFFER; interface=USB_C_DOWNSTREAM; watts=15; rating_basis=UP_TO | VERIFIED_MODEL_SCOPE: mode / interface / watts / rating_basis | 없음 |

fact별 기록 바인딩(화면용 추가 metadata를 제외한 원본 전체 fact SHA-256):

- [ ] `dell-u2723qe:1` · hash `0dbec3f9e910a072306d310403a0a54ceea6407d04177bd68feada2f6feb9faf` · source_refs `SRC-dell-u2723qe`
- [ ] `dell-u2723qe:2` · hash `4d2df1b5ad673babe1ef222e421f18e4d8f64d0099a5ca2be22a83dae025371b` · source_refs `SRC-dell-u2723qe`
- [ ] `dell-u2723qe:3` · hash `4088cc780000a54cd18b9835ed5bb08658109af70f84995cd7ea6b204ae7935f` · source_refs `SRC-dell-u2723qe`
- [ ] `dell-u2723qe:4` · hash `d6b6f59deb3a16b4409ef00577282b2233454d1674890e7e1689de91c4b29137` · source_refs `SRC-dell-u2723qe`

재확인 근거(기존 배치의 기록이며 이번 재접속 결과가 아님):

- `SR-DELL-PL` — [공식 문서](https://www.dell.com/pl-pl/shop/monitor-dell-ultrasharp-27-4k-z-koncentratorem-usb-c-u2723qe/apd/210-bcxk/monitory-i-akcesoria-do-monitor%C3%B3w) · 지역 PL · 기존 확인 2026-10-09 · 위치: Rozdzielczość / częstotliwość odświeżania; Złącza / Interfejsy

연결된 연구 기록(모델 연결 자체는 실물 SKU 동일성/호환성 승인 아님):

- 연결된 후기 없음. 다른 모델 후기를 대신 연결하지 않는다.

검토자가 남길 메모: 원문 확인 여부 / 확인한 필드 / 미확인 필드 / 지역 SKU / 화면 문구 / 판정 보류 이유. 작성 전까지 공란으로 둔다.

### LG 27UP850-W

제품 ID: `product:lg-27up850-w` · 원본 지역: `MY` · 공개 `UNKNOWN` · 사람 검토 `PENDING_HUMAN_REVIEW`.

원본 공식 출처:

- `SRC-lg-27up850-w` — [27" UHD 4K IPS Monitor with VESA DisplayHDR 400 - 27UP850-W](https://www.lg.com/my/monitors/ultrafine-uhd-4k-5k/27up850-w/) · 기존 확인일 2026-10-08 · 원본 `data/official/connection_model_pilot.json`

| fact / 원본 문장 | typed 값 | 기존 재확인 범위 | 미확인·검토 대기 필드 |
|---|---|---|---|
| `lg-27up850-w:1`: 패널 3840×2160, 60Hz | scope=PANEL; width=3840; height=2160; refresh_hz=60; interface=UNKNOWN | PENDING_HUMAN_REVIEW: 없음 | scope / width / height / refresh_hz / interface |
| `lg-27up850-w:2`: USB-C DP Alternate Mode 지원 | interface=USB_C; protocol=DISPLAYPORT; mode=ALT_MODE; support=SUPPORTED | VERIFIED_MODEL_SCOPE: interface / protocol / mode / support | 없음 |
| `lg-27up850-w:3`: USB-C PD 표기 96W | mode=OFFER; interface=USB_C; watts=96; rating_basis=RATED | PENDING_HUMAN_REVIEW: 없음 | mode / interface / watts / rating_basis |

fact별 기록 바인딩(화면용 추가 metadata를 제외한 원본 전체 fact SHA-256):

- [ ] `lg-27up850-w:1` · hash `1dea7a94dadb2138876ddd9cbf629ad085e8f55e54b60f6b1e6618107d01e1cb` · source_refs `SRC-lg-27up850-w`
- [ ] `lg-27up850-w:2` · hash `b063c1fef2cbcda2f002103a8a279e4c914db9cd5cf890cd617f4ecfc43296f5` · source_refs `SRC-lg-27up850-w`
- [ ] `lg-27up850-w:3` · hash `81079cf315908f0711e8d58bb1ea5c8ae79a6f75b30492ec1b27f6be0fdd575b` · source_refs `SRC-lg-27up850-w`

재확인 근거(기존 배치의 기록이며 이번 재접속 결과가 아님):

- `SR-LG-LV` — [공식 문서](https://www.lg.com/lv/monitori/lg-27up850-w) · 지역 LV · 기존 확인 2026-10-09 · 위치: SAVIENOJAMĪBA: HDMI/DP/USB-C maks. izšķirtspēja; DP versija; USB-C DP režīms/elektrības padeve
- 별도 assertion `SR-LG-PD`: USB-C에서 최대 96W 공급 표기 · `UP_TO` · 기존 fact를 대체하지 않음 · 한국 SKU `UNKNOWN`.

연결된 연구 기록(모델 연결 자체는 실물 SKU 동일성/호환성 승인 아님):

- 연결된 후기 없음. 다른 모델 후기를 대신 연결하지 않는다.

검토자가 남길 메모: 원문 확인 여부 / 확인한 필드 / 미확인 필드 / 지역 SKU / 화면 문구 / 판정 보류 이유. 작성 전까지 공란으로 둔다.

### Dell G2724D

제품 ID: `product:dell-g2724d` · 원본 지역: `US` · 공개 `UNKNOWN` · 사람 검토 `PENDING_HUMAN_REVIEW`.

원본 공식 출처:

- `SRC-dell-g2724d` — [Dell 27 Gaming Monitor - G2724D](https://www.dell.com/en-us/shop/dell-27-gaming-monitor-g2724d/apd/210-bhxc/monitors-monitor-accessories) · 기존 확인일 2026-10-08 · 원본 `data/official/connection_model_pilot.json`

| fact / 원본 문장 | typed 값 | 기존 재확인 범위 | 미확인·검토 대기 필드 |
|---|---|---|---|
| `dell-g2724d:1`: DisplayPort에서 2560×1440 165Hz | scope=PORT; width=2560; height=1440; refresh_hz=165; interface=DISPLAYPORT | PENDING_HUMAN_REVIEW: 없음 | scope / width / height / refresh_hz / interface |
| `dell-g2724d:2`: HDMI에서 2560×1440 144Hz | scope=PORT; width=2560; height=1440; refresh_hz=144; interface=HDMI | PENDING_HUMAN_REVIEW: 없음 | scope / width / height / refresh_hz / interface |

fact별 기록 바인딩(화면용 추가 metadata를 제외한 원본 전체 fact SHA-256):

- [ ] `dell-g2724d:1` · hash `35c762e62882ee134e2dddda0665d1df39d8a0649f0e188b43aed3d2b62543cb` · source_refs `SRC-dell-g2724d`
- [ ] `dell-g2724d:2` · hash `abf7e7911ec97fdf9131387518b226af3f8e2986604e1496942135ba14fb4c24` · source_refs `SRC-dell-g2724d`

재확인 근거(기존 배치의 기록이며 이번 재접속 결과가 아님):

- 별도 재확인 기록 없음. 원본에 있는 공식 출처를 사람이 직접 확인해야 한다.

연결된 연구 기록(모델 연결 자체는 실물 SKU 동일성/호환성 승인 아님):

- 연결된 후기 없음. 다른 모델 후기를 대신 연결하지 않는다.

검토자가 남길 메모: 원문 확인 여부 / 확인한 필드 / 미확인 필드 / 지역 SKU / 화면 문구 / 판정 보류 이유. 작성 전까지 공란으로 둔다.

### 주연테크 V32UE

제품 ID: `product:jooyon-v32ue` · 원본 지역: `KR` · 공개 `UNKNOWN` · 사람 검토 `PENDING_HUMAN_REVIEW`.

원본 공식 출처:

- `SITE-JYT-V32UE` — [주연테크 V32UE 출시 자료](https://www.jooyon.co.kr/bbs/board.php?bo_table=press&page=16&wr_id=227) · 기존 확인일 2026-10-09 · 원본 `data/site/monitor-batch-1-sources.json`

| fact / 원본 문장 | typed 값 | 기존 재확인 범위 | 미확인·검토 대기 필드 |
|---|---|---|---|
| `jooyon-v32ue:site-1`: 공식 출시 자료: 32형 IPS, 4K UHD 표기 | scope=PANEL; resolution_label=4K UHD; width=UNKNOWN; height=UNKNOWN; refresh_hz=UNKNOWN | PARTIALLY_VERIFIED: resolution_label | scope / width / height / refresh_hz |
| `jooyon-v32ue:site-2`: USB-C 영상 연결 기능 표기 | interface=USB_C; support=SUPPORTED; protocol=UNKNOWN | PENDING_HUMAN_REVIEW: 없음 | interface / support / protocol |
| `jooyon-v32ue:site-3`: USB-C 충전 공급 65W 표기; 실제 수전W 미확인 | mode=OFFER; interface=USB_C; watts=65; rating_basis=MANUFACTURER_STATED | PENDING_HUMAN_REVIEW: 없음 | mode / interface / watts / rating_basis |
| `jooyon-v32ue:site-4`: HDMI 2.0·DP 1.2·USB-C·USB-B·USB-A 2.0 제공 | interfaces=['HDMI_2.0', 'DISPLAYPORT_1.2', 'USB_C', 'USB_B', 'USB_A_2.0'] | PENDING_HUMAN_REVIEW: 없음 | interfaces |
| `jooyon-v32ue:site-5`: 리모컨으로 OSD·입력·볼륨 조절 | support=SUPPORTED | PENDING_HUMAN_REVIEW: 없음 | support |
| `jooyon-v32ue:site-6`: 100×100mm VESA 홀 표기 | width_mm=100; height_mm=100 | PENDING_HUMAN_REVIEW: 없음 | width_mm / height_mm |

fact별 기록 바인딩(화면용 추가 metadata를 제외한 원본 전체 fact SHA-256):

- [ ] `jooyon-v32ue:site-1` · hash `9a89213b3a4a43c2362898ec58a7363b8be8c70f5472594f332836411470bd4a` · source_refs `SITE-JYT-V32UE`
- [ ] `jooyon-v32ue:site-2` · hash `5a280f09dbb6b11bcb304a4304a880f6df841de225a630bfec281926369a2c93` · source_refs `SITE-JYT-V32UE`
- [ ] `jooyon-v32ue:site-3` · hash `d16fb420a51d4e523dcaeb3edc0bd98c170ad65ef18025976c38e9e6951dcc60` · source_refs `SITE-JYT-V32UE`
- [ ] `jooyon-v32ue:site-4` · hash `4cbe3646794106715a747bddb94291414519a2e02a3b5145325906927d39c793` · source_refs `SITE-JYT-V32UE`
- [ ] `jooyon-v32ue:site-5` · hash `78dfc5da028f3456a53507d8011ca2e87440257964254c51e942e80ae49e823c` · source_refs `SITE-JYT-V32UE`
- [ ] `jooyon-v32ue:site-6` · hash `0c27ce0a2d710c6297dbe10d143c055562bc930525198419a3d8ef827be8ceef` · source_refs `SITE-JYT-V32UE`

재확인 근거(기존 배치의 기록이며 이번 재접속 결과가 아님):

- `SR-JYT` — [공식 문서](https://www.jooyon.co.kr/bbs/board.php?bo_table=press&page=16&wr_id=227) · 지역 KR · 기존 확인 2026-10-09 · 위치: 본문 출시 설명: 32형·4K UHD·IPS

연결된 연구 기록(모델 연결 자체는 실물 SKU 동일성/호환성 승인 아님):

- [ ] `PUR-001` · 보고 결과 `{'status': 'UNKNOWN', 'closure': 'UNKNOWN', 'summary': '검토용 기능별 진술만 매핑; 게시물 전체 결과는 미승인', 'observation_ids': [], 'evidence_refs': ['e_context']}` · source: [원문](https://makeany.tistory.com/97) / [원문](https://makeany.tistory.com/97)

검토자가 남길 메모: 원문 확인 여부 / 확인한 필드 / 미확인 필드 / 지역 SKU / 화면 문구 / 판정 보류 이유. 작성 전까지 공란으로 둔다.

### 크로스오버 27ULD950

제품 ID: `product:crossover-27uld950` · 원본 지역: `KR` · 공개 `UNKNOWN` · 사람 검토 `PENDING_HUMAN_REVIEW`.

원본 공식 출처:

- `SITE-CROSS-27ULD950` — [크로스오버 27ULD950 일반 제품](https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757) · 기존 확인일 2026-10-09 · 원본 `data/site/monitor-batch-1-sources.json`

| fact / 원본 문장 | typed 값 | 기존 재확인 범위 | 미확인·검토 대기 필드 |
|---|---|---|---|
| `crossover-27uld950:site-1`: 27형 IPS 3840×2160, 60Hz 공식 표기 | scope=PANEL; width=3840; height=2160; refresh_hz=60; interface=UNKNOWN | PENDING_HUMAN_REVIEW: 없음 | scope / width / height / refresh_hz / interface |
| `crossover-27uld950:site-2`: USB PD 지원 표기; PD65는 상품명, 상세 전력 UNKNOWN | mode=OFFER; interface=UNKNOWN; watts=UNKNOWN; rating_basis=PRODUCT_LABEL_ONLY; label=PD65 | PARTIALLY_VERIFIED: label | mode / interface / watts / rating_basis |
| `crossover-27uld950:site-3`: KVM 스위치 기능 표기 | support=SUPPORTED | PENDING_HUMAN_REVIEW: 없음 | support |
| `crossover-27uld950:site-4`: 내장 스피커 표기 | support=SUPPORTED | PENDING_HUMAN_REVIEW: 없음 | support |
| `crossover-27uld950:site-5`: 스탠드 높이 조절 기능 표기 | support=SUPPORTED | PENDING_HUMAN_REVIEW: 없음 | support |
| `crossover-27uld950:site-6`: PIP·PBP 기능 표기 | support=SUPPORTED | PENDING_HUMAN_REVIEW: 없음 | support |
| `crossover-27uld950:site-7`: 75×75mm VESA 홀 표기 | width_mm=75; height_mm=75 | PENDING_HUMAN_REVIEW: 없음 | width_mm / height_mm |

fact별 기록 바인딩(화면용 추가 metadata를 제외한 원본 전체 fact SHA-256):

- [ ] `crossover-27uld950:site-1` · hash `43143f30f6ade3a88f0112ee5f367fc2bffc8713a8294eecc5776ccd93a28a26` · source_refs `SITE-CROSS-27ULD950`
- [ ] `crossover-27uld950:site-2` · hash `d1de1e84d1f083e5726855d364a40d33ee708c414c6ebd273b65b00901c5362d` · source_refs `SITE-CROSS-27ULD950`
- [ ] `crossover-27uld950:site-3` · hash `6e09fff790a301d77008101fc1d8384e5803812b1644b0fe2ce6c43d6f11a1c2` · source_refs `SITE-CROSS-27ULD950`
- [ ] `crossover-27uld950:site-4` · hash `fcda81afbe0ef4f9e47c204755af23c127cd40483ac3c815b82f58c00401a87c` · source_refs `SITE-CROSS-27ULD950`
- [ ] `crossover-27uld950:site-5` · hash `bcdf118f815c0d71841ca9a8c6f94c3859178173ecabc78873866c595f3d074a` · source_refs `SITE-CROSS-27ULD950`
- [ ] `crossover-27uld950:site-6` · hash `d8653d4d6b177803adf5cdab3a2790bbf87d60b1cdc32767ed56235b6469b3e4` · source_refs `SITE-CROSS-27ULD950`
- [ ] `crossover-27uld950:site-7` · hash `65d940094a59c6ed6ee10fd405a7532f0c350ef03166c76cd910d81a786eb1db` · source_refs `SITE-CROSS-27ULD950`

재확인 근거(기존 배치의 기록이며 이번 재접속 결과가 아님):

- `SR-CROSS` — [공식 문서](https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757) · 지역 KR · 기존 확인 2026-10-09 · 위치: 상품명 및 요약정보: PD65·USB PD 지원

연결된 연구 기록(모델 연결 자체는 실물 SKU 동일성/호환성 승인 아님):

- [ ] `PUR-005` · 보고 결과 `{'status': 'UNKNOWN', 'closure': 'UNKNOWN', 'summary': '검토용 기능별 진술만 매핑; 게시물 전체 결과는 미승인', 'observation_ids': [], 'evidence_refs': ['e_context']}` · source: [원문](https://quasarzone.com/bbs/qf_dp/views/515378) / [원문](https://quasarzone.com/bbs/qf_dp/views/515378)
- [ ] `PUR-006` · 보고 결과 `{'status': 'UNKNOWN', 'closure': 'UNKNOWN', 'summary': '검토용 기능별 진술만 매핑; 게시물 전체 결과는 미승인', 'observation_ids': [], 'evidence_refs': ['e_context']}` · source: [원문](https://quasarzone.com/bbs/qc_user/views/133467) / [원문](https://quasarzone.com/bbs/qc_user/views/133467)

검토자가 남길 메모: 원문 확인 여부 / 확인한 필드 / 미확인 필드 / 지역 SKU / 화면 문구 / 판정 보류 이유. 작성 전까지 공란으로 둔다.

### MSI MD271UL

제품 ID: `product:msi-md271ul` · 원본 지역: `GLOBAL` · 공개 `UNKNOWN` · 사람 검토 `PENDING_HUMAN_REVIEW`.

원본 공식 출처:

- `SITE-MSI-MD271UL` — [MSI Modern MD271UL 공식 사양](https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL/Specification) · 기존 확인일 2026-10-09 · 원본 `data/site/monitor-batch-1-sources.json`

| fact / 원본 문장 | typed 값 | 기존 재확인 범위 | 미확인·검토 대기 필드 |
|---|---|---|---|
| `msi-md271ul:site-1`: 27형 IPS 3840×2160, 60Hz 공식 표기 | scope=PANEL; width=3840; height=2160; refresh_hz=60; interface=UNKNOWN | PENDING_HUMAN_REVIEW: 없음 | scope / width / height / refresh_hz / interface |
| `msi-md271ul:site-2`: USB-C DP Alternate 영상 입력 표기 | interface=USB_C; protocol=DISPLAYPORT; mode=ALT_MODE; support=SUPPORTED | PENDING_HUMAN_REVIEW: 없음 | interface / protocol / mode / support |
| `msi-md271ul:site-3`: USB-C 65W Power Delivery 공급 표기 | mode=OFFER; interface=USB_C; watts=65; rating_basis=MANUFACTURER_STATED | PENDING_HUMAN_REVIEW: 없음 | mode / interface / watts / rating_basis |
| `msi-md271ul:site-4`: HDMI 입력 최대 3840×2160 60Hz 표기 | scope=PORT; interface=HDMI; width=3840; height=2160; refresh_hz=60; rating_basis=UP_TO | PENDING_HUMAN_REVIEW: 없음 | scope / interface / width / height / refresh_hz / rating_basis |
| `msi-md271ul:site-5`: DISPLAYPORT 입력 최대 3840×2160 60Hz 표기 | scope=PORT; interface=DISPLAYPORT; width=3840; height=2160; refresh_hz=60; rating_basis=UP_TO | PENDING_HUMAN_REVIEW: 없음 | scope / interface / width / height / refresh_hz / rating_basis |
| `msi-md271ul:site-6`: USB_C 입력 최대 3840×2160 60Hz 표기 | scope=PORT; interface=USB_C; width=3840; height=2160; refresh_hz=60; rating_basis=UP_TO | PENDING_HUMAN_REVIEW: 없음 | scope / interface / width / height / refresh_hz / rating_basis |
| `msi-md271ul:site-7`: 스탠드 틸트 -5°~20° 표기 | min_degrees=-5; max_degrees=20 | PENDING_HUMAN_REVIEW: 없음 | min_degrees / max_degrees |

fact별 기록 바인딩(화면용 추가 metadata를 제외한 원본 전체 fact SHA-256):

- [ ] `msi-md271ul:site-1` · hash `f15b53304d81c5d4c0b66739b59cd9915d476e44387e250821b7c789fe2dc004` · source_refs `SITE-MSI-MD271UL`
- [ ] `msi-md271ul:site-2` · hash `165ce80335f5bbbc52fd5425ba7fc0806236115480459e7a7ab50222dd69e6eb` · source_refs `SITE-MSI-MD271UL`
- [ ] `msi-md271ul:site-3` · hash `48eb12d1c32e7a8fd49073d5ba55a5c635fe4b70f681859afff7948461124906` · source_refs `SITE-MSI-MD271UL`
- [ ] `msi-md271ul:site-4` · hash `626fb45824ae0120873e2e183c36457cd4dfcdd1459a02d78842263f32f9329f` · source_refs `SITE-MSI-MD271UL`
- [ ] `msi-md271ul:site-5` · hash `91d5d53826894621e63721a55a83465a6f78c6059bb479db63ac5d15e0260b7b` · source_refs `SITE-MSI-MD271UL`
- [ ] `msi-md271ul:site-6` · hash `decfd3372f23f9d5a63d1c6d6d132bc36f29e95a5837e38095b99955daf4c71d` · source_refs `SITE-MSI-MD271UL`
- [ ] `msi-md271ul:site-7` · hash `509ed4e7fa55d82d983bf15cec086865814506e90953596b0d6969de0f9d704b` · source_refs `SITE-MSI-MD271UL`

재확인 근거(기존 배치의 기록이며 이번 재접속 결과가 아님):

- 별도 재확인 기록 없음. 원본에 있는 공식 출처를 사람이 직접 확인해야 한다.

연결된 연구 기록(모델 연결 자체는 실물 SKU 동일성/호환성 승인 아님):

- [ ] `PUR-014` · 보고 결과 `{'status': 'UNKNOWN', 'closure': 'UNKNOWN', 'summary': '검토용 기능별 진술만 매핑; 게시물 전체 결과는 미승인', 'observation_ids': [], 'evidence_refs': ['e_context']}` · source: [원문](https://seook.tistory.com/m/entry/맥북-4K-모니터-추천-MSI-MD271UL-4K-듀얼-모니터-실제-사용-후기) / [원문](https://seook.tistory.com/m/entry/맥북-4K-모니터-추천-MSI-MD271UL-4K-듀얼-모니터-실제-사용-후기)

검토자가 남길 메모: 원문 확인 여부 / 확인한 필드 / 미확인 필드 / 지역 SKU / 화면 문구 / 판정 보류 이유. 작성 전까지 공란으로 둔다.

## 완료 기록과 승인 범위

현재 검토자·날짜·검토 결과를 작성한 실제 ledger는 0건이다. 체크박스를 누르거나 이 문서를 읽었다는 사실만으로 자동 승인하지 않는다. 확인한 fact만 target hash와 해당 공식 source ID를 포함해 기록하고 검증기를 실행한다. 부분 확인의 상세 범위는 notes에 적는다.

EVIDENCE_SUFFICIENT도 편집 검토의 근거 충족 기록이며 공개 호환 승인이 아니다. 공개 UNKNOWN 및 호환성 사용 NO는 유지한다. main 통합과 서비스 공개 승인은 별도이며, 사람이 사이트 문구를 확인했다고 물리 출력·PD 협상을 시험한 것으로 기록하지 않는다.
