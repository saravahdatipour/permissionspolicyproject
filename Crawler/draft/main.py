from mypermissions import MyPermissions

url = "https://www.permissionspolicy.xyz"

my_permissions = MyPermissions(url)
my_permissions.get_iframe_policy()
my_permissions.get_features_to_check_conflict()
my_permissions.check_permission_policy_conflicts()
