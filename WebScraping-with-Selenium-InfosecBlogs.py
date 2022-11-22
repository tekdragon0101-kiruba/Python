# Author: kirubakaran kalidass
# Project Name: Web scraping with selenium for download infosec blogs
'''
description: This project extract the blog in infosecwriteups.com
			 through selenium and give it a file as csv using pandas
			 Library. You can also use for sending automation mail 
			 along with extracted blog content and also you can 
             schedule this script for getting the latest blogs for 
             daily articles.
			 check: ScrapItMailIt Project.
requirements: selenium, pandas
'''


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd


website = 'https://infosecwriteups.com/tagged/bug-bounty'

# headless mode
options_headless = Options()
options_headless.headless = True
driver = webdriver.Firefox(options=options_headless)
driver.get(website)

# scroll down for page loading and getting more content
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(10)

# finding titles via elements
blog_titles_list = []
blog_links_list = []
blog_titles = driver.find_elements(
    by='xpath',
    value="//div/h3[@class='graf graf--h3 graf-after--figure graf--title' \
    or @class='graf graf--h3 graf-after--figure graf--trailing graf--title'\
     or @class='graf graf--h3 graf--leading graf--title']")

# finding links via elements
blog_links = driver.find_elements(
    by='xpath', value='//div[@class="postArticle-readMore"]/a')

for (t, l) in zip(blog_titles, blog_links):
    blog_links_list.append(l.get_attribute('href'))
    blog_titles_list.append(t.text)

# for (t, l) in zip(blog_titles_list, blog_links_list):
#     print(t, ':', l)
# the above code is for reference

blog_pack = {'INFOSEC_BLOG_TITLE': blog_titles_list,
             'INFOSEC_BLOG_LINK': blog_links_list}

# converting dict to csv or other format what you want
data = pd.DataFrame(blog_pack)

# getting blog with date, for not confusing different blog.
now = time.strftime("%d-%b-%Y", time.gmtime(time.time()))

# storing file in system output path
file_name = f'infosecwriteups.com-blog-{now}.csv'
data.to_csv(file_name)
driver.quit()
