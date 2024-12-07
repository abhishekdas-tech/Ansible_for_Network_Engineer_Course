from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    get_config,
    load_config,
)

DOCUMENTATION = '''
---
module: cisco_port_security
short_description: Configure port security on Cisco devices
description:
    - This module generates commands to configure port security on specified Cisco interfaces.
options:
    interface:
        description: The interface on which to configure port security.
        required: true
        type: str
    max_mac:
        description: Maximum number of MAC addresses allowed.
        required: false
        default: 2
        type: int
    violation:
        description: Violation action to take (e.g., restrict, shutdown, protect).
        required: false
        default: restrict
        choices: ['restrict', 'shutdown', 'protect']
        type: str
author:
    - "Abhishek Das"
'''

EXAMPLES = '''
- name: Generate port security configuration commands
  cisco_port_security:
    interface: "GigabitEthernet1/0/1"
    max_mac: 2
    violation: restrict
  delegate_to: localhost
'''

RETURN = '''
commands:
    description: List of commands to be sent to the device.
    returned: success
    type: list
    sample:
      - interface GigabitEthernet1/0/1
      - switchport port-security
      - switchport port-security maximum 2
      - switchport port-security violation restrict
'''

def run_module():
  module_args = dict(
    interface=dict(type='str', required=True),
    max_mac=dict(type='int', required=False, default=2),
    violation=dict(type='str', required=False, default='restrict', choices=['restrict', 'shutdown', 'protect']),
  )

  result = dict(
    changed=False,
    original_message='Configuring Port Security',
    commands=[]
  )

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
  )

  # Collect arguments
  interface = module.params['interface']
  max_mac = module.params['max_mac']
  violation = module.params['violation']

  # Prepare the commands
  commands = [
    f'interface {interface}',
    'switchport port-security',
    f'switchport port-security maximum {max_mac}',
    f'switchport port-security violation {violation}'
  ]

  result['commands'] = commands

  if commands:
    if not module.check_mode:
      load_config(module, commands)
    result['changed'] = True
  result['changed'] = True
  module.exit_json(**result)

def main():
  run_module()

if __name__ == '__main__':
  main()