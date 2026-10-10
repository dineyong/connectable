# Monitor10 MSI·BenQ·크로스오버 독립 재검토

확인일: 2026-10-11. 입력은 사용자가 전달한 `connectable_monitor10_verified_20261010.json`의 M10-08/09/10 전체 identity, specifications, variant relationships, user observations, limitations이다. 입력의 확인 주장을 그대로 신규 DIRECT_CHECK로 복제하지 않았다. 이번 문서는 제품 승인·호환성 승인 기록이 아니다. 원본·코드·화면은 변경하지 않았다.

## 결론

| 대상 | 이번 직접 확인 범위 | 적용 판단 |
|---|---|---|
| MSI MPG 274URF-QD | 글로벌 사양표와 한국어 V1.1 설명서 텍스트, 핵심 8개 필드 묶음 | 새 조사 후보로 사용 가능. 높이와 USB-C 데이터/KVM 충돌 보류 |
| BenQ MOBIUZ EX2710Q | 캐나다 사양표 핵심 8개 필드 묶음 | 기존 CA 모델의 값과 일치. 한국 문서 재확인이나 한국 SKU 승인으로 승격 금지 |
| Crossover 27ULD950 | 한국 공식 HTML 요약 핵심 8개 필드 묶음 | 기존 사이트 6종 자료와 겹침. 상세 이미지 전용 정보는 재확인 실패로 보류 |

확인된 필드 묶음은 숫자 단일 필드 수와 다르다. 예를 들어 resolution은 가로·세로를, ports는 복수 입력을 묶는다. 각 항목의 값·범위·URL·위치는 별도 전달 JSON에 제공했다. 원본 30종 데이터나 기존 6종 사이트 자료를 합치거나 갱신하지 않았다.

## MSI MPG 274URF-QD

[글로벌 사양](https://www.msi.com/Monitor/MPG-274URF-QD/Specification)의 Panel Size/Panel Type/Panel Resolution/Refresh Rate/Video ports/Note와 [한국어 설명서](https://download-2.msi.com/archive/mnu_exe/monitor/MPG_274URF_QDv1.1_Korean.pdf)의 pp.8,20을 직접 읽었다.

27인치, Rapid IPS, 3840×2160, 최대 160Hz가 일치한다. 글로벌 표는 DP 1.4a 한 개, HDMI 2.1 두 개, DP Alt Mode Type-C 한 개를 열거한다. Note는 세 입력 모두 4K 최대 160Hz로 표기하나 모든 색심도·크로마·DSC 조건까지 증명하지 않는다. 설명서 p.8에서 Type-C DP Alt Mode와 최대 65W(20V/3.25A)를 확인했다. p.20에는 SDR 일반 400니트와 HDR 최대 400니트가 구분된다.

높이 조절은 설명서 pp.5,20의 130mm와 글로벌 Adjustment (Height)의 110mm가 실제로 충돌한다. 어느 쪽을 한국 판매 개체의 값으로 채택하지 않는다. 설명서 p.8의 USB-C 데이터 전송 미지원과 p.12의 KVM Type-C USB 입력 선택도 함께 남긴다. 영상·PD 확인을 USB 데이터/KVM 확정으로 확대하지 않는다.

기존 30종 및 구 사이트 모니터 목록에는 이 모델이 없다. MAG 모델, QD-OLED 모델과 병합하지 않는다. 한국어 설명서 표지 3CC2와 문서 V1.1은 한국 유통 SKU 및 하드웨어 리비전의 증명이 아니다.

## BenQ EX2710Q

[한국 제품 사양 URL](https://www.benq.com/ko-kr/monitor/gaming/ex2710q/spec.html)은 최초 제목과 길이 정보만 반환한 뒤 상세 조회가 404로 실패했다. 한국 사양 전체를 읽었다고 기록하지 않는다. [캐나다 공식 표](https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html)의 Display, Connectivity, Dimension and Weight를 직접 확인했다.

27인치 IPS, 2560×1440, 165Hz, HDMI 2.0 두 개와 DP 1.4 한 개를 확인했다. 일반 밝기 250니트와 HDR 최대 400니트, HDR10/DisplayHDR 400, 높이 100mm·기울기 -5~15도·스위블 좌우15도·VESA100×100mm가 기존 CA 자료와 일치한다. 일반 밝기를 SDR 전용 값으로 확장하지 않는다. 단자 목록의 USB-C 미열거는 명시적 미지원과 구분한다.

[영문 타이밍 PDF](https://esupportdownload.benq.com/esupport/LCD%20MONITOR/UserManual/EX2710Q/EX2710Q_RF_EN_210423192728.pdf) 텍스트는 확보했으나 열 위치가 평탄화됐다. screenshot 요청은 이미지 픽셀 대신 참조만 반환하여 표의 입력/색심도 열을 독립 시각 검증하지 못했다. 따라서 전달 자료의 DP165/HDMI144 및 색심도 조건은 이번 확정 목록에 추가하지 않았다. 이는 전달 값이 틀렸다는 판정이 아니다.

## Crossover 27ULD950

[한국 공식 제품 페이지](https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757)의 요약정보에서 27인치 IPS, 3840×2160, 60Hz, 400cd 표기, 높이/기울기/스위블/피벗 기능, VESA75×75mm, USB PD 지원을 재확인했다. 400cd에는 SDR/HDR 또는 typical/peak 수식어가 없다. HTML 요약의 PD 지원과 상품명 PD65는 실제 65W 공급 수치의 독립 근거가 아니다.

[공식 상세 이미지](https://www.crosslcd.co.kr/data/editor/2411/047dd0567fcc29d7226521dd0b0f9f78_1732598597_5708.jpg)는 web 도구가 16,004,212바이트 크기 제한 오류를 반환했다. CUA의 브라우저 목록도 비어 있어 이미지 픽셀을 직접 열람하지 못했다. 파일명·전달 좌표를 읽은 것으로 이미지 사실을 승인하지 않았다.

전달 자료의 DP1.4/1.2 충돌, 높이 `0~110m` 단위 문제, 스위블 ±30/±90도 충돌은 **전달 자료상 충돌·재확인 대기**다. PD65W의 qualifier도 UNKNOWN을 유지한다. mm로 자동 교정하거나 외형 높이 범위로 조절량을 계산하지 않는다. 기존 `content-v2.json`의 `PRODUCT_LABEL_ONLY`, watts UNKNOWN은 그대로 보존할 근거가 있다.

## 사용자 관측 검토

작성자명·본문 전문·사진은 저장하지 않았다. 전달된 개인 경험은 공식 사양, 실측, 독립 구매 인증 또는 공개 승인으로 변환하지 않는다.

| 원문 | 이번 확인 | 판정 |
|---|---|---|
| [MSI DPG 사용기](https://dpg.danawa.com/bbs/view?boardSeq=28&listSeq=5688052) | 페이지 틀과 제목 반환, 핵심 사용기 본문 추출 실패 | 전달 자료 기반으로 남김; 재확인 완료 아님 |
| [MSI Reddit](https://www.reddit.com/r/MSI_Gaming/comments/1dpvepw/mpg_274urf_qd/) | 이번 미열람 | 전달 자료만 검토; 승인 보류 |
| [BenQ 퀘이사존](https://quasarzone.com/bbs/qf_dp/views/522348) | 본문 직접 재확인 | 내장 오디오·자동 밝기 만족, 가격 아쉬움이라는 요약과 일치. 개인 눈 편안함을 의학적 효과로 일반화 금지 |
| BenQ Flipkart 후기 | 이번 미열람 | 해외 SKU·플랫폼 구매 표시·보상 여부 검토 대기 |
| [Crossover 첫 후기](https://quasarzone.com/bbs/qc_user/views/133467) | 본문 직접 재확인 | 맥북 클램쉘, 동봉 C-to-C 영상·충전 개인 보고와 일치. PD 측정 아님; 포인트 수령 기대와 결제금 구분 |
| [Crossover 3주 후기](https://quasarzone.com/bbs/qf_photo/views/919113) | 본문 직접 재확인 | T14 Gen6 AMD, 높이·전원선·피벗·OSD 불편 및 스탠드 만족 요약과 일치. 공식 각도/단위 충돌 해결 근거 아님 |

관련 공개 고지를 발견하지 못한 경우도 비협찬 인증은 아니다. 후기 6건을 독립 구매자 6명 또는 제품 전체 합의로 표시하지 않는다. 이번 직접 본문 재확인은 3건이다.

## 후속 권고

1. MSI는 확인한 문서 범위의 사양만 별도 후보에 연결한다. 두 충돌은 사용자 화면에도 미확인으로 남긴다.
2. BenQ는 기존 CA 출처를 유지하고 KR 페이지·타이밍 표 시각 확인을 후속 검토한다.
3. Crossover 이미지 전용 값은 표시 수치에 반영하기 전에 공식 이미지 직접 시각 검토가 필요하다. 원본이 확보돼도 충돌을 자의적으로 정정하지 않는다.
4. 후기 연결은 정확 모델 및 보상 문맥 검토와 함께 별도로 처리한다. 공개 승인·호환성 판정은 계속 보류한다.
