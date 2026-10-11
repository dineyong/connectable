# 한국 SKU·미확인 사양 4차 조사

2026-10-11 · `codex/monitor-purpose-design` · 기준 `08eb6e2`.

## 결론

6종의 공식 페이지 또는 설명서에 대해 원문 확인을 시도했다. 새로 읽은 자료는 있으나 기존 레코드의 지역·리비전·출처 계약을 충족하며 미확인 필드를 해소할 근거는 확보하지 못했다. **제품 데이터 변경 0건, 한국 SKU 승인 0건**이다. 결측을 없애기 위한 추측이나 출처 허용 목록 변경은 하지 않았다.

## 원문 확인 결과

| 대상 | 직접 확인한 공식 URL·위치 | 결과 |
|---|---|---|
| Modern MD271UL | [Global 사양](https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL/Specification), [한국 공식 소개](https://kr.msi.com/blog/upgrade-your-business-and-work-setup-with-the-msi-modern-md271ul-4k-monitor), [한국어 설명서](https://download.msi.com/archive/mnu_exe/monitor/Modern_MD271ULv1.1_Korean.pdf) 인쇄16쪽 | 소개는 기존65W와27인치 IPS UHD를 대조. 설명서는 모델3PB8, 밝기300 nits(typ.) 명시. Global 사양 추출에는 밝기 없음. 설명서 출처 연결 검토 미완료로300을 사이트에 추가하지 않음 |
| MPG 321URX QD-OLED | [소개](https://www.msi.com/Monitor/MPG-321URX-QD-OLED), [사양](https://www.msi.com/Monitor/MPG-321URX-QD-OLED/Specification) | 본문은 열렸으나 PIP 검색 결과 없음. 미기재를 PIP/PBP 미지원으로 바꾸지 않음. 신규 한국 SKU 근거 없음 |
| PG32UCDM | [한국 사양](https://rog.asus.com/kr/monitors/27-to-31-5-inches/rog-swift-oled-pg32ucdm/spec/), [Global 사양](https://rog.asus.com/monitors/27-to-31-5-inches/rog-swift-oled-pg32ucdm/spec/), [US 원본](https://rog.asus.com/us/monitors/27-to-31-5-inches/rog-swift-oled-pg32ucdm/spec/) | 한국 URL은 timeout. Global에는 명암비 Typ. 1,500,000:1이 있으나 US 추출에는 해당 명시를 확보하지 못했다. US 레코드의 contrast_native를 Global 값으로 대체하지 않음. PIP/PBP 미확인 유지 |
| M27Q rev.1.0 | [Global Rev.1](https://www.gigabyte.com/Monitor/M27Q-rev-10) | Internal Error. Rev.2 또는 다른 파생 모델로 대체하지 않음 |
| EX2710Q | [한국 사양 후보](https://www.benq.com/ko-kr/monitor/gaming/ex2710q/spec.html) | 이번 도구 응답은404. 이전 기록을 사이트 전체 단종·국내 미판매로 해석하지 않음 |
| PA248QV | [한국 기술 사양](https://www.asus.com/kr/displays-desktops/monitors/proart/proart-display-pa248qv/techspec/) | timeout. 검색 요약으로 정보 보완하지 않음 |

확인 방법은 공개 페이지 open/find 및 PDF 텍스트 추출이며 캐시가 포함될 수 있다. CAPTCHA·로그인·비공개 API 우회 없음. 제3자 검색 결과는 근거로 채택하지 않았다. PG32UCDM Gen3(PG32UCDM3), PA278QV Gen2(PA278QGV) 검색 결과는 다른 모델이므로 기존 제품에 전용하지 않았다.

## MD271UL 설명서 검토 기록

설명서 개정 V1.1(2023/10), 표지 Modern MD271UL(3PB8), 인쇄16쪽에서 밝기300 nits(typ.)를 확인했다. 인쇄15쪽 PD 설정은 최대65W(20V/3.25A), 인쇄18쪽은 HDMI와DP/USB-C의UHD60 사전 설정 모드다. 표의 전원 출력19V·5.79A를 모니터 소비전력으로 곱해 저장하지 않는다. 한국어 문서 자체가 국내 판매 품번이나 보증을 증명하지 않는다.

[공식 지원 페이지](https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL/support)는 이번 추출에서 미치환 템플릿만 반환하여 해당 PDF로 연결되는 링크를 확인하지 못했다. `download.msi.com`, `kr.msi.com`은 현재 연구 검증기의 MSI 허용 호스트(`www.msi.com`)와 다르다. 본문을 읽었다는 사실과 원본 fact에 등록할 출처 검토 완료를 분리한다. 출처 검토 없이 다른 URL로 바꿔 저장하거나 허용 목록을 확대하지 않았다.

## 다음 조사 재개 조건

같은 URL을 반복 확인하는 것을 진행 실적으로 계산하지 않는다.

| 대기 항목 | 다음에 필요한 근거 |
|---|---|
| MD271UL 밝기300 | 모델별 공식 지원 페이지에서 PDF 연결 확인, 정확한 다운로드 호스트의 제한적 출처 등록 검토 |
| PG32UCDM 명암비·PIP/PBP | 원본 US 모델/리비전 범위를 확인할 제품 설명서 또는 US 명시값 |
| M27Q | Rev.1 문서 접근 성공 또는 Rev.1을 명시한 공식 설명서 |
| EX2710Q·PA248QV 한국 모델 | 정상 접근 가능한 한국 공식 지원/제품 문서, 정확한 품번 매핑 |
| 기존 국내외 SKU 공통 | 지역별 품번·구성품·보증 적용 범위 근거. 한국어 페이지 존재만으로 전량 승인하지 않음 |

이는 사용자에게 사양의 진위를 대신 결정해 달라는 요청이 아니다. 현재 필요한 사용자 결정은 없다. 신규 근거가 없을 때 사이트를 그대로 두는 것이 이번 반영 결과다. 기존 [3차 보고서](KOREAN_SKU_SPEC_BATCH_3_REPORT.md)의 Dell 국내 부품 번호 및 지역 구분도 보존한다.

## 검증 및 보존

원본·파생 제품 데이터, UI, 스키마, 검증기, 테스트는 수정하지 않았다. 보고서와 진행 상태 문서만 커밋한다. 기존 사용자 미커밋 파일은 제외하며 테스트 생성 캡처를 복원한다. 전체 실행 결과는 아래에 추가한다. main 병합·공개 배포 없음.

- Python 전체: `python3 -m unittest discover -s tests -q` — 571개 통과.
- 브라우저 전체: `npm run test:e2e -- --workers=2` — 190개 통과(기존 로컬 미커밋 검사14개 포함).
- 공식/intake 검증, 생성 자료3종 check, 로컬 사이트 검사, 보고서 상대경로와 diff 검사 통과.
- data/schemas/scripts/제품별 정적 페이지·생성 JS의 Git diff 없음 확인. 테스트 생성 캡처 복원.
- 최종 커밋은 본 보고서를 포함한 커밋으로 식별하며 원격 CI 결과는 완료 응답에서 별도 확인한다.
