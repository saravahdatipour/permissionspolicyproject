from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--log-level=3')

# Configure SeleniumWire options
seleniumwire_options = {
    'request_interceptor': lambda request: None,
    'response_interceptor': lambda response: None
}

# Create Chrome driver with SeleniumWire
driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options)

url = "https://permissionspolicy.xyz/"


driver.get(url)
headerpolicylist = []
for request in driver.requests:
    request_str = (str(request))
    if  url in request_str :
        if request.response.status_code ==200: 
            permissions_policy = request.response.headers.get("Permissions-Policy")
            if permissions_policy:
                HasHeaderPolicy = True
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


driver.quit()
