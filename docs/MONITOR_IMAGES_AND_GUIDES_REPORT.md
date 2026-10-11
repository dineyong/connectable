# 제품 이미지 검토 및 구매 가이드

- 작업일: 2026-10-11
- 브랜치: `codex/monitor-purpose-design`
- 기준: `62bb5af`
- 최종 커밋: 이 문서를 포함한 Git 커밋으로 식별.

## 제품 이미지: 적용 보류

실제 제품 사진을 확보·적용했다고 보고하지 않는다. 이번에는 대표 제조사 Dell/ASUS의 공개 이용 조건과 공식 미디어 경로를 확인했다. 30개 제품의 이미지 권리를 모두 검토한 것은 아니다. 다운로드·핫링크·새 외부 이미지 요청은 없으며 기존 CSS 모니터 그림을 유지한다.

| 대상 | 확인 URL·위치 | 결과 |
|---|---|---|
| Dell | https://www.dell.com/en-us/legal/lp/site-terms-of-use-copyright · Copyrights, Materials 사용 허용 문단 | 개인·비상업 이용 범위의 허용을 확인. 이 제휴마케팅 사이트의 상업 재사용 권한은 확보하지 못했으므로 보류 |
| Dell assetshare | https://dam.dell.com/content/dell-assetshare/new-access-request-form.html | 검색 후보. 로그인·동의·신청이나 개별 이미지 사용권 확인은 수행하지 않음 |
| ASUS | https://www.asus.com/terms_of_use_notice_privacy_policy/official-site/ | 검색에서는 이용 조건이 표시됐으나 직접 열기는 도구 오류. 검색 요약으로 사용권을 확정하지 않음 |
| ASUS 지역 안내 | https://www.asus.com/sg/ASUS_Website_Information/Legal_information/ | 직접 페이지는 열렸지만 추출된 내용으로 상업 이미지 재사용 허용을 확인하지 못함 |
| ASUS 미디어 키트 | https://press.asus.com/media/media-kit/ | 검색 후보. 개별 제품·이미지별 조건은 미확인 |
| 나머지 제조사 | 이번 배치 미검토 | 허용 또는 금지로 추정하지 않음 |

사진 도입 시 필요한 기록: 정확한 제품 ID/지역/색상, 원본 이미지 URL, 권리자, 허용 근거와 적용 범위, 확인일, 필요한 출처 표기. 공식 홈페이지에 이미지가 있다는 사실과 재사용 권한은 별도다. 직접 촬영 원본 또는 허용 범위가 명시된 공급 자료를 받으면 모델과 조건을 확인한 뒤 반영한다. 현재 CSS 그림은 실제 제품 사진으로 표시하지 않는다.

## 구매 가이드 구현

[구매 가이드](../web/guides/monitor-buying.html)에 해상도·배율, 주사율·입력 조건, USB-C 영상·충전의 세 항목과 구매 전 확인 목록을 작성했다. 자체 CSS로 해상도 표기 예시를 만들었으며 실제 선명도 시뮬레이션으로 설명하지 않는다. 기존 메인 가이드 요약에서 해당 항목 또는 전체 가이드로 이동하고 제품 목록으로 돌아올 수 있다.

제품 추천 순위, 가짜 가격·후기, 개별 호환성 보장을 추가하지 않았다. 공식 원문을 길게 복제하지 않고 자체 설명과 선택 절차를 작성했다. 확인 날짜와 근거 링크를 표시하며 로컬 `noindex,nofollow`를 유지한다.

## 직접 확인한 가이드 근거

- Microsoft 해상도·배율: https://support.microsoft.com/en-us/windows/hardware/display-graphics/change-your-screen-resolution-and-layout-in-windows · Change the size of text and apps / Change the display resolution.
- Microsoft 주사율: https://support.microsoft.com/en-au/windows/hardware/display-graphics/change-the-refresh-rate-on-your-monitor-in-windows · To change the refresh rate / Important / Summary.
- VESA DisplayPort FAQ: https://www.displayport.org/faq/ · USB-C benefits, USB data/Power Delivery, Alt Mode support identification. 구형 문서의 최대 전력/최대 해상도 수치를 현행 보편 한도로 사용하지 않음.

## 보존과 남은 과제

원본 제품·코퍼스·후기·기존 사용자 변경을 수정하지 않는다. 기존 main 및 공개 배포는 변경하지 않는다. 제품별 실제 이미지 0개 추가. 다른 제조사 이미지 검토, 지역별 권리 범위 확인과 이미지 허가 확보는 남아 있다. 실제 운영 댓글, 광고·제휴 활성화, 공개 검색 노출은 이번 범위 밖이다.

## 검증 결과

- Python 전체: `python3 -m unittest discover -s tests -q` — 526 통과, 39.598초.
- 브라우저 전체: `npm run test:e2e -- --workers=2` — 146 통과, 56.0초.
- 새 가이드 데스크톱/모바일 테스트 2개: 목차, 출처 3개, noindex, 가로 넘침, axe 접근성, 목록 복귀 검증.
- 로컬 146개 중 기존 미커밋 테스트 14개는 이 커밋에서 제외. 원격 예상 132개.
- 메인·가이드의 내부 파일 경로/앵커 확인 통과, `git diff --check` 통과.
- 원본 data 변경 없음. 브라우저 스크린샷 생성으로 바뀐 기존 테스트 산출물은 복원.
- [데스크톱 검수 화면](screenshots/monitor-buying-guide-desktop.png), [모바일 검수 화면](screenshots/monitor-buying-guide-mobile.png).
