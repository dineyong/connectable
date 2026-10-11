# 한국 문서·미확인 사양 2차 조사

2026-10-11 · `codex/monitor-purpose-design` · 기준 `d75d07c`.

[기준 CI](https://github.com/dineyong/connectable/actions/runs/38118271720): 최초 확인 시 진행 중, 작업 도중 completed/success 확인.

## 조사 범위와 반영

12개 기존 모델 또는 한국 대응 후보의 공식 자료를 조사했다. 아래 “보류”는 조사 시도 결과이며 검증 완료 모델 수가 아니다. 기존 한국 SKU 확정 상태를 승격한 건은 0건이다.

| 기존 모델/후보 | 직접 연 공식 자료 | 결과 |
| --- | --- | --- |
| PD2725U | [한국 사양](https://www.benq.com/ko-kr/monitor/creative-pro/pd2725u/spec.html) | UHD60 IPS, TB3 입력65W/출력15W 대조. 한국 문서 출처·메모 추가. CA 지역과 한국 SKU 미확인 유지 |
| GW2790QT | [한국 사양](https://www.benq.com/ko-kr/monitor/home/gw2790qt/spec.html) | QHD75 IPS, USB-C 영상/65W, DP MST 대조. 출처·메모 추가. OS별 확장 판정은 생성하지 않음 |
| VA24EHF | [한국 소개](https://www.asus.com/kr/displays-desktops/monitors/eye-care/va24ehf/) | 23.8인치 IPS FHD100 및 Adaptive-Sync 대조. 출처·메모 추가. 이미지 설명의 FreeSync를 새 인증 사실로 채택하지 않음 |
| VG27AQ | [한국 기술 사양](https://www.asus.com/kr/displays-desktops/monitors/tuf-gaming/tuf-gaming-vg27aq/techspec/) | QHD165 IPS/HDR10 대조. 출처·메모 추가. 미기재 USB-C 등을 false로 만들지 않음 |
| M32U | [Global 소개](https://www.gigabyte.com/Monitor/M32U), Key Features | 명시된 Adaptive-Sync 신규 fact 1개. VRR 결측 해소. 입력별 범위/인증 등급/PD/한국 SKU 미확인 유지 |
| M27Q Rev.1.0 | [Rev.1 소개](https://www.gigabyte.com/Monitor/M27Q-rev-10) | 최초 페이지 열림 후 기능 찾기/재열기 Internal Error. 읽지 못한 기능 확정 없음. Rev.2로 대체하지 않음 |
| EX2710Q | [한국 사양](https://www.benq.com/ko-kr/monitor/gaming/ex2710q/spec.html) | 직접 열기 Internal Error. 검색 요약만으로 반영하지 않음 |
| PA248QV | [한국 기술 사양](https://www.asus.com/kr/displays-desktops/monitors/proart/proart-display-pa248qv/techspec/) | 첫 열기 후 세부 재조회 Internal Error. 미확인 기능 추가 없음 |
| Samsung S32CG554EU의 한국 후보 | [LS32CG550EKXKR 지원](https://www.samsung.com/sec/support/model/LS32CG550EKXKR/) | URL 모델 코드가 기존 해외 모델과 다르고 본문 추출의 모델명이 충분하지 않아 동일성 보류. 지원 표 수치를 기존 제품에 이식하지 않음 |
| S65UC의 한국 후보 | [LS34C650TAKXKR S65TC](https://www.samsung.com/sec/monitors/high-resolution-ls34c650takxkr-d2c/LS34C650TAKXKR/) | 한국 페이지는 S65TC/T 계열. 기존 S65UC/U 계열과 병합하지 않음 |
| 27UP850K-W의 한국 후보 | [27UP850K 한국 제품](https://www.lge.co.kr/product/monitors/27up850k) | 원문 열람했지만 추출 결과에 일반 구매 FAQ·사용자 후기가 혼재하고 제품별 PD 표가 충분하지 않음. 기존 UK 90W/이미지 설명96W 충돌 해소 근거로 사용하지 않음 |
| Modern MD271UL | [Global 소개](https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL) | 기존65W 설명은 재확인. 남은 밝기/소비전력/국내 SKU를 확정할 새 근거 부족. 데이터 변경 없음 |

총 5개 제품 객체 변경: 한국 문서 출처·메모 4종, M32U source/note와 신규 fact1개. 모든 과거 fact는 그대로 보존했다. 한국 문서의 존재는 국내 판매 P/N·구성품·보증의 동일성이나 현재 판매 여부 증명이 아니다.

## 보수적으로 유지한 구분

- PD2725U 입력65W와 TB3 출력15W를 합치거나 호스트 충전 전력으로 전파하지 않음. 페이지의 All-in-One Connection TB3/4/5 문구를 실제 포트 버전으로 바꾸지 않음.
- GW2790QT의 MST는 해당 문서 표기이며 macOS/Windows 개별 장치의 독립 확장 보장이 아님.
- Adaptive-Sync 명시만으로 FreeSync 등급·G-SYNC 인증·VRR 주파수 범위를 만들지 않음.
- LG 페이지에 포함된 사용자 맥북 후기는 공식 사양이나 호환성 근거로 사용하지 않음.
- 도구 Internal Error는 사이트 차단이라고 단정하지 않는다. 로그인·CAPTCHA 우회나 비공개 API 사용 없음.

## 남은 조사

한국 모델이 확인되지 않은 AOC Q27G3XMN, LG 27GR83Q-B/34WQ75C-B, BenQ GW2490, Dell U2724DE/AW3225QF 등의 정확한 제품/유통 식별 근거가 남아 있다. 이전 조사에서 확인한 LG/Dell/ASUS 자료는 보존한다. MSI 설명서의 공식 지원 링크 연결 및 조건 등록은 [1차 보고서](KOREAN_SKU_SPEC_BATCH_1_REPORT.md)의 보류 사항을 따른다. 페이지를 한 번 열었다고 전체 사양 재검증 완료로 집계하지 않는다.

## 사용자 결정

지금 추가 결정은 필요 없다. 공식 국내 판매 품번 자료가 부족한 항목은 미확인 유지하며 사용자 승인으로 대체하지 않는다. 공개 범위·도메인·이미지·광고 연결의 출시 전 결정은 기존 목록을 따른다. 이번에는 main 병합·공개 배포·구매·외부 문의를 하지 않았다.

## 검증 및 보존

원본 ID/제조사/표시 모델/지역/식별 상태 및 기존 facts를 객체 비교로 확인한다. intake는 원본 재대조 후 baseline hash/size만 갱신한다. 사용자 미커밋 README/DECISIONS/site-v2/content-review 및 미추적 문서는 포함하지 않는다. 테스트 실행 결과는 아래 기록한다.

- Python 전체: **569개 통과** (`python3 -m unittest discover -s tests -q`).
- 데스크톱/모바일 전체: **190개 통과** (`npm run test:e2e -- --workers=2`). 로컬 수치에는 기존 사용자 미커밋 검사 14개 포함.
- 생성 데이터/정적 문서/inventory 일치, intake, 로컬 링크·공개 차단 및 diff 검사 통과. 5종 외 제품 보존, 모든 기존 facts 및 식별 정보 동일.
- 테스트 생성 캡처 원상 복원. 최종 커밋은 이 문서를 포함한 커밋으로 식별한다.

## 추가 탐색 — 위 12건 반영 수와 별도

[GW2490 한국 사양](https://www.benq.com/ko-kr/monitor/home/gw2490/spec.html)을 직접 열어 HDMI1.4 2개/DP1.2 1개를 확인했으나 이는 기존 확인값이며 미기재 기능을 미지원으로 바꾸지 않았다. [Dell 한국 목록](https://www.dell.com/ko-kr/shop/all-monitors/sac/monitors/all-monitors/dell-ultrasharp?appliedRefinements=40636)도 열었으나 제품 상세별 SKU 대조 전 단계다. 목록의 오퍼링/가격/재고를 확정 데이터로 수입하지 않는다. AOC/LG 추가 검색은 제품별 한국 동일성 근거를 확보하지 못해 검색 요약에서 값을 수입하지 않았다.
