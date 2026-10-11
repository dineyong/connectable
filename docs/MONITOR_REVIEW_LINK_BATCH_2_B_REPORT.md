# 외부 후기 링크 배치 2 — 조사 세션 B

확인일: 2026-10-11. [제품 방향](PRODUCT_DIRECTION_V3.md)과 [세션 공통 규칙](PROJECT_SESSIONS.md)을 따른다. 원본 제품 데이터와 화면은 수정하지 않았다. 확인한 후보는 [통합 링크 원본](../data/research/monitor-review-links.json)에 통합했다.

## 결과와 확인 범위

대상 15제품 중 10제품의 신규 링크 10건을 확인했다. YouTube 8건, Blog 2건이며 전문 리뷰 9건·개인 사용기 1건이다. 영상은 공개 원문 제목·펼친 설명·리뷰 챕터·광고/제휴 고지를 직접 확인했다. 영상 전체를 시청하거나 시험 결과를 재현한 것은 아니다. YouTube의 자동 생성 요약과 검색 요약으로 제품 사양·실사용 결론을 채우지 않았다. 기존 한국 SKU·공식 사양 검토 상태는 유지한다.

| 대상 모델 | 결과 | 원문 | 모델 및 내용 확인 위치 |
|---|---|---|---|
| 27GP850-B | 포함 | [영상](https://www.youtube.com/watch?v=gMqm4vzCDVM) | 실제 원문 제목·펼친 설명에 -B 포함, 리뷰 소개 및 제휴 고지 |
| 27GR83Q-B | 보류 | [영상 후보](https://www.youtube.com/watch?v=IEv895dnoVY) | 실제 원문 제목·설명에는 27GR83Q만 명시. -B와의 동일성을 추정하지 않음 |
| 27GS95QE-B | 포함 | [영상](https://www.youtube.com/watch?v=rJB0Or1MLiw) | 실제 원문 제목에 -B 포함, 개봉·게임·설정 챕터 및 제휴 고지 |
| 32GS95UE-B | 포함 | [영상](https://www.youtube.com/watch?v=vDtBjH2g_G8) | 설명의 테스트 모델 LG 32GS95UE-B 및 시험 챕터 |
| 27UP850K-W | 제외/보류 | [확인한 후보](https://www.techeblog.com/lg-27up850k-w-ultrafine-4k-monitor-review-deal/) | 원문은 할인 상품 소개와 타인 후기 인용 중심. 작성자 본인 사용 근거 부족 |
| 34WQ75C-B.AUS | 접근 실패/보류 | [영상 후보](https://www.youtube.com/watch?v=PA0JGJmm2js) | 검색 발견 후 원문 도구가 CAPTCHA 페이지를 반환. 우회하지 않음. 검색 요약을 수집 데이터로 사용하지 않음 |
| Modern MD271UL | 포함 | [영상](https://www.youtube.com/watch?v=z_enSOWesWs) | 제목·설명에 Modern MD271UL이 직접 명시되어 별칭 추정 불필요 |
| MAG 274QRF QD E2 | 포함 | [영상](https://www.youtube.com/watch?v=6kZnaRwYsfM) | 제목·설명에 E2 포함, 색상·HDR·응답 챕터 및 제휴 고지 |
| MPG 321URX QD-OLED | 포함 | [영상](https://www.youtube.com/watch?v=uohrgsUX07o) | 설명의 테스트 모델 MPG 321URX QD-OLED 및 시험 챕터 |
| M27Q rev.1.0 | 포함 | [전문 블로그](https://pcmonitors.info/reviews/gigabyte-m27q/) | Specifications에 해당 리뷰가 Rev 1.0이라는 설명. Rev 2.0은 다른 패널로 별도 구분 |
| M28U | 포함 | [영상](https://www.youtube.com/watch?v=qttvOMM3C1w) | 설명의 Model tested: M28U 및 시험 소개·제휴 고지 |
| M32U | 포함 | [개인 블로그](https://tylee82.tistory.com/346) | 본문 직접 구매·설치·연결 점검·사용 중 단점. 광고/제휴 여부는 UNKNOWN |
| Q27G3XMN | 포함 | [영상](https://www.youtube.com/watch?v=kYwV_1bIJ4g) | 설명의 Model Tested: Q27G3XMN 및 시험 챕터 |
| S32CG554EU (LS32CG554EUXEN) | 보류 | 확인 가능한 후보 원문 미확보 | 정확한 전체 지역 SKU 후기 검색에서 직접 검토할 후보 미확보 |
| S65UC (LS34C650UEEXXY) | 보류 | 확인 가능한 후보 원문 미확보 | 정확한 전체 지역 SKU 후기 검색에서 직접 검토할 후보 미확보 |

## 접근·광고·모델 위험

- web 원문 도구의 YouTube 접근은 여러 건 Internal Error였으나 CAPTCHA를 반환하지 않은 후보는 일반 브라우저의 공개 페이지로 확인했다. 34WQ75C-B.AUS 후보의 CAPTCHA는 그대로 중단했다.
- 포함한 YouTube 8건과 PC Monitors 전문 블로그는 원문의 제휴/수익 고지를 확인하여 `commercial_context=PRESENT`로 기록한다. M32U 개인 블로그는 광고/제휴 없음으로 판정하지 않고 `UNKNOWN`을 유지한다.
- `checked_model`은 전체 현재 제품명과 일치시키고, LG 접미사·Gigabyte 리비전·MSI E2 및 Modern을 생략한 원문을 임의 동치 처리하지 않았다.
- 해외 모델 리뷰의 존재는 한국 판매 SKU 동일성·국내 보증·호환성 승인이 아니다. 후기 내용을 공식 사양으로 복사하지 않는다.
- 본문·영상 전체·이미지·썸네일·작성자명·연락처를 저장하지 않는다. Tistory의 URL 식별 부분은 원문 접근에 필요한 주소로만 유지한다.

## 검증과 편집 경계

후보 파일은 JSON 구문 검사 및 ID·URL 중복 검사를 통과했다. 최종 데이터 통합, 참조 검증, 새 탭 동작·전체 테스트·push·CI는 통합 세션에서 수행한다. 기존 공식 사양, 질문 코퍼스, 승인 정책 및 화면 파일은 이 조사 세션에서 수정하지 않았다. 생성한 임시 조사 브라우저 탭은 닫았으며 사용자 localhost 탭은 보존했다.
