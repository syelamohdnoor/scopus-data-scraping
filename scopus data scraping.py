#!/usr/bin/env python
# coding: utf-8

# In[22]:


import csv
from selenium import webdriver
from time import sleep
import pandas as pd
import math

# driver = webdriver.Chrome(executable_path='c:/chromedriver')
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# [EDIT] dataframe from input xlsx
df = pd.read_excel('')

# [EDIT] login information to Scopus.com
u = ''
p = ''

driver.get('https://www.scopus.com')
driver.find_element_by_xpath('//*[@id="signin_link_move"]').click()
sleep(3)
driver.find_element_by_xpath('//*[@id="bdd-email"]').send_keys(u)
sleep(3)
driver.find_element_by_xpath('//*[@id="bdd-elsPrimaryBtn"]').click()
sleep(3)
driver.find_element_by_xpath('//*[@id="bdd-password"]').send_keys(p)
sleep(3)
driver.find_element_by_xpath('//*[@id="bdd-elsPrimaryBtn"]').click()

for index, row in df.iterrows():
    row = row.copy()

    try:
        scopus_ids = str(row['Scopus ID']).split('; ')
        links = ['http://www.scopus.com/authid/detail.url?authorId=%s' %
                 scopus_id for scopus_id in scopus_ids]

        NUM_PUBS = 0
        CITES = 0
        HINDEX = 0
        HINDEX_SELF = 0
        TOT_CIT5Y = 0
        TOT_CIT = 0
        TOT_CIT5Y_WO = 0
        TOT_CIT_WO = 0

        for i in range(0, len(links)):
            link = links[i]
            scopus_id = scopus_ids[i]

            driver.get(link)
            sleep(6)

            # check id
            try:
                info = driver.find_element_by_class_name('authId')
                info = info.text.strip().split('\n')[0].split(': ')[1]
            except:
                pass

            # 01 total publication
            try:
                num_pubs = int(driver.find_element_by_id(
                    'authorDetailsDocumentsByAuthor').find_element_by_class_name('panel-body').text.split('\n')[0])
            except:
                num_pubs = 0
                pass

            # 02 h-index 
            try:

                hindex = driver.find_element_by_id('authorDetailsHindex')
                hindex = int(hindex.text.strip().split('\n')[2])

                if hindex > HINDEX:
                    HINDEX = hindex

            except:
                hindex = 0
                pass

            # 03 h-index w/o self citation
            try:
                hindex_self = driver.find_element_by_xpath(
                    '//*[@id="authorDetailsHindex"]/div[2]/button').click()
                hindex_self = driver.find_element_by_xpath(
                    '//*[@id="hindexCheckboxes"]/div[1]/label').click()
                hindex_self = driver.find_element_by_xpath(
                    '//*[@id="updateGraphButton_submit1"]').click()
                sleep(20)
                hindex_self = int(driver.find_element_by_xpath(
                    '//*[@id="analyzeSourceTitle"]/span[2]').text)

                if hindex_self > HINDEX_SELF:
                    HINDEX_SELF = hindex_self

            except:
                hindex_self = 0
                pass
            
            # 04 recent total citation (5 years)
            try:
                tot_cit5y = driver.find_element_by_xpath(
                    '//*[@id="authHirschPage"]/section/nav/div/a').click()
                tot_cit5y = driver.find_element_by_xpath(
                    '//*[@id="authorDetailsTotalCitations"]/div[2]/button').click()
                sleep(20)
                tot_cit5y = int(driver.find_element_by_xpath(
                    '//*[@id="subtotal"]/a/span').text)

                if tot_cit5y > TOT_CIT5Y:
                    TOT_CIT5Y = tot_cit5y

            except:
                tot_cit5y = 0
                pass
            
            # 05 total citation (overall)
            try:
                tot_cit = int(driver.find_element_by_xpath(
                    '//*[@id="grandtotal"]/a/span').text)

                if tot_cit > TOT_CIT:
                    TOT_CIT = tot_cit

            except:
                tot_cit = 0
                pass
            
            # 06 recent total citation (5 years) w/o self citation
            try:
                tot_cit5y_wo = driver.find_element_by_xpath(
                    '//*[@id="updateOverviewBox"]/div[1]').click()
                tot_cit5y_wo = driver.find_element_by_xpath(
                    '//*[@id="updateOverviewButtonOn"]').click()
                sleep(20)
                tot_cit5y_wo = int(driver.find_element_by_xpath(
                    '//*[@id="subtotal"]').text)

                if tot_cit5y_wo > TOT_CIT5Y_WO:
                    TOT_CIT5Y_WO = tot_cit5y_wo

            except:
                tot_cit5y_wo = 0
                pass
        
            # 07 total citation (overall) w/o self citation
            try:
                tot_cit_wo = int(driver.find_element_by_xpath(
                    '//*[@id="grandtotal"]').text)
                
                if tot_cit_wo > TOT_CIT_WO:
                    TOT_CIT_WO = tot_cit_wo

            except:
                tot_cit_wo = 0
                pass
            
            # throw a warning if the scopus link get redirect somewhere else
            if scopus_id != info:
                print('[WARN] SCOPUS_ID_REDIRECT: %s' % scopus_id)

            else:
                NUM_PUBS += num_pubs
                CITES += cites

            df.loc[index, 'Publication Number'] = NUM_PUBS
            df.loc[index, 'h-index'] = HINDEX
            df.loc[index, 'h-index w/o Self Citation'] = HINDEX_SELF
            df.loc[index, 'Recent Citation'] = TOT_CIT5Y
            df.loc[index, 'Overall Citation'] = TOT_CIT
            df.loc[index, 'Recent Citation w/o Self Citation'] = TOT_CIT5Y_WO
            df.loc[index, 'Overall Citation w/o Self Citation'] = TOT_CIT_WO
            
    except:
        pass

driver.close()
driver.quit()

# output
out_file = 'out.xlsx'
writer = pd.ExcelWriter(out_file)
df.to_excel(writer, sheet_name='out')
writer.save()

