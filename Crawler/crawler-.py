import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize variables
url = "https://www.permissionspolicy.xyz"
domain = url.split("//")[1].split("/")[0]
domain = domain.replace("www." , '')
conflict_number = 0

# Launch Chrome and load the page
driver = webdriver.Chrome()
driver.get(url)

# Find all the iframe elements on the page and store their policy data in a list
iframes = driver.find_elements(By.TAG_NAME, "iframe")
iframe_policy = []
for iframe in iframes:
    allow_value = iframe.get_attribute("allow")
    src_value = iframe.get_attribute("src").replace("https://", "")
    iframe_policy.append([allow_value, src_value])

# Print the iframe policy data
print("iframe policy data:", iframe_policy)

# Get the permissions policy from the response headers and parse it into a list
response = requests.get(url)
permissions_policy = response.headers.get("Permissions-Policy")
policies = [policy.split("=") for policy in permissions_policy.split(", ")]
policy = [(feature_name, allow_list.strip("()") if "(" in allow_list else allow_list) for feature_name, allow_list in policies]
policy = [(feature_name, allow_list if allow_list else "") for feature_name, allow_list in policy]
print(f"Page Permission Policy: {policy[0]}")

# Identify third-party iframes and the features they use
third_party_feature_and_domain = []
for iframe in iframe_policy:
    allow_value = iframe[0]
    src_value = iframe[1]
    src_domain = src_value.split("/")[0]
    if src_domain != domain:
        print("THIRD PARTY: source domain is: " + src_domain + "&  site domain is: " + domain)
        third_party_feature_and_domain.append([allow_value , src_domain])

# Identify features that may conflict with the website's policy
policy_from_website = policy
policy_from_iframe = iframe_policy
policy_to_check_conflict = []
def check_self_or_none(feature):
    for item in policy_from_website:
        if (item[1] == '') or (item[1] == 'self'):
            if item[0] == feature:
                policy_to_check_conflict.append(item[0])
for external_item in third_party_feature_and_domain:
    check_self_or_none(external_item[0])
print("The following have a potential conflict: " + str(policy_to_check_conflict))

# Quit the driver
driver.quit()
