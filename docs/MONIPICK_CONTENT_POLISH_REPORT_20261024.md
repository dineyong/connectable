# 모니픽 내부 링크·대표 제품 설명 후보

## 범위와 현재 상태

2026-10-24 사용자 요청: 최신 CI 확인, 내부 링크 정리, 대표 제품 설명 보강, 디자인 별도 시안, 검증·GitHub push. 광고·통계 비활성 유지. 이 작업은 **검토용 후보 구현**이며 운영 배포·main 병합을 하지 않는다. 운영 공개 파일 61개의 승인 fingerprint를 변경하지 않았으며 기존 운영 빌더는 계속 원래 내용을 빌드한다. 후보의 승인 flag는 false다. 디자인·내용 검수 뒤 실제 반영을 별도 진행할 수 있다.

기준 커밋 29a40cf0799c2f80328374c1f5ec2024da04bb16 / 기준 CI [40057204241](https://github.com/dineyong/connectable/actions/runs/40057204241) success 확인. 브랜치 codex/monipick-content-polish, 별도 managed worktree 사용. 원래 작업 폴더의 README/DECISIONS·JS/CSS·테스트 및 미추적 파일은 보존했다.

## 내부 링크

공개 형식 출력의 HTML 38개에서 내부 문서 별칭 링크 **168곳**을 최종 경로로 정리했다. .html과 제품 index.html 링크를 포함한다. query와 fragment를 보존하고 외부 URL·메일·fragment-only·query-only는 보존한다. 원본 web/은 변경하지 않는다. JS의 자료 대화상자에서 생성하는 monitor10-review.html# 링크 한 유형도 최종 /monitor10-review#로 변경했다. 예전 주소의 301/308 규칙, 사이트맵 34개, canonical/뉴스 제외 정책은 그대로다. 모든 URL을 임의 짧은 주소로 바꾸지 않고 이미 정의된 문서 경로만 처리한다.

## 대표 제품 3종

| 제품 | 요약한 사실 | 유지한 제한 |
|---|---|---|
| Dell U2724DE | 27형 QHD, IPS Black, 최대 120Hz, Thunderbolt 4 영상·데이터 업스트림과 별도 USB-C 데이터 전용 업스트림 구분 | 한국 SKU·입력별 동시 조건 미확인. 전 포트 120Hz나 기기 연결 성공 주장 없음 |
| ASUS PA279CRV | 27형 4K IPS, 최대 60Hz, USB-C DP Alt Mode, PD 공급 표기 96W | 실제 충전량·한국 SKU·동시 조건·실물 동작 보장 없음 |
| MSI Modern MD271UL | 27형 4K IPS, 최대 60Hz, USB-C DP Alternate, PD 공급 표기 65W | USB 허브·KVM·한국 SKU 미확인 유지 |

기존 검증된 공식 fact 기록을 편집 요약했으며 공식 원문을 새로 확인한 것으로 기록하지 않았다. 원래 문서 지역·확인일·출처를 유지한다. 각 문장은 속성/값/단위/표현 종류를 명시적으로 바인딩하고 해당 공식 URL과 확인일을 표시한다. 사실이 바뀌거나 UNKNOWN이 되거나 결측 상태가 해소되면 문구 재검토 전 빌드를 거부한다. 자연어 의미 전체를 자동 검증한다고 주장하지 않는다. 원본 사양·질문 코퍼스·후기·호환성 판정 데이터는 변경하지 않았다.

3종에 고유 description 및 소셜 description을 추가하고 기존 사양표 위에 ‘이 모델에서 먼저 볼 점’을 배치했다. 공식 근거·구매 전 확인·지역과 호환성 보류 안내·포트 선택 가이드·전체 목록 링크를 함께 제공한다. 가격·순위·별점·제품 실측·새 추천 주장은 추가하지 않았다.

## 디자인 시안

기존 회녹색/진녹색 스타일을 유지한 흰색 요약 영역이다. 사용자 확인 전 운영에 적용하지 않는다.

- [데스크톱](design/content-polish-20261024/desktop.png)
- [모바일](design/content-polish-20261024/mobile.png)
- 실행: `python3 -m scripts.serve_monipick_content_candidate --port 8897`
- 로컬 검토: http://127.0.0.1:8897/monitors/asus-pa279crv/

## 검증 및 실패 이력

- 기존 전체 Python + 신규 회귀 6개: **665개 통과**. 마지막 표시 스타일 조정 후 신규 6개 재검사 통과.
- 신규 데스크톱/모바일 후보 브라우저 검사: **14개 통과**. 기존 공개 후보의 검색·비교·상세·운영 안내·뉴스·실제 404·CSP 10개를 후보에도 적용하고, 3종 설명/접근성/가로 넘침과 최종 가이드 경로/anchor 4개를 추가했다.
- 첫 후보 브라우저 검사는 12개 통과/2개 실패. MSI의 기존 두 aside에 구분되는 접근성 이름이 없어 landmark-unique 위반이 드러났다. 테스트를 완화하지 않고 **후보에서만** 사양 안내와 공식 충돌 안내에 각각 이름을 붙인 뒤 14개 통과했다. 원래 운영본의 해당 문제까지 배포로 해결됐다고 주장하지 않는다.
- 첫 시안 캡처 시 8878 포트가 다른 프로세스에 사용 중이었다. 그 프로세스를 종료하지 않고 사용되지 않는 8897에서 후보를 실행했다. 잘못 열린 NOT_FOUND 화면 캡처는 올바른 후보 화면으로 교체했다.
- 원본 data 및 web/ 변경 없음, 원래 운영 승인 fingerprint 동일, 광고·통계 false·배포 승인 false 회귀 검사. 관련 없는 전체 상품 사양 추가 조사나 기존 불확실성 해소 없음.
- CI에 후보 전용 loopback 브라우저 검사 단계를 추가했다. 기존 검사를 삭제하거나 완화하지 않았다. 푸시 뒤 실제 CI 결과는 완료 응답에서 구분한다.

## 파일과 다음 단계

- data/editorial/monitor-summary-pilot.json: 원본과 분리한 편집 요약 및 사실 바인딩.
- scripts/prepare_monipick_content_candidate.py: 후보 변환 및 바이트·승인 보류 검증.
- scripts/serve_monipick_content_candidate.py: localhost 전용 후보 서버.
- scripts/serve_monipick_candidate.py: 기본 검증을 유지하면서 후보별 검증 함수를 받을 수 있게 확장.
- tests/test_monipick_content_candidate.py, tests/content-e2e/content-review.spec.js, playwright.content.config.js 및 CI 단계.

사용자 확인 대상은 위 설명 배치 시안이다. 실제 운영 반영은 후보 변경 범위를 검토해 기존 승인 파일과 별도로 처리해야 한다. 공개 CSP·사이트맵·광고/통계 비활성·Access·실제 URL을 재검증하는 다음 배포 단계는 이번에 수행하지 않았다. 대표 3종 외의 설명 확대와 실제 검색 색인 결과 확인은 후속 작업이다.
