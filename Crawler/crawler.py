import requests
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import logging
import csv
from dataanalyzer import get_data
## functions 
def check_self_or_none(feature):
    for value in headerpolicy:
        if (value[1] == '') or (value[1] == 'self'):
            if value[0] == feature:
                conflictingFeature.append(value[0])


#open and import urls from a csv file
with open('urls.csv') as file:
    readCSV = csv.reader(file)
    for row in readCSV:
        url = row[1]
        domain = url.replace("https://", "").split("/")[0]
        conflict_number = 0

        try:
            driver = webdriver.Chrome()
            driver.get(url)

            # Find all the iframe elements on the page and store their policy data in a list
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            iframe_policy = []
            for iframe in iframes:
                allow_value = iframe.get_attribute("allow")
                if allow_value == None:
                    HasInlinePolicy = False #mesvalue
                else:
                    src_value = iframe.get_attribute("src").replace("https://", "")
                    iframe_policy.append([allow_value, src_value])
                    HasInlinePolicy = True #mesvalue
                
             # print("iframe policy data:", iframe_policy)

            
            for request in driver.requests:
                request_str = (str(request))
                print(request_str)
                if  request_str in url :
                    permissions_policy= request.response.headers.get("Permissions-Policy")
                    HasHeaderPolicy = True #mesvalue
                    permissions_policy_stripped = [headerpolicy.split("=") for headerpolicy in permissions_policy.split(", ")]
                    headerpolicy = [(feature_name, allow_list.strip("()") if "(" in allow_list else allow_list) for feature_name, allow_list in permissions_policy_stripped]
                    headerpolicy = [(feature_name, allow_list if allow_list else "") for feature_name, allow_list in headerpolicy]

                else:
                    if HasHeaderPolicy == True:
                        continue
                    HasHeaderPolicy = False #mesvalue
                    print("No Permissions Policy Found",str(url))
                    continue


            # Identify third-party iframes and the features they use
            thirdParty_featureDomain = []
            for iframe in iframe_policy:
                allow_value = iframe[0]
                src_value = iframe[1]
                src_domain = src_value.split("/")[0]
                if src_domain != domain:
                    thirdParty_featureDomain.append([allow_value , src_domain])
                    # print("Third-party iframes and the features they use: " + str(third_party_feature_and_domain))  
                    
            ThirdPartyFrames = thirdParty_featureDomain #mesvalue

            # Identify features that may conflict with the website's policy
            policy_from_iframe = iframe_policy
            conflictingFeature = []

            for featuredomain in thirdParty_featureDomain:
                check_self_or_none(featuredomain[0])
            if conflictingFeature != []:
                print("The following have potential conflicts: " + str(conflictingFeature)+ " On the following website: " + str(domain))
                HasConflict = True #mesvalue
                NumberOfConflicts = len(conflictingFeature) #mesvalue
            else:
                print("No conflicts found on " + str(domain))
                HasConflict = False #mesvalue
            get_data(url, HasHeaderPolicy, HasInlinePolicy, HasConflict, conflictingFeature, NumberOfConflicts,ThirdPartyFrames)
            driver.quit()
        except Exception as e:
            logging.exception(e)
            driver.quit()


