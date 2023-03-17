import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from sqlalchemy import create_engine
import os
wd=webdriver.Chrome()
ac=ActionChains(wd)
wd.implicitly_wait(5)
url='https://list.jd.com/list.html?cat=9987,653,655'
img_list=[]
p_name_list=[]
p_comment_list=[]
p_shop_list=[]
price_list=[]
id_list=[]

def save_as_file(name,result):
    file = os.getcwd() + "/resource/" + name + ".txt"
    output = open(file, 'a', encoding='utf-8')
    output.write(result)
    output.close()

i=1
print('running,please wait...')
wd.get(url)




def getdata():
    global i
    goods=wd.find_elements(By.XPATH,'//div[@id="J_goodsList"]/ul/li')
    for good in goods:
        id_list.append(i)
        i+=1
        p_name=good.find_element(By.XPATH,'.//div[@class="p-name p-name-type-3"]/a/em').text
        p_name_list.append(p_name)
        p_comment=good.find_element(By.XPATH,'.//div[@class="p-commit"]/strong/a').text
        p_comment_list.append(p_comment)
        try:
            price=good.find_element(By.XPATH, './/div[@class="p-price"]//i').text
        except:
            price=''
        price_list.append(price)
        # print(price)
        try:
            p_shop=good.find_element(By.XPATH,'.//div[@class="p-shop"]/span/a').text
        except:
            p_shop=''
        img = good.find_element(By.XPATH, './/div[@class="p-img"]/a/img').get_attribute('src')
        if img==None:
            img='https:'+good.find_element(By.XPATH, './/div[@class="p-img"]/a/img').get_attribute('data-lazy-img')
        p_shop_list.append(p_shop)
        img_list.append(img)
    # print(p_name)
    # print(p_comment)
    # print(img)
    # print(good.find_element(By.XPATH,'.//div[@class="p-img"]/a/img').get_attribute('outerHTML'))
    # print(p_shop)


js="var action=document.documentElement.scrollTop=10000"

while i<600:
    wd.execute_script(js)
    time.sleep(3)
    getdata()
    ac.click(wd.find_element(By.XPATH,'//a[@class="pn-next"]')).perform()



wd.close()
data_dict={
    'id':id_list,
    'name':p_name_list,
    'price':price_list,
    'shop':p_shop_list,
    'comment_num':p_comment_list,
    'pic':img_list
}
df=pd.DataFrame(data_dict)
connection = create_engine(
        "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format('root', '123456', '127.0.0.1', '3306', 'test', 'utf8mb4'))
df.to_sql('jd_spu',connection,if_exists='replace',index=False)
print('succeed')