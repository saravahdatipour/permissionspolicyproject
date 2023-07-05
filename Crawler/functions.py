from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from logger import logger
from selenium.webdriver.remote.webelement import WebElement


conflictingFeature = []
#------------------Check if the feature is self or none in header policy but used in the iframe------------------
def check_self_or_none(featuredomain, headerpolicy):
    conflictingFeature = []  # Define conflictingFeature within the function scope
    for value in headerpolicy:
        if value[1] == '' or value[1] == 'self':
            
            if value[0] in featuredomain:
                
                conflictingFeature.append(value[0])
    
    return conflictingFeature

                

#------------------Find iframes and iframe permission policies------------------
def iframefinder(driver):
    src_value, allow_value,iframe_policy = [],[],[] 
    same_origin_iframe_policy = []

    elements = driver.find_elements(By.CSS_SELECTOR,"iframe")
    HasInlinePolicy = False
    for element in elements:
        if isinstance(element, WebElement) and element.tag_name == "iframe":
            logger.info("iframe found")
            src_value = element.get_attribute("src").replace("https://", "")
            allow_value = element.get_attribute("allow")
            if src_value != "":
                if allow_value != "":
                    logger.info(f"allow value is {allow_value} for cross origin")
                    iframe_policy.append([allow_value, src_value])
                    HasInlinePolicy = True #mesvalue
                else:
                    logger.info(f"third party iframe has no allow value ")
            elif allow_value!= "":
                HasInlinePolicy = True #mesvalue
                same_origin_iframe_policy.append([allow_value])
            

        else:
            logger.info("no iframe found")
        logger.info(f"iframe found: iframe policy: {iframe_policy} has inline policy: {HasInlinePolicy}")
    return iframe_policy,same_origin_iframe_policy, HasInlinePolicy, src_value, allow_value

#------------------Find Response header permission policies------------------

def headerpolicy_finder(driver, url, domain):
    headerpolicylist = []
    HasHeaderPolicy = False
    permissions_policy = ""
    for request in driver.requests:
        if request.response and request.response.status_code==200:
            if request.response.headers.get("Permissions-Policy"):
                permissions_policy = request.response.headers.get("Permissions-Policy")
                if  domain in str(request):
                    HasHeaderPolicy = True
                    logger.info(f"Permission policy header found {str(request)}") #newly added
                    if "," in permissions_policy or  ";" in permissions_policy:
                        if ";" in permissions_policy:
                            policy_separator = ";"
                        elif "," in permissions_policy:
                            policy_separator = ","
                        permissions_policy = permissions_policy.replace(" ", "")
                        seperated_policies = permissions_policy.split(policy_separator)
                        if seperated_policies[-1] == "":
                            seperated_policies.pop()
                        for headerpolicy in seperated_policies:
                            header_split = headerpolicy.split("=")
                            feature_name=  header_split[0]
                            allow_list = header_split[1].strip("()") if "(" in header_split[1] else header_split[1]
                            #if not the same permission policy is already in the list
                            if not any(feature_name in sublist for sublist in headerpolicylist):
                                headerpolicylist.append((feature_name, allow_list))
                    elif not any(feature_name in sublist for sublist in headerpolicylist):
                        feature_name = permissions_policy.split("=")[0]
                        allow_list = permissions_policy.split("=")[1].strip("()") if "(" in permissions_policy.split("=")[1] else permissions_policy.split("=")[1]
                        headerpolicylist.append((feature_name, allow_list))

                else:
                    logger.info(f"Not the same domain {domain} as the request: {str(request)}")
                    continue

            else:
                # check if there are no permission policies between all requests then log it    
                logger.info(f"no Permissions-Policy header on current request for {str(request)}") #fix this
        else:
            logger.info(f"No response on {str(request)}")

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

def calculate_conflicts(thirdParty_featureDomain, domain, headerpolicy):
    HasConflict, NumberOfConflicts, conflictingFeature = False, 0, []
    for featuredomain in thirdParty_featureDomain:
        conflictingFeature = check_self_or_none(featuredomain[0], headerpolicy)
        if conflictingFeature != []:
            logger.info(f"The following have potential conflicts: {conflictingFeature} on this domain {domain}")
            HasConflict = True  # message value
            NumberOfConflicts = len(conflictingFeature)  # message value
            # Move the subsequent code block inside the if statement
            return HasConflict, NumberOfConflicts, conflictingFeature
    logger.info(f"No conflicts found on {domain}")
    return HasConflict, NumberOfConflicts, conflictingFeature
