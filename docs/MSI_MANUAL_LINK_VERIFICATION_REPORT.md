# MSI 공식 지원 페이지–설명서 연결 확인

2026-10-11 · `codex/monitor-purpose-design` · 기준 `a2d10e1`.

## 확인 경로

1. [Modern MD271UL 공식 지원](https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL/support) 페이지를 일반 브라우저로 열었다.
2. 페이지 제목과 제품 영역의 Modern MD271UL을 확인하고, 기본 Drivers & Downloads 선택을 **Manual & Document**로 바꾸었다.
3. URL은 `support#manual`이 되었으며 Manual 목록에 [한국어 V1.1 PDF](https://download.msi.com/archive/mnu_exe/monitor/Modern_MD271ULv1.1_Korean.pdf)가 직접 링크로 표시됐다. English 등 다른 언어 파일도 같은 목록에 있었지만 등록 대상은 한국어 파일1개다.
4. 해당 PDF 원문을 재확인했다. 표지 Modern MD271UL(3PB8), 개정V1.1(2023/10), 인쇄16쪽에 일반 밝기300 nits(typ.)가 명시되어 있다.

이로써 [4차 보고서](KOREAN_SKU_SPEC_BATCH_4_REPORT.md)의 모델 지원 페이지와 설명서 연결 미확인 항목을 해소했다. 초기 단순 HTTP 요청은 접근 거부였으나 일반 브라우저에서는 공개 지원 메뉴가 정상 동작했다. 로그인·CAPTCHA·보안 경고·비공개 API 우회는 하지 않았다. 기존 추출 도구가 반환한 미치환 템플릿을 실제 페이지 부재로 단정하지 않았다.

## 반영과 제한

- MD271UL 원본에 설명서 출처1개와 **brightness_typical=300 nit** fact1개 추가, 해당 결측1개만 제거했다. 기존 fact와 Global 지역·모델·식별 상태는 보존했다.
- 한국어 설명서 제공은 한국 판매 SKU·보증 적용 증거가 아니다. 해당 결측과 호환성 사용 불가 상태 유지.
- 인쇄15쪽의 최대65W PD는 기존 사실이며 별도 신규 수치로 중복 추가하지 않았다. 설명서의19V·5.79A를 실제 소비전력으로 계산하지 않는다.
- 설명서 본문 전체나 사용자 정보는 저장하지 않았다. 경로·문서 위치·짧은 사실만 기록했다.

## 출처 검증 변경

다운로드 호스트 전체를 DOMAINS에 추가하지 않았다. `REVIEWED_MANUALS`에 **제조사 MSI + 내부 제품ID + 표시 모델명 + 정확한 HTTPS PDF URL** 조합1개를 등록했다. 기존 스킴·사용자정보·포트·인코딩 검사는 먼저 적용된다. 다른 모델, 다른 버전/경로, query/fragment, 위장 호스트 및 download-2 호스트는 이 등록으로 허용되지 않는다.

이는 이번에 직접 검토한 문서에 한정된 오프라인 출처 등록이며 실시간 리다이렉트/파일 무결성 감시 기능은 아니다. 문서 바이트 변경이나 미래 링크 변경까지 보장하지 않는다. MAG 274QRF QD E2 등 다른 MSI 설명서는 이번 등록 범위에 포함되지 않는다.

## 테스트 및 보존

수정 전 `test_exact_linked_manual_accepted`가 기존 호스트 제한으로 실패함을 확인했다. 수정 후 정상 URL 허용, 잘못된 경로·모델·호스트·query 등 거부, 밝기 보완과 국내SKU/소비전력 결측 분리를 검사한다. 전체 실행 결과는 아래에 기록한다.

사용자 README/DECISIONS/site-v2/content-review 및 미추적 문서는 제외한다. 제품별 상세·비교 파생 데이터와 제품 정보 목록은 재생성한다. main 병합·공개 배포·한국 SKU 승인 없음. 지금 사용자 결정은 필요 없다.

## 실행 결과

- Python 전체 `python3 -m unittest discover -s tests -q`: **574개 통과**.
- 브라우저 전체 `npm run test:e2e -- --workers=2`: **190개 통과**(기존 로컬 미커밋 검사14개 포함).
- official/intake 검증, 생성 데이터·정적 페이지·inventory check, 로컬 사이트·문서 상대경로·diff 검사 통과.
- MD271UL의 기존 facts/식별 정보 및 다른29종 객체 보존 확인. 테스트 캡처 복원.
- 최종 커밋은 이 문서를 포함한 커밋이며 CI 결과는 완료 응답에 기록한다.
