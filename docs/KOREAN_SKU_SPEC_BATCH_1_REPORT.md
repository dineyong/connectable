# 한국 문서·SKU 및 미확인 사양 후속 소배치

2026-10-11 · `codex/monitor-purpose-design` · 기준 `09ac401`.

[기준 커밋 CI](https://github.com/dineyong/connectable/actions/runs/38117828949)는 completed/success로 확인했다.

## 범위와 결과

이번에는 이전 LG/Dell/ASUS OLED 한국 문서 대조와 중복하지 않도록 PD2705U, PA279CRV, MAG 274QRF QD E2를 우선 조사하고, 남은 기능 결측 대상으로 M28U를 추가했다. 전체 30종의 한국 SKU가 확인됐다는 뜻은 아니다.

| 대상 | 직접 읽은 공식 문서·위치 | 확인 및 반영 | 미확인 유지 |
| --- | --- | --- | --- |
| BenQ PD2705U | [한국 사양표](https://www.benq.com/ko-kr/monitor/creative-pro/pd2705u/spec.html), Display·지원 단자 | 같은 모델명, UHD60 IPS 및 USB-C DP Alt Mode/65W 대조. 새 출처 및 상세 조사 메모 추가 | 기존 CA 레코드와 한국 판매 P/N 동치, VRR, 한국 보증 적용 |
| ASUS PA279CRV | [한국 기술 사양](https://www.asus.com/kr/displays-desktops/monitors/proart/proart-display-pa279crv/techspec/), Display·I/O·지역 각주 | 같은 모델명, UHD60 IPS 및 USB-C DP Alt Mode/96W 대조. 출처·메모 추가 | 기존 US와 국내 유통 SKU 동치, KVM, 한국 전체 보증 |
| MSI MAG 274QRF QD E2 | [한국어 설명서](https://download-2.msi.com/archive/mnu_exe/monitor/MAG_274QRF-QD-E2v1.1_Korean.pdf), 인쇄 p.7/11/16/18/19 | 한국어 설명서 존재 및 조건 검토를 이 보고서에 기록. 원본 fact는 변경하지 않음 | 국내 판매 SKU·보증·소비전력; 한국어 설명서만으로 한국 판매 증명 불가 |
| Gigabyte M28U | [Global 공식 소개](https://www.gigabyte.com/Monitor/M28U), Key Features / Adaptive-Sync, Gaming Features / PIP/PBP | 신규 fact 3개, 기존 결측 3개 해소. 상세·비교용 파생 자료 재생성 | VRR 입력별 범위, 동시 입력 모드, PD, USB-C 영상 규격, 한국 SKU/보증 |

확인일은 모두 2026-10-11이며 기존 출처 날짜는 변경하지 않았다. 제조사 페이지의 메뉴나 다른 제품 설명을 해당 제품 근거로 사용하지 않았다. 검색 결과는 링크 발견에만 사용하고 원문을 직접 열었다.

## 보증과 SKU를 확정하지 않은 이유

- BenQ [제품 보증 페이지](https://www.benq.com/ko-kr/support/downloads-faq/products/monitor/pd2705u/warranty.html)는 서비스센터 안내 이미지/링크 중심이다. [서비스센터](https://www.benq.com/ko-kr/support/repair-service/repair-center.html) 및 [보증 정책](https://www.benq.com/ko-kr/support/registration-warranty/warranty-information.html)도 열었지만 이번 텍스트 열람으로 제품별 기간·수입 경로·적용 조건을 충분히 확보하지 못했다. 이미지를 직접 판독한 검증으로 기록하지 않는다. warranty card는 보증 기간이 아니다.
- ASUS 한국 표의 LCD ZBD Warranty 3yr는 LCD 무결점 보증에 관한 표기다. 제품 전체 서비스 보증이나 모든 국내 판매품 적용으로 해석하지 않았다. 치수/무게/구성품의 지역 차이를 문서가 직접 안내한다.
- 한국어 페이지·모델명 일치와 수입사/판매 P/N·리비전·보증의 동일성은 다르다. 기존 region CA/US/Global을 KR로 바꾸지 않고 korean_sku_identity와 warranty_korea를 유지했다.

## MSI 조건 검토 — 이번 fact 반영에서 제외한 항목

한국어 설명서의 표지 모델은 MAG 274QRF-QD-E2 (3CC2)이다. 문서 식별자를 국내 판매 P/N으로 간주하지 않았다.

- 인쇄 p.7: USB-C DP Alt Mode 및 최대65W, 소스/케이블 조건.
- p.11: HDR 수신 시 PIP/PBP 등의 OSD 설정이 비활성.
- p.16: PIP/PBP 활성 시 MPRT·Adaptive-Sync가 꺼지는 조건.
- p.18: Type C PD 충전 켜기/끄기 설정.

기존 데이터에는 PIP/PBP·65W 사실이 이미 있으며, 이번 설명서의 조건을 공식 소비전력이나 새 한국 SKU 승인으로 전환하지 않는다. 설명서 호스트 `download-2.msi.com`은 현재 연구 데이터의 제한된 출처 허용 목록에 없고, [모델별 공식 지원 페이지](https://www.msi.com/Monitor/MAG-274QRF-QD-E2/support)는 이번 열람에서 템플릿만 반환했다. 호스트 검사 기준을 임의로 완화하거나 지원 페이지를 PDF 본문 근거로 대신 저장하지 않았다. 제조사 지원 링크의 PDF 연결 확인 및 조건을 반영할 근거 등록은 다음 조사 항목이다. 직접 읽은 PDF 내용은 이 보고서에만 한정해 기록했다.

## 데이터 보존

3개 제품 객체만 변경: 한국 문서 출처·메모 2종, 기능 facts 3개 추가 1종. 모든 기존 facts, 모델·지역·식별 상태 보존. 기존 MSI 원본도 변경하지 않음. intake는 원본 식별 정보 유지 확인 후 baseline hash/size만 갱신한다. 공식 catalog, 코퍼스, 후기, 사진, UI와 사용자 미커밋 작업은 수정하지 않는다.

## 사용자 결정

이번 조사에 필요한 결정은 없다. 국내 SKU 확정에 구매 대상의 공식 판매 링크나 P/N 자료가 있으면 추가 대조할 수 있다. 자료가 없다는 이유로 모든 모니터의 승인 여부를 사용자에게 대신 판단하도록 요청하지 않는다. 실제 출시 전에 해외 문서 기반 제품의 공개 범위, 도메인·광고·사진 사용권 결정은 별도 유지한다.

## 검증

실행 결과는 아래에 기록한다. 제조사 문서의 모든 조건 및 실물 동작 검증을 뜻하지 않는다.

- Python 전체 `python3 -m unittest discover -s tests -q`: **568개 통과**.
- 브라우저 전체 `npm run test:e2e -- --workers=2`: **190개 통과**, 데스크톱/모바일. 기존 사용자 미커밋 검사 14개 포함 로컬 결과.
- 파생 데이터/정적 30종 문서/제품 inventory `--check`, Quasarzone intake, 로컬 사이트 검증, `git diff --check` 통과.
- 3종 변경 및 전 제품의 기존 facts·식별자·지역·승인 상태 보존을 객체 비교로 확인. intake는 baseline hash/size 외 변경 없음. 공식 검증기의 민감 문자열·참조 검사 통과.
- 테스트 생성 캡처는 원래 파일로 복원. 기존 사용자 변경은 커밋에 포함하지 않음. main 병합·공개 배포 없음. 최종 커밋은 이 보고서를 포함한 커밋으로 식별한다.
