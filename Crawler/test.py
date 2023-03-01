string = "accelerometer=*, ambient-light-sensor=*, autoplay=*, camera=(), display-capture=*, document-domain=*, encrypted-media=*, execution-while-not-rendered=*, execution-while-out-of-viewport=*, fullscreen=*, gamepad=*, geolocation=(*), gyroscope=*, magnetometer=*, microphone=*, midi=*, navigation-override=*, payment=*, picture-in- picture=*, publickey-credentials-get=*, sync-xhr=*, usb=*, xr-spatial-tracking=*"

permission_policy = [policy.split("=") for policy in string.split(", ")]
policy = [(feature_name, allow_list.strip("()") if "(" in allow_list else allow_list) for feature_name, allow_list in permission_policy]
policy = [(feature_name, allow_list if allow_list else "") for feature_name, allow_list in policy]

print(policy)

count = 0
policy_to_check_conflict_from_self = []
policy_to_check_conflict_from_none = []
for item in policy:
    count += 1
    # print("count: " + str(count) + " " + str(item))
    # if it is set to none
    if (item[1] == ''):
        policy_to_check_conflict_from_none.append(item[0])
    elif (item[1] == 'self'):
        policy_to_check_conflict_from_self(item[0])

print("has none:" + str(policy_to_check_conflict_from_none))
print("has self:" + str(policy_to_check_conflict_from_self))




