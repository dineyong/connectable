# 공식 사양 2차 배치

2026-10-08. 기준 브랜치 research/question-corpus-foundation, 시작 커밋 4640a84.

## 수집 결과

| 제품 ID | 칩·형태 | 원문 | 저장한 동시 출력 |
| --- | --- | --- | --- |
| product:pro14-m1-pro-2021 | 14형 M1 Pro | [Apple 111902](https://support.apple.com/ko-kr/111902) | 내장 동시, 외장 최대 2대 각 6K 60Hz |
| product:pro14-m1-max-2021 | 14형 M1 Max | [Apple 111902](https://support.apple.com/ko-kr/111902) | 내장 동시, 6K 60Hz 3대 + 4K 60Hz 1대 |
| product:air13-m3-2024 | 13형 M3 | [Apple 118551](https://support.apple.com/ko-kr/118551), [듀얼 화면 요구 사항](https://support.apple.com/ko-kr/117373) | 내장 동시 6K 60Hz 1대; 덮개 닫힘 6K 60Hz + 5K 60Hz |

모두 공개 원문 직접 확인, 확인일 2026-10-08. 제품 사양 A등급, 공식 지원 안내 B등급.
지원 안내는 macOS 14.3 이상, 외장 입력 장치, 전원 연결을 요구한다.
공식 지원 안내의 게시일 2024-08-20을 기록했다. 다른 문서 갱신일은 미상이다.
새 제품의 모델 번호는 변형별 확정 자료를 충분히 대조하지 않아 생략했다.
118551 문서에는 M2 관련 문구와 여러 모델 번호도 포함되므로 해당 문구를 M3 사실로 자동 승계하지 않았다.
지원 안내에 있는 대체 4K 고주사율 프로파일은 이번 데이터에 수집하지 않았다. 미수집은 미지원 의미가 아니다.
세 제품 모두 사람 최종 검수 대기이며 사용자 사례의 공식 대조는 진행하지 않았다.

## 공식 데이터 구조 변경

[공식 스키마](../schemas/official-products.schema.json)와 [제품 원본](../data/official/products.json)의 version을 2로 올렸다.
질문 코퍼스 v2와 별개의 버전이다. 질문 스키마는 변경하지 않았다.

- applies_to_models 배열: 같은 공식 문서가 여러 칩 변형에 적용됨을 표현. 이전 단일 참조 2개는 값 손실 없이 배열로 이전.
- CONDITIONAL_NATIVE_DISPLAY_PROFILE: display_groups에 각 그룹의 count·resolution_label·refresh_hz를 저장.
- external_count는 그룹 수 합계. M1 Max를 4대 모두 6K로 평탄화하는 입력은 거부.
- prerequisites: builtin_state, lid_state, power_required, external_input_required 및 선택 minimum_macos.
- 모델 번호는 미확정 시 생략. 공식 지원 출처는 MANUFACTURER_SUPPORT/B로 분리.
- 기존 두 제품의 사양 객체는 그대로 유지. 기존 NATIVE_EXTERNAL_DISPLAY_PROFILE은 내장 동시 사용이라는 이전 정의를 유지.

[규칙 후보](../scripts/evaluate_display_count_candidate.py)는 내장 ON 프로파일만 적용한다.
M3 덮개 닫힘 프로파일은 저장하되 OS·전원·입력 장치를 검증하는 실행 규칙은 아직 만들지 않았다.
내장 ON과 덮개 CLOSED가 동시에 입력되면 UNKNOWN이다. 화면 수 이내도 전체 호환을 긍정하지 않는다.
프로파일이 여러 개 매칭되면 하나를 임의 선택하지 않는다.
이 규칙은 해상도별 적합성 또는 포트 경로를 평가하지 않는다. 기존 rule_id의 내장 동시 출력 제한 의미는 유지한다.

## 검증

```sh
python3 -m unittest discover -s tests -q
python3 -m scripts.validate_official_products
python3 scripts/validate_question_corpus.py
python3 scripts/validate_question_corpus_v2.py
```

Python 154개 PASS(기존 144 + 신규 10). 제품 5건·출처 5건 검증 PASS.
그룹 합계, 평탄화 거부, 닫힌 덮개와 내장 ON 모순, 지원 문서 등급, Pro/Max 분리,
M3 열림/닫힘 분리, OS·전원 조건 보존, 기존 두 제품 사양의 정규화 해시를 검사했다.
문서 경로·JSON 구문·diff 공백·기존 코퍼스/목업 무변경·신규 자료 개인정보/비밀값 패턴 검사를 수행했다.
사이트 파일을 변경하지 않아 이전 브라우저 12개 결과를 유지하며 이번에는 재실행하지 않았다.

## 남은 위험과 다음 배치

공식 원문 스냅샷 부재와 최종 사람 검수 대기는 계속 남는다.
모델 번호·포트 상세·PD 최소 전력·특정 독에서의 출력·독립 확장 확인은 미완료다.
단일 해상도 라벨과 그룹은 픽셀 타이밍·색 깊이·DSC 대역폭 계산을 대신하지 않는다.
다음 배치는 모니터와 독 데이터 구조 및 공식 출처를 추가하여 경로의 양 끝과 중간 장치 조건을 확보한다.
사이트 판정 연결, 공식 대조 결과 생성, 21~100번 질문 수집, main merge는 하지 않았다.
