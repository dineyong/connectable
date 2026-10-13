# 외부 후기 링크 배치 5 — Samsung 지역 SKU 조사

확인일: 2026-10-13. [직전 Samsung 조사](MONITOR_REVIEW_LINK_BATCH_4_SAMSUNG_REPORT.md)와 [플랫폼 검증 계약](MONITOR_REVIEW_LINK_PLATFORM_REPORT.md)을 확인했다. 모델별 신규 검색 3조합과 신규 유망 원문 2개씩으로 범위를 제한했다. 기존에 제외하거나 접근 실패한 후보는 다시 열지 않았다.

## 조사 결과

| 제품 | 결과 | 판단 |
|---|---|---|
| S32CG554EU / LS32CG554EUXEN | 직접 확인된 공개 포럼 원글 1건을 통합 후보로 전달 | 전체 SKU와 작성자 본인 구매·사용 관측이 함께 확인됨. 긍정 추천이 아니라 잔상 문제 관측 사례 |
| S65UC / LS34C650UEEXXY | 추가 보류 | 신규 발견은 판매점 고객 후기 모음이며 독립적인 YouTube·블로그·전문 리뷰 원문을 확보하지 못함 |

검색 조합은 XEN 모델의 `tested`, `review youtube`, `blog OR unboxing OR test`, XXY 모델의 `review`, `youtube monitor experience`, `tested OR experience OR unboxing`이며 이전 제외 사이트를 배제했다. 검색 제목과 요약은 발견에만 사용하고 원문 데이터로 저장하지 않았다.

## 원문별 확인과 처리

| 신규 원문 | 직접 확인 위치·접근 결과 | 처리 |
|---|---|---|
| [ComputerBase 원글](https://www.computerbase.de/forum/threads/samsung-odyssey-g55c-ghosting-ls32cg554euxen.2214872/) | 공개 제목·2024-10-23 원글 #1에서 LS32CG554EUXEN 전체 표기, 구매 2일 뒤 본인 사용, CS2 및 검은 배경의 잔상, 실제 설정 목록 확인 | 정확 SKU와 직접 사용 관측 확인. `Forum`·`FIRST_HAND_REVIEW` 후보. 블로그로 오분류하지 않음. 타인의 패널·교체 조언은 실제 수행·결과로 사용하지 않음 |
| [Reddit 후보](https://www.reddit.com/r/Monitors/comments/1jp9zsf) | 직접 열기 `TimeoutError` | 원문 재확인 불가. 검색 결과 내용은 사용하지 않고 제외 |
| [PB Tech 신규 발견 고객 후기 경로](https://www.pbtech.co.nz/product/MONSAM42265/help/article/38/returns/product/MONSAM42265/review) | 직접 열기 `Internal Error` | 해당 경로 원문 확인 불가. 접근 우회 없음 |
| [PB Tech 제품 페이지](https://www.pbtech.co.nz/product/MONSAM42265/Samsung-ViewFinity-S65UC-34-Ultrawide-QHD-1000R-Cu) | 공개 MPN에 LS34C650UEEXXY 확인. Reviews에 AI 종합과 개별 작성자의 설치·노트북 연결·다중 문서 사용 댓글이 별도로 존재함을 확인 | 모든 후기가 AI라는 이유로 제외한 것이 아님. 판매점 고객 후기 모음이고 개별 댓글 자체에는 전체 SKU가 명시되지 않아 이번 독립 후기 링크 범위에서 보류. 제품 페이지 MPN을 댓글의 직접 SKU 확인으로 승격하지 않음 |

ComputerBase 하단에는 사이트 광고 배너 운영 고지가 있다. 후보의 `commercial_context=PRESENT`는 사이트 광고 표시 의미이며 작성자 협찬·제휴를 확인했다는 뜻이 아니다. 원글의 문제 관측은 제품 추천·일반적 품질 판정·최종 사용 포기·공식 호환 승인으로 변환하지 않았다.

## 전달과 범위

신규 후보 1건은 통합 세션에 전달했다. 새 `Forum` 유형의 정확 URL·제품 바인딩과 새 창 표시는 통합 세션에서 최소 보강·검증한다. 원본 제품 사양·기존 후기·UI·Git은 이 조사 세션에서 변경하지 않았다. 임시 브라우저 탭을 생성하지 않았고 로그인·차단 우회도 하지 않았다. 사용자명·닉네임·이메일·사진·본문 전체·별점은 저장하지 않았다.

S65UC는 보류를 유지하며, 미연결 상태는 제품 실패나 부정적 평가를 의미하지 않는다. 전체 테스트·보존 검사·GitHub push·CI 결과는 통합 보고서에서 기록한다.
