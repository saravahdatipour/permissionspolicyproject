from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import logging
import csv
from dataanalyzer import define_df,append_data,save_data
from functions import iframefinder, headerpolicy_finder, featureUsedbyThirdParty,calculate_conflicts
from tqdm import tqdm
import pandas as pd
import os
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
            domain = url.replace("https://", "").split("/")[0]
            logger.info(f"domain inspecting now: {domain}")
            try:
                driver = webdriver.Firefox()
                driver.get(url)

                headerpolicy, HasHeaderPolicy = headerpolicy_finder(driver, url, domain)
                iframe_policy, HasInlinePolicy, src_value, allow_value = iframefinder(driver)
                ThirdPartyFrames, ThirdPartyDomains = featureUsedbyThirdParty(iframe_policy,domain)
                HasConflict, NumberOfConflicts, conflictingFeature= calculate_conflicts(ThirdPartyFrames,domain,headerpolicy)
                if not os.path.isfile(FILEPATH): 
                    df = define_df(url, HasHeaderPolicy, HasInlinePolicy, HasConflict, NumberOfConflicts, conflictingFeature, ThirdPartyDomains)
                    df = save_data(df, FILEPATH)
                else:
                    df = append_data(df,url, HasHeaderPolicy, HasInlinePolicy, HasConflict, NumberOfConflicts, conflictingFeature, ThirdPartyDomains)
                    df = save_data(df, FILEPATH)

                driver.quit()

            except Exception as e:
                logging.exception(e)
                driver.quit()


def crawl_single_url(url):
    domain = url.replace("https://", "").split("/")[0]
    conflict_number = 0

    try:
        driver = webdriver.Firefox()
        driver.get(url)

        headerpolicy, HasHeaderPolicy = headerpolicy_finder(driver, url, domain)
        iframe_policy, HasInlinePolicy, src_value, allow_value = iframefinder(driver)
        ThirdPartyFrames, ThirdPartyDomains = featureUsedbyThirdParty(iframe_policy,domain)
        HasConflict, NumberOfConflicts, conflictingFeature= calculate_conflicts(ThirdPartyFrames,domain,headerpolicy)
        # if not os.path.isfile(FILEPATH): 
        #     df = define_df(url, HasHeaderPolicy, HasInlinePolicy, HasConflict, NumberOfConflicts, conflictingFeature, ThirdPartyDomains)
        #     df = save_data(df, FILEPATH)
        # else:
        #     df = append_data(df,url, HasHeaderPolicy, HasInlinePolicy, HasConflict, NumberOfConflicts, conflictingFeature, ThirdPartyDomains)
        #     df = save_data(df, FILEPATH)

        driver.quit()

    except Exception as e:
        logging.exception(e)
        driver.quit()


# crawl_csvfile('urls.csv')
# crawl_single_url('https://google.com/')


