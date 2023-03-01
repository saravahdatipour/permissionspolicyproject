import requests
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import logging
import csv
#open and import urls from a csv file
with open('urls.csv') as file:
    readCSV = csv.reader(file)
    for row in readCSV:
        url = row[0]
        domain = url.split("//")[1].split("/")[0]
        domain = domain.replace("www." , '')
        conflict_number = 0

        try:
            driver = webdriver.Chrome()
            driver.get(url)

            # Find all the iframe elements on the page and store their policy data in a list
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            iframe_policy = []
            for iframe in iframes:
                allow_value = iframe.get_attribute("allow")
                src_value = iframe.get_attribute("src").replace("https://", "")
                iframe_policy.append([allow_value, src_value])
             # print("iframe policy data:", iframe_policy)

            permissions_policy = driver.requests[1].response.headers.get("Permissions-Policy")
            #write a conditional to check if the permissions policy is empty or only one = sign is present  
            if permissions_policy != None:
                permissions_policy_stripped = [policy.split("=") for policy in permissions_policy.split(", ")]
                policy = [(feature_name, allow_list.strip("()") if "(" in allow_list else allow_list) for feature_name, allow_list in permissions_policy_stripped]
                policy = [(feature_name, allow_list if allow_list else "") for feature_name, allow_list in policy]
            else:
                print("No Permissions Policy Found")
                continue
                

            # Identify third-party iframes and the features they use
            third_party_feature_and_domain = []
            for iframe in iframe_policy:
                allow_value = iframe[0]
                src_value = iframe[1]
                src_domain = src_value.split("/")[0]
                if src_domain != domain:
                    third_party_feature_and_domain.append([allow_value , src_domain])
                    # print("Third-party iframes and the features they use: " + str(third_party_feature_and_domain))  

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
            print("The following have potential conflicts: " + str(policy_to_check_conflict)+ " On the following website: " + str(url))

        except Exception as e:
            logging.exception(e)
            driver.quit()


