# 공개 사례 18건 원문 의미 검수

2026-10-08 · 로컬 `research/question-corpus-foundation` · 기준 HEAD `52a8bc3`.

## 결과와 승인 경계

18개 기존 URL을 개별 열어 공개 본문을 다시 확인했다. **일치 10건 / 교정 8건 / 본문 재확인 불가 0건**이다. 일치는 기존 요약의 핵심 범위가 현재 본문과 맞는다는 AI 검토 결과이며 완전성·사람 승인·공식 호환성이 아니다. 특정 근거의 재확인 한계는 아래에 별도로 기록했다.

18건 모두 C등급·REVIEW_ONLY·NEEDS_REVIEW·usable_for_compatibility=NO·공개 UNKNOWN·승인 골든0/30을 유지한다. 정식 코퍼스·catalog·pilot·Path Instance·판정 엔진에 편입하지 않았다. 신규 사례 수집, 공식 사양 대조, 실물 재현, 외부 게시·commit·push·PR·merge·배포·삭제는 수행하지 않았다.

검토 자료:

- [보존한 원본 조사 18건](../data/research/review/public_usage_batch_2026-10-08.jsonl)
- [교정한 검토 매핑 18건](../data/research/review/public_usage_mapped_2026-10-08.jsonl)
- [이전 매핑 보고서](PUBLIC_USAGE_REVIEW_MAPPING_REPORT.md)와 [화면 연결 보고서](PUBLIC_USAGE_REVIEW_UI_REPORT.md)는 당시 작업 기록으로 보존
- [검토 검사기](../scripts/validate_public_usage_review.py), [회귀 테스트](../tests/test_validate_public_usage_review.py)
- [정적 표시 어댑터](../scripts/build_public_usage_review_ui.py), [표시 데이터](../web/review-data.js), [화면 동작](../web/review-app.js), [브라우저 테스트](../tests/e2e/review.spec.js)

## 방법과 근거 이력

검색 요약을 사용하지 않고 기존18건의 직접 URL 본문을 열었다. 로그인·403·robots 제한 우회, 프록시·다른 호스트 재시도, 판매 링크 열기·구매는 하지 않았다. 이번18개 본문에는 접근 실패가 없었다. 원문 전체·댓글·이미지·닉네임을 저장하지 않고 위치와 짧은 사실 요약만 기록했다. 원문에서 보이는 댓글 작성자 표시는 동일 글의 역할을 확인하는 데만 사용하고 저장하지 않았다.

기존 조사 자료의 `source_line_sha256`과 source URL/날짜는 그대로 보존했다. `mapping_basis=EXISTING_REVIEW_SUMMARY`는 최초 매핑의 기반을 뜻한다. 이번 재확인은 검토 외곽의 선택 객체 `semantic_review`로 구분한다. status는 AI_MATCHED/AI_CORRECTED/UNVERIFIED, 확인일·같은 원문 URL·접근 여부·본문/작성자 댓글/추가 본문 위치·검토 메모를 담는다. 정식 v2 스키마 필드나 승인 상태를 추가한 것이 아니다.

새 근거와 교정 근거는 `/semantic_review/locations/N`에 연결하고 DIRECT_CHECK 확인일·kind·actor를 검사한다. 원본 행 해시는 최초 조사 기반의 불변성을 확인하며 새 근거까지 원본에 있었다는 뜻이 아니다. 새로운 근거에 원문 재확인 기록이 없거나 접근 실패라면 검증이 거부한다. 기존 원문 확인 이력은 신규 확인으로 일괄 덮어쓰지 않았다.

게시일·댓글 작성일·추가 작성일·관측일을 구분했다. 현재 본문만으로 과거 수정 이력과 정확한 관측 날짜를 복원하지 않는다. 글의 날짜를 실물 시험 날짜로 사용하지 않는다. 타인의 원인 설명·교체 권고·환불 결과는 작성자의 수행/결과가 아니다.

## 18건 대조표

아래 수정 전은 이전 매핑/화면의 의미 요약, 수정 후는 이번 검토 결과다. 모든 링크는 기존 원문이며 별도 사례로 추가하지 않았다.

| ID / 원문 | 결과 | 수정 전 → 현재 처리 / 근거 위치 | 남은 기능별 경계 |
|---|---|---|---|
| [PUR-001](https://makeany.tistory.com/97) | 교정 | 케이블 표시명 UNKNOWN → 동봉 USB-C 사용 표기 추가. 좋은점2·3, 케이블 사진 설명 | SKU·길이·실제 Hz 미상. 포장의60Hz·65W를 측정값으로 채우지 않음.3008×1692는 보기 설정 |
| [PUR-002](https://quasarzone.com/bbs/qc_user/views/109876) | 일치 | C-C 초기 불안정→미연결 / SOHO HDMI 정상 유지. 본문0·2·4·6 | 반품·AS 경위나 다른 기기 비교를 모델 전체 결함으로 사용 안 함. 충전·Hz·복귀 미상 |
| [PUR-003](https://quasarzone.com/bbs/qf_dp/views/369236) | 교정 | 초기 PC HDMI 무출력만 기록 → 2022-08-29 09:49 작성자 후속 댓글의 얕은 HDMI 삽입 설명을 별도 근거·진술로 추가 | 최종 UHD 점등·Hz 확인 없음. 초기 무출력을 정상으로 덮어쓰지 않음. 타인의 전원 재연결 성공은 미혼합 |
| [PUR-004](https://quasarzone.com/bbs/qf_dp/views/383048) | 교정 | 점등 UNKNOWN / 최대30Hz 선택만 → 사용 중 끊김 느낌을 VIDEO_OUTPUT PROBLEM으로 보존. 본문·작성자14:09/14:20 댓글 | Hz는 계속 SELECTABLE_LIMIT. 실제 타이밍 미측정. 허브 교체는 구매계획, 답변 채택은 교체 성공 아님 |
| [PUR-005](https://quasarzone.com/bbs/qf_dp/views/515378) | 교정 | Mac으로 묶인 USB-C 비교 → 소스 UNKNOWN 노드·구성으로 분리. Windows HDR 두 상태 결과 미상 → 모두 같은 증상 진술 보존. 본문 시도 목록 | 개별 설정 순서·타이밍 미상. 타인의38인치 보드 문제·환불을 작성자 결과로 사용 안 함 |
| [PUR-006](https://quasarzone.com/bbs/qc_user/views/133467) | 일치 | 번들 C-C 클램쉘 영상·충전 보고 유지. 본문 연결 후기·영상 사진 설명 | Mac 칩 미상.4K 콘텐츠와 신호Hz 분리. 포인트·구매권유 검토 유지 |
| [PUR-007](https://quasarzone.com/bbs/qf_etc/views/109078) | 일치 | MSI 직접 정상 / INC013qc 경유 미인식 / LG 비교 정상 유지. 본문·작성자 프로필 댓글 미리보기 | 혼합 M4 프로 맥스 표기는 프로필 미리보기에서만 재확인. 해당 댓글 전체 미확보, 정확한 칩UNKNOWN. 클램쉘 듀얼은 목표 |
| [PUR-008](https://gorisebuck.tistory.com/187) | 교정 | UGREEN7 결과 미확인 → 재구매 단락의 연결 정상 관측1개 추가 | 6-in-1의4K60·복귀 정상은7-in-1로 전파 안 함.7-in-1 Hz·PD·복귀UNKNOWN. EasyRes의 정확한 시행 경로 미상 |
| [PUR-009](https://node-js.tistory.com/31) | 일치 | 미러링ON/OFF 임시 정상·재연결/재부팅 뒤 재발 유지. 기기정보·임시 해결 단락 | 모니터·포트·케이블 미상. 영구 해결·복귀 정상으로 승격 안 함 |
| [PUR-010](https://jinibh.tistory.com/entry/맥북-듀얼모니터-사용하기-m1-맥북에어-4k-60hz-모니터-연결) | 일치 | 초기4K60 문제 / Apple 어댑터·HDMI2 설명 분리 유지. 초기 연결·포트 순서 단락 | 문제는 목표모드 미확보이고 완전 무신호 확정이 아님. 최종 전체 경로·Hz·어댑터 구매 미확인 |
| [PUR-011](https://jintograph.tistory.com/43) | 일치 | HD선택→재연결4K선택→60Hz설정 깜빡임→30Hz설정 안정 유지 | M1 16인치 원문 표기 유지. 선택값과 측정 타이밍 구분. C-HDMI교체는 조언 |
| [PUR-012](https://quasarzone.com/bbs/qc_user/views/124657) | 일치 | M1Air HOST C-C→MH510→DP / 별도PD IN / 충전 유지. 본인 사용 단락 | 상품 최대3화면·8K/4K120·100W와 실제 관측 분리. 모니터·실제Hz·수전W 미상 |
| [PUR-013](https://quasarzone.com/bbs/qc_user/views/125766) | 일치 | 외장3대 연결·일부복제·충전 유지. 세팅·이론상·미러링·충전 단락 | 독립3대 아님. 복제 전체 대수·어느그룹·수전W 미상. 제품 최대와 칩별 설명은 공식claim 아님 |
| [PUR-014](https://seook.tistory.com/m/entry/맥북-4K-모니터-추천-MSI-MD271UL-4K-듀얼-모니터-실제-사용-후기) | 교정 | Belkin TB4 확정 표기 → Thunderbolt 세대UNKNOWN. 현재 본문의 M2Air/M4mini·케이블 교체·PD옵션·QHD서술 대조 | 교체 당시 호스트 미상 유지. 추가/수정 시점UNKNOWN. 기존 제휴고지가 현재 본문 추출에 보이지 않아 재확인 불가; 광고 없음으로 바꾸지 않음 |
| [PUR-015](https://yelobean.tistory.com/80) | 교정 | FHD60 근거 ORIGINAL_POST → EDITED_POST 추가 단락·추가일UNKNOWN | DL 외장2대·충전 진술과 네이티브 출력 구분. 독립 대수·각화면Hz 미상. Watch 제한≠잠자기 복귀 |
| [PUR-016](https://mib428047.tistory.com/entry/macbookairm1usbchub4k60hz) | 일치 | 기존4K30→UGREEN구매 뒤4K60 진술 유지. 본문 | 모니터·허브SKU·OS·픽셀·PD·복귀 미상 |
| [PUR-017](https://blog.notepads.kr/182) | 일치 | 120Hz 사용 / 144Hz 선택 검은화면 / 대역폭·DP조언 분리 유지. 설정·왜 단락 | IP2730 표시명은 기존 확인 기록이고 이번 텍스트만으로 최종 식별 재확인 불가. Mac 모델·칩 하위모델 미상. 대역폭 원인 공식 확정 안 함 |
| [PUR-018](https://itnmobile.net/76) | 교정 | 케이스 간섭·제거 후 포괄 정상은 유지하고, 당분간 사용 보류를 분리 진술로 화면에 노출 | 조건부 보류≠영구 영상FAILURE. 기존 허브PD/HDMI불안정 미혼합. 신제품 영상·PD·Hz 개별결과UNKNOWN |

PUR-003 후속 댓글은 작성자의 문제 설명이며 HDMI 삽입 수정 후 실제 UHD60을 측정했다는 문장은 아니다. 조치·정상 관측을 만들지 않았다. PUR-018은 기존 결측 메모에 있던 조건부 보류를 명확히 보여주는 교정이며 새 구성 실패 결론을 만들지 않았다. PUR-015의 추가 단락은 본문에 `(추가)` 표시가 있지만 편집일은 없어 게시일에 결합하지 않았다. PUR-014의 현 본문이 과거와 어느 시점에 달라졌는지는 과거 스냅샷이 없어 알 수 없다.

## 기능별 정보 누락

한 사례에 해당 기능의 알려진 관측이 하나라도 있는지 기준으로 집계했다. 정상만 세지 않았으며 서로 다른 구성을 합친 호환성 성공률이 아니다.

| 검토 슬롯 | 진술/표기 있는 사례 | 전부UNKNOWN인 사례 | 한계 |
|---|---:|---:|---|
| 영상 관련 문제·정상 | 17 | 1 | 목표모드 문제도 포함. 점등/최종 성공 대수 집계가 아님 |
| 해상도/Hz 표기 | 6 | 12 | 실제 출력 진술·선택상한·선택설정을 구분 |
| UI배율 | 2 | 16 | 신호 픽셀로 변환 금지 |
| 충전 보고 | 6 | 12 | USB-PD협상 확인 아님 |
| 클램쉘 관측 | 2 | 16 | 덮개 사용 목표·전환문제와 별개 |
| 잠자기 복귀 | 1 | 17 | 특정 허브 결과를 다른 허브로 전파 금지 |
| 재연결 | 3 | 15 | 임시 우회·재발과 영구 해결 구분 |

실제 신호 픽셀과 협상/실측 충전W는18건 모두UNKNOWN이다. SKU·길이·OS버전·케이블 세대·관측 기간·모니터별타이밍 결측도 남는다. 화면3대 연결과 독립3대·복제3대는 같은 값이 아니다. PUR-013/015의 미상 대수는 계속 생략했다.

교정 후 구성46개(실제44/목표1/조언1), 수행 시도13개, 관측51개다. 새 관측은 PUR-008의7-in-1 연결 정상1개이며 새 사건/사용자/사례가 아니다. 전체 outcome은18건 모두UNKNOWN으로 보존했다.

## 공식·실물 대조 우선 후보 — 최대3개

1. **PUR-001 / M1Air–V32UE 직접C-C:** 영상·충전·배율을 따로 검증하기에 단순하다. 사용자의 코드웨이 케이블과 글의 번들케이블은 서로 다른 대상이다. 먼저 실제 SKU·길이·입력포트·OS·덮개·전원을 식별한 후 OSD/시스템의 신호Hz와 PD·복귀를 별도 확인한다. 공개 후기만으로 사용자 조합 승인 안 함.
2. **PUR-007 / 직접MSI와 INC013qc 경유 비교:** 동일 표시모니터의 경로 차이를 조사할 가치가 있다. 호스트 정확한 칩·모델과 실제 독 출력포트부터 확인해야 한다. 케이블을 Thunderbolt라고 부른 것만으로 프로토콜/routing을 승인하지 않는다.
3. **PUR-008 / UGREEN6·7과 Baseus 비교:** 영상 모드와 잠자기 복귀의 범위 분리 검증 후보. 정확한 허브SKU·모니터·OS부터 필요하다.7-in-1 정상 진술에60Hz·PD·복귀를 자동 추가하지 않는다.

이는 다음 검수 후보이며 공식자료 조사·상품추천·실물시험·골든승인은 아직 수행하지 않았다.

## 검증과 보존

```sh
python3 -m unittest discover -s tests -q
python3 -m scripts.validate_public_usage_review
python3 scripts/validate_question_corpus.py
python3 scripts/validate_question_corpus_v2.py
python3 -m scripts.validate_official_products
python3 scripts/validate_connection_model_pilot.py
python3 scripts/path_instance_v1.py --check
python3 -m scripts.build_public_usage_review_ui
npm run test:e2e -- --workers=2
node --check web/review-app.js
git diff --check
```

Python **309개(기존299+의미 회귀10) 통과**, 브라우저 **34개(기존32+데스크톱/모바일 의미회귀2) 통과**. 기존 중복URL 테스트의 합성 URL변경에 새 검수URL 메타데이터도 같이 맞추어 기존 중복 거부 검사를 유지했다. 원문 불가를 정상 검수로 바꾸기, 다른 작성자 역할, 잘못된 근거 포인터, 다른 출처·사람승인 상태를 거부한다.7-in-1 Hz/PD/복귀 미승격·초기실패/후속설명 분리·선택상한·케이블 세대·추가일 미추정·USB-C호스트 미추정을 회귀 검사했다.

데스크톱/모바일 Chromium153.0.8010.12에서 전체 목업과 내부검토 화면을 검사했다. 목록·상세 WCAG 자동검사 위반0, 가로넘침·키보드·초점복귀·필터·뒤로가기·오류화면·XSS문자표시·원본파일 비노출 검사가 통과했다. Codex In-app Browser에서도 교정된 PUR-008 상세와 UNKNOWN 슬롯을 직접 확인했다. localhost8873에서 미리보기하고 테스트는 별도8874를 사용했다. 실제 iPhone·네이티브Safari 실기는 미검사다.

- [데스크톱 상세 기록](screenshots/public-usage-detail-desktop.png)
- [모바일 상세 기록](screenshots/public-usage-detail-mobile.png)

작업 전 91개 파일의 SHA-256 스냅샷과 비교했다. 허용된 검토 파일·UI 자산·시험스크린샷10개가 변경됐고 기존81개는 바이트 그대로다. 원본18건, v1·영어예시·정식v2, 정식schema·catalog·pilot·path·기존목업, README·골든계획의 기존 미커밋 변경을 보존했다. 원본18건 SHA-256은 `8131cea42edf5644c8fc5f276690c6f4767bf4e2a355dd000e037b6bc777eb43`이다. 변경 대상은 검토 매핑·검사기/회귀·얇은표시어댑터/자산/메모와 UI시험스크린샷뿐이다. 개인정보·비밀패턴, ID/정규화URL/로컬객체ID/참조, 원본행hash, JSONL형식, 문서내부경로와diff를 확인했다.

## 남은 위험

본문 접근 성공이 모든 댓글·이미지·수정이력 확보를 의미하지 않는다. 특히 PUR-007 댓글 전체, PUR-014 과거제휴고지·수정일, PUR-017 모니터표시명은 이번 재확인 범위가 제한된다. AI가 위치·범위를 잘못 해석할 가능성도 남으므로 사람 검토 상태는 유지한다. 공식 사양·실물 재현은 별도 단계이며 UNKNOWN을 낮추거나 골든승인수를 늘리는 근거로 이번 의미검수를 사용하지 않는다.
