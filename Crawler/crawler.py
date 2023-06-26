from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
import logging
import csv
from dataanalyzer import define_df,append_data,save_data
from functions import iframefinder, headerpolicy_finder, featureUsedbyThirdParty,calculate_conflicts
from tqdm import tqdm
import pandas as pd
import os
import sys

from logger import logger
FILEPATH = 'crawlresults.xlsx'
# ---------------------------------------------------Main-------------------------------------------------------------



def crawl_csvfile(csvfile):

    with open(csvfile) as file:
        readCSV = csv.reader(file)
        rows = list(readCSV)
        total_rows = len(rows)
        for row in tqdm(rows,mininterval=0.1):
            url = row[1]
            domain = url.replace("https://www.", "").split("/")[0]
            logger.info(f"domain inspecting now: {domain}")
            chrome_options = webdriver.ChromeOptions()
            WarningScenario = False

            # chrome option for not showing devtools
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--remote-debugging-port=0')
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
            try:
                driver.get(url)
                
                headerpolicy, HasHeaderPolicy = headerpolicy_finder(driver, url, domain)
                iframe_policy,same_origin_iframe_policy, HasInlinePolicy, src_value, allow_value = iframefinder(driver)
                ThirdPartyFrames, ThirdPartyDomains = featureUsedbyThirdParty(iframe_policy,domain)
                HasConflict, NumberOfConflicts, conflictingFeature= calculate_conflicts(ThirdPartyFrames,domain,headerpolicy)


                if not os.path.isfile(FILEPATH): 

                    if HasHeaderPolicy == False and iframe_policy == "":
                        WarningScenario = True

                    
                    df = define_df(url, HasHeaderPolicy,headerpolicy, HasInlinePolicy,iframe_policy,same_origin_iframe_policy, HasConflict, NumberOfConflicts, conflictingFeature, ThirdPartyDomains,WarningScenario)
                    df = save_data(df, FILEPATH)
                else:
                    if HasHeaderPolicy == False and iframe_policy == "":
                        WarningScenario = True
                    df = append_data(df , url, HasHeaderPolicy,headerpolicy, HasInlinePolicy,iframe_policy,same_origin_iframe_policy, HasConflict, NumberOfConflicts, conflictingFeature, ThirdPartyDomains,WarningScenario)
                    df = save_data(df, FILEPATH)

                driver.quit()

            except Exception as e:
                logger.exception(e)
                driver.quit()


def crawl_single_url(url):
    domain = url.replace("https://www.", "").split("/")[0]
    chrome_options = webdriver.ChromeOptions()
    # chrome option for not showing devtools
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--log-level=3')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    try:
        driver.get(url)

        headerpolicy, HasHeaderPolicy = headerpolicy_finder(driver, url, domain)
        iframe_policy,same_origin_iframe_policy, HasInlinePolicy, src_value, allow_value = iframefinder(driver)
        ThirdPartyFrames, ThirdPartyDomains = featureUsedbyThirdParty(iframe_policy,domain)
        HasConflict, NumberOfConflicts, conflictingFeature= calculate_conflicts(ThirdPartyFrames,domain,headerpolicy)
        WarningScenario = False
        if HasHeaderPolicy == False and iframe_policy == "":
            WarningScenario = True

        if not os.path.isfile(FILEPATH): 
            df = define_df(url, HasHeaderPolicy,headerpolicy, HasInlinePolicy,iframe_policy,same_origin_iframe_policy, HasConflict, NumberOfConflicts, conflictingFeature, ThirdPartyDomains,WarningScenario)
            df = save_data(df, FILEPATH)
        # else:
        #     df = append_data(df,url, HasHeaderPolicy,headerpolicy, HasInlinePolicy, HasConflict, NumberOfConflicts, conflictingFeature, ThirdPartyDomains)
        #     df = save_data(df, FILEPATH)

        driver.quit()

    except Exception as e:
        logger.exception(e)
        driver.quit()


# crawl_csvfile('urls.csv')
# crawl_single_url('https://google.com/')


