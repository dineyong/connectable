# MSI MAG 274QRF QD E2 설명서 연결·사양 검토

2026-10-11 · `codex/monitor-purpose-design` · 기준 `f764d52`.

## 공식 연결 확인

[모델 지원 페이지](https://www.msi.com/Monitor/MAG-274QRF-QD-E2/support)에서 제품명 MAG 274QRF QD E2를 확인하고 브라우저의 **Manual & Document** 버튼을 눌렀다. `support#manual` 목록에 [한국어 설명서](https://download.msi.com/archive/mnu_exe/monitor/MAG_274QRF-QD-E2v1.1_Korean.pdf)가 직접 표시된다. PDF 본문 표지 모델은 MAG 274QRF-QD-E2(3CC2), 개정V1.1(2024/11)이다. 로그인·CAPTCHA·비공개 API 없이 공개 메뉴를 확인했다.

기존 MD271UL 방식과 같이 제조사·제품ID·표시 모델·정확한 PDF URL을 함께 등록한다. download.msi.com 전체 또는 download-2.msi.com을 포괄 허용하지 않는다. 문서 링크 검토는 한국 판매 SKU 승인이나 실시간 리다이렉트 감시가 아니다.

## 확인 결과

[공식 사양 페이지](https://www.msi.com/Monitor/MAG-274QRF-QD-E2/Specification)의 해당 모델 표와 PDF를 대조했다.

| 항목 | 공식 근거 위치 | 처리 |
|---|---|---|
| HDR 수신 시 PIP/PBP 설정 비활성 | 설명서 인쇄11쪽 | 조사 메모 추가 |
| PIP/PBP 사용 시 MPRT·Adaptive-Sync 꺼짐, HDMI CEC 꺼짐/선택불가, 응답 시간 선택불가 | 설명서16쪽 | 조사 메모 추가. 동시 입력별 주사율 보장으로 확대하지 않음 |
| DCI-P3 | 웹98%, 설명서19–20쪽95%, 양쪽CIE1976 | `CONFLICT_REVIEW` 명시. 기존98% 원본값 보존, 해결된 것으로 처리하지 않음 |
| 포장 포함 중량 | 웹GW8.6kg, 설명서20쪽Gross13.3kg | 충돌 메모. 기존 본체중량6.05kg과 구분, 포장중량 fact 추가 없음 |
| 외부 전원 공급120.08W | 설명서19쪽 | 모니터 소비전력으로 기록하지 않음 |
| USB-C 최대65W, HDMI QHD144/DP QHD180 | 설명서7/18쪽 및 웹Note | 기존값 대조. 신규 수치 중복 추가 없음 |
| 국내 SKU·보증 | 적용 범위 근거 부족 | 미확인 유지 |

신규 numeric fact 0개, 출처1개 및 조건·충돌 메모5개 추가. 기존 사실·결측·Global 지역·식별 상태 보존. 부분 조건이 확인돼도 `per_input_simultaneous_conditions` 전체 결측은 유지한다. 기존 충돌 표시 기능을 통해 상세·비교 및 정적 제품 페이지에 경고가 전달된다. 수치가 다르다는 이유만으로 어느 문서를 정답으로 고르거나 평균내지 않는다.

## 검증

- 변경 전 정확한 MAG 설명서 URL 수용 테스트가 실패하는 것을 확인했다. 등록 후 정상 URL 통과, 다른 모델 설명서·버전·query·download-2 경로는 거부한다.
- 색역 기존값 보존, 충돌 메모와 PIP/PBP 제한 유지, 한국 SKU·소비전력 미확인 회귀 검사 추가.
- 기존 corpus/catalog/UI 코드·사용자 미커밋 파일 보존. 생성 데이터·정적 문서·목록만 재생성. main 병합·배포 없음.
- 전체 결과는 아래 기록한다. 최종 커밋은 이 보고서를 포함한 커밋이다.

## 남은 위험과 결정

색역·포장중량 차이의 원인(문서 오류·지역·리비전)은 미확인이다. 지원 페이지의 문서 연결을 검증했어도 문서 내용의 충돌까지 해결되지는 않는다. 공식 정정 또는 정확한 리비전별 설명이 필요하며 사용자가 대신 수치를 선택할 사항은 없다. 현재 추가 사용자 결정 없음.

## 실행 결과

- Python 전체 `python3 -m unittest discover -s tests -q`: **576개 통과**.
- 브라우저 전체 `npm run test:e2e -- --workers=2`: **190개 통과**(기존 로컬 미커밋 검사14개 포함).
- 공식/intake 검증, 생성 데이터·정적 페이지·inventory check, 로컬 사이트·보고서 경로·diff 검사 통과.
- MAG의 기존 facts/결측/식별 정보 및 다른29종 객체 보존 확인. 정적 페이지에 충돌 안내가 생성됨을 확인. 테스트 캡처 복원.
- CI는 push 후 완료 응답에서 최종 확인한다.
