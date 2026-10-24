# SEO/GEO 후속 변경 검토본 · 2026-10-24

실제 사이트 반영 전 사용자 검토용이다. 운영 배포·DNS·계정 설정·검색 제출은 실행하지 않았다.

## 현재 등록 상태 — 화면에서 읽기 확인

- Google Search Console: monipick.com 도메인 속성 확인. 제출된 사이트맵 1개, 상태 성공, 발견 페이지 34, 마지막 읽은 날짜 2026-10-24. 페이지 색인 보고서는 데이터 처리 중으로 개별 색인 수를 확인할 수 없었다.
- 네이버: 사용자가 직접 로그인한 뒤 모니픽 등록일 26.10.24와 해당 사이트 관리 접근을 확인. 제출된 sitemap.xml / 26.10.24 12:05:36 유지. 요약의 노출·클릭·진단·수집 정보는 아직 없음. 재제출·수집 요청·등록 변경 안 함.
- Bing: 현재 Chrome에서 로그인되지 않은 소개 화면으로 이동했다. 계정 내부 목록에 접근하지 않았으므로 등록 유무는 미확인이다. 신규 가입·계정 연결·권한 부여를 진행하지 않았다.

사이트맵 제출과 색인·검색 노출을 구분했다. Google/Naver 등록을 중복 진행하지 않았다.

## 기존 완료 작업과 이번 추가 변경

새 작업을 시작할 때 운영본은 이미 내부 링크 정리와 제품 3종 설명을 포함하고 있었다. 이전 감사의 별칭 링크를 다시 미해결로 다루지 않는다. ASUS PA279CRV, Dell U2724DE, MSI Modern MD271UL의 기존 설명은 보존하고 나머지 27종을 보완했다.

- 모델별 초기 HTML에 근거가 연결된 설명 2개와 구매 전 조건을 제공한다. 해상도·패널·주사율 및 입력·전력·모드처럼 해당 제품에서 확인할 차이를 설명한다.
- 신규 27개 description과 OG/Twitter description을 같은 근거의 고유 설명으로 맞춘다.
- 30개 상세에 홈 → 전체 모니터 → 현재 모델의 보이는 breadcrumb와 비교표 읽는 법·자료/정정 기준 링크를 추가한다. 링크는 운영 canonical 경로로 연결한다.
- 원본 사양표·조건·출처·확인일·지역·UNKNOWN/충돌·후기를 보존한다. 가격·별점·구매 인증·추천 순위·실측 결과를 만들지 않는다.
- 기존 공식 기록의 재서술이며 제조사 원문을 오늘 새로 전수 재확인했다는 뜻이 아니다. 미확인 상태를 승인으로 바꾸지 않는다.
- 새 editorial 파일에서 각 문장의 value/unit/qualifier와 scope/location/source_refs를 원본에 묶었다. 관련 근거가 달라지면 재검토 전 빌드를 거부한다.

## 검토할 화면과 예시

- [검토본 전체 목록](http://127.0.0.1:8885/monitors/)
- [Dell U2724D](http://127.0.0.1:8885/monitors/dell-u2724d/): 데이터 전용 USB-C와 HDMI 2.1의 TMDS 조건. U2724DE의 Thunderbolt 기능을 가져오지 않음.
- [LG 32GS95UE-B](http://127.0.0.1:8885/monitors/lg-32gs95ue-b/): 4K 최대 240Hz와 FHD 최대 480Hz 구분. 4K 480Hz로 표시하지 않음.
- [Gigabyte M28U](http://127.0.0.1:8885/monitors/gigabyte-m28u/): DSC/4:4:4 또는 4:2:0의 PC 조건과 4K 120Hz/4:2:0 콘솔 조건 구분.

로컬 서버는 이 Mac의 127.0.0.1에만 바인딩한다. 후보는 실제 운영 형식이나 배포/공개/색인/광고/통계 승인 flag는 모두 false다. 이 출력을 외부에 업로드하지 않는다. 기존 운영 승인 fingerprint와 운영 빌더는 보존하며 새 검토 빌더를 운영에 연결하지 않았다.

## 변경 파일과 보존

별도 worktree `/Users/bigmacbookman/.codex/worktrees/seo-product-review/커넥터블`, 브랜치 `codex/seo-product-review`에서 작업했다. 공유 작업 폴더의 사용자 미커밋 변경·쿠팡/이미지 작업·기존 서버는 수정하지 않았다.

- `data/editorial/monitor-summary-expansion.json`: 전체 30개 모델 근거 연결. 기존 3개 요약 문구 보존, 신규 27개 추가.
- `scripts/prepare_monipick_seo_review.py`: 별도 검토 출력·정합성 검사·루프백 서버.
- `scripts/prepare_monipick_content_candidate.py`: reviewed_summaries의 선택적 입력 경로 지원만 추가. 기본값과 기존 운영 출력은 동일.
- `tests/test_monipick_seo_review.py`: 근거·조건 변형 거부, 전체 모델/링크/표/승인 보존 검사.

공식 원본·schemas·web·운영 승인 파일은 수정하지 않았다. commit/push/배포는 하지 않았다. 생성 HTML은 임시 검토 폴더에만 있다.

## 다음 순서

변경 내용과 화면을 사용자에게 먼저 제시한다. 이번 변경의 운영 반영 전에는 사용자의 검토 결과를 기다린다. 구조화 데이터·공통 OG 이미지·favicon·Lighthouse/PSI는 이 설명/링크 검토 후 후속으로 두고 임의 적용하지 않았다. Bing 내부 확인은 사용 중인 계정으로 로그인된 상태가 필요하며 등록 부재로 단정하지 않는다.

## 실제 검증 결과

- 전체 Python **677개 통과**, 154.757초. 새 근거/링크/검토 게이트 7개 포함. 테스트의 의도적 변조 fixture가 출력하는 FAIL 문구와 최종 unittest OK/exit 0은 구분한다.
- 기존 운영 빌드/콘텐츠 승인/검색 소유확인 관련 **15개 통과**. 기존 운영 출력 fingerprint가 승인 기록과 동일함을 확인했다.
- 제품 30개 모두 JavaScript를 끈 상태로 새 요약 1개와 사양표를 읽을 수 있음을 확인했다.
- Dell U2724D, LG 32GS95UE-B, Gigabyte M28U × 1280/390px의 **6개 조건**에서 실행 오류·문서 가로 넘침·검사한 WCAG 태그의 axe 위반 0. [브라우저 결과](design/seo-review-20261024/browser-results.json).
- [Dell 데스크톱](design/seo-review-20261024/dell-1280.png), [Dell 모바일](design/seo-review-20261024/dell-390.png), [LG 듀얼 모드](design/seo-review-20261024/lg-dual-mode.png). 마지막 Dell 문구를 더 쉬운 표현으로 다듬은 후 Dell 캡처를 갱신했다.
- 사양표 HTML은 기존 운영본과 30개 모두 동일. 설명 근거의 값·단위·qualifier·scope·문서 위치·source_refs 변경을 거부하며 원본·후기·지역·미확인 표시는 보존한다.
- 공개 출력에서 알려진 문서 별칭 링크 부재 및 fragment 대상 존재 검사 통과. 기존 3종 설명과 운영 fingerprint 보존 검사 통과.
- `git diff --check` 통과. 실제 반영·운영 HTTP 재검증·검색 재제출·순위/인용 효과는 미실행이다.

검사 명령의 최초 시도에서 존재하지 않는 test_monipick_production_build 이름을 지정해 import 오류가 났다. 실제 모듈명 test_monipick_cloudflare_build로 수정하여 관련 15개와 전체 677개를 통과했다. 앱 오류로 처리하지 않는다.

## 모델별 변경 전후 설명

기존 운영용 산출물과 새 검토본의 description 비교다. 기존 3종 설명은 동일하며 탐색 링크만 보완했다. 아래 설명과 같은 근거의 본문 요약 2개를 실제 검토 화면에서 확인할 수 있다.

| 모델 | 기존 설명 | 검토본 설명 |
|---|---|---|
| AOC Q27G3XMN | AOC Q27G3XMN의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | AOC Q27G3XMN: 27형 2560×1440, 최대 180Hz. 로컬 디밍 336구역 표기 확인. |
| ASUS PA248QV | ASUS PA248QV의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | ASUS PA248QV: 24.1형 1920×1200, 최대 75Hz. 1920×1200 해상도 확인. |
| ASUS PA278QV | ASUS PA278QV의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | ASUS PA278QV: 27형 2560×1440, 최대 75Hz. HDMI 1.4·DisplayPort 1.2 표기 확인. |
| ASUS PA279CRV | 27형 4K·최대 60Hz, USB-C 영상 입력과 공급 전력 96W 표기를 확인하세요. | 27형 4K·최대 60Hz, USB-C 영상 입력과 공급 전력 96W 표기를 확인하세요. |
| ASUS PG32UCDM | ASUS PG32UCDM의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | ASUS PG32UCDM: 31.5형 3840×2160, 최대 240Hz. USB-C 영상 모드·90W 공급 표기 확인. |
| ASUS VA24EHF | ASUS VA24EHF의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | ASUS VA24EHF: 23.8형 1920×1080, 최대 100Hz. HDMI 입력 구성 확인. |
| ASUS VG27AQ | ASUS VG27AQ의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | ASUS VG27AQ: 27형 2560×1440, 최대 165Hz. HDMI·DisplayPort 입력별 조건 확인. |
| ASUS XG27AQDMG | ASUS XG27AQDMG의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | ASUS XG27AQDMG: 26.5형 2560×1440, 최대 240Hz. 26.5형 표기와 입력 조건 확인. |
| BenQ EX2710Q | BenQ EX2710Q의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | BenQ EX2710Q: 27형 2560×1440, 165Hz. GtG·MPRT 응답시간 방식 구분. |
| BenQ GW2490 | BenQ GW2490의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | BenQ GW2490: 23.8형 1920×1080, 100Hz. HDMI 2개·DisplayPort 입력 구성 확인. |
| BenQ GW2790QT | BenQ GW2790QT의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | BenQ GW2790QT: 27형 2560×1440, 75Hz. USB-C 영상·65W 공급 표기 확인. |
| BenQ PD2705U | BenQ PD2705U의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | BenQ PD2705U: 27형 3840×2160, 60Hz. USB-C 업스트림·65W 공급 표기 확인. |
| BenQ PD2725U | BenQ PD2725U의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | BenQ PD2725U: 27형 3840×2160, 60Hz. Thunderbolt 3·전력 공급 방향 구분. |
| Dell AW3225QF | Dell AW3225QF의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | Dell AW3225QF: 31.6형 3840×2160, 최대 240Hz. 1700R 곡률·USB-C 다운스트림 역할 확인. |
| Dell U2724D | Dell U2724D의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | Dell U2724D: 27형 2560×1440, 최대 120Hz. 데이터 전용 USB-C·HDMI TMDS 조건 확인. |
| Dell U2724DE | 27형 QHD·최대 120Hz, Thunderbolt와 USB-C 포트를 구분하세요. | 27형 QHD·최대 120Hz, Thunderbolt와 USB-C 포트를 구분하세요. |
| Gigabyte M27Q rev.1.0 | Gigabyte M27Q rev.1.0의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | Gigabyte M27Q rev.1.0: 27형 2560×1440, 최대 170Hz. rev.1.0 범위·USB-C 영상 모드 확인. |
| Gigabyte M28U | Gigabyte M28U의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | Gigabyte M28U: 28형 3840×2160, 최대 144Hz. DSC·색차 형식·콘솔 120Hz 조건 구분. |
| Gigabyte M32U | Gigabyte M32U의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | Gigabyte M32U: 31.5형 3840×2160, 최대 144Hz. PC·콘솔 입력과 색차 형식 조건 구분. |
| LG 27GP850-B | LG 27GP850-B의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | LG 27GP850-B: 27형 2560×1440, 최대 165Hz. 문서의 USB-C 미지원 표기 확인. |
| LG 27GR83Q-B | LG 27GR83Q-B의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | LG 27GR83Q-B: 27형 2560×1440, 최대 240Hz. DSC와 HDMI 버전 미확인 구분. |
| LG 27GS95QE-B | LG 27GS95QE-B의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | LG 27GS95QE-B: 26.5형 2560×1440, 최대 240Hz. HDMI 수량·입력별 조건 확인. |
| LG 27UP850K-W | LG 27UP850K-W의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | LG 27UP850K-W: 27형 3840×2160, 최대 60Hz. USB-C 영상 모드·90W 공급 표기 구분. |
| LG 32GS95UE-B | LG 32GS95UE-B의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | LG 32GS95UE-B: 31.5형 3840×2160, 최대 240Hz. 4K 240Hz·FHD 480Hz 모드 구분. |
| LG 34WQ75C-B.AUS | LG 34WQ75C-B.AUS의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | LG 34WQ75C-B.AUS: 34.14형 3440×1440, 최대 60Hz. 3440×1440·3800R 및 USB-C 조건 확인. |
| MSI MAG 274QRF QD E2 | MSI MAG 274QRF QD E2의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | MSI MAG 274QRF QD E2: 27형 2560×1440, 최대 180Hz. USB-C 영상 모드·입력별 주사율 확인. |
| MSI Modern MD271UL | 27형 4K·최대 60Hz, USB-C 영상 입력과 공급 전력 65W 표기를 확인하세요. | 27형 4K·최대 60Hz, USB-C 영상 입력과 공급 전력 65W 표기를 확인하세요. |
| MSI MPG 321URX QD-OLED | MSI MPG 321URX QD-OLED의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | MSI MPG 321URX QD-OLED: 31.5형 3840×2160, 최대 240Hz. USB-C 영상 모드·90W 공급 표기 확인. |
| Samsung S32CG554EU (LS32CG554EUXEN) | Samsung S32CG554EU (LS32CG554EUXEN)의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | Samsung S32CG554EU (LS32CG554EUXEN): 32형 2560×1440, 최대 165Hz. 정확 SKU·1000R 곡률·USB-C 미지원 확인. |
| Samsung S65UC (LS34C650UEEXXY) | Samsung S65UC (LS34C650UEEXXY)의 수집된 공식 사양, 입력 조건과 미확인 항목을 모니픽에서 함께 확인하세요. | Samsung S65UC (LS34C650UEEXXY): 34형 3440×1440, 최대 100Hz. 호주 SKU·USB-C 영상 모드 미확인 구분. |

출력 비교: 기존 파일 35개에서 변경, 기존 승인된 네이버 소유확인 파일 1개를 검토본에도 동일 바이트로 보존. 문서 루트 밖 manifest는 미승인 검토 상태다.
