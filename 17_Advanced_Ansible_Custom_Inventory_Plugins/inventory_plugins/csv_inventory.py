import csv
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.errors import AnsibleParserError

DOCUMENTATION = '''
    author: Abhishek Das
    name: csv_inventory
    plugin_type: inventory
    short_description: Ansible dynamic inventory plugin for CSV files
    description:
        - Generates an inventory from a CSV file containing device information
    options:
        plugin:
            description: Name of the plugin
            required: true
            choices: ['csv_inventory']
        path_to_csv:
            description: Path to the CSV file containing inventory data
            required: true
            type: str
'''

class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
  NAME = 'csv_inventory'

  def verify_file(self, path):
    if not path.endswith(('.yaml', '.yml')):
      raise AnsibleParserError("Invalid file extension, expected a .yaml or .yml file !!!!")
    return super(InventoryModule, self).verify_file(path)
  
  def parse(self, inventory, loader, path, cache=True):
    # Load options from inventory configuration
    super(InventoryModule, self).parse(inventory, loader, path)
    config_data = self._read_config_data(path)
    csv_path = config_data.get('path_to_csv')
    
    if not csv_path:
      raise AnsibleParserError("path_to_csv is a required parameter !!!!")
    
    try:
        with open(csv_path, mode='r') as file:
          csv_reader = csv.DictReader(file)
          for row in csv_reader:
            self._parse_device(row, inventory)
    except Exception as e:
      raise AnsibleParserError(f"Error reading CSV file: {e}")
    
  
  def _parse_device(self, row, inventory):
    # Set device name as hostname
    device_name = row.get("Device Name")
    regions = []
    sitename = []
    devicerole = []
    platform = []

    if not row.get('Region') in regions:
      regions.append(row['Region'])
      inventory.add_group(row['Region'])

    if not row.get("Site Name") in sitename:
      sitename.append(row["Site Name"])
      inventory.add_group(row["Site Name"])

    if not row.get("Device Role") in devicerole:
      devicerole.append(row["Device Role"])
      inventory.add_group(row["Device Role"])
    
    if not row.get("Platform") in platform:
      platform.append(row["Platform"])
      inventory.add_group(row["Platform"])
    
    # Add host to the inventory
    inventory.add_host(device_name)

    # Set host variables
    inventory.set_variable(device_name, 'ansible_host', row.get('Mgmt IP'))
    inventory.set_variable(device_name, 'ansible_network_os', row.get('Platform'))

    # Add hosts to groups based on Region, Site Name, Device Role and Platform
    inventory.add_host(device_name, group=row.get('Region'))
    inventory.add_host(device_name, group=row.get('Site Name'))
    inventory.add_host(device_name, group=row.get('Device Role'))
    inventory.add_host(device_name, group=row.get('Platform'))