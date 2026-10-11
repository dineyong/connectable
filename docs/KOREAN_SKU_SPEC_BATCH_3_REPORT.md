# 한국 SKU·미확인 사양 3차 조사

2026-10-11 · `codex/monitor-purpose-design` · 기준 `b6c70b8`.

## 범위와 결과

남은 6개 모델을 대상으로 공개 공식 문서 본문을 직접 확인했다. 검색 요약은 후보 URL 탐색에만 사용했다. DIRECT_CHECK는 이번 원문 확인 범위이며 웹 추출에 캐시가 포함될 수 있다.

| 모델 | 공식 근거·위치 | 결과와 반영 |
|---|---|---|
| GW2490 | [BenQ 한국 사양](https://www.benq.com/ko-kr/monitor/home/gw2490/spec.html), 디스플레이·지원 단자 | FHD100 IPS, HDMI1.4 2개/DP1.2 1개 대조. 출처·메모 추가. 기존 US region 및 미기재 기능 유지 |
| U2724DE | [Dell 한국 상세](https://www.dell.com/ko-kr/shop/monitors/apd/dell-ultrasharp-27-thunderbolt-허브-모니터-u2724de/u2724de_withstnd_mon/-), 일반 정보 | 제조업체 부품 5PXK3 / Dell 부품 n32y09 / 오퍼링 u2724de_withstnd_mon 확인. 국내 문서 식별자를 메모로 보존. 기존 US 사양 전체의 국내 동일성 승인은 아님 |
| AW3225QF | [Dell 한국 상세](https://www.dell.com/ko-kr/shop/monitors/apd/alienware-32-240hz-4k-qdoled-gaming-monitor-aw3225qf/aw3225qf_monitor/-), 일반 정보·인터페이스 | 제조업체 부품 20YX5 / Dell 부품 t4w7j4 / 오퍼링 aw3225qf_monitor 확인. 출처·메모 추가. DP DSC와 HDMI FRL 각각 UHD240 표기 대조, USB-C 다운스트림을 영상 입력/노트북 충전으로 만들지 않음 |
| 27GR83Q-B | [LG 한국 27GR83Q](https://www.lge.co.kr/product/monitors/27gr83q), 제품 상세 스펙·기본정보; [27GR83Q-BB 지원](https://www.lge.co.kr/support/product-27GR83Q-BB) | 국내 후보 확인. 한국 표에는 밝기400/HDMI2.1/PBP·PIP 미지원/1년 보증이 있으나 GB 모델과 동일성 부족. 후보 차이를 메모에 기록하고 수치는 이식하지 않음 |
| 34WQ75C-B.AUS | [미국 원본 PDF](https://www.lg.com/us/support/products/documents/34WQ75C_Spec_Sheet.pdf), 1쪽 INPUT/OUTPUT; [UK 후보](https://www.lg.com/uk/monitors/ultrawide/34wq75c-b/), CONNECTIVITY | 미국 원본은 DP 버전 미기재, UK는1.4. UK 출처·지역 차이 메모만 추가, 미국 버전 결측 유지. [한국 검색](https://www.lge.co.kr/search?keyword=34WQ75C-B&tab=all)에서는 충분한 제품별 자료 확보 못함 |
| Q27G3XMN | [AOC 미국 공식 표](https://www.aoc.com/us/gaming/monitors/q27g3xmn), Power consumption / Product dimensions | 전원 꺼짐 소비전력0.3W fact1개 추가. WxHxD 축 라벨과 첫 치수의 범위 관계가 의심스러워 치수 자동 보완 보류. 한국어 설명서 링크만으로 한국 SKU 확정하지 않음 |

총 6개 제품 객체의 조사 메모 갱신, 5개 출처 항목 추가, 신규 fact는 AOC 전원 꺼짐 소비전력 1개다. 기존 사실·ID·지역·variant 상태는 그대로다. 국내 페이지 부품 번호를 찾은 것과 기존 해외 사양 전체를 국내 SKU에 승인하는 것은 구분한다. 한국 SKU 동일성/국내 보증 결측 제거는 0건이다.

## 보류·접근·검증 경계

- Dell 페이지의 제품 선택 UI에는 다른 모델 옵션도 함께 추출된다. U2724DE의140W 및 AW3225QF의 추가 VRR 옵션을 현재 제품 사양으로 가져오지 않았다. 가격·재고·판매 순위 수입 없음.
- AW3225QF의 첫 한국어 슬러그와 LG UK 34WQ75C의 첫 열기는 Internal Error였다. 공개 Dell 구형 상품 링크는 같은 제조사 새 상품 URL로 리다이렉트되어 본문을 확인했고, LG 재열기는 성공했다. 로그인·차단 우회 없음.
- LG 한국 호스트 `www.lge.co.kr`은 현재 원본 검증기 허용 목록 밖이다. 처음 출처 추가 시 검증 실패를 확인한 뒤 해당 출처 추가를 취소했다. 허용 목록을 느슨하게 하지 않고 한국 근거는 이 보고서에 보존했다. 제품에는 후보 모델 차이를 설명하는 메모만 남겼다.
- 기존 [LG UK 27GR83Q-B](https://www.lg.com/uk/monitors/gaming/27gr83q-b/)에서 부족한 밝기·USB-C·PIP 근거를 추가 확보하지 못했다. 한국 후보의 수치로 대체하지 않았다.
- AOC 치수 축을 사람이 보기 그럴듯한 순서로 교환하지 않았다. 명시된 전원 꺼짐 소비는 PD 공급·보통 소비·최대 소비와 별도다.

## 검증과 보존

회귀 검사는 국내 부품 번호 발견 후에도 US 지역/승인 보류 유지, LG 지역별 포트 버전 이식 방지, AOC 전원 소비와 PD/치수 결측 구분을 검사한다. 기존 facts를 객체 비교로 보존 확인하며 intake baseline hash/size만 갱신한다.

테스트 결과는 실행 완료 후 아래에 기록한다. 기존 사용자 README/DECISIONS/site-v2/content-review 및 미추적 문서는 커밋에서 제외한다. main 병합·공개 배포·광고 활성화 없음.

## 다음 조사와 사용자 결정

지금 사용자의 결정이 필요한 항목은 없다. 추가 수치가 없다는 이유로 미확인을 없애지 않는다. 남은 핵심은 해외 원본과 국내 품번의 적용 범위, AOC 치수 축, LG 지역별 구분이다. 공개 출시 시 도메인·이미지 권리·광고/제휴·사람 검토 결정은 기존 목록을 따른다.

## 실행 결과

- Python 전체: `python3 -m unittest discover -s tests -q` — **571개 통과**.
- 브라우저 전체: `npm run test:e2e -- --workers=2` — **190개 통과**. 로컬 기존 미커밋 검사14개 포함이며 원격 테스트 수와 구분한다.
- official/intake 검증, 생성 데이터·정적 페이지·inventory `--check`, 로컬 링크·공개 차단 검사와 `git diff --check` 통과.
- 6종 외 객체 및 기존 facts/ID/지역/variant/결측 목록을 비교하여 보존 확인. 원본 질문 코퍼스·official catalog·기존 UI 코드 변경 없음. 테스트가 생성한 캡처는 복원했다.
- 최종 커밋은 이 보고서를 포함한 커밋으로 식별한다. CI 결과는 완료 응답에서 별도 확인한다.
