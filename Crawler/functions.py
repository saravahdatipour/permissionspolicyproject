from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from logger import logger
from selenium.webdriver.remote.webelement import WebElement


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
    src_value, allow_value,iframe_policy = [],[],[] 
    elements = driver.find_elements(By.CSS_SELECTOR,"iframe")
    HasInlinePolicy = False
    for element in elements:
        if isinstance(element, WebElement) and element.tag_name == "iframe":
            logger.info("iframe found")
            allow_value = element.get_attribute("allow")
            if allow_value != "":
                logger.info(f"allow value is {allow_value}")
                src_value = element.get_attribute("src").replace("https://", "")
                iframe_policy.append([allow_value, src_value])
                HasInlinePolicy = True #mesvalue
        else:
            logger.info("no iframe found")
        logger.info(f"iframe found: iframe policy: {iframe_policy} has inline policy: {HasInlinePolicy}")
    return iframe_policy, HasInlinePolicy, src_value, allow_value

#------------------Find Response header permission policies------------------

def headerpolicy_finder(driver, url, domain):
    headerpolicylist = []
    HasHeaderPolicy = False

    for request in driver.requests:
        request_str = (str(request))

        if  domain in request_str and request.response.status_code ==200 :
            permissions_policy = request.response.headers.get("Permissions-Policy")
            if permissions_policy: 
                if ","  in permissions_policy:
                    for headerpolicy in permissions_policy.split(", "):
                        feature_name=  headerpolicy.split("=")[0]
                        allow_list = headerpolicy.split("=")[1].strip("()") if "(" in headerpolicy.split("=")[1] else headerpolicy.split("=")[1]
                        #if not the same permission policy is already in the list
                        if not any(feature_name in sublist for sublist in headerpolicylist):
                            headerpolicylist.append((feature_name, allow_list))
                else:
                    feature_name = permissions_policy.split("=")[0]
                    allow_list = permissions_policy.split("=")[1].strip("()") if "(" in permissions_policy.split("=")[1] else permissions_policy.split("=")[1]
                    headerpolicylist.append((feature_name, allow_list))

            else:
                logger.info(f"No header policy with response 200 on {domain}")
        else:
            logger.info(f"Not the target url: {request_str}")
            continue
    return headerpolicylist, HasHeaderPolicy

    
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
        logger.info(f"The following have potential conflicts: {conflictingFeature} on this domain {domain}")
        HasConflict = True #mesvalue
        NumberOfConflicts = len(conflictingFeature) #mesvalue
    else:
        logger.info(f"fNo conflicts found on {domain}")
    return HasConflict, NumberOfConflicts, conflictingFeature