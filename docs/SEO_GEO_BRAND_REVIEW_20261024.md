# 모니픽 구조화 데이터·공유 이미지·파비콘 검토본

2026-10-24. 로컬 검토용이며 운영 배포는 하지 않았습니다.

## 변경 내용

- 홈페이지에 WebSite 1개, 색인 대상 34개 페이지에 WebPage를 추가했습니다. 기존 제목·설명·대표 URL을 그대로 사용합니다.
- 제품 상세 30개에 화면에 표시되는 ‘홈 → 전체 모니터 → 해당 제품’과 같은 BreadcrumbList를 추가했습니다.
- 가격·재고·별점·리뷰·FAQ·Product 구조화 데이터는 추가하지 않았습니다. 현재 확인된 화면 정보만 표시합니다.
- 기존 짙은 녹색과 밝은 배경을 사용한 공통 공유 이미지(1200×630 PNG)를 제작했습니다. Open Graph와 Twitter 이미지 및 대체 텍스트를 연결했습니다.
- 같은 모니터 모양 아이콘으로 SVG, PNG 48/180/192, ICO 16/32/48을 준비했습니다. 브라우저 탭과 Apple 홈 화면 아이콘을 연결했습니다.
- 기존 본문, 제품 설명, 내부 링크, CSS/JS, robots, canonical, 사이트맵 및 보안 정책은 유지했습니다.

## 검토

로컬 검토: http://127.0.0.1:8886/

제품 상세: http://127.0.0.1:8886/monitors/dell-u2724d/

공유 이미지: http://127.0.0.1:8886/assets/brand/monipick-share-v1.png

홈·Dell 상세·구매 가이드를 PC 1280px 및 모바일 390px에서 기존 검토본과 비교한 6가지 조합 모두 스크린샷 픽셀이 동일했습니다. 가로 넘침과 브라우저 오류가 없었고, 이미지/아이콘 6개 모두 HTTP 200과 올바른 MIME 유형을 확인했습니다. 증거: `design/brand-review-20261024/browser-results.json`.

구조화 데이터, 화면 경로와 일치 여부, 원본 본문 보존, 이미지 크기, 메타 태그, JSON 삽입 안전성, 승인 플래그 및 파일 변조 거부, 정적 자산 응답을 자동 검증했습니다.

전체 Python 테스트 688개와 `git diff --check`가 통과했습니다.

현재 운영 빌드 승인 및 배포 경로는 변경하지 않았습니다. 새 이미지의 운영 URL은 배포 이후에만 실제로 제공되며, 카카오 등 외부 서비스의 공유 캐시와 Google 검색 표시 채택 여부는 아직 확인 대상이 아닙니다. Google의 사이트 이름 선택이나 리치 결과 노출은 구조화 데이터 추가만으로 보장되지 않습니다.

## 근거 문서

- https://developers.google.com/search/docs/appearance/site-names
- https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- https://developers.google.com/search/docs/appearance/favicon-in-search
- https://ogp.me/
