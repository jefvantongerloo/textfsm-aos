Alcatel-Lucent Enterprise AOS6 TextFSM templates

# Example usage - Fetching
## Netmiko

**Python script**

```python
from netmiko import ConnectHandler
from rich import print

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

**Output**

```python
[
    {'resource': 'Receive', 'limit': '80', 'current': '01', 'min_avg': '01', 'hr_avg': '01', 'hr_max': '01'},
    {'resource': 'Transmit/Receive', 'limit': '80', 'current': '01', 'min_avg': '01', 'hr_avg': '01', 'hr_max': '01'},
    {'resource': 'Memory', 'limit': '80', 'current': '76', 'min_avg': '76', 'hr_avg': '76', 'hr_max': '76'},
    {'resource': 'Cpu', 'limit': '80', 'current': '32', 'min_avg': '33', 'hr_avg': '29', 'hr_max': '97'}
]
```