"""Local inventory of existing evidence; not a new source check or publication approval."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/site/monitor-v3.json'
OUTPUT = ROOT / 'docs/PRODUCT_INFORMATION_IMAGE_INVENTORY.md'
LABELS = {'size':'크기', 'width':'가로 픽셀', 'height':'세로 픽셀', 'refresh':'주사율', 'panel':'패널', 'usb_c_video':'USB-C 영상'}


def build(raw):
    data = json.loads(raw)
    products = data['products']
    lines = ['# 제품 정보·이미지 준비 목록', '',
             '기존 파생 데이터의 정리이며 공식 원문 재확인이나 이미지 사용권 검증 결과가 아니다.', '',
             f'- 원본: `data/site/monitor-v3.json` · SHA-256 `{hashlib.sha256(raw).hexdigest()}`',
             f'- 제품 {len(products)}종 · 자료 확인일 {data["checked_on"]} · 공개 상태 {data["public_status"]}',
             '- 이미지: 모든 제품은 CSS 형태 예시. 제품 사진 원본 URL·권리자·상업 사용 허용 근거·모델/지역 일치 검토는 미확인. 실제 사진 적용 0건.',
             '- 승인된 이미지 레지스트리가 아직 없으므로 이 목록은 제품에 사진 사용권을 부여하지 않는다.',
             '- 자세한 기존 이미지 검토: [기존 보고서](MONITOR_IMAGES_AND_GUIDES_REPORT.md). 이번에 해당 이용 조건을 재확인하지 않았다.', '',
             '| 제품 ID / 모델 | 문서 지역 | 검색 핵심값 미확인 | 기록된 결측 수 | 공식 출처 | 이미지 |',
             '| --- | --- | --- | --- | --- | --- |']
    for p in sorted(products, key=lambda x:(x['manufacturer'], x['display_model'])):
        missing = [LABELS[k] for k in LABELS if p['filters'].get(k) is None]
        sources = ' · '.join(f'[문서 {i+1}]({s["url"]})' for i,s in enumerate(p['source_refs']))
        lines.append(f'| `{p["id"]}` / {p["manufacturer"]} {p["display_model"]} | {p["region"]} | {", ".join(missing) or "없음 (검색용 값만)"} | {len(p["missing_fields"])} | {sources} | 형태 예시 / 사진 권한 미확인 |')
    lines += ['', '## 기록된 결측 빈도', '', '| 필드 | 제품 수 |', '| --- | --- |']
    counts = Counter(f for p in products for f in p['missing_fields'])
    lines += [f'| `{key}` | {count} |' for key,count in counts.most_common()]
    lines += ['', '## 적용 우선순위', '',
              '1. 크기·패널·주사율 등 검색 핵심값이 없는 제품부터 공식 원문 보완. 입력 포트 조건이 다른 주사율을 무조건적인 최대값으로 합치지 않는다.',
              '2. 한국 판매 모델 대조: 동일 모델명만으로 지역 SKU·보증·전력을 승격하지 않는다.',
              '3. 사진 자료 확보: 제품 ID, 지역/색상, 원본 URL 또는 파일, 권리자, 사용 허용 증빙, 허용 범위, 확인일, 출처 표기, 대체 텍스트를 함께 검토한다.',
              '4. 승인 전까지 CSS 형태 예시를 유지한다. 상품 소개 페이지 URL은 이미지 라이선스가 아니다.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build(SOURCE.read_bytes())
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text() != result:
            raise SystemExit('FAIL: product inventory differs from current source')
        print('PASS: product information/image inventory matches source')
    else:
        OUTPUT.write_text(result)


if __name__ == '__main__':
    main()
