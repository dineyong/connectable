# 후기 기반 모니터 표시 자료 1차 배치

확인일·파생일: 2026-10-09 (Asia/Seoul). research/question-corpus-foundation 로컬 checkout. 사람 검토 대기이며 공개 호환 판정은 UNKNOWN이다.

## 결과

기존 공개 후기에서 식별되는 후보 4개를 검토해 V32UE·27ULD950·MD271UL 3개를 추가하고 S43BM700은 변형 확인 부족으로 보류했다. 기존 모니터 3개를 보존해 표시 모니터는 총 6개다. 기존 연결 기록 38건은 유지하며 그중 PUR-001/005/006/014에 모델 수준 연결 4개를 추가했다. 독립 사용자·독립 사건 4건이나 호환 승인 4건이라는 뜻이 아니다. 신규 사용자 후기 수집은 없다.

먼저 README, 제품방향 v2, 경쟁 사이트 벤치마크 보고서와 기존 생성기·계약·테스트·공개 모델 목록을 읽었다. 벤치마크의 같은 모델 기능/경험 연결 및 기능별 결측 유지 제안을 이번 배치의 자료 구조에 반영했다.

새 근거는 [monitor-batch-1-sources.json](../data/site/monitor-batch-1-sources.json)에만 기록하고 공식 catalog·연구 pilot·원본/매핑 후기·정식 코퍼스·schema를 변경하지 않았다. 공개 원문 전체·댓글 원문·닉네임·사진·비공개 대화는 저장하지 않았다. 가격·별점·추천순위·판매/제휴 링크도 추가하지 않았다.

## 직접 확인한 근거와 연결

web 도구로 제조사 자료 및 아래 기존 공개 원문 본문을 열어 모델명과 해당 위치를 직접 읽었다. DIRECT_CHECK는 도구에서 공개 본문을 읽었다는 뜻이며 실물 검사·완전한 댓글/이미지 검수·독립적 진위 검증은 아니다. 로그인, CAPTCHA 해결, robots/차단 회피, 다른 호스트 우회, 구매를 하지 않았다. 검색 요약만으로 기능을 확정하지 않았다.

| 후보 | 공식 근거 | 기존 공개 원문 | 처리·범위 |
|---|---|---|---|
| 주연테크 V32UE | [제조사 출시 자료](https://www.jooyon.co.kr/bbs/board.php?bo_table=press&page=16&wr_id=227), 2021-12-06 | [PUR-001](https://makeany.tistory.com/97), 제목·좋은점2/3·케이블 사진 설명 | 동일 V32UE 표시 모델 연결. USB-C 영상·65W 공급, 입력 인터페이스, 리모컨·VESA 표기 사용. V32UE-E로 확장 안 함. 공식 Hz·KVM·높이 조절·스피커 사양은 이번 자료에서 UNKNOWN |
| 크로스오버 27ULD950 | [일반 제품 페이지](https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757), 게시일 UNKNOWN | [PUR-005](https://quasarzone.com/bbs/qf_dp/views/515378) 본문 모델명·연결/시도, [PUR-006](https://quasarzone.com/bbs/qc_user/views/133467) 모델명·클램쉘 단락 | 동일 27ULD950 연결. 일반/무결점은 정책 차이이며 리비전 일치는 UNKNOWN. 패널·KVM·스피커·높이 조절·PIP/PBP·VESA 확인. 상세 공급W·USB-C 영상 프로토콜은 UNKNOWN |
| MSI MD271UL | [글로벌 공식 사양](https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL/Specification), 게시일 UNKNOWN | [PUR-014](https://seook.tistory.com/m/entry/맥북-4K-모니터-추천-MSI-MD271UL-4K-듀얼-모니터-실제-사용-후기), 제목·연결성·케이블 교체·PD 설정 | Modern MD271UL 표시 모델 연결. DP Alt Mode·65W 공급·입력별 UHD60 상한·틸트 사용. MD271ULDE·지역 Part No·한국 SKU로 확대 안 함. 공식 KVM·스피커·높이 조절 UNKNOWN |
| 삼성 M7 S43BM700 | [국내 S43BM700UK 지원 사양](https://www.samsung.com/sec/support/model/LS43BM700UKXKR/), 게시일 UNKNOWN | [PUR-003](https://quasarzone.com/bbs/qf_dp/views/369236), 본문 모델명·실험 목록 | 원문은 S43BM700, 문서는 S43BM700UK/LS43BM700UKXKR이다. 지역 접미사 일치 근거가 없어 카드·기능·후기 연결 모두 보류. PUR-002의 ‘M7 43인치’도 연결하지 않음 |

크로스오버 공식 홈의 모델 링크는 목록 페이지로 연결됐으나 같은 사이트의 일반 제품 본문을 확인했다. 먼저 확인한 [등외품 페이지](https://www.crosslcd.co.kr/shop/item.php?it_id=1725254113)의 판매 상태·문의·가격을 정상 제품 정보로 편입하지 않았다. 일반 제품 요약의 USB PD 지원과 상품명 PD65는 확인됐지만 상세 이미지·협상 프로파일을 읽지 않았으므로 숫자 65를 확정 공급W로 저장하지 않았다. 공식 이벤트 본문도 열었으나 행사·판매 문구는 기능 근거에 편입하지 않았다.

## 관측과 사양의 경계

PUR-001의 영상·충전과 보기 배율, PUR-005의 HDMI 문제와 호스트 미상 USB-C 비교, PUR-006의 번들 C-C 클램쉘 영상·충전, PUR-014의 케이블 교체와 충전 옵션 설명은 기존 관측/기능별 구조 그대로 보존한다. 새 제조사 기능을 후기 실측으로 채우지 않는다. 실제 신호 픽셀·수전W·복귀·리비전 결측도 유지한다. MD271UL의 공식 영상 규격은 DP Alt Mode이고 작성자가 케이블을 Thunderbolt로 부른 것을 모니터 Thunderbolt 지원으로 승격하지 않는다. 교체 당시 호스트와 케이블 세대는 UNKNOWN이다.

source의 신규 확인일과 모델 대조 근거는 추가 source_refs 및 monitor_links에 기록한다. 원래 후기 확인일·semantic_review·광고 맥락·관측을 이번 날짜로 덮어쓰지 않는다. 원문 내용이 시간이 지나 수정됐을 수 있으며 이번 배치는 모델 연결에 필요한 직접 대조 범위다. 사람 승인이나 원문 전체 재검수로 표시하지 않는다.

## 호환 확장 계약

최상위 schema_version="2", monitors/reviews/guides/disclosures와 기존 ID는 유지한다. 생성일은 이번 자료 파생일로 갱신했다. 새 source 파일도 provenance에 포함한다.

- 새 monitors는 기존 features 구조를 그대로 따른다. feature의 source_refs는 source ID 배열이며 모니터 source_refs의 record_id와 batch source registry로 추적한다. feature는 조건·위치·payload·DIRECT_CHECK·PENDING_HUMAN_REVIEW를 갖는다.
- 신규 optional `variant`, `capabilities`를 제공한다. capabilities의 usb_c_video/pd_supply/kvm/speakers/height_adjustment는 status, feature_refs, notes를 갖는다. CONFIRMED_MANUFACTURER_STATEMENT는 제조사 표기 확인이며 사람 승인·Mac 실물 동작 확인이 아니다. UNKNOWN은 미지원 의미가 아니다. pd_supply 확인만으로 정확 전력을 추정하지 말고 POWER_TRANSFER payload의 watts/rating_basis를 함께 읽는다. 기존 3개에는 이 필드가 없으므로 화면은 없을 때 UNKNOWN으로 처리한다.
- 신규 property KVM/SPEAKERS/HEIGHT_ADJUSTMENT/PIP_PBP/PORTS/REMOTE_CONTROL/VESA/TILT는 일반 features.summary로 표시 가능하다. 필터를 붙일 때 capability 상태와 근거를 함께 사용한다.
- 연결된 reviews는 monitor_ids에 해당 product ID를 추가하고 `monitor_links`에 node_id, exact 원문 표기, 근거 source ID, MODEL_ONLY, variant_match=UNKNOWN, NEEDS_REVIEW를 기록한다. 유사명·가족명·전체 SKU 추정으로 연결하지 않는다. source_refs의 첫 항목은 기존 원문 근거 그대로며 새 직접확인 근거만 뒤에 추가한다.
- 기존 guides의 문단과 ID를 유지하며 관련 모니터/공식 근거가 생성기의 기존 규칙에 따라 추가된다. 새로운 추천 결론은 없다.

화면 담당의 정적 JS 재생성은 별도 소유 범위다. 이번에는 content-v2.json만 갱신했고 web/site-content-v2.js와 화면 파일은 수정하지 않았다. 화면 통합 시 기존 `web/derive-site-content.py`를 사용해 새 JSON에서 표시 자산을 생성해야 한다.

## 검증·보존

```sh
python3 scripts/build_site_content_v2.py
python3 scripts/build_site_content_v2.py --check
python3 -m unittest tests.test_site_content_v2 -v
python3 -m unittest discover -s tests -q
git diff --check
```

콘텐츠 검사 10개(기존4+추가6)와 전체 Python 319개 통과. 재생성 일치·read-only·공개 원문 URL과 기록 연결·fact/feature/capability 참조·내부 콘텐츠 링크를 검사했다. 비슷한 모델/다른 게시물/다른 제품 연결, 검색요약 DIRECT_CHECK 승격, 사용자 진술을 제조사 사양으로 사용, 사람 승인 승격을 거부하는 회귀 검사를 추가했다. 가격·평점·이미지 UNKNOWN, 민감정보 패턴/개인 식별 필드 부재도 통과했다.

작업 시작의 data/·schemas/ 바이트 해시를 확보했고 기존 연구·catalog·pilot·schema 해시는 [보존 manifest](../data/site/monitor-batch-1-preservation.json)에 기록했다. 기존 모니터3개 전체 구조와 38개 후기 기존 필드 구조도 hash로 확인했다(허용된 monitor_ids 추가 및 신규 monitor_links/source_refs 추가는 비교에서 분리). 원본 보존 검사는 통과했다. 이 manifest는 미래 승인된 원본 변경 시 새 보존 기준이 필요하며 과거 해시를 덮어써서 실패를 숨기면 안 된다.

신규 batch의 9개 source URL은 이번 도구에서 직접 열었다(제조사4+기존공개원문5). 그 외 기존 source URL은 링크 구문·로컬 참조만 검사했으며 이번에 전체 38건을 다시 열었다는 뜻은 아니다. 새 근거의 출처/확인일/본문 위치를 확인했으며 원문 사진·자산 재배포 권리는 확인하지 않아 복제하지 않았다.

담당 변경: data/site/content-v2.json, data/site/monitor-batch-1-sources.json, data/site/monitor-batch-1-preservation.json, scripts/build_site_content_v2.py, tests/test_site_content_v2.py, 이 보고서. 기존 dirty 변경과 다른 세션 소유 파일을 보존했고 Git index·commit·push·main·배포·다른 세션 메시징을 수행하지 않았다.
