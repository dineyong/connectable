# 질문 코퍼스 기반 작업 기록

- 확인일: 2026-10-07 (Asia/Seoul)
- 브랜치: research/question-corpus-foundation
- 기준 커밋: c58dee5f3d1222d49e598dddbac5c8c6a7b4b8f0
- README 및 docs 기준선 전체를 읽음. 기존 사용자 변경 없음.
- origin/main fetch 후 기준 HEAD와 차이 0 확인.
- 작업 전 테스트: python3 -m unittest discover → 0건. 기존 테스트 없음.
- 범위: 스키마·수집 기준·검증 도구·실제 example 5건. 제품 개발 없음.

조사 및 최종 검증 결과는 해당 작업 완료 시 아래에 추가한다.

## 조사 결과

공개 본문을 직접 확인한 실제 사례 5건. 본문 전체와 개인 사용자명은 저장하지 않았다.

| ID | 출처 | 보고 결과 | 주의점 |
|---|---|---|---|
| UQ-0001 | [Apple 커뮤니티](https://discussions.apple.com/thread/254292556) | 미해결 | M1 Air + Thunderbolt Display 두 대 + D6000; 드라이버·경로 미상 |
| UQ-0002 | [Apple 커뮤니티](https://discussions.apple.com/thread/252168947) | 미해결 | M1 Air + BenQ EW3280U 4K 30Hz; 다른 댓글의 해결 결과 미통합 |
| UQ-0003 | [Dell 게시판](https://www.dell.com/community/en/conversations/monitors/s3221qs-m1-macbook-pro-periodic-black-screen-fix/647f9fc4f4ccf8a8de4ad0cf) | 성공 자기보고 | M1 Pro MBP + S3221QS; 60Hz 항목 변경 후 화면 꺼짐 해소; 이후 가변 표시 |
| UQ-0004 | [Apple 커뮤니티](https://discussions.apple.com/thread/255860955) | 미해결 | M2 Air + ViewSonic; 모델명 미상; macOS 15.1.1 이후 검은 화면 |
| UQ-0005 | [Dell 게시판](https://www.dell.com/community/en/conversations/monitors/s3422dw-macbookpro-m1-input-timing-is-not-supported/647f9a74f4ccf8a8dee19ade) | 제한적 성공 | 14인치 2021 MBP의 원문 M1 표기는 모델 검수 필요; 2560×1080만 성공 보고 |

모두 영어 원문이며 C등급이다. 공식 대조는 후속 단계로 남겼으며 모두
NOT_CHECKED, NEEDS_REVIEW, usable_for_compatibility=NO다. 원문에서 명시되지
않은 픽셀 해상도·OS·출시 연도·PD·클램쉘·확장 모드·포트는 추정하지 않았다.
목표 해상도와 관측된 실제 해상도를 분리했다.

클리앙·퀘이사존 한국어 후보 검색에서는 이 회차에 조건을 만족하는 공개
본문을 확보하지 못했다. 한국어 Reddit 후보와 별도 Apple 후보 각 1개는
본문 열기 오류로 제외했다. 차단 원인을 추정하거나 우회하지 않았다.
한국어 질문 100건 수집은 미완료이며 영어 example은 목표 건수에 미산입이다.
단일 사례·과거 OS·모델 결측 때문에 이 데이터만으로 호환성을 확정할 수 없다.
