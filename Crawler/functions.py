from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import logging


conflictingFeature = []
#------------------Check if the feature is self or none in header policy but used in the iframe------------------
def check_self_or_none(featuredomain,headerpolicy):
    for value in headerpolicy:
        if (value[1] == '') or (value[1] == 'self'):
            if value[0] == featuredomain:
                conflictingFeature.append(value[0])
    return conflictingFeature
        
                

#------------------Find iframes and iframe permission policies------------------
def iframefinder(driver):
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    src_value, allow_value,iframe_policy = [],[],[]
    HasInlinePolicy = False
    for iframe in iframes:
        allow_value = iframe.get_attribute("allow")
        if allow_value != None:
            src_value = iframe.get_attribute("src").replace("https://", "")
            iframe_policy.append([allow_value, src_value])
            HasInlinePolicy = True #mesvalue
    return iframe_policy, HasInlinePolicy, src_value, allow_value

#------------------Find Response header permission policies------------------

def headerpolicy_finder(driver, url, domain):
    headerpolicy = []
    HasHeaderPolicy = False

    for request in driver.requests:
        request_str = (str(request))
        if  request_str in url :
            logging.info(f"Target url: {request_str}")
            permissions_policy= request.response.headers.get("Permissions-Policy")
            logging.info(f"permissions_policy: {permissions_policy}")
            if permissions_policy != None:
                HasHeaderPolicy = True #mesvalue
                permissions_policy_stripped = [headerpolicy.split("=") for headerpolicy in permissions_policy.split(", ")]
                headerpolicy = [(feature_name, allow_list.strip("()") if "(" in allow_list else allow_list) for feature_name, allow_list in permissions_policy_stripped]
                headerpolicy = [(feature_name, allow_list if allow_list else "") for feature_name, allow_list in headerpolicy]
        else:
            logging.info(f"Not the target url: {request_str}")
            continue

    return headerpolicy, HasHeaderPolicy
    
#------------------Find third-party iframes and the features they use------------------
def featureUsedbyThirdParty(iframe_policy,domain):
    ThirdPartyFrames = []
    src_domains = []
    for iframe in iframe_policy:
        allow_value = iframe[0]
        src_value = iframe[1]
        src_domain = src_value.split("/")[0]
        if src_domain != domain:
            ThirdPartyFrames.append([allow_value , src_domain])    
            src_domains.append(src_domain)
    return ThirdPartyFrames, src_domains

#--------------------------------Find conflicts-----------------------------------

def calculate_conflicts(thirdParty_featureDomain,domain,headerpolicy):
    HasConflict, NumberOfConflicts, conflictingFeature = False, 0, []
    for featuredomain in thirdParty_featureDomain:
        conflictingFeature= check_self_or_none(featuredomain[0],headerpolicy)
    if conflictingFeature != []:
        logging.info(f"The following have potential conflicts: {conflictingFeature} on this domain {domain}")
        HasConflict = True #mesvalue
        NumberOfConflicts = len(conflictingFeature) #mesvalue
    else:
        logging.info(f"fNo conflicts found on {domain}")
    return HasConflict, NumberOfConflicts, conflictingFeature