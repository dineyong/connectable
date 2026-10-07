# Path Instance 최초 5건 사람 검수 자료

- 작성일: 2026-10-08
- 상태: REVIEW_CANDIDATES / PENDING_HUMAN_REVIEW
- 기준 경로: [path_instances_v1.json](../data/rules/path_instances_v1.json)
- 구조: [path-instance-v1.schema.json](../schemas/path-instance-v1.schema.json)
- 승인 골든: **0/30**. 아래 예상 결과는 AI 작성 검토안으로 사람 정답이 아니다.

모두 예정 구성이다. 실제 연결 성공 기록이나 실사용 재현 결과로 읽지 않는다.
현재 공식 catalog와 pilot에 이미 확인된 claim을 연결했다. 제품을 추가 조사하거나
공식 자료의 최대값을 조합 전체의 성공 보증으로 확장하지 않았다.

사람은 각 건의 제품 식별·포트 연결·근거 범위·조건·기대 상태를 독립적으로 검토해야 한다.
검토 의견 또는 승인 이력 없이 이 파일이나 테스트 통과만으로 승인 건수를 올리지 않는다.
승인 시에도 UNKNOWN 사례를 승인할 수 있으며, 공개 COMPATIBLE 승인은 별도다.

| 경로 | 골든 계획 | 검토안 | 내부 실행 | 공개 | 사람 승인 |
|---|---|---|---|---|---|
| PI-001 | GP-02 | UNKNOWN | UNKNOWN | UNKNOWN | 대기 |
| PI-002 | GP-03 | UNKNOWN | UNKNOWN | UNKNOWN | 대기 |
| PI-003 | GP-07 | UNKNOWN | UNKNOWN | UNKNOWN | 대기 |
| PI-004 | GP-06 | UNKNOWN | UNKNOWN | UNKNOWN | 대기 |
| PI-005 | GP-25 | INCOMPATIBLE | INCOMPATIBLE | UNKNOWN | 대기 |

## PI-001 / GP-02

### 제품과 목표

- `host`: SOURCE / `product:air-m1-2020` / EXACT
- `middle`: CABLE / `product:cablematters-201036` / EXACT
- `screen1`: DISPLAY / `product:dell-g2724d` / EXACT

```json
{
  "output_method": "NATIVE",
  "independent_external_count": 1,
  "display_device_ids": [
    "screen1"
  ],
  "context": {
    "os_family": "macOS",
    "os_version": "14.3",
    "builtin_state": "ON",
    "lid_state": "OPEN"
  },
  "targets": [
    {
      "display_device_id": "screen1",
      "width": 2560,
      "height": 1440,
      "refresh_hz": 60
    }
  ]
}
```

### 포트와 영상 경로

| 포트 ID | 기기 | 커넥터 | 식별 범위 | claim |
|---|---|---|---|---|
| host-usbc | host | USB_C | PORT_CLASS_MEMBER | product:air-m1-2020:ports |
| middle-in | middle | USB_C | DOCUMENTED_PORT | cablematters-201036:1 |
| middle-out | middle | DISPLAYPORT | DOCUMENTED_PORT | cablematters-201036:1 |
| screen1-in | screen1 | DISPLAYPORT | DOCUMENTED_PORT | dell-g2724d:1 |

```text
host-to-middle: host-usbc → middle-in [PHYSICAL]
middle-route: middle-in → middle-out [INTERNAL_ROUTING]
middle-to-screen: middle-out → screen1-in [PHYSICAL]
```

### 근거

- `cablematters-201036:1`: USB-C 소스에서 DP 입력 화면으로 연결하는 케이블 / 위치: Article 79 / introductory specification; full 8K troubleshooting / [SRC-cablematters-201036](https://kb.cablematters.com/index.php?EntryID=79&View=entry)
- `dell-g2724d:1`: DisplayPort에서 2560×1440 165Hz / 위치: Resolution / Refresh Rate; Ports / [SRC-dell-g2724d](https://www.dell.com/en-us/shop/dell-27-gaming-monitor-g2724d/apd/210-bhxc/monitors-monitor-accessories)
- `product:air-m1-2020:display`: 내장 화면과 동시에 외장 1대, 최대 6K 60Hz / 위치: 비디오 지원 / [APPLE-111883](https://support.apple.com/ko-kr/111883)
- `product:air-m1-2020:ports`: Thunderbolt/USB 4 포트 2개에서 충전 및 DisplayPort 지원 / 위치: 충전 및 확장 / [APPLE-111883](https://support.apple.com/ko-kr/111883)

### 조건·공유 자원·전력 구조

```json
{
  "predicates": [],
  "resources": [],
  "power_flows": []
}
```

### 검토 결과안과 남은 정보

정확한 경로 전체 영상/전원 조건과 검수 근거 부족

- `포트별 상세 영상 협상·색 조건`
- `최종 사람 검수`

내부 결과: **UNKNOWN**, 공개 결과: **UNKNOWN**. 기록된 전력 상한: NoneW (실제 충전량 아님).

- 요청 SHA-256: `a2b9f6d737f5d17a0c06de8e313642bce5c0ce18c9a5715f49d335a428af0a0f`
- 근거 catalog SHA-256: `f93cbf9b755f39dad92725776a2c2e67c658f3a4dc7dc0a1075ef40b9d2f884f`
- 규칙 버전: `path-instance-v1.0`
- 사람 검수자·검수일·승인 결과: **미기록 / 대기**

## PI-002 / GP-03

### 제품과 목표

- `host`: SOURCE / `product:air-m1-2020` / EXACT
- `middle`: ADAPTER / `product:belkin-avc002` / EXACT
- `screen1`: DISPLAY / `product:dell-g2724d` / EXACT
- `hdmi-cable`: CABLE / `UNKNOWN` / UNKNOWN

```json
{
  "output_method": "NATIVE",
  "independent_external_count": 1,
  "display_device_ids": [
    "screen1"
  ],
  "context": {
    "os_family": "macOS",
    "os_version": "14.3",
    "builtin_state": "ON",
    "lid_state": "OPEN"
  },
  "targets": [
    {
      "display_device_id": "screen1",
      "width": 2560,
      "height": 1440,
      "refresh_hz": 60
    }
  ]
}
```

### 포트와 영상 경로

| 포트 ID | 기기 | 커넥터 | 식별 범위 | claim |
|---|---|---|---|---|
| host-usbc | host | USB_C | PORT_CLASS_MEMBER | product:air-m1-2020:ports |
| middle-in | middle | USB_C | DOCUMENTED_PORT | belkin-avc002:1 |
| middle-out | middle | HDMI | DOCUMENTED_PORT | belkin-avc002:1 |
| screen1-in | screen1 | HDMI | DOCUMENTED_PORT | dell-g2724d:2 |
| hdmi-cable-a | hdmi-cable | HDMI | UNKNOWN | UNKNOWN |
| hdmi-cable-b | hdmi-cable | HDMI | UNKNOWN | UNKNOWN |
| middle-pd-in | middle | USB_C | DOCUMENTED_PORT | belkin-avc002:3 |

```text
host-to-middle: host-usbc → middle-in [PHYSICAL]
middle-route: middle-in → middle-out [INTERNAL_ROUTING]
middle-to-screen-a: middle-out → hdmi-cable-a [PHYSICAL]
hdmi-cable-route: hdmi-cable-a → hdmi-cable-b [INTERNAL_ROUTING]
middle-to-screen-b: hdmi-cable-b → screen1-in [PHYSICAL]
```

### 근거

- `belkin-avc002:1`: 호스트 USB-C→HDMI 영상, 별도 USB-C 전원 입력 / 위치: POWER AND VIDEO; CHARGE WHILE YOU WORK; ULTRA-HIGH-DEFINITION VIDEO / [SRC-belkin-avc002](https://www.belkin.com/tw/en/p/usb-c-to-hdmi-charge-adapter/P-AVC002.html)
- `belkin-avc002:3`: 별도 PD 입력을 통과해 최대 60W 공급 / 위치: POWER AND VIDEO; CHARGE WHILE YOU WORK; ULTRA-HIGH-DEFINITION VIDEO / [SRC-belkin-avc002](https://www.belkin.com/tw/en/p/usb-c-to-hdmi-charge-adapter/P-AVC002.html)
- `dell-g2724d:2`: HDMI에서 2560×1440 144Hz / 위치: Resolution / Refresh Rate; Ports / [SRC-dell-g2724d](https://www.dell.com/en-us/shop/dell-27-gaming-monitor-g2724d/apd/210-bhxc/monitors-monitor-accessories)
- `product:air-m1-2020:display`: 내장 화면과 동시에 외장 1대, 최대 6K 60Hz / 위치: 비디오 지원 / [APPLE-111883](https://support.apple.com/ko-kr/111883)
- `product:air-m1-2020:ports`: Thunderbolt/USB 4 포트 2개에서 충전 및 DisplayPort 지원 / 위치: 충전 및 확장 / [APPLE-111883](https://support.apple.com/ko-kr/111883)

### 조건·공유 자원·전력 구조

```json
{
  "predicates": [],
  "resources": [],
  "power_flows": [
    {
      "id": "adapter-power-route",
      "from_port": "middle-pd-in",
      "to_port": "middle-in",
      "mode": "PASS_THROUGH",
      "claim_refs": [
        "belkin-avc002:3"
      ]
    },
    {
      "id": "host-power-unknown",
      "from_port": "middle-in",
      "to_port": "host-usbc",
      "mode": "REQUIREMENT_UNKNOWN",
      "claim_refs": []
    }
  ]
}
```

### 검토 결과안과 남은 정보

정확한 경로 전체 영상/전원 조건과 검수 근거 부족

- `포트별 상세 영상 협상·색 조건`
- `최종 사람 검수`
- `별도 HDMI 케이블 모델`
- `외부 PD 공급 장치·입력 케이블`
- `Mac PD accepted profiles·어댑터 자체 소비`

내부 결과: **UNKNOWN**, 공개 결과: **UNKNOWN**. 기록된 전력 상한: 60W (실제 충전량 아님).

- 요청 SHA-256: `15129108f54e62de0ae9a75220e2989fd77e4748df8dc54528f5bbc8c5e3677a`
- 근거 catalog SHA-256: `f93cbf9b755f39dad92725776a2c2e67c658f3a4dc7dc0a1075ef40b9d2f884f`
- 규칙 버전: `path-instance-v1.0`
- 사람 검수자·검수일·승인 결과: **미기록 / 대기**

## PI-003 / GP-07

### 제품과 목표

- `host`: SOURCE / `product:air-m2-2022` / EXACT
- `middle`: CABLE / `product:apple-tb4-pro-cable` / PARTIAL
- `screen1`: DISPLAY / `product:dell-u2723qe` / EXACT

```json
{
  "output_method": "NATIVE",
  "independent_external_count": 1,
  "display_device_ids": [
    "screen1"
  ],
  "context": {
    "os_family": "macOS",
    "os_version": "14.3",
    "builtin_state": "ON",
    "lid_state": "OPEN"
  },
  "targets": [
    {
      "display_device_id": "screen1",
      "width": 3840,
      "height": 2160,
      "refresh_hz": 60
    }
  ]
}
```

### 포트와 영상 경로

| 포트 ID | 기기 | 커넥터 | 식별 범위 | claim |
|---|---|---|---|---|
| host-usbc | host | USB_C | PORT_CLASS_MEMBER | product:air-m2-2022:ports |
| middle-in | middle | USB_C | DOCUMENTED_PORT | apple-tb4-pro-cable:3 |
| middle-out | middle | USB_C | DOCUMENTED_PORT | apple-tb4-pro-cable:3 |
| screen1-in | screen1 | USB_C | DOCUMENTED_PORT | dell-u2723qe:2 |

```text
host-to-middle: host-usbc → middle-in [PHYSICAL]
middle-route: middle-in → middle-out [INTERNAL_ROUTING]
middle-to-screen: middle-out → screen1-in [PHYSICAL]
```

### 근거

- `apple-tb4-pro-cable:2`: 케이블 전력 전달 최대 100W / 위치: Video; Data transfer; Charging / Thunderbolt 4-specific paragraphs / [SRC-apple-tb4-pro-cable](https://support.apple.com/en-gb/118204)
- `apple-tb4-pro-cable:3`: DisplayPort HBR3 영상 출력 지원 / 위치: Video; Data transfer; Charging / Thunderbolt 4-specific paragraphs / [SRC-apple-tb4-pro-cable](https://support.apple.com/en-gb/118204)
- `dell-u2723qe:2`: 영상용 USB-C upstream은 DP 1.4 Alt Mode / 위치: Resolution / Refresh Rate; Ports; Tech Specs / [SRC-dell-u2723qe](https://www.dell.com/en-gb/shop/dell-ultrasharp-27-4k-usb-c-hub-monitor-u2723qe/apd/210-bcxk/monitors-monitor-accessories)
- `dell-u2723qe:3`: 영상용 USB-C upstream에서 최대 90W 공급 / 위치: Resolution / Refresh Rate; Ports; Tech Specs / [SRC-dell-u2723qe](https://www.dell.com/en-gb/shop/dell-ultrasharp-27-4k-usb-c-hub-monitor-u2723qe/apd/210-bcxk/monitors-monitor-accessories)
- `product:air-m2-2022:display`: 내장 화면과 동시에 외장 1대, 최대 6K 60Hz / 위치: 디스플레이 지원 / [APPLE-111867](https://support.apple.com/ko-kr/111867)
- `product:air-m2-2022:ports`: Thunderbolt/USB 4 포트 2개에서 충전 및 DisplayPort 지원 / 위치: 충전 및 확장 / [APPLE-111867](https://support.apple.com/ko-kr/111867)

### 조건·공유 자원·전력 구조

```json
{
  "predicates": [],
  "resources": [],
  "power_flows": [
    {
      "id": "monitor-offer",
      "from_port": "screen1-in",
      "to_port": "middle-out",
      "mode": "OFFER",
      "claim_refs": [
        "dell-u2723qe:3"
      ]
    },
    {
      "id": "cable-ceiling",
      "from_port": "middle-out",
      "to_port": "middle-in",
      "mode": "TRANSPORT_LIMIT",
      "claim_refs": [
        "apple-tb4-pro-cable:2"
      ]
    },
    {
      "id": "host-acceptance",
      "from_port": "middle-in",
      "to_port": "host-usbc",
      "mode": "REQUIREMENT_UNKNOWN",
      "claim_refs": []
    }
  ]
}
```

### 검토 결과안과 남은 정보

정확한 경로 전체 영상/전원 조건과 검수 근거 부족

- `포트별 상세 영상 협상·색 조건`
- `최종 사람 검수`
- `케이블 SKU·길이`
- `Mac PD 최소 요구·accepted profiles`

내부 결과: **UNKNOWN**, 공개 결과: **UNKNOWN**. 기록된 전력 상한: 90W (실제 충전량 아님).

- 요청 SHA-256: `695eecf3dae515356bb3e11859512fe9e7b98bed3e72d36ade8a25b42086fc02`
- 근거 catalog SHA-256: `f93cbf9b755f39dad92725776a2c2e67c658f3a4dc7dc0a1075ef40b9d2f884f`
- 규칙 버전: `path-instance-v1.0`
- 사람 검수자·검수일·승인 결과: **미기록 / 대기**

## PI-004 / GP-06

### 제품과 목표

- `host`: SOURCE / `product:air-m1-2020` / EXACT
- `middle`: DOCK / `product:plugable-ud-6950h` / EXACT
- `screen1`: DISPLAY / `product:dell-g2724d` / EXACT
- `screen2`: DISPLAY / `product:dell-g2724d` / EXACT
- `cable1`: CABLE / `UNKNOWN` / UNKNOWN
- `cable2`: CABLE / `UNKNOWN` / UNKNOWN
- `upstream-cable`: CABLE / `UNKNOWN` / UNKNOWN

```json
{
  "output_method": "DISPLAYLINK",
  "independent_external_count": 2,
  "display_device_ids": [
    "screen1",
    "screen2"
  ],
  "context": {
    "os_family": "macOS",
    "os_version": "14.3",
    "builtin_state": "ON",
    "lid_state": "OPEN",
    "displaylink_driver": "UNKNOWN"
  },
  "targets": [
    {
      "display_device_id": "screen1",
      "width": 2560,
      "height": 1440,
      "refresh_hz": 60
    },
    {
      "display_device_id": "screen2",
      "width": 2560,
      "height": 1440,
      "refresh_hz": 60
    }
  ]
}
```

### 포트와 영상 경로

| 포트 ID | 기기 | 커넥터 | 식별 범위 | claim |
|---|---|---|---|---|
| host-usbc | host | USB_C | PORT_CLASS_MEMBER | product:air-m1-2020:ports |
| middle-in | middle | UNKNOWN | UNKNOWN | plugable-ud-6950h:1 |
| middle-out1 | middle | DISPLAYPORT | PORT_CLASS_MEMBER | plugable-ud-6950h:1 |
| cable1-a | cable1 | DISPLAYPORT | UNKNOWN | UNKNOWN |
| cable1-b | cable1 | DISPLAYPORT | UNKNOWN | UNKNOWN |
| screen1-in | screen1 | DISPLAYPORT | DOCUMENTED_PORT | dell-g2724d:1 |
| middle-out2 | middle | DISPLAYPORT | PORT_CLASS_MEMBER | plugable-ud-6950h:1 |
| cable2-a | cable2 | DISPLAYPORT | UNKNOWN | UNKNOWN |
| cable2-b | cable2 | DISPLAYPORT | UNKNOWN | UNKNOWN |
| screen2-in | screen2 | DISPLAYPORT | DOCUMENTED_PORT | dell-g2724d:1 |
| upstream-cable-a | upstream-cable | USB_C | UNKNOWN | UNKNOWN |
| upstream-cable-b | upstream-cable | UNKNOWN | UNKNOWN | UNKNOWN |

```text
middle-route1: middle-in → middle-out1 [INTERNAL_ROUTING]
out-to-cable1: middle-out1 → cable1-a [PHYSICAL]
cable1-route: cable1-a → cable1-b [INTERNAL_ROUTING]
cable-to-screen1: cable1-b → screen1-in [PHYSICAL]
middle-route2: middle-in → middle-out2 [INTERNAL_ROUTING]
out-to-cable2: middle-out2 → cable2-a [PHYSICAL]
cable2-route: cable2-a → cable2-b [INTERNAL_ROUTING]
cable-to-screen2: cable2-b → screen2-in [PHYSICAL]
host-to-middle-a: host-usbc → upstream-cable-a [PHYSICAL]
upstream-cable-route: upstream-cable-a → upstream-cable-b [INTERNAL_ROUTING]
host-to-middle-b: upstream-cable-b → middle-in [PHYSICAL]
```

### 근거

- `dell-g2724d:1`: DisplayPort에서 2560×1440 165Hz / 위치: Resolution / Refresh Rate; Ports / [SRC-dell-g2724d](https://www.dell.com/en-us/shop/dell-27-gaming-monitor-g2724d/apd/210-bhxc/monitors-monitor-accessories)
- `plugable-ud-6950h:1`: DP/HDMI 출력은 독립 외장 화면 최대 2대, DisplayLink 드라이버 필요 / 위치: Features; 12 Ports; Monitor Compatibility; Power and Charging / [SRC-plugable-ud-6950h](https://plugable.com/products/ud-6950h/)
- `product:air-m1-2020:display`: 내장 화면과 동시에 외장 1대, 최대 6K 60Hz / 위치: 비디오 지원 / [APPLE-111883](https://support.apple.com/ko-kr/111883)
- `product:air-m1-2020:ports`: Thunderbolt/USB 4 포트 2개에서 충전 및 DisplayPort 지원 / 위치: 충전 및 확장 / [APPLE-111883](https://support.apple.com/ko-kr/111883)

### 조건·공유 자원·전력 구조

```json
{
  "predicates": [
    {
      "id": "driver",
      "context_key": "displaylink_driver",
      "operator": "EQ",
      "expected": "INSTALLED",
      "claim_refs": [
        "plugable-ud-6950h:1"
      ]
    },
    {
      "id": "os-version",
      "context_key": "os_version",
      "operator": "VERSION_GTE",
      "expected": "10.14",
      "claim_refs": [
        "plugable-ud-6950h:1"
      ]
    }
  ],
  "resources": [
    {
      "id": "video-pool",
      "device_id": "middle",
      "output_port_ids": [
        "middle-out1",
        "middle-out2"
      ],
      "max_independent_displays": 2,
      "claim_ref": "plugable-ud-6950h:1",
      "allocation_status": "AGGREGATE_ONLY"
    }
  ],
  "power_flows": []
}
```

### 검토 결과안과 남은 정보

정확한 경로 전체 영상/전원 조건과 검수 근거 부족

- `포트별 상세 영상 협상·색 조건`
- `최종 사람 검수`
- `물리 케이블과 독 출력 채널 쌍 매핑`
- `독 실제 upstream 단자와 호스트 케이블`

내부 결과: **UNKNOWN**, 공개 결과: **UNKNOWN**. 기록된 전력 상한: NoneW (실제 충전량 아님).

- 요청 SHA-256: `b02d98f0507367ab929c8337b1b372faa18c053c84ff49574c29f69fd2fbf867`
- 근거 catalog SHA-256: `f93cbf9b755f39dad92725776a2c2e67c658f3a4dc7dc0a1075ef40b9d2f884f`
- 규칙 버전: `path-instance-v1.0`
- 사람 검수자·검수일·승인 결과: **미기록 / 대기**

## PI-005 / GP-25

### 제품과 목표

- `host`: SOURCE / `product:air-m1-2020` / EXACT
- `middle`: HUB / `product:startech-mst14cd122hd` / EXACT
- `screen1`: DISPLAY / `product:dell-g2724d` / EXACT
- `screen2`: DISPLAY / `product:dell-g2724d` / EXACT
- `cable1`: CABLE / `UNKNOWN` / UNKNOWN
- `cable2`: CABLE / `UNKNOWN` / UNKNOWN

```json
{
  "output_method": "NATIVE",
  "independent_external_count": 2,
  "display_device_ids": [
    "screen1",
    "screen2"
  ],
  "context": {
    "os_family": "macOS",
    "os_version": "14.3",
    "builtin_state": "ON",
    "lid_state": "OPEN"
  },
  "targets": [
    {
      "display_device_id": "screen1",
      "width": 2560,
      "height": 1440,
      "refresh_hz": 60
    },
    {
      "display_device_id": "screen2",
      "width": 2560,
      "height": 1440,
      "refresh_hz": 60
    }
  ]
}
```

### 포트와 영상 경로

| 포트 ID | 기기 | 커넥터 | 식별 범위 | claim |
|---|---|---|---|---|
| host-usbc | host | USB_C | PORT_CLASS_MEMBER | product:air-m1-2020:ports |
| middle-in | middle | USB_C | DOCUMENTED_PORT | startech-mst14cd122hd:1 |
| middle-out1 | middle | HDMI | PORT_CLASS_MEMBER | startech-mst14cd122hd:1 |
| cable1-a | cable1 | HDMI | UNKNOWN | UNKNOWN |
| cable1-b | cable1 | HDMI | UNKNOWN | UNKNOWN |
| screen1-in | screen1 | HDMI | DOCUMENTED_PORT | dell-g2724d:2 |
| middle-out2 | middle | HDMI | PORT_CLASS_MEMBER | startech-mst14cd122hd:1 |
| cable2-a | cable2 | HDMI | UNKNOWN | UNKNOWN |
| cable2-b | cable2 | HDMI | UNKNOWN | UNKNOWN |
| screen2-in | screen2 | HDMI | DOCUMENTED_PORT | dell-g2724d:2 |

```text
host-to-middle: host-usbc → middle-in [PHYSICAL]
middle-route1: middle-in → middle-out1 [INTERNAL_ROUTING]
out-to-cable1: middle-out1 → cable1-a [PHYSICAL]
cable1-route: cable1-a → cable1-b [INTERNAL_ROUTING]
cable-to-screen1: cable1-b → screen1-in [PHYSICAL]
middle-route2: middle-in → middle-out2 [INTERNAL_ROUTING]
out-to-cable2: middle-out2 → cable2-a [PHYSICAL]
cable2-route: cable2-a → cable2-b [INTERNAL_ROUTING]
cable-to-screen2: cable2-b → screen2-in [PHYSICAL]
```

### 근거

- `dell-g2724d:2`: HDMI에서 2560×1440 144Hz / 위치: Resolution / Refresh Rate; Ports / [SRC-dell-g2724d](https://www.dell.com/en-us/shop/dell-27-gaming-monitor-g2724d/apd/210-bhxc/monitors-monitor-accessories)
- `product:air-m1-2020:display`: 내장 화면과 동시에 외장 1대, 최대 6K 60Hz / 위치: 비디오 지원 / [APPLE-111883](https://support.apple.com/ko-kr/111883)
- `product:air-m1-2020:ports`: Thunderbolt/USB 4 포트 2개에서 충전 및 DisplayPort 지원 / 위치: 충전 및 확장 / [APPLE-111883](https://support.apple.com/ko-kr/111883)
- `startech-mst14cd122hd:1`: MST 분기, macOS 비호환 표기, Windows에서 드라이버 불필요 / 위치: PDF pp.1–3 / Features; Power; Performance; Hardware / [SRC-startech-mst14cd122hd](https://media.startech.com/cms/pdfs/mst14cd122hd_datasheet.pdf)

### 조건·공유 자원·전력 구조

```json
{
  "predicates": [
    {
      "id": "os-family",
      "context_key": "os_family",
      "operator": "NEQ",
      "expected": "macOS",
      "claim_refs": [
        "startech-mst14cd122hd:1"
      ]
    }
  ],
  "resources": [
    {
      "id": "video-pool",
      "device_id": "middle",
      "output_port_ids": [
        "middle-out1",
        "middle-out2"
      ],
      "max_independent_displays": 2,
      "claim_ref": "startech-mst14cd122hd:1",
      "allocation_status": "AGGREGATE_ONLY"
    }
  ],
  "power_flows": []
}
```

### 검토 결과안과 남은 정보

공식 MST hub의 macOS 비호환 조건에 대한 내부 부정 후보; 공개 승인 아님

- `포트별 상세 영상 협상·색 조건`
- `최종 사람 검수`
- `물리 케이블과 독 출력 채널 쌍 매핑`

내부 결과: **INCOMPATIBLE**, 공개 결과: **UNKNOWN**. 기록된 전력 상한: NoneW (실제 충전량 아님).

- 요청 SHA-256: `59f25236b6d0986cdd1a3b59bc9b11a340057f1e5bcf958f95c16130cd328c3f`
- 근거 catalog SHA-256: `f93cbf9b755f39dad92725776a2c2e67c658f3a4dc7dc0a1075ef40b9d2f884f`
- 규칙 버전: `path-instance-v1.0`
- 사람 검수자·검수일·승인 결과: **미기록 / 대기**


GP-02/03 연결은 확보된 Dell G2724D를 사용하는 QHD60 축소 변형이다.
원래 계획의 4K60 충족 또는 해당 골든 시나리오 완료로 계산하지 않는다.
원래 목표의 최종 승인에는 별도의 4K 화면·포트 근거 바인딩이 필요하다.
