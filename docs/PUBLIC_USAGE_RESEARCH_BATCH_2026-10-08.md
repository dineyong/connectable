# 공개 실사용 조사 배치 — 2026-10-08

로컬 검토 자료다. 공개 UNKNOWN / 사람 골든 승인 0/30을 유지한다. 정식 코퍼스·official catalog·pilot·golden·판정 엔진·목업에 합치지 않았다. commit/push/PR/배포는 하지 않는다.

## 범위와 산출물

Apple Silicon 맥북의 USB-C/DP/HDMI, 4K60, 독·허브, PD, 클램쉘, 잠자기 복귀, 깜빡임과 30Hz 제한을 조사했다. 공개 본문 확인 사례는 중복 제거 후 **18건(기존 제공 링크 9건 재확인 + 신규 발견 9건)**이다. 같은 글의 댓글·비교 구성·여러 시도는 독립 사례로 세지 않았다. 모든 확인일은 2026-10-08, 단일 작성자 출처 등급은 C다.

[검토용 JSONL 목록](../data/research/review/public_usage_batch_2026-10-08.jsonl)에 사례별 URL·게시일·확인일·근거 위치·호스트·칩·OS·경로·개별 관측·수행 변경·상업성·결측을 저장했다. 이는 **정식 v2 코퍼스가 아닌 REVIEW_ONLY 연구 목록**이다. 미기재 SKU·길이·픽셀·OS·HDR·전원·덮개 조건은 UNKNOWN이며, 알려진 조건은 author_observations 또는 reported_paths에서 원문 범위 그대로 설명한다. 상세 객체별 재구조화와 모델·결과 최종 검수는 미완료다. 게시일은 직접 보인 날짜이며 검색의 상대 발행일과 다를 수 있다.

본문을 확인했다는 뜻은 작성자의 진술을 확인했다는 뜻이다. 연구자가 실물을 재현했거나 제조사 공식 호환성이 검증됐다는 뜻이 아니다. 전체 본문·댓글·자막·스크린샷·닉네임·이메일·판매 제휴 URL은 저장하지 않았다.

## 플랫폼별 조사 커버리지와 제한

| 플랫폼 | 시도 | 결과 / 포함 건수 |
|---|---|---|
| 네이버 검색 | M1 V32UE 코드웨이 조합 검색 URL 직접 열기 및 외부 검색 엔진의 관련 검색 | 네이버 검색 URL은 이 도구에서 접근 불가. 네이버 자체 검색 결과 본문을 확인했다고 주장하지 않는다. 0건 |
| 네이버 블로그 | M1 4K60/깜빡임 검색, 발견한 공개 PostView 글 열기 | robots.txt 및 restricted URL 오류. 재시도·다른 호스트·프록시 우회 안 함. 0건. 퀘이사존 재게시의 Naver 출처는 별개 사례로 미계수 |
| 네이버 지식인 | M1 30Hz/클램쉘 검색, 공개 질문 링크 열기 | restricted URL 오류. 검색 요약의 질문/답변은 검증 사례에서 제외. 0건 |
| 쿨앤조이 | 맥북 M1 모니터 관련 검색, 홈페이지 및 검색에서 나온 글 열기 | 관련 결과 부족. M1 mini 프로젝터 등 동명이물 검색 오염 확인. 홈페이지·프로젝터 글 timeout. 0건. 사이트 전체 접근 불가능 또는 관련 사례 없음이라고 일반화하지 않음 |
| 퀘이사존 | 기존 링크 6건 및 MH510·PD2307 후기 2건 개별 열기 | 공개 본문 확인 8건. 댓글과 본문이 함께 보이는 경우 작성자 여부 분리. 화면 출력 결과가 없는 판매 소개는 배제 |
| 유튜브 | M1 허브/4K60 검색, 공개 검색 URL 및 발견한 watch URL 열기 | 검색 URL throttled, watch 페이지 fetch 오류. 실제 시청·자막·타임스탬프 확보 못함. 0건. 제목·썸네일로 관측 생성 안 함 |
| 허용 대체 출처 | Tistory·개인 블로그 개별 원문 열기 | Tistory 8건 + 개인 블로그 2건. 대량 크롤링 없음 |

접근 오류는 도구와 조사 시점의 상태다. 삭제·로그인 필수라고 단정하지 않는다. 수량 목표 15~25를 충족했으나 플랫폼 대표성은 부족하다. 사이트별 성공률·모델 불량률을 계산하지 않는다. 독립 사용자의 동일 조합 재현 여부도 아직 확인하지 않았다.

## 우선 조합 조사 결과

M1 Air + 주연테크 V32UE + 코드웨이 USB4 C-C 240W/40Gbps 표기 케이블을 우선 검색했다. 세 구성품이 모두 명시된 독립 공개 본문은 확보하지 못했다. PUR-001은 **M1 Air + V32UE의 C-C 영상/충전** 진술이 있지만 코드웨이 SKU·길이·60Hz는 없다. 정확한 사용자 조합의 검증으로 승격하지 않는다.

쇼핑 검색에는 1.2m 상품 옵션이 나타났지만 그것은 실제 보유 케이블 식별 근거가 아니다. **사용자 케이블 길이는 UNKNOWN**으로 유지한다. USB4/40Gbps/240W 광고 표기도 실제 영상 모드·협상 전력·인증·포트 호환 보장으로 변환하지 않는다.

## 사람이 검토할 사례 요약

각 ID는 위 검토 JSONL의 상세 근거와 연결한다. 결과는 기능별 관측이고 정식 outcome 승인이나 FAILURE 분류가 아니다. 원글 본문과 작성자 댓글을 같은 사건으로 다루며 타인의 조언은 변경 후 성공 근거로 쓰지 않는다.

| ID / 발견 | 원문 / 게시일 | 관측과 분리할 사항 |
|---|---|---|
| PUR-001 기존 | [V32UE](https://makeany.tistory.com/97), 2021-12-22 | M1 Air C-C 영상·충전 사용. 3008×1692 설정은 전송 픽셀/60Hz 측정 아님 |
| PUR-002 기존 | [M7 43인치](https://quasarzone.com/bbs/qc_user/views/109876), 2022-02-12 | C-C 불안정/미연결 → SOHO Dock HDMI 정상 진술. 모델 전체 불량 주장 채택 안 함 |
| PUR-003 기존 | [M7 비교 구성](https://quasarzone.com/bbs/qf_dp/views/369236), 2022-08-23 | M1 직접 C-C/C-HDMI 정상, SSD 허브 경로 무출력. Windows 비교 구성·원격 우회 별도 |
| PUR-004 기존 | [M2 30Hz](https://quasarzone.com/bbs/qf_dp/views/383048), 2022-11-05 | Belkin 허브 HDMI 최대30Hz. 작성자 구매 예정 댓글만 있고 교체 후 성공 없음 |
| PUR-005 기존 | [27ULD950 깜빡임](https://quasarzone.com/bbs/qf_dp/views/515378), 2024-10-12 | M2 Pro/Windows·HDMI/C-C·Hz/HDR 변경에도 증상 지속. 원인과 종결 실패 미확정 |
| PUR-006 기존 | [27ULD950 후기](https://quasarzone.com/bbs/qc_user/views/133467), 2024-11-25 | 클램쉘 영상·충전 정상. Mac 칩 미상, 포인트·구매권유 검토 필요 |
| PUR-007 기존 | [Belkin INC013qc](https://quasarzone.com/bbs/qf_etc/views/109078), 2025-01-15 | MSI 직접 정상/독 경유 미인식, LG 비교 정상. 혼합된 M4 모델 표기 보존 |
| PUR-008 기존 | [UGREEN 교체](https://gorisebuck.tistory.com/187), 2022-12-10 | M1 Baseus 4K30·복귀 문제 → UGREEN 4K60·복귀 정상 진술. 클램쉘 전환 해상도는 EasyRes 대응 |
| PUR-009 기존 | [Monterey 임시 우회](https://node-js.tistory.com/31), 2022-01-09 | M1 Air 12.1 깜빡임 → 미러링 ON/OFF 임시 정상. 재연결·재부팅마다 반복 필요 |
| PUR-010 신규 | [U28E590D](https://jinibh.tistory.com/entry/맥북-듀얼모니터-사용하기-m1-맥북에어-4k-60hz-모니터-연결), 2022-01-23 | M1 초기4K60 미출력, HDMI 입력 번호 차이 설명. 소개한 Apple 어댑터 구매/성공은 미확인 |
| PUR-011 신규 | [HDMI 60→30](https://jintograph.tistory.com/43), 2023-09-27 | 원문 M1 16인치 표기 모순 가능성 보존. 재연결로4K 선택, 30Hz에서 깜빡임 없어짐 |
| PUR-012 신규 | [Artmu MH510](https://quasarzone.com/bbs/qc_user/views/124657), 2023-09-03 | M1 Air DP 영상·동시충전 사용 진술. 최대3화면·100W 상품 수치를 본인 측정으로 미채택 |
| PUR-013 신규 | [Spigen PD2307](https://quasarzone.com/bbs/qc_user/views/125766), 2023-11-12 | M1 Pro 모니터3대 일부 복제. 독립3대 아님. PD90/96W 혼재·Naver 재게시·행사 링크 검토 |
| PUR-014 신규 | [MSI MD271UL](https://seook.tistory.com/m/entry/맥북-4K-모니터-추천-MSI-MD271UL-4K-듀얼-모니터-실제-사용-후기), 2026-01-18 | M2 Air 호환 케이블 깜빡임→Belkin 교체 후 정상 진술. 제휴 고지 있음. 현재 Mac mini 2대 구성과 분리 |
| PUR-015 신규 | [DisplayLink](https://yelobean.tistory.com/80), 2021-09-04 | M1 Air DL 설치 후 외장2대·FHD60 진술. 네이티브 성공으로 저장 안 함 |
| PUR-016 신규 | [UGREEN 4K60](https://mib428047.tistory.com/entry/macbookairm1usbchub4k60hz), 2021-12-20 | 기존허브4K30→새 UGREEN4K60 진술. 정확한 SKU·길이·픽셀 미상 |
| PUR-017 신규 | [IP2730 FHD120](https://blog.notepads.kr/182), 2021-02-02 | M1+UGREEN HDMI FHD120 정상/144 검은 화면. 작성자 대역폭 계산을 공식 원인으로 채택 안 함 |
| PUR-018 신규 | [UGREEN 일체형 허브](https://itnmobile.net/76), 2021-03-02 | M1 Air 케이스 간섭, 제거 후 사용 정상. 포트별4K60/30은 소개 수치. 물리 장착과 영상 결과 분리 |

18건 모두 C등급·DIRECT_CHECK·NO(호환성 재사용)다. 기본 목표와 완전히 동일한 실측 4K60 승인 사례 18건이라는 뜻이 아니다. 화면 성공, 일부 제한, 미해결, 임시 우회가 섞인 연구 표본이다. 정확한 SKU·길이가 대체로 비고 상세 OS는 PUR-009 외 대부분 미상이다. PUR-006·007·011·017은 특히 호스트 모델 최종 식별 검수가 필요하다.

## 검증 사례에 넣지 않은 리드와 보조 자료

| URL | 확보 범위 | 처리 |
|---|---|---|
| [네이버 지식인 클램쉘](https://m.kin.naver.com/qna/dirs/1010401/docs/478449448?d1id=1) | 검색 발췌, 직접 본문 restricted | LEAD_ONLY. 답변 주장·해결 여부 미채택 |
| [네이버 블로그 보조배터리 글](https://blog.naver.com/PostView.naver?blogId=itshare23&logNo=223422631749) | 검색 발췌, robots 제한 | LEAD_ONLY. 모니터 경로도 불충분 |
| [유튜브 M1 액세서리](https://www.youtube.com/watch?v=_0ROSmU95No) | 검색 제목·설명 발췌, watch fetch 오류 | LEAD_ONLY. 타임스탬프·관측 없음 |
| [유튜브 액세서리 소개](https://www.youtube.com/watch?v=3YeUADO8YIE) | 검색 결과만 | LEAD_ONLY / 본문 열기 미시도. 검증 사례 미계수 |
| [쿨앤조이 M1 mini](https://coolenjoy.net/bbs/copy_preview/170645) | 검색 결과, 직접 열기 timeout | 범위 밖 프로젝터, Mac M1과 혼동하지 않음 |
| [블로그 일반 가이드](https://archivers.tistory.com/77) | 본문 확인, 2020-08-17 | 구체적 본인 경로·결과 부족 및 Apple Silicon 이전 글. 사례 미계수 |
| [LG32UD59 설정](https://gorisebuck.tistory.com/100) | 본문 확인, 2020-10-14 | AMD/Windows 시점의 인접 사례. PUR-008의 Mac 경로로 합치지 않음; 별도18건에 미계수 |
| [UGREEN No PD 후기](https://blime.tistory.com/991) | 본문 확인, 2021-06-19 | 모든 포트 정상이라는 포괄 진술만 있어 구체적 영상 모드 근거 부족.18건에 미계수 |
| [M1 독 개요](https://itnmobile.net/87) | 본문 확인, 2021-03-23 | PUR-018과 같은 블로그의 관련 구매·사용 설명. 중복/연속 사건 가능성이 있어 추가 독립 사례로 미계수 |
| [M1 스탠드·모니터 글](https://chunchu.tistory.com/2008) | 검색 발췌, 도구 접근 불가 | LEAD_ONLY |

공개 본문이 읽힌 자료만 포함하고, 검색 엔진이 원문 전체처럼 긴 발췌를 제공하더라도 direct open이 실패하면 검증 사례에 포함하지 않았다. 플랫폼 제한을 우회하거나 제3자에게 연락·댓글·로그인하지 않았다.

## 반복되는 문제와 Connectable 적용

1. **모니터 제품명만으로 경로가 결정되지 않는다.** 직접 C-C, C-HDMI, 독·허브를 통한 경로의 관측을 구성별로 분리해야 한다(PUR-002·003·007).
2. **30Hz 제한과 60Hz 안정성은 별개다.** 60Hz 선택 자체가 불가능한 경우와 선택 후 깜빡이는 경우를 나눠 기록한다(PUR-004·011·016). 낮춰서 안정화는 원래60Hz 목표 달성으로 표시하지 않는다.
3. **케이블 교체 뒤 정상과 케이블이 원인이었다는 증명은 다르다.** 동일 제품군·40Gbps 표기·길이 추정만으로 원인을 확정하지 않는다(PUR-001·005·014).
4. **영상·충전·잠자기 복귀는 독립 기능이다.** 영상 정상이라도 전력·OSD 충전 설정·복귀 결과가 미상일 수 있다(PUR-008·012·014). 실제 공급 와트와 상품 최대값 분리 필요.
5. **덮개 전환·재연결의 시간 조건이 중요하다.** 영구 해결과 매번 재실행하는 우회를 구분한다(PUR-008·009). 최초/변경후/재발 관측을 연결해야 한다.
6. **화면 수·복제·DisplayLink를 섞으면 과대 판정이 발생한다.** 물리3대가 독립3대는 아니며 DL 성공은 네이티브와 별개다(PUR-013·015). 모르는 대수는 UNKNOWN 유지.
7. **배율과 전송 타이밍은 다른 정보다.** 3008×1692 또는 QHD 설정 표기를 실제 전송 픽셀로 덮어쓰지 않는다(PUR-001·014). 4K 영상 재생도4K60 신호 측정이 아니다.
8. **장착 간섭·상업성·모델 혼합이 검수에 영향을 준다.** 케이스 때문에 포트가 맞물리지 않는 문제도 있고, 판매 후기에는 실제 결과와 최대 사양 홍보가 공존한다(PUR-006·011·012·018).

이는 반복 주제의 질적 관찰이다. 시장 빈도·고장률·성공 확률·통계적 원인을 의미하지 않는다.

## 기존 v2로 표현 가능한 항목과 최소 개선 제안

| 정보 | 현재 표현 | 제안 / 적용 여부 |
|---|---|---|
| 소스·모니터·허브·케이블과 부분 경로 | nodes/ports/configurations + UNKNOWN_GAP | 충분함. 실제 수행 구성만 OBSERVED, 구매계획·조언은 별도 유지 |
| 비교 구성·복제·DL·클램쉘·HDR | 구성·환경·counts/display_state·객체 evidence_refs | 충분함. 모호한 수치는 생략하고 notes에 보존 |
| 변경후 정상·임시 우회·재발 | attempts/observations·durability·recurrence_of | 충분함. 기간 미명시는 장기 성공으로 만들지 않음 |
| 명시적 특정 구성 사용 포기 | configuration_conclusions + 작성자 종결 근거 | 기존 구조 사용. 단순 검은 화면을 FAILURE로 만들지 않음 |
| 상업적 후기 | review.commercial_context | 충분함. 제공·제휴 고지 없음은 광고 없음과 다름 |
| 배율·신호·렌더링 픽셀 | 현재 display_state의 해상도 + notes | **최소 후보:** resolution_role(enum: SIGNAL/UI_SCALE/RENDERED/UNKNOWN) 또는 별도 ui_scale 객체. 우선 notes를 쓰고 자동 숫자 정규화 금지. 이번 변경 안 함 |
| 기능별 영상/충전/복귀/오디오 결과 | 현재 관측 요약·notes로 보존 가능 | **최소 후보:** observation_domain enum 도입을 검토. 수전 와트는 실측/협상/상품상한 구분 필요. PD 계산 모델과 섞지 않음. 변경 안 함 |
| 유튜브 근거 위치 | evidence.location 자유문장으로 타임스탬프 기록 가능 | 나중에 video_time_start/end와 캡션 종류 선택 필드 검토. 이번엔 영상 근거가 없으므로 스키마 확장 불필요 |
| 재게시·후속글 의미 중복 | URL 중복 검사 + 사람 검수 | 이번엔 보조 리드로 묶음. 향후 related_case_ref/dedup_reason 검토, 개인 식별자 저장 금지 |

18건을 v2에 즉시 넣거나 현재 스키마를 바꾸지 않는다. 해석이 필요한 정보는 별도 연구 표본에 두고 상세 v2 변환·사람 검수 후 추가 여부를 결정한다. 이 조사는 저장소의 근거 자료를 늘린 것이며 모델 자체의 영구 학습이 아니다.

## 다음 최소 개발 작업

1. 검토 자료 입력·표시에서 **미확인 / 작성자 진술 / 공식 근거 / 실물 재현** 상태를 독립 표시하고, 구매계획·조언이 관측으로 들어가는 것을 막는 회귀 검사를 만든다.
2. 해상도 입력에서 **배율과 신호 모드**를 구분하는 작은 스키마 제안을 먼저 검토한다. 그동안 요약 notes를 그대로 보존한다.
3. 사용자의 M1 Air·V32UE·코드웨이 실물 정보를 확보해 케이블 SKU·길이·실제 Hz·PD·잠자기 복귀를 각각 확인하는 한 조합 체크리스트를 만든다. 외부 공개 사례가 사용자 실물 테스트를 대체하지 않는다.

## 검증 기록

신규 검토 목록의 UTF-8/LF JSONL, 18개 ID·정규화 URL 중복, 필수 검토 메타데이터·날짜·URL·개인정보/비밀 패턴, 문서 내부 링크, 기존 원본 바이트 보존을 검사한다. 정식 v2 스키마 검사 대상이 아니므로 REVIEW_ONLY 목록이 v2 검증을 통과한다고 표현하지 않는다. 기존 전체 테스트와 기존 데이터 검증은 별도 실행하여 결과를 아래에 기록한다.

실행 결과: `python3 -m unittest discover -s tests -q` **236개 통과**. 위 목록 검사 전부 통과. 작업 시작 스냅샷 대비 추적 중인 data/schema/mockup 15파일 바이트 보존. 데이터·스키마·UI 코드 수정과 새 테스트 추가는 없으며 문서/별도 연구 목록만 생성했다. 개인정보 패턴 검사는 사람이 요약을 검수하는 절차를 대체하지 않는다.

기존 검증 실행: `python3 scripts/validate_question_corpus.py`, `python3 scripts/validate_question_corpus_v2.py`, `python3 -m scripts.validate_official_products`, `python3 scripts/validate_connection_model_pilot.py`, `python3 scripts/path_instance_v1.py --check`, `git diff --check` 모두 통과했다. PUR-014는 M2 Air 소개와 현재 Mac mini 구성이 한 글에 있어 케이블 교체 시점의 호스트 바인딩도 검수 대기로 남긴다.
