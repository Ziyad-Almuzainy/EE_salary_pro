# -*- coding: utf-8 -*-
"""
Created on Wed Sep  14 07:58: 2022

by: ZiyadAlHaarbi

**** Original code credit: Omer Sakarya and Ken Jee 
Omer Sakarya: https://github.com/arapfaik/scraping-glassdoor-selenium
Ken Jee  : https://github.com/PlayingNumbers/ds_salary_proj ****

"""

# Importing

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    #Initializing the webdriver
    options = webdriver.ChromeOptions()

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')

    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url='https://www.glassdoor.com/Job/' + keyword + '-jobs-SRCH_KO0,14.htm'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CSS_SELECTOR,  '[data-selected="true"]').click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element(By.XPATH,('.//div[@id="JAModal"]//span[@alt="Close"]')).click()
        except NoSuchElementException:
            pass

        #Going through each job in this page
        job_buttons = driver.find_elements(By.CSS_SELECTOR,'[data-test="job-link"]') #jl for Job Listing. These are the buttons were going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(1)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH,'.//div[@class="css-xuk5ye e1tk4kwz5"]').text
                    location = driver.find_element(By.XPATH,'.//div[@class="css-56kyx5 e1tk4kwz1"]').text
                    job_title = driver.find_element(By.XPATH,'.//div[contains(@class, "css-1j389vi e1tk4kwz2")]').text
                    job_description = driver.find_element(By.XPATH,'.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(By.XPATH,'.//span[@class="css-1hbqxax e1wijj240"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
        
            try:
                rating = driver.find_element(By.CSS_SELECTOR,'[data-test="detailRating"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))
            
             #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:

                driver.find_element_by_xpath("//div[@class='css-t3xrds e856ufb2']").click()


                try:
                    #<div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    #</div>
                    size = driver.find_element_by_xpath("//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*").text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath("//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath("//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text
                except NoSuchElementException:
                    type_of_ownership = -1


                try:
                    industry = driver.find_element_by_xpath("//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath("//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath("//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*").text
                except NoSuchElementException:
                    revenue = -1

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1

            
            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            
            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,})
            #add job to jobs

        #Clicking on the "next page" button
        try:
            driver.find_element(By.CSS_SELECTOR, "[alt='next-icon']").click
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.