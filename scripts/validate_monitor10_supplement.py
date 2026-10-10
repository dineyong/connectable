"""Validate the bounded 10-model supplement, not truth of arbitrary specs.

Exact model/field source bindings and payload shapes require code review to expand.
The allowlist does not authenticate live redirects or grant human approval.
"""
import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.validate_monitor_expansion import load, url
from scripts.validate_question_corpus_v2 import sensitive_strings
DATA=ROOT/'data/research/monitor-expansion/monitor10_verified_supplement.json'
SOURCE_HASH='ea6ba0de4a31fb128e7c1672630ae6dd467a2262baaf887523e18b6e148d28af'
CONTRACTS = {'m10-01': {'model': '27GP850',
            'fields': {'screen_size_cm': {'shape': 'number',
                                          'url': 'https://www.lge.co.kr/monitors/27gp850',
                                          'scope': 'KR official listed product 27GP850'},
                       'resolution': {'shape': ['tuple', 'number', 'number'],
                                      'url': 'https://www.lge.co.kr/monitors/27gp850',
                                      'scope': 'KR official listed product 27GP850'},
                       'panel': {'shape': 'text',
                                 'url': 'https://www.lge.co.kr/monitors/27gp850',
                                 'scope': 'KR official listed product 27GP850'},
                       'input_profiles': {'shape': {'DP': {'normal_hz': 'number', 'overclock_hz': 'number'},
                                                    'HDMI': {'max_hz': 'number'}},
                                          'url': 'https://www.lge.co.kr/monitors/27gp850',
                                          'scope': 'KR official listed product 27GP850'},
                       'connectivity': {'shape': {'hdmi_count': 'number',
                                                  'displayport_count': 'number',
                                                  'usb_3_0_upstream': 'number',
                                                  'usb_3_0_downstream': 'number'},
                                        'url': 'https://www.lge.co.kr/monitors/27gp850',
                                        'scope': 'KR official listed product 27GP850'},
                       'brightness_cd_m2': {'shape': {'typical': 'number', 'minimum': 'number'},
                                            'url': 'https://www.lge.co.kr/monitors/27gp850',
                                            'scope': 'KR official listed product 27GP850'},
                       'hdr': {'shape': ['tuple', 'text', 'text'],
                               'url': 'https://www.lge.co.kr/monitors/27gp850',
                               'scope': 'KR official listed product 27GP850'},
                       'support_product_link': {'shape': {'from': 'text',
                                                          'to': 'text',
                                                          'relationship': 'text'},
                                                'url': 'https://www.lge.co.kr/support/product-27GP850-BB',
                                                'scope': 'KR support to KR listed product only'}},
            'conflict_fields': []},
 'm10-02': {'model': '27GS95QE',
            'fields': {'screen_size_cm': {'shape': 'number',
                                          'url': 'https://www.lge.co.kr/monitors/27gs95qe',
                                          'scope': 'KR official listed product 27GS95QE'},
                       'resolution': {'shape': ['tuple', 'number', 'number'],
                                      'url': 'https://www.lge.co.kr/monitors/27gs95qe',
                                      'scope': 'KR official listed product 27GS95QE'},
                       'panel': {'shape': 'text',
                                 'url': 'https://www.lge.co.kr/monitors/27gs95qe',
                                 'scope': 'KR official listed product 27GS95QE'},
                       'input_profiles': {'shape': {'HDMI2.1': {'width': 'number',
                                                                'height': 'number',
                                                                'max_hz': 'number'},
                                                    'DP1.4': {'width': 'number',
                                                              'height': 'number',
                                                              'max_hz': 'number'}},
                                          'url': 'https://www.lge.co.kr/monitors/27gs95qe',
                                          'scope': 'KR official listed product 27GS95QE'},
                       'connectivity': {'shape': {'hdmi_count': 'number',
                                                  'displayport_count': 'number',
                                                  'usb_3_0_upstream': 'number',
                                                  'usb_3_0_downstream': 'number',
                                                  'hdmi_version': 'text',
                                                  'displayport_version': 'text'},
                                        'url': 'https://www.lge.co.kr/monitors/27gs95qe',
                                        'scope': 'KR official listed product 27GS95QE'},
                       'brightness_cd_m2': {'shape': {'typical': 'number',
                                                      'minimum': 'number',
                                                      'HDR_peak': {'typical': 'number',
                                                                   'minimum': 'number',
                                                                   'APL_percent': 'number'}},
                                            'url': 'https://www.lge.co.kr/monitors/27gs95qe',
                                            'scope': 'KR official listed product 27GS95QE'},
                       'hdr': {'shape': ['tuple', 'text', 'text'],
                               'url': 'https://www.lge.co.kr/monitors/27gs95qe',
                               'scope': 'KR official listed product 27GS95QE'},
                       'support_product_link': {'shape': {'from': 'text',
                                                          'to': 'text',
                                                          'relationship': 'text'},
                                                'url': 'https://www.lge.co.kr/support/product-27GS95QE-BB',
                                                'scope': 'KR support to KR listed product only'}},
            'conflict_fields': []},
 'm10-03': {'model': '32GS95UE',
            'fields': {'screen_size_cm': {'shape': 'number',
                                          'url': 'https://www.lge.co.kr/monitors/32gs95ue',
                                          'scope': 'KR official listed product 32GS95UE'},
                       'resolution': {'shape': ['tuple', 'number', 'number'],
                                      'url': 'https://www.lge.co.kr/monitors/32gs95ue',
                                      'scope': 'KR official listed product 32GS95UE'},
                       'panel': {'shape': 'text',
                                 'url': 'https://www.lge.co.kr/monitors/32gs95ue',
                                 'scope': 'KR official listed product 32GS95UE'},
                       'input_profiles': {'shape': {'HDMI2.1': ['tuple',
                                                                {'width': 'number',
                                                                 'height': 'number',
                                                                 'max_hz': 'number'},
                                                                {'width': 'number',
                                                                 'height': 'number',
                                                                 'max_hz': 'number'}],
                                                    'DP1.4': ['tuple',
                                                              {'width': 'number',
                                                               'height': 'number',
                                                               'max_hz': 'number'},
                                                              {'width': 'number',
                                                               'height': 'number',
                                                               'max_hz': 'number'}]},
                                          'url': 'https://www.lge.co.kr/monitors/32gs95ue',
                                          'scope': 'KR official listed product 32GS95UE'},
                       'connectivity': {'shape': {'hdmi_count': 'number',
                                                  'displayport_count': 'number',
                                                  'usb_3_0_upstream': 'number',
                                                  'usb_3_0_downstream': 'number',
                                                  'hdmi_version': 'text',
                                                  'displayport_version': 'text'},
                                        'url': 'https://www.lge.co.kr/monitors/32gs95ue',
                                        'scope': 'KR official listed product 32GS95UE'},
                       'brightness_cd_m2': {'shape': {'typical': 'number',
                                                      'minimum': 'number',
                                                      'HDR_peak': {'typical': 'number',
                                                                   'minimum': 'number',
                                                                   'APL_percent': 'number'}},
                                            'url': 'https://www.lge.co.kr/monitors/32gs95ue',
                                            'scope': 'KR official listed product 32GS95UE'},
                       'hdr': {'shape': ['tuple', 'text', 'text'],
                               'url': 'https://www.lge.co.kr/monitors/32gs95ue',
                               'scope': 'KR official listed product 32GS95UE'},
                       'support_product_link': {'shape': {'from': 'text',
                                                          'to': 'text',
                                                          'relationship': 'text'},
                                                'url': 'https://www.lge.co.kr/support/product-32GS95UE-BB',
                                                'scope': 'KR support to KR listed product only'}},
            'conflict_fields': []},
 'm10-04': {'model': 'M27Q 2.0',
            'fields': {'screen_size_inch': {'shape': 'number',
                                            'url': 'https://www.gigabyte.com/kr/Monitor/M27Q-rev-20/sp',
                                            'scope': 'Official M27Q Gaming Monitor (Rev. 2.0), KR '
                                                     'manufacturer page; distributor SKU UNKNOWN'},
                       'resolution': {'shape': ['tuple', 'number', 'number'],
                                      'url': 'https://www.gigabyte.com/kr/Monitor/M27Q-rev-20/sp',
                                      'scope': 'Official M27Q Gaming Monitor (Rev. 2.0), KR manufacturer '
                                               'page; distributor SKU UNKNOWN'},
                       'panel': {'shape': 'text',
                                 'url': 'https://www.gigabyte.com/kr/Monitor/M27Q-rev-20/sp',
                                 'scope': 'Official M27Q Gaming Monitor (Rev. 2.0), KR manufacturer page; '
                                          'distributor SKU UNKNOWN'},
                       'max_refresh_hz': {'shape': {'normal': 'number', 'overclock': 'number'},
                                          'url': 'https://www.gigabyte.com/kr/Monitor/M27Q-rev-20/sp',
                                          'scope': 'Official M27Q Gaming Monitor (Rev. 2.0), KR manufacturer '
                                                   'page; distributor SKU UNKNOWN'},
                       'connectivity': {'shape': {'HDMI': {'count': 'number', 'version': 'text'},
                                                  'DisplayPort': {'count': 'number', 'version': 'text'},
                                                  'USB_Type_C': {'count': 'number',
                                                                 'mode': 'text',
                                                                 'direction': 'text'},
                                                  'USB_3_0': {'downstream': 'number', 'upstream': 'number'}},
                                        'url': 'https://www.gigabyte.com/kr/Monitor/M27Q-rev-20/sp',
                                        'scope': 'Official M27Q Gaming Monitor (Rev. 2.0), KR manufacturer '
                                                 'page; distributor SKU UNKNOWN'},
                       'usb_c_pd_page_max_w': {'shape': 'number',
                                               'url': 'https://www.gigabyte.com/kr/Monitor/M27Q-rev-20/sp',
                                               'scope': 'Official M27Q Gaming Monitor (Rev. 2.0), KR '
                                                        'manufacturer page; distributor SKU UNKNOWN'},
                       'brightness_typical_cd_m2': {'shape': 'number',
                                                    'url': 'https://www.gigabyte.com/kr/Monitor/M27Q-rev-20/sp',
                                                    'scope': 'Official M27Q Gaming Monitor (Rev. 2.0), KR '
                                                             'manufacturer page; distributor SKU UNKNOWN'},
                       'hdr': {'shape': 'text',
                               'url': 'https://www.gigabyte.com/kr/Monitor/M27Q-rev-20/sp',
                               'scope': 'Official M27Q Gaming Monitor (Rev. 2.0), KR manufacturer page; '
                                        'distributor SKU UNKNOWN'}},
            'conflict_fields': []},
 'm10-05': {'model': 'M32U',
            'fields': {'screen_size_inch': {'shape': 'number',
                                            'url': 'https://www.gigabyte.com/kr/Monitor/M32U/sp',
                                            'scope': 'KR manufacturer model M32U'},
                       'resolution': {'shape': 'text',
                                      'url': 'https://www.gigabyte.com/kr/Monitor/M32U/sp',
                                      'scope': 'PANEL'},
                       'panel': {'shape': 'text',
                                 'url': 'https://www.gigabyte.com/kr/Monitor/M32U/sp',
                                 'scope': 'PANEL'},
                       'hdmi_supported_modes': {'shape': {'pc': 'text', 'console': 'text'},
                                                'url': 'https://www.gigabyte.com/kr/Monitor/M32U/sp',
                                                'scope': 'HDMI'},
                       'displayport_supported_modes': {'shape': 'text',
                                                       'url': 'https://download.gigabyte.com/FileList/Manual/GIGABYTE_M32U_UM_Korean.pdf',
                                                       'scope': 'DISPLAYPORT'},
                       'usb_c_video': {'shape': ['literal', True],
                                       'url': 'https://download.gigabyte.com/FileList/Manual/GIGABYTE_M32U_UM_Korean.pdf',
                                       'scope': 'USB_C_INPUT'},
                       'usb_c_power_profiles': {'shape': ['tuple', 'text', 'text', 'text', 'text'],
                                                'url': 'https://download.gigabyte.com/FileList/Manual/GIGABYTE_M32U_UM_Korean.pdf',
                                                'scope': 'USB_C_POWER'},
                       'usb_c_external_power_advice': {'shape': 'text',
                                                       'url': 'https://download.gigabyte.com/FileList/Manual/GIGABYTE_M32U_UM_Korean.pdf',
                                                       'scope': 'USB_C_POWER'}},
            'conflict_fields': []},
 'm10-06': {'model': 'U2724D',
            'fields': {'exact_korean_sku': {'shape': {'manufacturer_part': 'text',
                                                      'dell_part': 'text',
                                                      'offering_id': 'text'},
                                            'url': 'https://www.dell.com/ko-kr/shop/monitors/apd/dell-ultrasharp-27-%EB%AA%A8%EB%8B%88%ED%84%B0-u2724d/u2724d_monitor/-',
                                            'scope': 'KR_CURRENT_OFFERING'},
                       'screen_size_inch': {'shape': 'number',
                                            'url': 'https://www.dell.com/ko-kr/shop/monitors/apd/dell-ultrasharp-27-%EB%AA%A8%EB%8B%88%ED%84%B0-u2724d/u2724d_monitor/-',
                                            'scope': 'PANEL'},
                       'resolution': {'shape': 'text',
                                      'url': 'https://www.dell.com/ko-kr/shop/monitors/apd/dell-ultrasharp-27-%EB%AA%A8%EB%8B%88%ED%84%B0-u2724d/u2724d_monitor/-',
                                      'scope': 'PANEL'},
                       'panel': {'shape': 'text',
                                 'url': 'https://www.dell.com/ko-kr/shop/monitors/apd/dell-ultrasharp-27-%EB%AA%A8%EB%8B%88%ED%84%B0-u2724d/u2724d_monitor/-',
                                 'scope': 'PANEL'},
                       'hdmi_supported_modes': {'shape': {'resolution': 'text',
                                                          'refresh_hz': 'number',
                                                          'signalling': 'text',
                                                          'vrr': 'text',
                                                          'frl': ['literal', False],
                                                          'dsc': ['literal', False]},
                                                'url': 'https://dl.dell.com/content/manual17047281-dell-ultrasharp-27-monitor-u2724d-user-s-guide.pdf?language=en-us',
                                                'scope': 'HDMI'},
                       'displayport_ports': {'shape': {'input_count': 'number',
                                                       'output_count': 'number',
                                                       'input_version': 'text'},
                                             'url': 'https://dl.dell.com/content/manual17047281-dell-ultrasharp-27-monitor-u2724d-user-s-guide.pdf?language=en-us',
                                             'scope': 'DISPLAYPORT'},
                       'usb_c_video': {'shape': ['literal', False],
                                       'url': 'https://dl.dell.com/content/manual17047281-dell-ultrasharp-27-monitor-u2724d-user-s-guide.pdf?language=en-us',
                                       'scope': 'USB_C_UPSTREAM'},
                       'usb_c_power_delivery': {'shape': {'downstream_charging_w': 'number',
                                                          'upstream_host_power_delivery': ['literal',
                                                                                           'UNKNOWN']},
                                                'url': 'https://dl.dell.com/content/manual17047281-dell-ultrasharp-27-monitor-u2724d-user-s-guide.pdf?language=en-us',
                                                'scope': 'USB_C_DOWNSTREAM'}},
            'conflict_fields': ['rj45']},
 'm10-07': {'model': 'XG27AQDMG',
            'fields': {'screen_size_inch': {'shape': 'number',
                                            'url': 'https://rog.asus.com/kr/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/spec/',
                                            'scope': 'KR_MODEL_PANEL'},
                       'resolution': {'shape': 'text',
                                      'url': 'https://rog.asus.com/kr/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/spec/',
                                      'scope': 'PANEL'},
                       'panel': {'shape': 'text',
                                 'url': 'https://rog.asus.com/kr/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/spec/',
                                 'scope': 'PANEL'},
                       'max_refresh_hz': {'shape': 'number',
                                          'url': 'https://rog.asus.com/kr/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/spec/',
                                          'scope': 'PANEL_UP_TO'},
                       'hdmi_supported_modes': {'shape': 'text',
                                                'url': 'https://dlcdnets.asus.com/pub/ASUS/LCD%20Monitors/XG27AQDMG/ASUS_XG27AQDMG_UM_Korean.pdf?model=XG27AQDMG',
                                                'scope': 'HDMI_QHD'},
                       'displayport_supported_modes': {'shape': 'text',
                                                       'url': 'https://dlcdnets.asus.com/pub/ASUS/LCD%20Monitors/XG27AQDMG/ASUS_XG27AQDMG_UM_Korean.pdf?model=XG27AQDMG',
                                                       'scope': 'DISPLAYPORT_QHD'},
                       'hdr_peak_brightness_nits': {'shape': 'number',
                                                    'url': 'https://rog.asus.com/kr/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg/spec/',
                                                    'scope': 'HDR_PEAK'},
                       'distinct_related_model': {'shape': {'model': 'text',
                                                            'name': 'text',
                                                            'merge_allowed': ['literal', False]},
                                                  'url': 'https://rog.asus.com/monitors/27-to-31-5-inches/rog-strix-oled-xg27aqdmg-gen2-xg27aqdmgr/spec/',
                                                  'scope': 'RELATED_MODEL_ONLY'}},
            'conflict_fields': ['hdmi_vertical_frequency_scope']},
 'm10-08': {'model': 'MPG 274URF-QD',
            'fields': {'screen_size_inch': {'shape': 'number',
                                            'url': 'https://www.msi.com/Monitor/MPG-274URF-QD/Specification',
                                            'scope': 'GLOBAL_MODEL'},
                       'resolution': {'shape': {'width': 'number', 'height': 'number'},
                                      'url': 'https://www.msi.com/Monitor/MPG-274URF-QD/Specification',
                                      'scope': 'GLOBAL_MODEL'},
                       'panel': {'shape': 'text',
                                 'url': 'https://www.msi.com/Monitor/MPG-274URF-QD/Specification',
                                 'scope': 'GLOBAL_MODEL'},
                       'max_refresh_hz': {'shape': 'number',
                                          'url': 'https://www.msi.com/Monitor/MPG-274URF-QD/Specification',
                                          'scope': 'GLOBAL_MODEL'},
                       'video_ports': {'shape': {'displayport': {'count': 'number', 'version': 'text'},
                                                 'hdmi': {'count': 'number', 'version': 'text'},
                                                 'usb_c': {'count': 'number', 'mode': 'text'}},
                                       'url': 'https://www.msi.com/Monitor/MPG-274URF-QD/Specification',
                                       'scope': 'GLOBAL_MODEL'},
                       'usb_c_video': {'shape': 'text',
                                       'url': 'https://download-2.msi.com/archive/mnu_exe/monitor/MPG_274URF_QDv1.1_Korean.pdf',
                                       'scope': 'KOREAN_LANGUAGE_MANUAL_MODEL_3CC2'},
                       'usb_c_pd_power_w': {'shape': {'watts': 'number',
                                                      'qualifier': ['literal', 'UP_TO'],
                                                      'volts': 'number',
                                                      'amps': 'number'},
                                            'url': 'https://download-2.msi.com/archive/mnu_exe/monitor/MPG_274URF_QDv1.1_Korean.pdf',
                                            'scope': 'KOREAN_LANGUAGE_MANUAL_MODEL_3CC2'},
                       'brightness': {'shape': {'sdr_typical_nits': 'number', 'hdr_peak_nits': 'number'},
                                      'url': 'https://download-2.msi.com/archive/mnu_exe/monitor/MPG_274URF_QDv1.1_Korean.pdf',
                                      'scope': 'KOREAN_LANGUAGE_MANUAL_MODEL_3CC2'}},
            'conflict_fields': ['stand_height_mm', 'usb_c_data_kvm']},
 'm10-09': {'model': 'BenQ MOBIUZ EX2710Q',
            'fields': {'screen_size_inch': {'shape': 'number',
                                            'url': 'https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html',
                                            'scope': 'CA_MODEL'},
                       'resolution': {'shape': {'width': 'number', 'height': 'number'},
                                      'url': 'https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html',
                                      'scope': 'CA_MODEL'},
                       'panel': {'shape': 'text',
                                 'url': 'https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html',
                                 'scope': 'CA_MODEL'},
                       'max_refresh_hz': {'shape': 'number',
                                          'url': 'https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html',
                                          'scope': 'CA_MODEL'},
                       'video_ports': {'shape': {'hdmi': {'count': 'number', 'version': 'text'},
                                                 'displayport': {'count': 'number', 'version': 'text'}},
                                       'url': 'https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html',
                                       'scope': 'CA_MODEL'},
                       'brightness': {'shape': {'typical_mode_unspecified_nits': 'number',
                                                'hdr_peak_nits': 'number'},
                                      'url': 'https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html',
                                      'scope': 'CA_MODEL'},
                       'hdr': {'shape': 'text',
                               'url': 'https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html',
                               'scope': 'CA_MODEL'},
                       'stand_and_mount': {'shape': {'tilt_deg': ['tuple', 'number', 'number'],
                                                     'swivel_deg': ['tuple', 'number', 'number'],
                                                     'height_mm': 'number',
                                                     'vesa_mm': ['tuple', 'number', 'number']},
                                           'url': 'https://www.benq.com/en-ca/monitor/gaming/ex2710q/spec.html',
                                           'scope': 'CA_MODEL'}},
            'conflict_fields': []},
 'm10-10': {'model': 'Crossover 27ULD950',
            'fields': {'screen_size_inch': {'shape': 'number',
                                            'url': 'https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757',
                                            'scope': 'KR_DISPLAY_MODEL'},
                       'resolution': {'shape': {'width': 'number', 'height': 'number'},
                                      'url': 'https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757',
                                      'scope': 'KR_DISPLAY_MODEL'},
                       'panel': {'shape': 'text',
                                 'url': 'https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757',
                                 'scope': 'KR_DISPLAY_MODEL'},
                       'max_refresh_hz': {'shape': 'number',
                                          'url': 'https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757',
                                          'scope': 'KR_DISPLAY_MODEL'},
                       'brightness_advertised': {'shape': {'value': 'number',
                                                           'unit': ['literal', 'cd/m²'],
                                                           'qualifier': ['literal', 'UNKNOWN']},
                                                 'url': 'https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757',
                                                 'scope': 'KR_DISPLAY_MODEL'},
                       'stand_adjustments': {'shape': ['tuple', 'text', 'text', 'text', 'text'],
                                             'url': 'https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757',
                                             'scope': 'KR_DISPLAY_MODEL'},
                       'vesa_mm': {'shape': ['tuple', 'number', 'number'],
                                   'url': 'https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757',
                                   'scope': 'KR_DISPLAY_MODEL'},
                       'usb_pd_support': {'shape': 'text',
                                          'url': 'https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757',
                                          'scope': 'KR_DISPLAY_MODEL'}},
            'conflict_fields': ['displayport_version', 'stand_height_mm', 'stand_swivel_deg']}}


CONFLICT_SHAPES = {'m10-01': {},
 'm10-02': {},
 'm10-03': {},
 'm10-04': {},
 'm10-05': {},
 'm10-06': {'rj45': {'field': 'text', 'location': 'text', 'notes': 'text', 'status': 'text', 'url': 'text'}},
 'm10-07': {'hdmi_vertical_frequency_scope': {'field': 'text',
                                              'notes': 'text',
                                              'related_url': 'text',
                                              'status': 'text',
                                              'url': 'text'}},
 'm10-08': {'stand_height_mm': {'claims': ['tuple',
                                           {'location': 'text', 'url': 'text', 'value': 'number'},
                                           {'location': 'text', 'url': 'text', 'value': 'number'}],
                                'field': 'text',
                                'resolution': 'text',
                                'status': 'text'},
            'usb_c_data_kvm': {'claims': ['tuple',
                                          {'location': 'text', 'url': 'text', 'value': 'text'},
                                          {'location': 'text', 'url': 'text', 'value': 'text'}],
                               'field': 'text',
                               'resolution': 'text',
                               'status': 'text'}},
 'm10-09': {},
 'm10-10': {'displayport_version': {'claims': ['tuple', 'text', 'text'],
                                    'field': 'text',
                                    'resolution': 'text',
                                    'status': 'text'},
            'stand_height_mm': {'claims': ['tuple', 'text'],
                                'field': 'text',
                                'resolution': 'text',
                                'status': 'text'},
            'stand_swivel_deg': {'claims': ['tuple', 'text', 'text'],
                                 'field': 'text',
                                 'resolution': 'text',
                                 'status': 'text'}}}

def payload(value, schema, path, errors):
    if isinstance(schema,dict):
        if not isinstance(value,dict) or set(value)!=set(schema):
            errors.append(path+': payload object keys');return
        for key, child in schema.items():payload(value[key],child,path+'.'+key,errors)
    elif isinstance(schema,list):
        if schema[0]=='literal':
            if type(value)!=type(schema[1]) or value!=schema[1]:errors.append(path+': fixed semantic value')
        elif not isinstance(value,list) or len(value)!=len(schema)-1:errors.append(path+': payload array shape')
        else:
            for i,child in enumerate(schema[1:]):payload(value[i],child,path+f'[{i}]',errors)
    elif schema=='number':
        if type(value) not in (int,float) or not math.isfinite(value):errors.append(path+': finite number required')
        elif not any(k in path for k in ('tilt_deg','swivel_deg')) and value<=0:errors.append(path+': positive number required')
    elif not isinstance(value,str) or not value.strip():errors.append(path+': nonblank text required')


def validate(data):
    errors=[]
    def text(v,p):
        if not isinstance(v,str) or not v.strip():errors.append(p+': nonblank text required')
    def day(v,p):
        try:
            if not isinstance(v,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',v):raise ValueError()
            date.fromisoformat(v)
        except (ValueError,TypeError):errors.append(p+': invalid date')
    if not isinstance(data,dict) or set(data)!={'schema_version','checked_on','public_status','source_file_sha256','records'}:
        return ['root: missing/unexpected fields']
    if type(data['schema_version']) is not int or data['schema_version']!=1:errors.append('schema_version')
    if data['public_status']!='UNKNOWN':errors.append('public_status must remain UNKNOWN')
    if data['source_file_sha256']!=SOURCE_HASH:errors.append('source hash mismatch')
    day(data['checked_on'],'checked_on')
    errors.extend(sensitive_strings(data))
    if not isinstance(data['records'],list):return errors+['records array required']
    ids=[]
    for index,r in enumerate(data['records']):
        p=f'records[{index}]'
        if not isinstance(r,dict) or set(r)!={'id','selection_model','checked_on','confirmed','conflicts','unconfirmed','existing_match_notes'}:
            errors.append(p+': record fields');continue
        if not isinstance(r['id'],str) or r['id'] not in CONTRACTS:errors.append(p+': unknown ID');continue
        ids.append(r['id']);contract=CONTRACTS[r['id']]
        if r['selection_model']!=contract['model']:errors.append(p+': model/ID mismatch')
        day(r['checked_on'],p+'.checked_on')
        if r['checked_on']!=data['checked_on']:errors.append(p+': check date differs from batch')
        text(r['existing_match_notes'],p+'.existing_match_notes')
        if not isinstance(r['unconfirmed'],list) or not r['unconfirmed']:errors.append(p+': uncertainty must be retained')
        else:
            for v in r['unconfirmed']:text(v,p+'.unconfirmed')
        if not isinstance(r['confirmed'],list) or not r['confirmed']:errors.append(p+': confirmed evidence required');continue
        fields=[]
        for j,f in enumerate(r['confirmed']):
            q=p+f'.confirmed[{j}]'
            if not isinstance(f,dict) or set(f)!={'field','value','url','location','scope','notes'}:errors.append(q+': fact fields');continue
            if not isinstance(f['field'],str) or f['field'] not in contract['fields']:errors.append(q+': unsupported field');continue
            fields.append(f['field']);fc=contract['fields'][f['field']]
            for k in ('location','scope'):text(f[k],q+'.'+k)
            if not isinstance(f['notes'],str):errors.append(q+': notes text required')
            try:url(f['url'])
            except (ValueError,TypeError,UnicodeError):errors.append(q+': unsafe URL')
            if f['url']!=fc['url']:errors.append(q+': source URL not bound to model/field')
            if f['scope']!=fc['scope']:errors.append(q+': verified scope changed')
            payload(f['value'],fc['shape'],q+'.value',errors)
        if len(fields)!=len(set(fields)):errors.append(p+': duplicate confirmed field')
        if set(fields)!=set(contract['fields']):errors.append(p+': selected field coverage changed')
        if not isinstance(r['conflicts'],list):errors.append(p+': conflicts array required');continue
        conflict_fields=[]
        for c in r['conflicts']:
            if not isinstance(c,dict) or not isinstance(c.get('field'),str):errors.append(p+': conflict field required');continue
            conflict_fields.append(c['field'])
            schema=CONFLICT_SHAPES[r['id']].get(c['field'])
            if schema is None:errors.append(p+': unknown conflict field')
            else:payload(c,schema,p+'.conflict.'+c['field'],errors)
            if c['field'] in fields:errors.append(p+': conflict cannot be confirmed')
            if c.get('status') not in ('CONFLICT','CONFLICT_PENDING','SCOPE_REVIEW','USER_SUPPLIED_CONFLICT_PENDING_RECHECK','USER_SUPPLIED_AMBIGUITY_PENDING_RECHECK'):errors.append(p+': unresolved conflict status required')
            allowed_urls={fc['url'] for fc in contract['fields'].values()}
            def check_conflict_urls(obj):
                if isinstance(obj,dict):
                    for key,value in obj.items():
                        if key in ('url','related_url'):
                            try:url(value)
                            except (ValueError,TypeError,UnicodeError):errors.append(p+': unsafe conflict URL')
                            if not isinstance(value,str) or value not in allowed_urls:errors.append(p+': conflict URL not bound to model')
                        else:check_conflict_urls(value)
                elif isinstance(obj,list):
                    for value in obj:check_conflict_urls(value)
            check_conflict_urls(c)
        if sorted(conflict_fields)!=sorted(contract['conflict_fields']):errors.append(p+': known conflicts must remain')
    if len(ids)!=len(set(ids)):errors.append('duplicate record ID')
    if set(ids)!=set(CONTRACTS) or len(ids)!=10:errors.append('all 10 model records required')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('path',nargs='?',type=Path,default=DATA)
    args=parser.parse_args()
    try:errors=validate(load(args.path))
    except (ValueError,TypeError,OSError) as exc:errors=[str(exc)]
    if errors:
        print('\n'.join(errors),file=sys.stderr);return 1
    print('PASS: 10-model supplement; source-bound evidence; public UNKNOWN');return 0

if __name__=='__main__':raise SystemExit(main())
