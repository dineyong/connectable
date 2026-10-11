# 나머지 모니터 미확인 사양 공식 재검토

2026-10-11 · 작업 브랜치 `codex/monitor-purpose-design` · 기준 `297741b`.

## 범위와 CI

[기준 커밋 CI](https://github.com/dineyong/connectable/actions/runs/38116435735)는 completed/success로 확인했다.
지난 작업의 ASUS XG27AQDMG/PG32UCDM을 제외한 28종의 기존 공식 사양 URL을 직접 열고, 제품 전용 표와 미확인 필드를 대조했다. MSI 2종은 공식 제품 소개의 KVM 절을 추가로 읽었다. 이는 모든 사양의 검증 완료나 한국 판매 SKU 승인이 아니다. 추출 실패/미기재 값은 유지했고 검색 요약·타 모델·사용자 리뷰로 보충하지 않았다.

## 반영

- LG 27GP850-B: HDR, USB-C 명시적 NO, USB 3.0 허브, PIP/PBP 명시적 NO, 스탠드, 치수, 무게 8개 facts. 기존 HDMI/DP version null만 2.0/1.4로 보완. ES 문서 범위 유지.
- Dell U2724D: 스탠드 포함 치수(inch), 근사 무게(lb), 미국 문서 3년 제한 보증 3개 facts. 무단 단위 변환 및 국내 보증 승격 없음.
- MSI MAG 274QRF QD E2 / MPG 321URX QD-OLED: 각 KVM 1개 fact. 구체적인 포트 조합·동시 영상 출력을 추정하지 않음.
- LG 27UP850K-W: 제품 Key Features의 AMD FreeSync 1개 fact. 주파수 범위와 포트별 지원은 미확인.
- 합계 신규 facts 14개, 포트 버전 2개 보완. 5종 변경, 나머지 25종 원본 객체 보존.
- 새 출처 확인일 2026-10-11을 별도 기록. 과거 출처 확인일을 덮어쓰지 않음.

## 제품별 조사 결과

아래 링크는 이번에 연 공식 문서다. “미확인”은 “미지원”이 아니다. 모든 제품의 한국 SKU, 국내 보증, 실측 및 전체 동시 입력 조건은 별도 근거가 필요하다.

| 모델 | 공식 자료 | 결과/남은 불확실성 |
| --- | --- | --- |
| PA279CRV | [공식 문서](https://www.asus.com/us/displays-desktops/monitors/proart/proart-display-pa279crv/techspec/) | KVM의 명시 근거 없음. |
| VG27AQ | [공식 문서](https://www.asus.com/us/displays-desktops/monitors/tuf-gaming/tuf-gaming-vg27aq/techspec/) | USB-C/PD/허브/PIP/PBP 명시 근거 없음. 포트 목록 부재를 미지원으로 해석하지 않음. |
| PA278QV | [공식 문서](https://www.asus.com/sg/displays-desktops/monitors/proart/proart-display-pa278qv/techspec/) | HDR/USB-C/PD/KVM/PIP/PBP 미확인 유지. |
| PA248QV | [공식 문서](https://www.asus.com/us/displays-desktops/monitors/proart/proart-display-pa248qv/techspec/) | HDR/USB-C/PD/KVM/PIP/PBP 미확인. 재조회 일부 추출 실패. |
| VA24EHF | [공식 문서](https://www.asus.com/displays-desktops/monitors/eye-care/va24ehf/techspec/) | 색역 및 미기재 포트·부가기능 확인 불가. |
| PD2705U | [공식 문서](https://www.benq.com/en-ca/monitor/creative-pro/pd2705u/spec.html) | VRR와 지역 보증 근거 부족. |
| PD2725U | [공식 문서](https://www.benq.com/en-ca/monitor/creative-pro/pd2725u/spec.html) | TB3 영상/PD 설명은 있으나 별도의 USB-C 필드와 VRR/보증을 추정하지 않음. |
| EX2710Q | [공식 문서](https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html) | USB-C/PD/KVM/PIP/PBP 및 보증 미확인. |
| GW2790QT | [공식 문서](https://www.benq.com/en-ca/monitor/home/gw2790qt/spec.html) | HDR/KVM/PIP/PBP/VRR/보증 미확인. |
| GW2490 | [공식 문서](https://www.benq.com/en-us/monitor/home/gw2490/spec.html) | 제품 전용 누락 기능 확인 부족. 공통 탐색 메뉴의 기능은 근거 제외. |
| 27GP850-B | [공식 문서](https://www.lg.com/es/monitores/monitores-ultragear-gaming/27gp850-b/) | 신규 8 facts + HDMI 2.0/DP 1.4 보완. VESA 표기 불일치로 해당 필드 유지. |
| 27GR83Q-B | [공식 문서](https://www.lg.com/uk/monitors/gaming/27gr83q-b/) | 일반 밝기·정상 소비전력·미기재 기능의 조건 근거 부족. |
| 27GS95QE-B | [공식 문서](https://www.lg.com/uk/monitors/gaming/27gs95qe-b/) | 전원 어댑터 DC 출력과 대기 소비전력은 일반 소비전력으로 변환하지 않음. HDMI 개수는 사진 설명만으로 추가하지 않음. |
| 32GS95UE-B | [공식 문서](https://www.lg.com/ca_en/monitors/gaming/32gs95ue-b/) | 누락 기능 재확인 불충분. 후속 조회 추출 실패를 미지원 근거로 쓰지 않음. |
| 27UP850K-W | [공식 문서](https://www.lg.com/uk/monitors/uhd-4k-5k/27up850k-w/) | 제품 Key Features의 AMD FreeSync 추가. PD 90/96W 충돌 메모; 소비전력/하드웨어 KVM 추정 금지. |
| 34WQ75C-B.AUS | [공식 문서](https://www.lg.com/us/support/products/documents/34WQ75C_Spec_Sheet.pdf) | 공식 1쪽 사양서에서 PIP/VRR/HDMI·DP 버전 미확인. |
| Modern MD271UL | [공식 문서](https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL/Specification) | 누락 밝기/부가기능/보증 확인 부족. 어댑터 출력을 소비전력으로 사용하지 않음. |
| MAG 274QRF QD E2 | [공식 문서](https://www.msi.com/Monitor/MAG-274QRF-QD-E2/Specification) | 공식 제품 소개의 KVM 추가. 소비전력·보증 미확인. |
| MPG 321URX QD-OLED | [공식 문서](https://www.msi.com/Monitor/MPG-321URX-QD-OLED/Specification) | 공식 제품 소개의 KVM 추가. PIP/PBP/소비전력 미확인. |
| M27Q rev.1.0 | [공식 문서](https://www.gigabyte.com/Monitor/M27Q-rev-10/sp) | 공식 사양표에 없는 값은 미확인 유지. |
| M28U | [공식 문서](https://www.gigabyte.com/Monitor/M28U/sp) | USB-C PD/영상 프로토콜 및 PIP/PBP/VRR/보증 미확인. |
| M32U | [공식 문서](https://www.gigabyte.com/Monitor/M32U/sp) | USB-C PD/영상 프로토콜·VRR·보증 미확인. |
| Q27G3XMN | [공식 문서](https://www.aoc.com/us/gaming/monitors/q27g3xmn) | 700cd/m²를 typical로 추정하지 않음. 치수 축 순서가 제목과 불일치할 가능성 있어 자동 변환 보류. |
| S32CG554EU (LS32CG554EUXEN) | [공식 문서](https://images.samsung.com/is/content/samsung/assets/de/display/pdf/Datenblatt_Monitor_LS32CG554EUXEN.pdf) | 지역 SKU 문서 유지. 색역 단위/PD/영상 프로토콜 등 누락 값을 추정하지 않음. |
| S65UC (LS34C650UEEXXY) | [공식 문서](https://www.samsung.com/au/monitors/high-resolution/viewfinity-s6-s65uc-34-inch-ultra-wqhd-ls34c650ueexxy/) | 지역 SKU 문서 유지. 색역 단위/PD/영상 프로토콜 등 누락 값을 추정하지 않음. |
| U2724D | [공식 문서](https://www.dell.com/en-us/shop/dell-ultrasharp-27-monitor-u2724d/apd/210-bksf/monitors-monitor-accessories) | 스탠드 포함 치수/근사 무게/US 3년 제한 보증 추가. 한국 보증 유지. |
| U2724DE | [공식 문서](https://www.dell.com/en-us/shop/dell-ultrasharp-27-thunderbolt-hub-monitor-u2724de/apd/210-bksj/monitors-monitor-accessories) | VRR·한국 SKU/보증 추가 확정 없음. |
| AW3225QF | [공식 문서](https://www.dell.com/en-us/shop/alienware-32-4k-qd-oled-gaming-monitor-aw3225qf/apd/210-blmq/computer-monitors) | 1000nit·동적 명암비를 typical/native로 전환하지 않음. 무게의 스탠드 조건 및 USB-C PD 미확인. |

MSI 추가 근거: [MAG 274QRF QD E2 / KVM](https://www.msi.com/Monitor/MAG-274QRF-QD-E2), [MPG 321URX QD-OLED / KVM](https://www.msi.com/Monitor/MPG-321URX-QD-OLED).
Dell U2724D 기존 링크는 [새 공식 URL](https://www.dell.com/en-us/shop/monitors/apd/dell-ultrasharp-27-monitor-u2724d/u2724d_monitor/-)로 이동하며 모델명을 재확인했다.

## 충돌과 보류

- 27UP850K-W: UK 사양표/USB-C 본문은 90W, 갤러리 대체텍스트는 96W. 기존 사양표 값 90W와 원본을 보존하고 제품 notes에 CONFLICT_REVIEW 기록. 96W fact는 생성하지 않았다. 본문에는 다른 모델 27UP85NP도 등장하므로 해당 문장으로 기능을 확정하지 않았다. FreeSync는 이 제품 Key Features의 명시 항목에 한정한다.
- 27GP850-B: 인증 절의 VESA wall mount standard NO와 물리 장착 절의 100×100mm가 공존한다. 다른 의미일 수 있으나 단정하지 않고 vesa 미확인 유지. 패널 165Hz를 DP OC180Hz로 임의 변경하지 않음.
- Q27G3XMN: 치수 제목 W×H×D와 숫자 순서가 일치하는지 불확실. 축을 자동 교환하지 않았다. 700cd/m²는 typical 표시가 없어 일반 밝기로 추가하지 않았다.
- Dell AW3225QF: 피크/일반 밝기, 동적/native 명암비, 스탠드 무게 조건을 합치지 않음.
- LG/MSI 어댑터 DC 출력, 슬립·꺼짐 전력을 일반 소비전력으로 사용하지 않음. LG Dual Controller를 하드웨어 KVM으로 승격하지 않음.
- 외국 공식 문서의 정확한 모델과 한국 판매 P/N 동일성은 별개다. 모든 공개 승인/호환성 사용 금지 상태 유지.

## 보존과 재생성

공식 연구 데이터에서 확인된 항목만 추가/보완하고 기존 생성기로 카드·상세·비교용 데이터와 30개 정적 제품 문서를 재생성했다. intake의 제품 식별자/제조사/모델/지역/상태 동일성을 확인한 후 baseline hash/size만 갱신했다. 기존 코퍼스·후기·catalog·호환성 엔진·이미지·UI 코드 및 사용자 미커밋 변경을 변경하지 않았다.

## 사용자 확인이 필요한 것만

지금 추가 결정이나 승인은 필요 없다. 국내 판매 SKU/보증까지 확정할 때 실제 구매 대상 판매 링크 또는 제조사·공식 유통사의 P/N 자료가 필요하다. 승인만으로 미확인 사양을 확정하지 않는다. 이미지 사용권, 도메인·광고 연결은 기존 보류 유지.

## 검증

검증 실행 결과는 아래에 기록한다. 테스트는 자료 구조와 표시 회귀를 확인하며 실제 제품 호환성이나 제조사 문서의 무오류를 보장하지 않는다.

- `python3 -m unittest discover -s tests -q`: 565개 통과(회귀 6개 추가).
- `npm run test:e2e -- --workers=2`: 데스크톱·모바일 186개 통과(기존 사용자 미커밋 검사 14개 포함 로컬 결과).
- 공식 자료/Quasarzone intake 검증, 생성 데이터·제품 문서·inventory `--check`, `validate_local_site.py`, `git diff --check` 통과.
- 30종 식별 정보, 기존 facts 보존 확인(명시한 LG 포트 version null 보완 2개 제외). 5종만 변경. intake는 baseline hash/size 외 동일.
- 개인정보/비밀값 패턴 검사 통과. 테스트가 갱신한 화면 캡처는 기준 파일로 복원. 기존 사용자 README/DECISIONS/site-v2/content-review 변경은 커밋에서 제외.
- main 병합 및 공개 배포 없음. 최종 커밋은 이 보고서를 포함한 커밋으로 식별한다.
