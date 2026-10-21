# 모니픽 공개 설정·운영 안내 준비 결과

기준일: 2026-10-22. 기준 커밋 `5d15fb9`. 작업 브랜치 `codex/monipick-cloudflare-preparation`.
사용자 결정: 통계는 미도입. 운영 이메일은 사용자 결정 대기. 실제 공개·DNS 연결·main 병합은 금지 상태다.

## 변경 사항

- [운영 안내](../web/information.html#operation)에 통계/광고 제외, 브라우저 저장 범위, 외부 사이트 이동, 정정 요청 절차와 **연락처 준비 중**을 표시했다. 이메일·mailto·접수 폼을 임의 생성하지 않았다. 운영 안내 정리일은 개별 제품 근거 확인일과 분리했다.
- [운영 절차서](MONIPICK_OPERATIONS_RUNBOOK.md)에 정정 처리·출처/모델 검증·공개 전환의 승인 경계·롤백 준비를 기록했다. 호스팅 보안 로그와 방문 통계를 구분했다.
- [비활성 공개 준비 생성기](../scripts/prepare_monipick_release.py)를 추가했다. 기존 비공개 패키지의 noindex/robots/no-store를 유지하며, 별도 activation-drafts에 canonical/색인 범위 JSON·사이트맵·robots·헤더·리다이렉트 초안 5개를 만든다.
- 대표 origin 안은 `https://monipick.com`. 안정적인 34개 주소(홈·목록·제품 30개·가이드·자료 안내)를 사이트맵 후보로 만든다. 뉴스 저장 목록·별도 보강 조사·404는 초기 색인 후보에서 제외하며 접근 가능한 페이지 자체는 삭제하지 않는다. 임의 검색/비교 조합이나 가짜 lastmod를 생성하지 않는다.
- 공개 헤더 초안은 CSP/frame/nosniff/referrer/permissions를 준비하고 Pages 기본 캐시부터 사용한다. 오래된 JS가 남지 않도록 비해시 자산의 장기 immutable 캐시는 추가하지 않는다.
- manifest에는 통계 false·이메일 null·공개/색인 승인 false·미해결 항목 2개를 유지한다. 승인 상태나 연락처를 임의 승격한 계획은 검증에서 거부한다.
- 기존 후보 생성기·Cloudflare 빌드 명령·출력 경로·Access·noindex 정책은 변경하지 않았다. 새 도구에는 배포나 승인 해제 기능이 없다. 초안은 자동으로 사이트에 합쳐지지 않는다.
- [GitHub CI](../.github/workflows/validate.yml)에 비활성 초안을 생성하는 로컬 빌드 검사만 추가했다. 배포/도메인/API 호출이나 새 권한·비밀값은 추가하지 않았다.

## 실제 검증

| 항목 | 결과 |
| --- | --- |
| 변경 전 Python 전체 | 626개 통과 |
| 변경 후 Python 전체 | 633개 통과 |
| 새 준비 생성기 테스트 | 7개 통과 |
| 데스크톱·모바일 브라우저 전체 | 226개 통과; 사용자 미커밋 테스트 14개 포함 |
| 내부 경로·HTML·메타데이터·공개 보류 | 기존 검사기 통과 |
| 제품 정적 문서·10종 보강 문서 | 기존 원본으로 재현성 검사 통과 |
| 준비 출력 | 59개 비공개 파일 + 문서 루트 밖 초안 5개, 공개/업로드 없음 |
| 원본 보존 | data/schema와 기존 사용자 변경 4개 SHA-256 일치 |
| diff·문서 경로·초안 형식 | diff 검사, 상대 경로, JSON/XML·hash 검사 통과 |

새 [Python 테스트](../tests/test_prepare_monipick_release.py)는 실제 패키지의 보류 유지, 초안 미노출, 이메일/승인/통계 정책, canonical·색인 범위 오류, 중복 경로, sitemap 중복/lastmod 방지, hash/원본 보존, 기존 폴더 덮어쓰기 금지, 헤더/리다이렉트 범위를 검사한다. 새 [브라우저 테스트](../tests/e2e/operations-guide.spec.js)는 데스크톱/모바일에서 안내와 미정 연락처·폼 미생성·가로 넘침을 검사한다.

```sh
python3 -m unittest discover -s tests -q
python3 -m unittest tests.test_prepare_monipick_release -q
npm run test:e2e -- --workers=2
python3 scripts/validate_local_site.py
python3 -m scripts.build_monitor_pages_v3 --check
python3 -m scripts.build_monitor10_review --check
python3 -m scripts.prepare_monipick_release --output /tmp/monipick-release-prep-20261022
```

GitHub CI는 이 보고서와 코드를 함께 push한 커밋의 check를 기준으로 확인한다. [준비 브랜치 실행 목록](https://github.com/dineyong/connectable/actions?query=branch%3Acodex%2Fmonipick-cloudflare-preparation)에서 해당 SHA를 확인할 수 있다. 최종 완료 응답에는 실제 확인한 실행 URL과 결과를 기록한다. CI에는 사용자 미커밋 테스트 14개를 포함하지 않아 브라우저 수가 로컬과 다르다.

## 적용하지 않은 것과 남은 단계

- 실제 운영 배포, DNS/Custom domain, production 자동 배포, canonical/robots/색인 정책 적용, 검색 제출, 분석 도구·광고·제휴 활성화, main 병합은 하지 않았다.
- 기존 비공개 검수 브랜치와 `3afd8034` 배포는 변경하지 않았다. 새 운영 안내는 저장소와 로컬 검증 기준이며 원격에 반영됐다고 주장하지 않는다.
- 현재 준비 패키지의 문서 루트는 site/뿐이다. 초안 5개를 넣은 상위 디렉터리 전체를 업로드하지 않는다.
- 사용자에게 남은 항목은 **공개 가능한 이메일**과 **최종 공개 승인**이다. 이메일이 오면 안내에 반영하고 공개 후보를 재검수한다.
- 공개 승인 후에만 초안을 실제 릴리스 출력물에 일관되게 적용하고 운영 origin/호스트 이동/200/404/헤더/색인/모바일을 검증한다. 현재 초안·로컬 테스트는 도메인에서의 실제 동작이나 법적 안내의 완결성을 보장하지 않는다.
- 사진·남은 SKU·댓글·공개 반응 서버·광고·실시간 뉴스는 첫 출시의 추가 필수 조건으로 늘리지 않는다.

사용자 변경 README/DECISIONS/content-review.spec.js/site-v2.js 및 기존 미추적 문서는 보존했다. 테스트가 갱신한 기존 캡처 2개만 실행 전 Git 내용으로 복원했다. 원본 조사·판정 데이터나 과거 보고서는 변경하지 않았다.
