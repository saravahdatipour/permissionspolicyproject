import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

class MyPermissions:
    def __init__(self, url):
        self.url = url
        self.domain = url.split("//")[1].split("/")[0]
        self.conflict_number = 0
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def __del__(self):
        self.driver.quit()

    def get_iframe_policy(self):
        # Find all the iframe elements on the page
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

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

        return iframe_policy

    def get_page_permission_policy(self):
        #sending request to get header value
        response = requests.get(self.url)
        permissions_policy = response.headers.get("Permissions-Policy")

        policies = [policy.split("=") for policy in permissions_policy.split(", ")]
        policy = [(feature_name, allow_list.strip("()") if "(" in allow_list else allow_list) for feature_name, allow_list in policies]
        policy = [(feature_name, allow_list if allow_list else "") for feature_name, allow_list in policy]
        return policy[0]

    def get_third_party_feature_and_domain(self, iframe_policy):
        third_party_feature_and_domain = []
        for iframe in iframe_policy:
            allow_value = iframe[0]
            src_value = iframe[1]
            src_domain = src_value.split("/")[0]

            if src_domain != self.domain:
                third_party_feature_and_domain.append([allow_value, src_domain])

        return third_party_feature_and_domain

    def get_features_to_check_conflict(self, policy, third_party_feature_and_domain):
        features_to_check_conflict = []
        for external_item in third_party_feature_and_domain:
            feature_name = external_item[0]
            for item in policy:
                if (item[1] == '') or (item[1] == 'self'):
                    if item[0] == feature_name:
                        features_to_check_conflict.append(item[0])

        return features_to_check_conflict

    def check_permission_policy_conflicts(self):
        iframe_policy = self.get_iframe_policy()
        page_permission_policy = self.get_page_permission_policy()
        third_party_feature_and_domain = self.get_third_party_feature_and_domain(iframe_policy)
        features_to_check_conflict = self.get_features_to_check_conflict(page_permission_policy, third_party_feature_and_domain)

        if features_to_check_conflict:
            print("The following have a potential conflict: " + str(features_to_check_conflict))
        else:
            print("No potential conflicts found")
