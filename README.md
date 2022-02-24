# TEXTFSM-AOS

> Alcatel-Lucent Enterprise AOS CLI parsing

Python package for Alcatel-Lucent Enterprise aos6 and aos8 parsing based on TextFSM templates.

## Why TextFSM-AOS?

Parse semi-structured cli data to structured data ready to be ingested by your network automation pipeline. Autmatically transform gathered output from screen-scraping tools like Netmiko, Scrapli and Paramiko. Receive uniform data accross Alcatel-Lucent Enterprise devices running aos6 or aos8.

## Installing / Getting started

Python package available through PyPi

```bash
pip install textfsm-aos
```

Provide screen-scraped data to parser

```python
from textfsm_aos.parser import parse

sample_data = """
   Package           Release       Size     Description
-----------------+---------------+--------+-----------------------------------
KFbase.img        6.7.2.89.R06    18059551 Alcatel-Lucent Enterprise Base Softw
KFos.img          6.7.2.89.R06     3566798 Alcatel-Lucent Enterprise OS
KFeni.img         6.7.2.89.R06     6123991 Alcatel-Lucent Enterprise NI softwar
KFsecu.img        6.7.2.89.R06      649383 Alcatel-Lucent Enterprise Security M
"""

parse("ale_aos6", "show microcode", sample_data)
```

parse result

```python
[
   {
      "package":"KFbase.img",
      "release":"6.7.2.89.R06",
      "size":"18059551",
      "description":"Alcatel-Lucent Enterprise Base Softw"
   },
   {
      "package":"KFos.img",
      "release":"6.7.2.89.R06",
      "size":"3566798",
      "description":"Alcatel-Lucent Enterprise OS"
   },
   {
      "package":"KFeni.img",
      "release":"6.7.2.89.R06",
      "size":"6123991",
      "description":"Alcatel-Lucent Enterprise NI softwar"
   },
   {
      "package":"KFsecu.img",
      "release":"6.7.2.89.R06",
      "size":"649383",
      "description":"Alcatel-Lucent Enterprise Security M"
   }
]
```

## Supported commands

| command                        |        aos6        |        aos8        |
|--------------------------------|:------------------:|:------------------:|
| show 802.1x users              | :heavy_check_mark: |        :x:         |
| show 802.1x non-supplicant     | :heavy_check_mark: |        :x:         |
| show 802.1x non-supplicant unp | :heavy_check_mark: |        :x:         |
| show chassis                   | :heavy_check_mark: |        :x:         |
| show health                    | :heavy_check_mark: |        :x:         |
| show history                   | :heavy_check_mark: |        :x:         |
| show interface status          | :heavy_check_mark: |        :x:         |
| show ip interface              | :heavy_check_mark: |        :x:         |
| show ip route                  | :heavy_check_mark: |        :x:         |
| show lld remote system         | :heavy_check_mark: |        :x:         |
| show mac-address-table         | :heavy_check_mark: |        :x:         |
| show microcode                 | :heavy_check_mark: |        :x:         |
| show ntp server status         | :heavy_check_mark: |        :x:         |
| show user                      | :heavy_check_mark: |        :x:         |
| show snmp station              | :heavy_check_mark: |        :x:         |
| show snmp community map        | :heavy_check_mark: |        :x:         |
| show system                    | :heavy_check_mark: |        :x:         |
| show vlan                      | :heavy_check_mark: |        :x:         |
| show vlan port mobile          | :heavy_check_mark: |        :x:         |

## Direct TextFSM example usage

Bypass the build-in parser functionality and use the TextFSM templates directly in network cli scraping and orchestration tools like Netmiko, Scrapli and Ansible.

### Scrapli

Python script

```python
from scrapli import Scrapli
from scrapli.helper import textfsm_parse

device = {
    "host": "<host ip>",
    "auth_username": "<username>",
    "auth_password": "<password>",
    "auth_strict_key": False,
    "transport": "ssh2",
    "platform": "alcatel_aos",
}

with Scrapli(**device) as conn:
    response = conn.send_command("show health").result
    structured_response = textfsm_parse(
        "templates/ale_aos6_show_health.textfsm", response
    )
```

Example output

```python
[
   {
      "resource":"Receive",
      "limit":"80",
      "current":"01",
      "min_avg":"01",
      "hr_avg":"01",
      "hr_max":"01"
   },
   {
      "resource":"Transmit/Receive",
      "limit":"80",
      "current":"01",
      "min_avg":"01",
      "hr_avg":"01",
      "hr_max":"01"
   },
   {
      "resource":"Memory",
      "limit":"80",
      "current":"76",
      "min_avg":"76",
      "hr_avg":"76",
      "hr_max":"76"
   },
   {
      "resource":"Cpu",
      "limit":"80",
      "current":"32",
      "min_avg":"33",
      "hr_avg":"29",
      "hr_max":"97"
   }
]
```

### Netmiko

Python script

```python
from netmiko import ConnectHandler

device = {
    'device_type': 'alcatel_aos',
    'host': '<host ip>',
    'username': '<username>',
    'password': '<password>'
}

with ConnecHandler(**device) as conn:
    output = conn.send_command("show health", use_textfsm=True, textfsm_template="textfsm-aos/templates/ale_aos6_show_health.textfsm")
```

Example Output

```python
[
   {
      "resource":"Receive",
      "limit":"80",
      "current":"01",
      "min_avg":"01",
      "hr_avg":"01",
      "hr_max":"01"
   },
   {
      "resource":"Transmit/Receive",
      "limit":"80",
      "current":"01",
      "min_avg":"01",
      "hr_avg":"01",
      "hr_max":"01"
   },
   {
      "resource":"Memory",
      "limit":"80",
      "current":"76",
      "min_avg":"76",
      "hr_avg":"76",
      "hr_max":"76"
   },
   {
      "resource":"Cpu",
      "limit":"80",
      "current":"32",
      "min_avg":"33",
      "hr_avg":"29",
      "hr_max":"97"
   }
]
```

### Ansible

Ansible task

```yaml
- name: AOS6 >> parsed with textfsm
  set_fact:
    health: "{{ health-aos6 | ansible.netcommon.parse_cli_textfsm('textfsm/templates/ale_aos6_show_health.textfsm') }}"
```

Example Output

```yaml
    health:
    - healthModuleCpu1HrAvg: '29'
      healthModuleCpu1HrMax: '98'
      healthModuleCpu1MinAvg: '26'
      healthModuleCpuLatest: '31'
      healthModuleCpuLimit: '80'
      healthModuleMemory1HrAvg: '76'
      healthModuleMemory1HrMax: '76'
      healthModuleMemory1MinAvg: '76'
      healthModuleMemoryLatest: '76'
      healthModuleMemoryLimit: '80'
      healthModuleRx1HrAvg: '01'
      healthModuleRx1HrMax: '01'
      healthModuleRx1MinAvg: '01'
      healthModuleRxLatest: '01'
      healthModuleRxLimit: '80'
      healthModuleRxTxRx1HrAvg: '01'
      healthModuleRxTxRx1HrMax: '01'
      healthModuleRxTxRx1MinAvg: '01'
      healthModuleRxTxRxLatest: '01'
      healthModuleRxTxRxLimit: '80'
      healthModuleSlot: '1'
```

## How to contribute

## Related projects

- Google TextFSM: https://github.com/google/textfsm
- Scrapli: https://github.com/carlmontanari/scrapli
- Netmiko: https://github.com/ktbyers/netmiko
