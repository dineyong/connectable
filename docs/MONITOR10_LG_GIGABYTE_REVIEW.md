# Monitor10 독립 재확인 — LG 3종·Gigabyte Rev.2

확인일: 2026-10-11. 사용자 제공 `connectable_monitor10_verified_20261010.json`의 앞 4개 모델에 대해 식별·변형 관계·공식 사양·사용자 관측·후보·제한 섹션을 검토했다. 공식 원문을 다시 읽은 선택 사실만 별도 확인 결과로 전달했다. 제공 파일의 DIRECT 표기를 자동 승계하지 않았다. 원본 사양과 기존 제품 ID는 수정하지 않았다.

## 공개 원문 재확인

| 모델 | 직접 연 공식 자료 | 이번 확인 범위 |
|---|---|---|
| 27GP850 | [한국 제품](https://www.lge.co.kr/monitors/27gp850), [BB 지원](https://www.lge.co.kr/support/product-27GP850-BB) | 상세 스펙 화면/입력 신호/영상·음성, 지원 페이지 제품 정보 링크와 도착 제품코드 |
| 27GS95QE | [한국 제품](https://www.lge.co.kr/monitors/27gs95qe), [BB 지원](https://www.lge.co.kr/support/product-27GS95QE-BB) | 같은 범위, 특히 HDR peak APL 조건 |
| 32GS95UE | [한국 제품](https://www.lge.co.kr/monitors/32gs95ue), [BB 지원](https://www.lge.co.kr/support/product-32GS95UE-BB) | 같은 범위, 특히 대체 화면 모드와 HDR APL 조건 |
| M27Q Rev.2.0 | [한국 제조사 사양](https://www.gigabyte.com/kr/Monitor/M27Q-rev-20/sp) | Panel Size, Resolution, Refresh Rate, Connectivity, Brightness, HDR Support |

LG 3개 상품 URL은 같은 제조사 `product/monitors/…?modelId=…&pdpType=PURCHASE` 경로로 이동했다. 지원 페이지의 `제품 정보` 링크를 실제 클릭하여 각각 무접미사 한국 제품코드로 연결됨을 확인했다. 이 링크는 해외 -B나 전체 공장 SKU의 동일성을 보증하지 않는다. 27GP850 페이지에는 단종 제품이며 상세 정보 기준일이 2026-02-10이라는 표시가 있다. 확인일과 제품 정보 기준일은 다르다.

## 채택 가능한 선택 사실

각 모델 8개 사실 묶음을 직접 재확인했다. 제품당 수치는 다른 지역 제품에 덮어쓰지 않는다.

- **27GP850 한국 제품:** 68.5cm, QHD, Nano IPS. 입력별 QHD HDMI144 / DP165·OC180 조건, 연결단자 수, 일반 밝기400/320, HDR 명칭과 BB 지원 연결을 확인했다. OC는 DP1.4 지원 GPU 조건을 보존한다.
- **27GS95QE 한국 제품:** 67.3cm, QHD, OLED. HDMI2.1/DP1.4 QHD240, 단자 수, 일반 밝기275/250와 HDR peak1300/800 **3% APL**, HDR 명칭과 BB 지원 연결을 확인했다.
- **32GS95UE 한국 제품:** 79.9cm, UHD, OLED. HDMI2.1/DP1.4의 UHD240 또는 FHD480, 단자 수, 일반 밝기275/250와 HDR peak1300/1040 **1.5% APL**, HDR 명칭과 BB 지원 연결을 확인했다. 두 모드는 동시 출력이 아니다.
- **M27Q Rev.2.0:** 27inch SS IPS, QHD, 165Hz/OC170Hz, 단자 수·버전·USB-C Alternate Mode upstream, USB-C PD **up to10W**, 일반 밝기350, DisplayHDR400을 확인했다. 인증명400을 peak 실측400으로 치환하지 않는다.

LG 일반 밝기값을 SDR 조건이 명시된 값으로 이름을 바꾸지 않는다. cm를 inch로 환산하거나 마케팅 크기로 반올림하지 않는다. USB-C 미표기를 0개·미지원으로 바꾸지 않는다.

## 기존 30종과의 대조

기존 [공식 조사 원본](../data/research/monitor-expansion/official_specs.json)의 LG 근거 지역은 27GP850-B **ES**, 27GS95QE-B **GB**, 32GS95UE-B **CA**다. 제공 자료에 나오는 US/AU 근거와도 구분해야 한다. 이번 한국 문서가 상세하더라도 해외 모델의 결측을 덮어쓰는 근거가 아니다. 해상도·주사율 일부가 같다는 것은 SKU 동일성 증거가 아니다.

기존 M27Q는 **Rev.1.0**이며 이번은 **Rev.2.0**이다. 기존 원본의170Hz/색영역92%/0.5ms MPRT와 Rev.2 페이지의165·OC170Hz/95%/1ms MPRT를 별도 리비전 값으로 유지한다. 이번에는 Rev.1 공식 웹페이지를 다시 열지 않았으므로 Rev.1 쪽 수치는 기존 저장 자료와의 비교이지 신규 DIRECT_CHECK가 아니다. 제조사 Rev.2 모델과 유통명 `M27Q 2.0 제이씨현`의 완전한 동일 SKU 증명은 미확인이다.

## 미확인·비채택

- LG 전체 한국 공장/유통 SKU, 하드웨어 리비전, 해외 -B 동치, USB-C/PD는 미확인 유지.
- 제공 LG 설명서의 소수점 타이밍·DSC·색심도·크로마·스탠드 세부 각도는 이번 선택 사실 목록에 넣지 않았다. 한국 상품표에서 보이는 값 외 설명서 근거를 신규 직접 확인으로 표시하지 않는다.
- [M27Q 한국어 설명서](https://download.gigabyte.com/FileList/Manual/GIGABYTE_M27Q_20_UM_Korean_20220520.pdf?v=c004a9cca600889965d58ec3a476ebb4)는 열렸지만 36/38쪽 screenshot 호출 결과가 읽을 수 있는 이미지로 표시되지 않았다. 따라서 제공 자료의 켜짐10W/대기15W 및 입력별 타이밍 열은 이번 재검증에서 채택하지 않았다. 상품표의 up to10W만 별도 확인했다. 접근 제한 우회는 하지 않았다.
- 사용자 후기 섹션은 제공 자료로 읽었으나 원문을 이번 공식 사양 검토에서 다시 열지 않았다. 후기의 DIRECT 상태나 모델 연결 승인으로 전용하지 않는다.
- 선택 사실과 제공 값 사이의 명백한 모순은 발견하지 못했다. 미검토 필드까지 검증 완료라는 뜻은 아니다.

정형 결과는 상위 작업자에게 `/tmp/connectable-monitor10-lg.json`으로 전달했다. 이 임시 파일은 배포 기준 원본이 아니며 상위 작업의 승인 보류 조사 계층에 통합할 입력이다. 코드·원본 데이터·Git은 변경하지 않았다.
