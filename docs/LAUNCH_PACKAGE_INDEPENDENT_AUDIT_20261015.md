# 출시 후보 패키지 독립 검수 · 2026-10-15

기준: `codex/monitor-purpose-design` · `c9cbfb78ced4559728003056f72d57dd122a951d`.

범위는 [패키지 생성기](../scripts/prepare_launch_preview.py), [회귀 테스트](../tests/test_prepare_launch_preview.py), [HTML 검사기](../scripts/validate_local_site.py), 실제 `/tmp/connectable-launch-preview-20261015-final/site`이다. 읽기 전용으로 검수하고 고립된 임시 복사본에만 잘못된 입력을 주입했다. 원본 코드·제품 데이터·사용자 변경은 수정하지 않았다. 전체 브라우저 테스트, 외부 자료 수집, 서버 배포는 이 세션에서 수행하지 않았다.

## 실제 후보 확인

| 항목 | 결과 | 확인 방법 |
| --- | --- | --- |
| 파일 목록 및 해시 | 통과 | manifest 55개와 실제 파일 SHA256 전부 일치 |
| HTML 문서 | 통과 | 루트 별칭 포함 36개. 기존 기본 대상 외 보강페이지까지 확장 검사 결과 오류 0 |
| 현재 디자인 진입점 | 통과 | 후보 index.html은 monitor-v3.html의 복사본이며 기존 원본 index.html은 그대로 보존 |
| 제품 상세 | 통과 | monitors 하위 30개 정적 상세 포함 |
| 의존성 | 현재 후보 통과 | 명시적 HTML href/src의 로컬 파일·fragment 검사 통과. CSS url/@import, JS fetch/Worker/import 동적 의존성 발견 없음 |
| 과거 화면 격리 | 통과 | legacy.html, review.html, site-v2.js, research 원본·스크린샷 제외. manifest는 site 밖에 있음 |
| 자료 구분 | 통과 | 상세와 비교에 문서지역·한국 SKU 미확인·사람검토 보류 표시. 보강페이지는 별도 지역 사실을 기존 제품 승인으로 승격하지 않음 |
| 공개 보류 | 현재 후보 통과 | 모든 HTML 실제 robots noindex 확인. manifest deployment_authorized=false/domain=null |
| 패키지 회귀 테스트 | 통과 | `python3 -m unittest tests.test_prepare_launch_preview -v`: 6개 통과 |

후기·제조사 원문 링크는 기존 산출물을 포함한 것이며 이번 세션에서 외부 원문이나 리다이렉트를 재확인하지 않았다. 현재 후보의 데이터 정확도·사진 사용권·한국 SKU 동일성·호환성 승인까지 이 결과가 보장하지 않는다.

## 잘못된 입력 재현: 현재 파일의 오류와 검사 경계의 빈틈 구분

현재 패키지에서 아래 오류가 발견된 것은 아니다. 그러나 같은 생성기가 손상된 미래 입력을 승인할 수 있다. 임시 `web` 복사본에 각각 아래 변경을 한 뒤 `prepare(new_output, web=temporary_web)`를 호출했다. 네 경우 모두 예외 없이 55파일 패키지가 생성됐다.

### P2-1. 보강페이지의 실제 noindex·canonical·의존성 검사 누락

`validate_site()` 기본 목록에는 monitor-v3, 제품목록/상세, 가이드, 뉴스만 있다. 명시적으로 배포후보에 들어가는 monitor10-review.html은 기본 검증 대상에서 빠진다. 마지막 HTML 보호는 문자열 `noindex` 존재만 검사하므로 실제 robots directive를 보증하지 않는다.

독립 재현 입력:

1. monitor10-review.html의 `content="noindex,nofollow"`를 `content="index,follow"`로 바꾸고 끝에 `<!-- historical noindex -->` 추가 → 승인.
2. 같은 페이지 head에 `<link rel="canonical" href="https://example.invalid/product">` 추가 → 승인.
3. 같은 페이지 head에 `<link rel="stylesheet" href="missing.css">` 추가 → 승인.

영향: 현재 보강페이지는 올바르지만, 이후 수정에서 공개 보류·내부 경로 계약이 페이지마다 달라질 수 있다. 온라인 공개에 들어가기 전에 반드시 닫아야 할 경계다. 모든 포함 HTML을 실제 metadata/경로 검사 대상으로 삼고, 루트 index와 monitor-v3가 의도적 별칭이라는 이유로 동일 title/description을 허용하는 방식이 적절하다. substring 검사만 늘리는 방식은 부족하다.

### P2-2. 실행 스크립트 및 파생 데이터 바이트의 검증 범위 부족

임시 monitor-v3-data.js 전체를 아래로 바꿨다.

```js
window.CONNECTABLE_MONITORS = ;
```

생성기는 승인했다. HTML 검사는 파일의 존재만 확인하며 JS 구문이나 원본에서 올바르게 생성한 artifact인지 확인하지 않는다. manifest SHA256은 복사본 동일성만 증명하고 내용 유효성을 증명하지 않는다.

영향: 이 입력은 JS SyntaxError를 일으키며 현재 UI는 데이터가 없으면 불러오기 실패/기능 비활성 처리하므로 호환성 승인으로 바뀌지는 않는다. 하지만 “정상 후보 패키지 생성 통과”가 기능 정상임을 뜻하지 않게 된다. 파생 산출물 원본 계약 검사 및 JS 구문 검사 또는 실제 브라우저 후보 smoke test를 독립적으로 연결해야 한다. 기존 CI의 생성기 --check와 브라우저 검사와 중복될 수 있으므로 한 검사 계층을 명확히 소유하게 하고 테스트 통과 표현을 좁혀야 한다.

## 파일 경로 및 보안 경계

- 누락 파일, 파일 자체 symlink, resolve 후 원본 web 바깥으로 향하는 파일은 생성기에서 차단한다. 실제 자산에서 우회·원본 노출은 발견하지 않았다.
- 임시 monitors/aoc-q27g3xmn 디렉터리를 같은 web 내 shadow-aoc로 옮기고 symlink로 연결한 입력도 상대 경로가 web 밖을 가리키는 것으로 판정되어 원본 검증 단계에서 거부됐다. 이 한 재현은 모든 symlink/경합 조건을 증명하지 않는다.
- 출력은 기존 경로를 덮어쓰지 않고, 소스 web 내부 출력도 금지한다. web 외 새 디렉터리의 생성은 허용된 로컬 동작이다.
- 현재는 오프라인 패키지다. HTTP 인증·CSP 및 보안 헤더·캐시·404 정책·호스팅 fallback은 포함하지 않는다. 로컬 noindex는 접근통제가 아니며 업로드/공개 승인도 아니다.
- 최종 원격 미리보기는 승인된 호스팅에서 실제 URL·인증·헤더·404·모바일을 다시 확인해야 한다. 이 세션은 서비스 전체 보안 감사가 아니다.

## 권장 순서와 판단

1. 보강페이지 포함 모든 HTML의 noindex·canonical·로컬 경로 검증을 통일하고 위 3개 실패 입력 회귀 테스트 확보.
2. 패키지 단계의 JS/파생 자산 검증 책임을 기존 생성기 검사와 연결하고 malformed JS 거부 또는 실제 후보 smoke 결과를 필수로 기록.
3. 수정한 패키지를 새 경로에 생성하여 모든 파일 hash 및 실제 후보 브라우저 동선을 다시 확인.
4. 사용자 도메인·호스팅 결정 이후 접근 제한 원격 미리보기와 공개 승인 절차 진행.

현재 정상 패키지를 로컬에서 계속 검토하는 것은 가능하다. 잘못된 입력 검사 빈틈을 확인했으므로 생성 성공만으로 공개 준비 완료를 판정하지 않는다. main 병합·실제 공개는 보류한다.

## 후속 수정 독립 재검증 · 2026-10-15

루트 세션이 위 P2 경계에 회귀 테스트 4개를 먼저 추가하여 수정 전 실패를 확보한 뒤 생성기를 보강했다. 이 세션은 변경 코드를 읽고 targeted 테스트와 원래 잘못된 입력 4개를 독립적으로 다시 실행했다. 초기 발견 내용은 수정 전 기록으로 보존하며, 아래 결과가 현재 수정본의 판단이다.

- 모든 패키지 포함 HTML을 원본·후보 양쪽에서 실제 metadata/경로 검사 대상으로 삼는다. 루트 index 별칭은 별도 검사하여 monitor-v3와 의도적인 동일 title/description을 허용한다. 문자열 noindex 검사는 실제 robots 검사로 대체됐다.
- 모니터·후기링크·저장 뉴스·제품뉴스의 4개 파생 데이터 JS를 검증된 기존 원본으로 메모리 내 재생성한 기대값과 비교한다. 원본과 복사본에서 모두 byte 일치를 요구하며 원본 생성/수정 또는 네트워크 수집은 하지 않는다.
- `python3 -m unittest tests.test_prepare_launch_preview -v`: **10개 통과**. 정상 패키지 및 원본 보존 테스트도 통과했다.
- malformed monitor-v3-data.js는 `stale or altered generated display data`로 거부됐다.
- 보강페이지 index/주석noindex는 `local preview must preserve unambiguous noindex`, canonical은 공개URL보류, missing.css는 로컬대상누락 오류로 각각 거부됐다.
- 네 비정상 입력 모두 출력 디렉터리가 생성되지 않았다. 원본은 TemporaryDirectory 복사본에만 변조했다.

따라서 **이번 세션에서 재현한 4개 검증 빈틈은 수정본에서 차단 확인**했다. 4개 파생 데이터에 대한 원본 일치 검사는 임의 JS 전부의 구문·보안 감사가 아니며, 일반 실행스크립트와 실제 브라우저 동선 검증은 계속 별도 검사로 유지해야 한다. 호스팅 인증·헤더·404 동작·도메인·공개승인 또한 아직 별도 단계다. 이번 후속 확인은 루트가 추가할 수 있는 404 화면 및 전체 통합 테스트의 최종 결과를 대신하지 않는다.
