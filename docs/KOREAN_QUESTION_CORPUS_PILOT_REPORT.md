# 한국어 공개 질문 코퍼스 파일럿 보고서

확인일: 2026-10-07 (한국 시간). 작업 브랜치: `research/question-corpus-foundation`.

## 결과와 범위

[실제 데이터](../data/research/user_questions.csv)에 한국어 20건(UQ-0006~UQ-0025)을 추가했다.
[영어 예시 5건](../data/research/user_questions.example.csv)은 별도로 유지했다.
README와 docs 전체를 다시 읽었고 시작 시 작업 트리는 깨끗했다. 변경 전 기존 26개 테스트가 통과했다.
기존 스키마·수집 지침·DECISIONS와 MVP 범위를 변경하지 않았다. 사용자 지시에 따라 이번 조사 표본만
Windows·데스크톱·Intel Mac까지 포함했다. 공식 자료 대조와 웹사이트 개발은 수행하지 않았다.

20건은 실제 원문·필요한 작성자 후속댓글을 개별 열람한 문제 질문 또는 작성자의 문제 해결 기록이다.
검색 제목·요약만으로 채운 행은 없다. 한 게시물에서 여러 기기를 시험한 글은 한 PC 구성만 선택했다.
모든 행은 `ko`, 공개 접근 `YES`, 단일 사례 `C`, `NOT_CHECKED`, 충돌 `UNKNOWN`,
`NEEDS_REVIEW`, `usable_for_compatibility=NO`다. 공식 사이트의 사용자 글도 공식 사양으로 취급하지 않았다.
작성자 이름·닉네임·이메일·전화번호·원문 전체·스크린샷·판매 링크는 저장하지 않았다.
데이터의 모델·포트·해상도 표현은 작성자 보고이며 제품 공식 사양을 확인한 값이 아니다.

**표본 조건의 미충족 사항:** 성공과 출력 실패 증상은 모두 포함했으나, 기존 결과 정의에 따른
최종 `FAILURE`는 0건이다. 해결을 기다리는 글을 `FAILURE`로 바꾸지 않았다.
최종 실패·사용 포기 결과를 작성자가 명시한 한국어 공개 사례는 후속 수집에서 보완해야 한다.
100건 전체 수집의 완료를 의미하지 않는다. 충전 문제 중심 사례와 DisplayLink 확인 사례도 없다.

## 사람이 검토할 20건 요약표

모델명은 원문 표기를 정리한 값이다. “직접”은 최종 보고 경로에 별도 허브·어댑터가 없는 경우다.
변환 케이블은 “중간 장치·변환”에 포함했다. HDMI 언급만 있고 중간 장치 생략 여부가 불명확한 글은
“경로 일부 미상”으로 남겼다. 배열에 최종 경로를 우선 기록하고 이전·병렬 경로는 메모로 구분했다.
아래 표는 검수용이며 사람의 승인 완료를 뜻하지 않는다.

| ID·원문 | 소스 기기 | 모니터·장치 | 경로 | 증상·결과 근거 | 결과 |
| --- | --- | --- | --- | --- | --- |
| [UQ-0006](https://meeco.kr/mini/37328357) (미코) | 갤럭시북 이온2 | 4K / Baseus | 중간 장치·변환 | 직접 HDMI는 정상이나 Baseus 허브 HDMI 경로에서 색상이 녹색으로 틀어짐 / 작성자 후속댓글에서 30Hz로 낮추면 정상이라고 확인 | LIMITED_SUCCESS |
| [UQ-0007](https://discussionskorea.apple.com/thread/255632196) (Apple 지원 커뮤니티(한국어)) | MacBook Air 15인치 M3 | 모델 미상 화면 / 모델 미상 화면 | 경로 일부 미상 | 집에서는 두 화면이 복제되고 설정에는 하나만 잡힘. 회사에서는 두 대 사용 가능 / 원글의 실패 증상만 확인되며 해결 후속 확인 없음 | UNRESOLVED |
| [UQ-0008](https://m.ppomppu.co.kr/new/bbs_view.php?id=computer&no=654438) (뽐뿌) | LG 그램 17ZD990-VX5BK | 34UC75 | 직접 | 해상도 설정 문제. 55Hz에서는 깜빡임 / 작성자 2022-08-08 댓글에서 3440x1440 50Hz 정상 출력과 모니터 오디오 미인식을 보고 | LIMITED_SUCCESS |
| [UQ-0009](https://node-js.tistory.com/31) (Tistory) | M1 MacBook Air | 모델 미상 화면 | 경로 일부 미상 | Monterey 업데이트 뒤 외장 모니터가 깜빡임 / 내장 Retina 화면 미러링 후 미러링을 해제하면 일시 해결. 재연결·재부팅 때 반복 필요 | LIMITED_SUCCESS |
| [UQ-0010](https://jhsoso.tistory.com/10) (Tistory) | MacBook M3 Pro | 32UN650 / 27UP550N | 직접 | C to C 화면 연결 시 HDMI 화면이 검게 됨 / 작성자가 사용자별 WindowServer 디스플레이 설정 파일 삭제 후 재시작하여 두 화면 정상이라고 보고 | SUCCESS |
| [UQ-0011](https://somingoose.tistory.com/178) (Tistory) | M1 맥북 | 모델 미상 화면 | 경로 일부 미상 | C to C 연결 중 커서·스크롤이 간헐적으로 멈춤 / HDMI 변경 직후 정상이라고 썼으나 다음 날 증상 재발. 빈도 감소만 보고 | LIMITED_SUCCESS |
| [UQ-0012](https://sidongblog.tistory.com/783) (Tistory) | MacBook Pro Retina 15인치 2015 | 32UN880 | 직접 | mini DisplayPort to HDMI 경로는 출력되나 끊김. Thunderbolt 어댑터 직접 연결은 무반응 / 작성자가 최종 mini DisplayPort to DisplayPort 케이블로 4K 60Hz 부드러운 출력 확인 | SUCCESS |
| [UQ-0013](https://pgd078.tistory.com/279) (Tistory) | 모델 미기재 노트북 | 모델 미상 화면 / 모델 미상 화면 / USB 3.0 to Dual HDMI Multi-Monitor Adapter | 중간 장치·변환 | 처음 사용한 듀얼 HDMI 장치는 외장 화면을 복제함 / 작성자가 j5create USB 3.0 to Dual HDMI 어댑터로 세 개의 독립 화면을 사용한다고 보고 | SUCCESS |
| [UQ-0014](https://discussionskorea.apple.com/thread/254154256) (Apple 지원 커뮤니티(한국어)) | MacBook Pro M1 Pro | TFX32U06B | 경로 일부 미상 | 업데이트 뒤 HDMI 외장 모니터가 반복적으로 깜빡이고 꺼짐 / 원글의 지속 증상만 확인. 답변의 일반 점검 제안에 대한 작성자 결과 없음 | UNRESOLVED |
| [UQ-0015](https://discussionskorea.apple.com/thread/120038536) (Apple 지원 커뮤니티(한국어)) | MacBook Pro 13인치 2017 Thunderbolt 3 포트 2개 | U2415 / ADAPTER | 중간 장치·변환 | 설정에서 모니터가 인식되나 실제 화면은 검음 / 입력 선택을 확인했으나 해결 확인 댓글 없음 | UNRESOLVED |
| [UQ-0016](https://discussionskorea.apple.com/thread/255740759) (Apple 지원 커뮤니티(한국어)) | MacBook Pro 14인치 M3 Pro | 4K | 경로 일부 미상 | 덮개를 열면 내장 메뉴가 작아지고 해상도 표시 방식도 달라짐 / 재부팅 필요 여부를 질문하며 확인된 최종 해결 결과 없음 | UNRESOLVED |
| [UQ-0017](https://discussionskorea.apple.com/thread/256235569) (Apple 지원 커뮤니티(한국어)) | MacBook Pro 16인치 M1 Pro | 모델 미상 | 경로 일부 미상 | 한 사용자 계정에서 화면 출력 문제. 다른 계정은 정상 / 재연결·재부팅 등은 실패했으나 답변 이후 작성자가 해결됐다고 확인. 실행한 세부 단계는 미상 | SUCCESS |
| [UQ-0018](https://macblogger.tistory.com/entry/%EB%85%B8%ED%8A%B8%EB%B6%81-%EC%99%B8%EB%B6%80-%EB%AA%A8%EB%8B%88%ED%84%B0-%EC%9D%B8%EC%8B%9D%EB%B6%88%EA%B0%80-%ED%95%B4%EA%B2%B0%EB%B0%A9%EB%B2%95) (Tistory) | Gigabyte Aero 15 WA | U2913WM | 경로 일부 미상 | HDMI 연결에서 일반 모니터로 인식되고 목표 해상도는 검게 됨 / 작성자가 최종 DP 케이블 시험에 성공하여 해당 모니터로 글을 작성한다고 보고. 최종 픽셀 수는 별도 확인되지 않음 | SUCCESS |
| [UQ-0019](https://m.ppomppu.co.kr/new/bbs_view.php?id=computer&no=637640) (뽐뿌) | 조립 PC (i5-6500, ASRock B150M Pro4) | u2777m | 직접 | HDMI 연결에서 1080 이상 설정이 보이지 않음 / 작성자 후속댓글에서도 1080 상태. 재시도·그래픽카드 구매는 계획일 뿐 결과 없음 | UNRESOLVED |
| [UQ-0020](https://www.ppomppu.co.kr/zboard/view.php?id=computer&no=646452) (뽐뿌) | 구형 데스크톱 | 16MQ70 | 중간 장치·변환 | HDMI to C 케이블과 추가 C to C 전원 시도에도 화면이 나오지 않음 / 다른 삼성 노트북 Thunderbolt에서는 출력됨. 데스크톱 해결 확인 없음 | UNRESOLVED |
| [UQ-0021](https://www.ppomppu.co.kr/zboard/view.php?id=computer&no=693122) (뽐뿌) | Mac mini M4 기본형 | OMEN 32q | 직접 | 직접 HDMI에서 검은 화면. 허브 또는 다른 휴대용 화면이 함께 있을 때만 일부 주사율 출력 / 작성자 12월 7일 댓글에서 케이블 변경 후 144Hz 정상. 12월 8일 모니터 동봉 HDMI 케이블이라고 추가 확인 | SUCCESS |
| [UQ-0022](https://meeco.kr/Review/37397129) (미코) | Surface Go 1세대 | ProDisplay P221 / Newsync B274K / MH610 / ADAPTER | 중간 장치·변환 | 4K 한 대는 30Hz. FHD 화면 추가 시 4K 유지 불가 / 작성자 Surface Go 시험에서 FHD 두 화면은 사용 가능하다고 보고 | LIMITED_SUCCESS |
| [UQ-0023](https://meeco.kr/mini/32113967) (미코) | 갤럭시북 이온 i5 | 4K | 직접 | 바탕화면 출력은 정상이나 YouTube 4K 영상이 끊김 / 작성자 5월 16일 댓글에서 HDR 해제 후 정상 확인. HDR 사용 희망은 남음 | LIMITED_SUCCESS |
| [UQ-0024](https://m.ppomppu.co.kr/new/bbs_view.php?id=computer&no=697599) (뽐뿌) | SER8 미니 PC | 모델 미상 화면 | 직접 | 모니터 그림 표시 C 포트는 무반응이고 번개 표시 C 포트는 정상 / 원글에서 다른 포트 정상 출력 확인. 원하는 포트의 해결은 미확인 | LIMITED_SUCCESS |
| [UQ-0025](https://m.ppomppu.co.kr/new/bbs_view.php?id=computer&no=695639) (뽐뿌) | LEGION 노트북 | 모델 미상 화면 / 모델 미상 화면 | 경로 일부 미상 | 현재 외장 한 대 사용. 두 대 연결 방법과 허브 충전 조건을 질문 / 구매 전 질문과 감사 댓글만 있으며 제안된 구성의 실제 시험 결과 없음 | UNKNOWN |

## 수집 분포

### 출처

| 값 | 건수 |
| --- | ---: |
| 미코 | 3 |
| Apple 지원 커뮤니티(한국어) | 5 |
| 뽐뿌 | 6 |
| Tistory | 6 |

### 결과

| 값 | 건수 |
| --- | ---: |
| LIMITED_SUCCESS | 7 |
| UNRESOLVED | 6 |
| SUCCESS | 6 |
| UNKNOWN | 1 |
| FAILURE | 0 |

### 소스 모델 식별

| 값 | 건수 |
| --- | ---: |
| PARTIAL | 11 |
| EXACT | 7 |
| UNKNOWN | 2 |

### 원문에 명시된 OS

| 값 | 건수 |
| --- | ---: |
| 미기재 | 9 |
| macOS | 7 |
| Windows | 4 |

### 최종 연결 경로

| 경로 | 건수 |
| --- | ---: |
| 중간 장치·변환 | 5 |
| 경로 일부 미상 | 8 |
| 직접 | 7 |

디스플레이 객체의 모델 식별 분포: UNKNOWN 12개, EXACT 12개 (사례 수와 다름).

플랫폼 최대 비중은 6/20(30%)이다. Tistory 6건은 서로 다른 블로그다.
문제 해결 기록의 비중이 있으며, 커뮤니티 질문만을 대표하는 무작위 표본은 아니다.
OS가 없는 글에서 기기명만으로 Windows/macOS를 채우지 않았다.

## 결측과 스키마 적용 결과

### 자주 비어 있던 필드

다음은 CSV의 빈 셀 또는 UNKNOWN 기준이다. 공식 검증 관련 결측은 의도적인 단계 분리다.

| 필드 | 빈 값·UNKNOWN 건수 |
| --- | ---: |
| source_normalized_model | 20 |
| source_release_year | 17 |
| source_chip | 10 |
| source_variant | 13 |
| os_name | 9 |
| os_version | 13 |
| output_mode | 20 |
| display_mode | 18 |
| clamshell | 16 |
| pd_charging | 20 |
| pd_watts | 20 |
| actual_external_display_count | 3 |

디스플레이·연결 장치에는 정확한 모델, 목표·실제 픽셀 해상도, 케이블 모델,
드라이버·전원 상태가 자주 빠졌다. 각 행의 `missing_fields`에 생략된 키와 UNKNOWN 경로를 기록했다.
4K/FHD 표현을 픽셀 수로 바꾸거나 케이블의 단자로 프로토콜을 판정하지 않았다.
PD 충전은 소스 기기 충전 관측이므로 모니터 전원 공급이나 충전기 정격과 구분했다.

### 표현하기 어려웠던 사례와 해석이 애매한 필드

- UQ-0010·0022: 병렬 연결과 출력 분기가 평면 장치 배열에서 직렬로 오해될 수 있다. 메모로 분기별 화면을 구분했다.
- UQ-0012·0018·0021: 여러 시도와 최종 경로를 한 배열에 넣으면 실패 경로와 성공 경로가 섞인다. 최종 경로를 구조화하고 실제 시도는 별도 배열에 기록했다.
- UQ-0009·0011: 재연결 후 재발 또는 다음 날 재발을 단일 최종 결과와 실제 주사율만으로 표현하기 어렵다. 일시적 효과를 LIMITED_SUCCESS와 근거에 기록했다.
- UQ-0007: 복제로 켜진 외장 두 대와 독립 확장 출력 수가 다르다. actual_external_display_count=2는 켜진 물리 화면 수로 읽어야 한다.
- UQ-0016: 외장 화면 사용 후 내장 화면 배율 증상은 외장 디스플레이 객체에 대응하지 않는다. 내장 증상을 요약과 검토 메모에만 기록했다.
- UQ-0017: “듀얼”이 외장 두 대인지 내장 포함인지 불명확하고 해결됐다는 답만 있다. 대수와 실행한 세부 조치를 추정하지 않았다.
- UQ-0018: 원문 “Thunderbolt 3(DP3.1)” 혼용 표기는 공식 규격으로 저장하지 않았다. 최종 호스트 단자와 픽셀 해상도는 미확정이다.
- UQ-0019·0021: 원문 픽셀 표기의 오타 가능성을 임의 수정하지 않았다. 2556x1440 및 2580x1440을 검증된 픽셀 값으로 넣지 않았다.
- UQ-0025: 구매 전 제안 장치를 실제 사용 장치와 구분했다. 기존 한 대와 목표 두 대가 달라 displays가 목표를 표현한다는 점을 검수해야 한다.
- EXACT는 원문에 충분히 특정한 SKU 또는 칩·화면 크기·제품군 조합이 있을 때 사용했다. 부품 전체나 모든 옵션의 공식 확인을 의미하지 않는다. 칩 또는 세대만 특정되면 PARTIAL, 일반 “노트북·구형 데스크톱”이면 UNKNOWN으로 두었다.
- 최초·최종 HDR, 미러링·확장 상태를 한 필드로 표현할 때 시간 순서를 메모에 적었다. 미러링 후 해제를 MIXED로 바꾸지 않았다.

### 중복 판정의 어려움

같은 모델의 연결 실패라는 이유만으로 다른 작성자의 글을 중복으로 보지 않았다.
사용자명은 보관하지 않아 다른 사이트 재게시의 동일 작성자 확인은 제한된다.
UQ-0017의 다른 계정 시험, UQ-0020의 비교 노트북, UQ-0022의 다른 호스트 시험,
UQ-0021의 작성자 후속댓글은 추가 독립 사례로 세지 않았다.
모바일·PC 뽐뿌 URL은 사이트·게시판 id·게시물 no로 정규화하여 중복 검사했다.
20개 한국어 URL과 기존 영어 예시 5개를 합쳐 ID 및 정규화 URL 중복이 없다.

### 100건 수집 전 최소 변경 제안 — 미적용

1. 스키마 변경 없이 먼저 결과 분류 예시를 지침에 보강할지 검토한다. 미해결 질문과 최종 포기·실패를 구분하고, 재발·조건부 성공을 명시한다.
2. 경로와 관측 시점을 구분하는 소규모 구조 확장을 별도 설계한다. 구성별 ID, 단계/분기, 목표·관측 구분을 두고 displays와 장치를 연결하는 방법이 필요하다.
3. 실제 외장 화면 수와 독립 확장 화면 수의 정의를 명확히 한다. 내장 화면 포함 여부와 구매 전 목표 장치 기록 방법도 검토한다.
4. EXACT/PARTIAL 판정 예시, 해상도 오타 처리, 응답 “해결됨”의 조치 확실성 기록 기준을 보강한다. 새 enum을 즉시 추가하지 않는다.
5. 실제 질문과 회고형 해결 기록을 구분할 필요를 검토하고, 광고 제외 기준과 판매 링크가 동반된 실사용 기록의 경계를 명확히 한다. UQ-0012는 이 경계 때문에 추가 사람 검수가 필요하다.
6. 다음 표본은 최종 FAILURE, PD 충전, 확인 가능한 DisplayLink, 독 연결 사례를 먼저 보완한다. 차단된 출처 대신 공개 정책이 허용하는 사이트에서 개별 확인한다.

이 제안들은 기존 [스키마](QUESTION_CORPUS_SCHEMA.md), [지침](QUESTION_COLLECTION_GUIDE.md),
[결정 기록](DECISIONS.md)을 변경하지 않는다. 데이터 수집과 공식 사양 대조는 별도 단계로 유지한다.

## 접근과 제외 기록

사이트 목록·검색 결과 전체를 자동 수집하지 않았고 원문은 개별 수동 확인 수준으로 열람했다.
뽐뿌 일부 페이지는 웹 도구의 문자 디코딩이 실패하여 공개 브라우저에서 원문과 작성자 댓글을 확인했다.
접근 권한·로그인·CAPTCHA·차단 우회는 하지 않았다. 정책을 확인하지 못한 사이트를 자동 수집 허용으로 간주하지 않았다.

| 후보·사이트 | 제외 사유·조치 |
| --- | --- |
| 클리앙 | 검색 도구 robots 제한. 본문 확인 불가로 제외 |
| 다모앙 | robots.txt의 GPTBot 및 ChatGPT-User 접근 금지 확인. 수집 제외 |
| 퀘이사존 question/171141 및 후보 116282429·311308 | 원문 접근 실패. 검색 요약에서 행을 만들지 않음 |
| 2CPU QnA/710628 | 공개 브라우저에서 읽기 권한·로그인 요구 확인. 제외 |
| 2CPU nas/34149 | 원문 접근 실패. 제외 |
| Apple 한국어 thread/252477545·256136773 | 429 응답으로 본문 미확인. 제외 |
| Apple 한국어 thread/255952620·256247140 | 접근 실패. 제외 |
| 미코 mini/31295800·36937388 및 free/41230137 | 원문 접근 실패. 제외 |
| 확인된 글의 타인 댓글 해결책, 동일 작성자 후속댓글, 비교용 다른 기기 | 실제 실행·독립 사례로 추정하지 않음 |

뽐뿌·미코·Apple·퀘이사존·2CPU의 robots/policy를 도구로 확정하지 못한 경우가 있다.
따라서 자동 수집 확대의 근거로 이 파일럿을 사용하면 안 된다. 블로그도 향후 대량 수집 전 개별 정책 재확인이 필요하다.
접근 실패는 현재 도구 환경에서의 실패이며 원문 삭제라고 단정하지 않았다.

## 검증 기록

변경 전과 실제 데이터 추가 후 기존 테스트를 실행했다. 데이터 기록 중 일회성 작성 스크립트의
중복 키 오류를 수정한 뒤 파일을 생성했고, 아래 검증은 실제 20행 파일을 대상으로 다시 통과했다.
CSV는 UTF-8, LF, 기존 46개 헤더 순서와 JSON 배열 직렬화를 유지한다.

| 명령·검사 | 결과 |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | 기존 26개 모두 통과 |
| `python3 scripts/validate_question_corpus.py` | 한국어 실제 CSV 20행 및 영어 예시 5행 PASS |
| `python3 -m json.tool schemas/user-question.schema.json > /dev/null` | 구문 검사 통과 |
| 표준 라이브러리 csv로 실제 헤더만 임시 CSV 생성 후 검증기 실행 | 빈 템플릿 PASS |
| ID·원문 URL 집합 비교 및 뽐뿌 게시판/게시물 번호 정규화 | 25행 합산 중복 0 |
| 모든 행 ko/C/NOT_CHECKED/NO 상태 검사 | 통과 |
| README 및 docs Markdown 상대 링크 대상 존재 검사 | 통과 |
| 이메일·휴대전화·AWS 키·GitHub 토큰·개인키 패턴 검사 및 작성 필드 검토 | 발견 없음 |
| `git diff --check` 및 변경 내용 검토 | 통과, 데이터와 보고서만 변경 |
| 영어 example·JSON Schema·DECISIONS 변경 비교 | 변경 없음 |

패턴 검사는 모든 개인정보를 자동 식별하는 증명이 아니다. 모델·장치·조건·증상·결과만 요약해
개인 식별 내용을 제거했으나, 공개 원문 링크 자체는 작성자 페이지로 이어질 수 있다.
사람의 출처·중복·광고 경계 검토와 공식 대조가 남아 있어 모든 행을 NEEDS_REVIEW/NO로 유지한다.
출처 소실, 시간에 따른 OS 변화, 불완전한 모델명, 해결 원인의 인과관계 불확실성이 남는다.

## Git 기록

데이터 커밋: `ee116c2e2fd4b6c16bb1fc97ee5cc71d947990e3` (`data: collect 20 Korean question corpus pilot cases`).

보고서 검증 후 같은 조사 브랜치에 별도 커밋하고 push한다. main 변경·merge·강제 push는 하지 않는다. 최종 커밋 SHA와 push 결과는 작업 완료 응답에서 보고한다.
