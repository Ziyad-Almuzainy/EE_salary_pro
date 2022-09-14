#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 09:37:45 2022

@author: ziyadalhaarbi

Ken Jee  : https://github.com/PlayingNumbers/ds_salary_proj
"""

import pandas as pd 

df = pd.read_csv('/Users/ziyadalhaarbi/Documents/EE_salary_pro/Fetch_Data.csv')

#salary parsing 

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[-1]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

#Company name text only
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] <0 else x['Company Name'][:-3], axis = 1)

#state field 
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df.job_state.value_counts()

df['same_state'] = df.apply(lambda x: 1 if x.min_salary == x.max_salary else 0, axis = 1)

#age of company 
df['age'] = df.Founded.apply(lambda x: x if x <1 else 2020 - x)


#parsing of job description (design, ect.)

#design
df['design'] = df['Job Description'].apply(lambda x: 1 if 'design' in x.lower() else 0)

#protection 
df['protection'] = df['Job Description'].apply(lambda x: 1 if 'electrical system' in x.lower() or 'r-studio' in x.lower() else 0)
df.protection.value_counts()
 
#installation 
df['installation'] = df['Job Description'].apply(lambda x: 1 if 'installation' in x.lower() else 0)
df.installation.value_counts()

#power_system
df['power_system'] = df['Job Description'].apply(lambda x: 1 if 'power system' in x.lower() else 0)
df.power_system.value_counts()


#excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel.value_counts()

df.columns

#df_out = df.drop(['Unnamed: 0'], axis =2)

#out.df.to_csv('Users/ziyadalhaarbi/Documents/EE_salary_pro/salary_data_cleaned.csv')

