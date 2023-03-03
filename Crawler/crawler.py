from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import logging
import csv
from dataanalyzer import get_data
from functions import iframefinder, headerpolicy_finder, featureUsedbyThirdParty,calculate_conflicts


# ---------------------------------------------------Main-------------------------------------------------------------

def crawl_csvfile(csvfile):

    with open(csvfile) as file:
        readCSV = csv.reader(file)
        for row in readCSV:
            url = row[1]
            domain = url.replace("https://", "").split("/")[0]

            try:
                driver = webdriver.Chrome()
                driver.get(url)

                headerpolicy, HasHeaderPolicy = headerpolicy_finder(driver, url, domain)
                iframe_policy, HasInlinePolicy, src_value, allow_value = iframefinder(driver)
                ThirdPartyFrames, ThirdPartyDomains = featureUsedbyThirdParty(iframe_policy,domain)
                HasConflict, NumberOfConflicts, conflictingFeature= calculate_conflicts(ThirdPartyFrames,domain,headerpolicy)
                

                get_data(url, HasHeaderPolicy, HasInlinePolicy, HasConflict, conflictingFeature, NumberOfConflicts,ThirdPartyDomains)
                driver.quit()

            except Exception as e:
                logging.exception(e)
                driver.quit()


def crawl_single_url(url):
    domain = url.replace("https://", "").split("/")[0]
    conflict_number = 0

    try:
        driver = webdriver.Chrome()
        driver.get(url)

        headerpolicy, HasHeaderPolicy = headerpolicy_finder(driver, url, domain)
        iframe_policy, HasInlinePolicy, src_value, allow_value = iframefinder(driver)
        ThirdPartyFrames, ThirdPartyDomains = featureUsedbyThirdParty(iframe_policy,domain)
        HasConflict, NumberOfConflicts, conflictingFeature= calculate_conflicts(ThirdPartyFrames,domain,headerpolicy)

        get_data(url, HasHeaderPolicy, HasInlinePolicy, HasConflict, conflictingFeature, NumberOfConflicts,ThirdPartyDomains)
        driver.quit()

    except Exception as e:
        logging.exception(e)
        driver.quit()


# crawl_csvfile('urls.csv')
# crawl_single_url('https://google.com/')


