# 외부 모니터 리뷰 링크 초기 수집

확인일: 2026-10-11. 기준: 모니터 비교 v3 제품 방향. 개인 후기·전문 리뷰의 원문 링크 안내이며 공식 사양·호환성 승인 데이터가 아니다.

## 초기 링크와 직접 확인

| 제품 | 출처 | 유형 | 직접 확인한 위치 | 광고·제휴 |
|---|---|---|---|---|
| M32U | [퀘이사존 사용기](https://quasarzone.com/bbs/qf_dp/views/310312) | 개인 사용기 | 본문의 M32U 구매 과정·PC 게임 사용·설정 경험 | UNKNOWN |
| M32U | [RTINGS 리뷰](https://www.rtings.com/monitor/reviews/gigabyte/m32u) | 전문 리뷰 | 모델 제목·본문·게임 응답/화질/문자 가독성 시험 항목 | PRESENT |
| XG27AQDMG | [RTINGS 리뷰](https://www.rtings.com/monitor/reviews/asus/rog-strix-oled-xg27aqdmg) | 전문 리뷰 | 모델 제목·공개 본문·OLED/게임 시험 항목 | PRESENT |
| PG32UCDM | [RTINGS 리뷰](https://www.rtings.com/monitor/reviews/asus/rog-swift-oled-pg32ucdm) | 전문 리뷰 | 모델 제목·공개 본문·화질/색상/게임 시험 항목 | PRESENT |
| Q27G3XMN | [RTINGS 리뷰](https://www.rtings.com/monitor/reviews/aoc/q27g3xmn) | 전문 리뷰 | 모델 제목·공개 본문·로컬 디밍/게임 시험 항목 | PRESENT |

RTINGS는 페이지 상단에서 판매처 링크를 통한 제휴 수수료 가능성을 고지했다. 퀘이사존에서 광고가 없다고 확정하지 않는다. RTINGS의 점수·측정값·이미지는 저장하지 않는다. 제목은 직접 작성한 모델별 안내이고 요약은 한 문장으로 다루는 주제만 소개한다. 닉네임·개인정보를 저장하지 않는다.

퀘이사존 1건은 기존 `mr:m32u-pc-games`와 같은 모델·같은 URL임을 검사한다. 신규 전문 리뷰 4건은 기존 개인 후기 원본에 넣지 않고 `source_review_id: null`로 분리한다. `EXACT_DOCUMENT_MODEL`은 문서에 나온 모델 이름의 일치이며 한국 SKU·리비전·모든 사용 조건의 일치 승인이 아니다.

## 제외와 남은 범위

Dell U2724D RTINGS 후보는 직접 원문 열기에 실패하여 제외했다. 검색 요약으로 채우지 않았다. 기존 LG 27GP850/27GR83Q는 -B 접미사 불확실성, M27Q는 리비전 미상 때문에 현재 제품과 자동 연결하지 않았다. MD271UL/Modern MD271UL 별칭은 이번에 임의 동치하지 않았다. YouTube는 실제 영상·정확 모델 검토가 아직 없어 가짜 링크를 만들지 않았다.

개별 공개 페이지 6개만 수동 확인 수준으로 열었다. 로그인·접근 제한 우회·대량 크롤링·영상/본문/썸네일 다운로드를 하지 않았다. 퀘이사존 자동 수집 정책과 외부 콘텐츠 재사용 허가는 미확인이다. 이번 범위는 텍스트 원문 링크와 직접 작성한 짧은 안내이며 자동 수집·복제 허가를 주장하지 않는다. 사이트별 정책 검토와 링크 제거 요청 대응은 공개 운영 전에 별도 점검할 항목이다.

## 원본·파생 계약과 검증

- [새 링크 원본](../data/research/monitor-review-links.json)은 기존 후기 원본 24건과 분리한다.
- [생성기](../scripts/build_monitor_review_links.py)는 기존 공식 제품·후기 원본 검증을 먼저 실행한다. `build()`는 읽기만 하고 검증된 공개 필드를 반환한다.
- [JSON 파생](../data/site/monitor-review-links.json), [브라우저 데이터](../web/monitor-review-links-data.js)는 원본에서 생성한다.
- HTTPS만 허용하며 사용자정보·포트·쿼리·fragment·인코딩·우회 경로·출처 호스트 불일치를 거부한다. 수동 확인한 전문 리뷰의 제품별 경로를 정확 바인딩한다.
- ID·정규화 URL 중복, 존재하지 않는 제품·후기 참조, 다른 모델 연결, 빈 근거, 잘못된 날짜·enum, HTML·이메일·전화번호를 거부한다.
- `python3 -m unittest tests.test_monitor_review_links -q`: **11개 통과**.
- `python3 scripts/build_monitor_review_links.py --check`: **5건 검증·파생 일치**.

[회귀 테스트](../tests/test_monitor_review_links.py)는 다른 제품으로 재바인딩하면서 모델명도 바꾸는 입력, 출처 URL 바꾸기, 중복, 악의 URL, 비문자 날짜·참조를 포함한다. 원본의 확인 위치를 코드만으로 실증할 수는 없으므로 새로운 링크의 직접 확인은 계속 필요한 편집 검토다. 링크는 향후 삭제·유료화될 수 있고 URL 검증은 외부 리다이렉트의 실시간 검사까지 보장하지 않는다.
