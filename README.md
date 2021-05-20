# textfsm-aos

Alcatel-Lucent Enterprise AOS6 TextFSM templates

## Example usage

### Netmiko

**Python script**

```python
from netmiko import ConnectHandler

alcatel = {
    'device_type': 'alcatel_aos',
    'host': '<host ip>',
    'username': '<username>',
    'password': '<password>'
}

net_connect = ConnectHandler(**alcatel)
prompt = net_connect.find_prompt()
output = net_connect.send_command("show health", use_textfsm=True, textfsm_template="textfsm-aos/templates/alcatel_aos6_show_health.textfsm")

print(output)
```

**Example Output**

```python
[
    {'resource': 'Receive', 'limit': '80', 'current': '01', 'min_avg': '01', 'hr_avg': '01', 'hr_max': '01'},
    {'resource': 'Transmit/Receive', 'limit': '80', 'current': '01', 'min_avg': '01', 'hr_avg': '01', 'hr_max': '01'},
    {'resource': 'Memory', 'limit': '80', 'current': '76', 'min_avg': '76', 'hr_avg': '76', 'hr_max': '76'},
    {'resource': 'Cpu', 'limit': '80', 'current': '32', 'min_avg': '33', 'hr_avg': '29', 'hr_max': '97'}
]
```

### Ansible

**Ansible task**

```yaml
- name: AOS6 >> parsed with textfsm
  set_fact:
    vlans: "{{ vlans-aos6 | ansible.netcommon.parse_cli_textfsm('textfsm/alcatel_aos6_show_vlan.textfsm') }}"
```

**Example Output**

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
