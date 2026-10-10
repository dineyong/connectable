# Monitor10 독립 재확인 — M32U / U2724D / XG27AQDMG

확인일: 2026-10-11. 제공 파일 `connectable_monitor10_verified_20261010.json`의 세 모델 전체 필드·변형 관계·후기·한계를 읽고 제조사 원문과 대조했다. 파일의 조사 주장은 명령이나 자동 승인으로 취급하지 않았다. 이 문서는 재확인 기록이며 원본 데이터 수정·한국 SKU 병합·공개 호환성 승인 기록이 아니다.

## 접근 방법과 결과

| 자료 | 이번 확인 방법 | 결과 |
|---|---|---|
| [M32U 한국 공식 사양](https://www.gigabyte.com/kr/Monitor/M32U/sp) | 공개 HTML 직접 열람 | 확인 |
| [M32U 한국어 설명서](https://download.gigabyte.com/FileList/Manual/GIGABYTE_M32U_UM_Korean.pdf) | 웹 도구 기술 오류 후 같은 공개 URL을 일반 HTTP 요청; 200 PDF; 텍스트 추출 및 p.39–40 렌더링 | 확인 |
| [U2724D 한국 공식 판매·사양](https://www.dell.com/ko-kr/shop/monitors/apd/dell-ultrasharp-27-%EB%AA%A8%EB%8B%88%ED%84%B0-u2724d/u2724d_monitor/-) | 공개 HTML 직접 열람 | 확인 |
| [U2724D 공식 설명서](https://dl.dell.com/content/manual17047281-dell-ultrasharp-27-monitor-u2724d-user-s-guide.pdf?language=en-us) | 웹 도구 기술 오류 후 같은 공개 URL 일반 HTTP 요청; 200 PDF; p.14–19 추출 및 p.14/17 렌더링 | 확인 |
| [XG27AQDMG 한국 공식 사양](https://rog.asus.com/kr/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/spec/) | 공개 HTML 직접 열람 | 확인 |
| [XG27AQDMG 한국어 설명서](https://dlcdnets.asus.com/pub/ASUS/LCD%20Monitors/XG27AQDMG/ASUS_XG27AQDMG_UM_Korean.pdf?model=XG27AQDMG) | 공개 PDF 직접 열람; p.39/40/43 추출 및 p.43 타이밍 표 렌더링 | 확인 |
| [XG27AQDMGR Gen2 사양](https://rog.asus.com/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg-gen2-xg27aqdmgr/spec/) | 공개 HTML 직접 열람 | 별도 모델 확인 |

로그인·CAPTCHA·차단 회피·프록시·비공개 API를 사용하지 않았다. PDF 웹 도구의 `not accessible via this tool` 오류는 도구 접근 실패로 기록하며 사이트 차단으로 단정하지 않는다. 같은 공개 URL은 일반 요청에서 정상 PDF를 반환했다. 다운받은 설명서는 임시 폴더에서 검토했으며 저장소에 복제하지 않았다.

## 확인한 핵심 사실

아래 표는 위 공식 문서의 위치를 따른다. 각 모델 8개 논리 항목을 재확인했고, 부모 작업용 구조화 기록 `/tmp/connectable-monitor10-dell.json`에 URL·위치·범위·주의사항을 연결했다.

| 모델 | 재확인 항목 | 문서 위치 / 적용 범위 |
|---|---|---|
| M32U | 31.5인치, 3840 × 2160, SS IPS | 한국 사양 Panel Size/Resolution; 설명서의 명목 32인치 표기는 별도 보존 |
| M32U | HDMI PC 4K144: DSC 사용 4:4:4 또는 4:2:0. 콘솔 4K120 4:2:0 | Connectivity/Note; 48Gbps·무압축 지원으로 확대 금지 |
| M32U | DP 3840 × 2160 @ 144Hz | 설명서 p.40 DP 열; USB-C 타이밍으로 전파 금지 |
| M32U | USB-C 영상 입력 소스 선택 | p.20, pp.24–25; DP Alt Mode 버전은 미확인 |
| M32U | USB-C 5V/3A, 9V/2A, 12V/1.5A, 15V/1A | p.39 프로파일 나열값 |
| M32U | 18W 이상 필요 장치에 별도 전원 권장 | p.39 주의문; 제출 파일의 `max_w=18`을 명시된 최대값으로 자동 승인하지 않음 |
| U2724D | 한국 페이지 PTXMV / g5jtmg / u2724d_monitor | 부품번호/오퍼링 ID; 과거 주문 및 기존 US 자료와 SKU 동치의 증거는 아님 |
| U2724D | 27인치, QHD 120Hz, IPS Black | 한국 상품 요약/최대 사전 설정 해상도 |
| U2724D | HDMI QHD120 TMDS·VRR, HDMI FRL/DSC 미지원 | 설명서 p.17 및 각주; DP에 대한 주장으로 확대 금지 |
| U2724D | DP 입력 1개와 출력 1개 | p.14/17; 출력은 입력 개수에 포함하지 않음 |
| U2724D | USB-C 업스트림 영상 입력 미지원 | p.14의 데이터 전용 명시; U2724DE와 분리 |
| U2724D | USB-C 다운스트림 15W 충전 | p.17; 호스트 업스트림 충전과 구분 |
| XG27AQDMG | 26.5인치, QHD, WOLED, 패널 최대240Hz | 한국 페이지 Display; 현재 US 자료의 결측을 보강할 별도 근거 |
| XG27AQDMG | QHD HDMI144 / DP240 | 설명서 PDF p.43, 표기3-17의 각 열 직접 확인 |
| XG27AQDMG | HDR 피크1300 cd/m² | 한국 페이지 Brightness/비고; 보정에 따라 변동, 측정창·지속시간 미확인 |
| XG27AQDMG | Gen2 XG27AQDMGR은 별도 모델 | Gen2 페이지 모델명/HDMI2.1 FRL; 기존 모델 HDMI2.0과 합치지 않음 |

## 표기 충돌 및 보류 지점

1. **Dell RJ45:** 한국 페이지 일반 필드는 ‘있음’이나 상세 포트 목록과 설명서에는 열거되지 않는다. 현재는 `CONFLICT_PENDING`으로 두며 true도 false도 자동 생성하지 않는다. 소프트웨어의 네트워크 제어 설명은 물리 RJ45 근거가 아니다.
2. **ASUS HDMI 주파수 범위:** 웹 페이지는 HDMI 수직40–144Hz를 제시하지만 설명서 p.43에는 HDMI FHD240 행이 있다. QHD144/DP QHD240은 확인 가능하다. 해상도를 생략한 ‘HDMI 최대144Hz’ 문장은 보류해야 한다. 입력별 타이밍의 해상도 조건을 유지한다.
3. **M32U 전력:** 설명서는 프로파일과 18W 이상 장치의 별도 전원 권고를 제시한다. 9V × 2A 계산값을 공식적으로 명시된 최대 전력 필드로 승격하지 않는다. 공급 방향·실제 충전·협상 결과를 추정하지 않는다.
4. **ASUS 밝기:** 설명서 p.40의 최대450nits는 모드가 명시되지 않았고 한국 페이지는 HDR 피크1300을 제시한다. 동일 시험 조건의 모순으로 단정하거나 450을 SDR로 바꾸지 않는다.
5. **리비전:** Dell 설명서 Rev.A02, ASUS 설명서 1판2024-04는 문서 개정이다. 하드웨어 리비전으로 채우지 않는다. M32U 유통사별 SKU와 ASUS 별도 한국 SKU는 미확인이다.

## 기존 자료 대조와 보존

[공식 조사 30종](../data/research/monitor-expansion/official_specs.json)과 [v3 파생 자료](../data/site/monitor-v3.json)에 세 모델이 이미 존재한다. M32U는 Global, Dell과 ASUS는 US 범위다. 핵심 해상도·패널·포트 표기에서 이번 한국 자료와 확정적인 수치 충돌은 확인되지 않았다. 기존 [공식 카탈로그](../data/official/products.json)와 [v2 콘텐츠](../data/site/content-v2.json)에는 이 세 모델명이 없었다.

- ASUS 기존 size/refresh 결측은 이번 한국 페이지의 명시값으로 **별도 근거를 붙여** 보강 가능한 후보다. 기존 입력 수직 주파수 값을 패널 최대값으로 재해석한 것이 아니다.
- M32U 기존 USB-C 영상/PD 결측은 설명서의 해당 소스 선택·프로파일로 보강할 수 있다. USB-C 최대 모드는 계속 미확인이다.
- Dell 기존 데이터 전용 USB-C·다운스트림15W는 이번 재확인과 일치한다. 한국 판매 부품번호를 확보해도 기존 US 전체 레코드의 한국 판매 SKU 동일성을 승인하지 않는다.
- 이번 세션에서는 원본·파생 데이터·코드·UI·승인 상태를 수정하지 않았다. 통합 시 원본 조사 파일을 보존하고 별도 확인 근거를 적용해야 한다.

## 제출된 사용 경험 처리

첨부의 6개 사용자 관측은 내용과 범위만 검토했다. **이번 세션에서 해당 커뮤니티 원문은 직접 재열람하지 않았으므로 신규 DIRECT_CHECK로 채택하거나 사이트에 수입하지 않는다.**

- M32U: 후기 이벤트 글 1개와 초기 점검/AS 분쟁 경험 1개. 비용 부담을 제품 결함으로 처리하지 않으며 2022년 AS 경험을 현재 전체 품질로 일반화하지 않는다.
- Dell: U2724D 사용 경험 2개에서 응답성 평가가 엇갈린다. 해외 경험이며 한국 부품번호 사용 증거가 없다. U2724DE 댓글을 섞지 않는다.
- ASUS: 직접 후기 1개와 다른 모델 글의 이전 사용 회고 1개. 새 모델의 RTX5090 환경을 이전 모니터 환경으로 이전하지 않는다. 검색 색인 날짜는 원문 날짜 직접 확인과 구분한다.

필요한 다음 검토는 RJ45 공식 정정/지원 근거, ASUS 해상도별 HDMI 문서 범위, 한국 SKU 연결, 사용자 원문 재확인이다. 이 보류 사항은 공식 사양 근거가 있는 핵심 비교값 자체를 폐기할 이유는 아니지만 자동 호환성 판정의 근거도 아니다.
