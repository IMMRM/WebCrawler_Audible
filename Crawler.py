#importing standard libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

#Target website
url="https://www.audible.in/adblbestsellers?ref_pageloadid=not_applicable&ref=a_hp_t1_navTop_pl1cg0c1r0&pf_rd_p=4e150d5e-ca98-47fb-823b-f6fcb252aced&pf_rd_r=VK4B52FHT6A4NAYGCB9S&pageLoadId=vZLQy1PiDQIGLqER&ref_plink=not_applicable&creativeId=2e6787a2-0cd0-4a6e-afe0-05766cd505e5"


#load driver
driver=webdriver.Chrome()
driver.get(url)

driver.implicitly_wait(10)



#pagination
pagination=driver.find_elements(by=By.XPATH,value="//div[@class='linkListWrapper']/span/ul")
page=pagination[0].find_elements(by=By.TAG_NAME,value='li')

page=pagination[0].find_elements(by=By.TAG_NAME,value="li")
last_page=int(page[-2].text)

currPage=1


title_name=[]
author_list=[]
ratings_got=[]
release_date=[]

while(currPage<=last_page):
    time.sleep(3)
    titles = driver.find_elements(by=By.XPATH, value="//h3")[1:]
    authors = driver.find_elements(by=By.XPATH, value="//li[contains(@class, 'authorLabel')]")

    ratings = driver.find_elements(by=By.XPATH, value="//li[contains(@class, 'rating')]")

    rating = ratings[0].find_elements(by=By.TAG_NAME, value='div')
    # print(rating[0].get_attribute("innerHTML"))
    releasedate=driver.find_elements(by=By.XPATH,value="//li[contains(@class,'releaseDateLabel')]")
    for title, author, rating, release in zip(titles, authors, ratings,releasedate):
            title_name.append(title.text)
            author_list.append(author.text.split(":")[1])
            try:
                ratingDiv = rating.find_element(by=By.TAG_NAME, value="div")
                ratingSpans = ratingDiv.find_elements(by=By.TAG_NAME, value="span")
                ratings_got.append(len(ratingSpans))
            except:
                ratings_got.append(" ")
            release_date.append(release.text.split(":")[1])
    next=driver.find_element(By.XPATH,"//span[contains(@class,'nextButton')]")
    currPage=currPage+1
    next.click()




    

driver.quit()

#Dumping the data
df=pd.DataFrame({"Title":title_name,"Author":author_list,"Ratings":ratings_got,"Release Date":release_date})
df.to_csv("Book_Details.csv",index=False)


