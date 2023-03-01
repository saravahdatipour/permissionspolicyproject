import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://www.permissionspolicy.xyz"
domain = url.split("//")[1].split("/")[0]
conflict_number = 0



driver = webdriver.Chrome()
driver.get(url)


# Find all the iframe elements on the page
iframes = driver.find_elements(By.TAG_NAME, "iframe")

# Create a list to store the iframe policy data
iframe_policy = []

# Iterate through the iframe elements
for iframe in iframes:
    # Get the allow attribute value
    allow_value = iframe.get_attribute("allow")
    # Get the src attribute value
    src_value = iframe.get_attribute("src")
    # Strip the "https://" from the src value
    src_value = src_value.replace("https://", "")
    # Add the allow value and src value to the iframe policy list
    iframe_policy.append([allow_value, src_value])

# Print the iframe policy data
print("iframe policy data:", iframe_policy)


#sending request to get header value
response = requests.get(url)
permissions_policy = response.headers.get("Permissions-Policy")

policies = [policy.split("=") for policy in permissions_policy.split(", ")]
policy = [(feature_name, allow_list.strip("()") if "(" in allow_list else allow_list) for feature_name, allow_list in policies]
policy = [(feature_name, allow_list if allow_list else "") for feature_name, allow_list in policy]
print(f"Page Permission Policy: {policy[0]}")


# Get the domain of the URL given to Selenium
domain = url.split("//")[1].split("/")[0]




# Initialize the conflict number
conflict_number = 0

# Get the domain of the URL given to Selenium
domain = url.split("//")[1].split("/")[0]

# Initialize the conflict number
conflict_number = 0

# Initialize a list to store the conflicts
conflicts = []

# Iterate through the iframe policy data
# src_domains = []


third_party_feature_and_domain = []
for iframe in iframe_policy:
    allow_value = iframe[0]
    src_value = iframe[1]
    src_domain = src_value.split("/")[0]
    print(f"src_domain {src_domain}")
    # src_domains.append(src_domain)

    if src_domain != domain:
        third_party_feature_and_domain.append([allow_value , src_domain])

    
# if in the policy_from_iframe the domain is external, get the feature for that exact instance,
# check in the policy_from_website if that exact feature has been set to self or none.



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

print("The following have a potential conflict" + str(policy_to_check_conflict))



# # external check
# external_domains = []
# for item in src_domains:
#     if src_domain != domain:
#         # the domain is external domain
#         external_domains.append(src_domain)

#         #get the attributes attached to this specific domain 


#         pass

    





driver.quit()
