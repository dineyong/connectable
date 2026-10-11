# ASUS 핵심 사양 보완 및 한국 문서·SKU 대조

2026-10-11 · codex/monitor-purpose-design · 기준 233c997.

## CI

[233c997 CI](https://github.com/dineyong/connectable/actions/runs/38115959023)는 completed/success로 직접 확인했다.

## 직접 확인한 공식 근거

| 모델 | 공식 URL / 위치 | 확인 내용 |
| --- | --- | --- |
| XG27AQDMG | [US 제품 소개](https://rog.asus.com/us/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/) · 제조사 제목·특징, OLED 장점 | 가시 화면 26.5인치(27인치급), 패널 최대 240Hz, 0.03ms GtG, DCI-P3 99% |
| XG27AQDMG | [KR 기술 스펙](https://rog.asus.com/kr/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/spec/) · 모델·디스플레이·I/O·주파수 | 같은 모델명, 핵심값 일치. DP 수직 40–240Hz, HDMI 수직 40–144Hz |
| PG32UCDM | [US 제품 소개](https://rog.asus.com/us/monitors/27-to-31-5-inches/rog-swift-oled-pg32ucdm/) · 제조사 제목·특징·TYPE-C PD 각주 | QD-OLED, 최대 240Hz, 0.03ms GtG, DCI-P3 99%, 내장 KVM. PD 기본 65W이며 90W는 OSD 활성화 필요 |
| PG32UCDM | [KR 기술 스펙](https://rog.asus.com/kr/monitors/27-to-31-5-inches/rog-swift-oled-pg32ucdm/spec/?config=90LM09T0-B01310) · 모델·디스플레이·I/O | 같은 모델명, 31.5인치·QD-OLED·240Hz 및 90W 표기 확인 |

모두 2026-10-11 직접 열어 확인했다. 페이지에 삽입된 미디어/사용자 리뷰를 제조사 사양 근거로 사용하지 않았다. US 기술 스펙 추출의 결측을 US 제조사 소개 본문으로 보완했고, KR 문서는 별도의 대조 출처로 추가했다. 기존 US 지역은 유지했다. 기존 출처 확인일을 전체 재검증 날짜로 덮어쓰지 않았다.

## 반영과 보존

- 신규 fact 9개: 두 모델의 핵심값 각 2개, 응답 시간·색역 각 2개, PG32UCDM KVM 1개.
- PG32UCDM 기존 PD 90W fact 값은 유지하고 공식 소개 출처와 기본 65W/OSD 조건을 근거 위치에 추가했다. 필터/카드의 숫자만으로 실제 충전을 보장하지 않는다.
- XG27AQDMG 패널 240Hz와 입력별 주파수 범위는 별개다. 해상도별 타이밍, HDR/DSC 조합 및 모든 케이블에서 240Hz를 보장하지 않는다.
- XG27AQDMGR(Gen2), PG32UCDM3 등 다른 모델을 섞지 않았다.
- 카드·검색·상세·비교·정적 제품 문서를 기존 생성기로 재생성했다. 다른 28개 제품의 원본 객체는 변경하지 않았다.

## 한국 SKU 판단

**한국 공식 문서의 같은 모델명과 핵심 사양은 확인. 실제 국내 유통 SKU 동일성은 UNKNOWN 유지.**

XG27AQDMG의 `config=90LM0AH0-B01A10` URL도 직접 열었으나 페이지 본문에서 그 품번과 한국 유통 구성의 관계를 입증하지 못했다. PG32UCDM의 `config=90LM09T0-B01310` 역시 쿼리 존재를 판매 SKU 증거로 간주하지 않았다. KR 페이지 자체도 지역에 따라 판매·구성이 달라질 수 있음을 안내한다. 한국어 문서 또는 같은 모델명만으로 국내 보증·구성품·유통 SKU를 승인하지 않는다.

PG32UCDM 기본 KR spec URL은 최초 조회 뒤 재열기에서 도구 Internal Error가 발생했다. 검색에서 실제 발견한 config 포함 공식 URL은 본문을 확인할 수 있었으며 우회·비공개 API를 사용하지 않았다.

## 남은 미확인 및 위험

- 두 모델 한국 판매 P/N, 국내 보증 적용과 구성품 동일성.
- 일반 밝기, 네이티브 명암비 구분, PIP/PBP 등 기존 남은 결측. 마케팅 명암비를 native 측정값으로 자동 전환하지 않았다.
- XG27AQDMG USB-C·PD·KVM은 미지원으로 바꾸지 않았다.
- PG32UCDM DP/Type-C 수평 주파수 `510~501kHz`는 공식 KR 문서에도 표시됨. 오기 가능성을 임의 수정하지 않았다.
- 이미지 사용권, 사람 검토, 호환성 공개 승인은 변함없다.

## 사용자 확인이 필요한 것만

지금 추가 응답은 필요 없다. 국내 판매 SKU까지 확정할 때 제조사/공식 유통사의 품번 확인 자료 또는 실제 구매 대상 링크가 있으면 대조할 수 있다. 자료 없이 사람의 승인만으로 SKU 동일성을 만들지 않는다. 도메인·광고 연결과 댓글은 기존 보류 결정을 유지한다.

## 검증 과정

최초 Python 실행에서 기존 ASUS 주사율 null 전제 테스트와 Quasarzone intake의 원본 해시 검사 2건이 실패했다. 신규 패널 fact를 제외한 상황에서도 입력 주파수만으로 refresh가 생기지 않는 회귀를 유지하도록 테스트를 갱신했다. 30종 ID/제조사/표시 모델/지역/식별 상태가 전후 동일함을 확인한 뒤 intake의 baseline hash만 갱신했고 후보·매핑·원문 자료는 변경하지 않았다. 검증 기준을 완화하지 않았다.

## 최종 검증

- `python3 -m unittest discover -s tests -q`: 559개 통과.
- `npm run test:e2e -- --workers=2`: 186개 통과(기존 사용자 미커밋 검사 14개 포함 로컬 결과).
- 생성 데이터·정적 제품 30개·정리 목록의 `--check`, Quasarzone intake 검증, 로컬 사이트 검증과 `git diff --check` 통과.
- 공식 원본 변경은 대상 2종뿐임을 객체 비교로 확인. intake는 baseline hash/size 외 변경 없음.
- 원본 출처·기존 fact 보존, PD fact 조건 보강, 확인된 새 fact 추가. 코퍼스·호환성 엔진·이미지 변경 없음.
- 기존 README/DECISIONS/site-v2/content-review 사용자 변경은 커밋에 포함하지 않음. main 병합 및 공개 배포 없음.

최종 커밋은 이 보고서를 포함한 커밋으로 식별한다.
