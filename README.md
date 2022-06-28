[![Build Status](https://app.travis-ci.com/jefvantongerloo/textfsm-aos.svg?branch=main)](https://app.travis-ci.com/jefvantongerloo/textfsm-aos)

# TEXTFSM-AOS

> Alcatel-Lucent Enterprise AOS CLI parsing

Python package for Alcatel-Lucent Enterprise aos6 and aos8 parsing based on TextFSM templates.

## Why TextFSM-AOS?

Parse semi-structured cli data to structured data ready to be ingested by your network automation pipeline. Autmatically transform gathered output from screen-scraping tools like Netmiko, Scrapli and Paramiko. Receive uniform data accross Alcatel-Lucent Enterprise devices running aos6 or aos8.

## Installation

Textfsm-aos can be installed using Git + Poetry or PyPI.

## Git

```bash
git clone https://github.com/jefvantongerloo/textfsm-aos
poetry install
```

## PyPI

```bash
pip install textfsm-aos
```

## Getting started

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

parsed result

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

| command                        |                 aos6                |                aos8               |
|--------------------------------|:-----------------------------------:|:---------------------------------:|
| history                        |        `alias: show history`        |         :heavy_check_mark:        |
| show 802.1x users              |          :heavy_check_mark:         |       `alias: show unp user`      |
| show 802.1x users unp          |          :heavy_check_mark:         |                :x:                |
| show 802.1x non-supplicant     |          :heavy_check_mark:         |                :x:                |
| show 802.1x non-supplicant unp |          :heavy_check_mark:         |                :x:                |
| show arp                       |                 :x:                 |         :heavy_check_mark:        |
| show chassis                   |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show cmm                       |                 :x:                 |         :heavy_check_mark:        |
| show command-log               |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show hardware-info             |                 :x:                 |         :heavy_check_mark:        |
| show health                    |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show history                   |          :heavy_check_mark:         |          `alias: history`         |
| show interface status          |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show interfaces                |                 :x:                 |         :heavy_check_mark:        |
| show ip interface              |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show ip route                  |          :heavy_check_mark:         |       `alias: show ip routes`     |
| show ip routes                 |        `alias: show ip route`       |         :heavy_check_mark:        |
| show linkagg                   |                 :x:                 |         :heavy_check_mark:        |
| show linkagg port              |                 :x:                 |         :heavy_check_mark:        |
| show lld remote system         |          :heavy_check_mark:         |                :x:                |
| show log events                |                 :x:                 |         :heavy_check_mark:        |
| show mac-address-table         |          :heavy_check_mark:         |     `alias: show mac-learning`    |
| show mac-learning              |   `alias: show mac-address-table`   |         :heavy_check_mark:        |
| show microcode                 |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show ntp server status         |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show port-security brief       |                 :x:                 |         :heavy_check_mark:        |
| show qos port                  |                 :x:                 |         :heavy_check_mark:        |
| show unp user                  |     `alias: show 802.1x users`      |         :heavy_check_mark:        |
| show user                      |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show running-directory         |                 :x:                 |         :heavy_check_mark:        |
| show snmp station              |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show snmp community map        |          :heavy_check_mark:         |  `alias: show snmp community-map` |
| show snmp community-map        |   `alias: show snmp community map`  |         :heavy_check_mark:        |
| show spantree ports            |                 :x:                 |         :heavy_check_mark:        |
| show system                    |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show transceivers              |                 :x:                 |         :heavy_check_mark:        |
| show vlan                      |          :heavy_check_mark:         |         :heavy_check_mark:        |
| show vlan members              |                 :x:                 |         :heavy_check_mark:        |
| show vlan port mobile          |          :heavy_check_mark:         |                :x:                |

## Direct TextFSM example usage

Bypass the build-in parser functionality and use the TextFSM templates directly in network cli scraping and orchestration tools like Netmiko, Scrapli and Ansible.

### Scrapli

Python script:

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

Example output:

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

Python script:

```python
from netmiko import ConnectHandler

device = {
    'device_type': 'alcatel_aos',
    'host': '<host ip>',
    'username': '<username>',
    'password': '<password>'
}

with ConnectHandler(**device) as conn:
    output = conn.send_command("show health", use_textfsm=True, textfsm_template="textfsm-aos/templates/ale_aos6_show_health.textfsm")
```

Example Output:

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

Ansible task:

```yaml
- name: AOS6 >> parsed with textfsm
  set_fact:
    health: "{{ health-aos6 | ansible.netcommon.parse_cli_textfsm('textfsm/templates/ale_aos6_show_health.textfsm') }}"
```

Example Output:

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

1. Fork and create a branch with naming `<platform>_<command>` (for example: ale_aos8_show_system).

2. Add TextFSM template file in templates folder with naming `<platform>_<command>.textfsm`.

3. Add entry in templates_index with attribute command and platform.

4. Add test folder in 'templates' with naming `<platform>_<command>`.

5. Add sample cli output file in newly created folder `<platform>_<command>.txt`.

6. Add expected parsed data from sample cli output in `<platform>_<command>.yml`.

7. Run linting `tox` and tests `pytest`.

## How to setup development environment

1. Install `Poetry` package manager via `pip install poetry`

2. Install dev dependencies and textfsm-aos package in development mode with `poetry install`

3. Open virtual environment `poetry shell`

## Related projects

- Google TextFSM: [https://github.com/google/textfsm](https://github.com/google/textfsm)
- Scrapli: [https://github.com/carlmontanari/scrapli](https://github.com/carlmontanari/scrapli)
- Netmiko: [https://github.com/ktbyers/netmiko](https://github.com/ktbyers/netmiko)
- Getting started with TextFSM: [https://pyneng.readthedocs.io](https://pyneng.readthedocs.io/en/latest/book/21_textfsm/index.html)
