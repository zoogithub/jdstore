from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from sqlalchemy import create_engine



option=webdriver.ChromeOptions()
option.add_experimental_option("detach",True)
wd=webdriver.Chrome(options=option)
wd.implicitly_wait(5)
url='https://www.jd.com/'
wd.get(url)
ac=ActionChains(wd)
#先将一级列表长度列出来，然后依次将鼠标移到列表标题上
first_topic_length=len(wd.find_elements(By.XPATH,'//div[@class="mod_container"]//div[@class="grid_c1 fs_inner"]//div[@class="fs_col1"]//ul/li'))
i=1
topic3_id=1
preid = 0
topic2_id=first_topic_length+1
topic3_name_list=[]
topic3_preid_list=[]
id_list=[]
name_list=[]
pre_id_list=[]



print('running,please wait......')
while True:
    if i>first_topic_length:
        break
    # 预加载一级标题
    topic1s = wd.find_elements(By.XPATH,
                             '//div[@class="mod_container"]//div[@class="grid_c1 fs_inner"]//div[@class="fs_col1"]//ul/li[{}]/a'.format(i))
    topic_content=[]
    for topic1 in topic1s:
        topic_content.append(topic1.text)
    # 保存一级标题
    id_list.append(i)
    name_list.append('/'.join(topic_content))
    pre_id_list.append(preid)
    # 鼠标移动到标题上
    ac.move_to_element(
        wd.find_element(By.XPATH,"//div[@class='mod_container']//div[@class='grid_c1 fs_inner']//div[@class='fs_col1']//ul/li[{}]/a".format(i))
    ).perform()

    # 获取二三级标题
    topics23=wd.find_elements(By.XPATH,'//div[@class="mod_container"]//div[@class="grid_c1 fs_inner"]'
                                       '//div[@class="fs_col1"]//div[@id="cate_item{}"]/div[@class="cate_part_col1"]/div[@class="cate_detail"]/dl'.format(i))
    second_topic_length=len(topics23)
    for topics in topics23:
        # 异常处理:没有超链接的分类要单独列出
        if topic2_id==78 or topic2_id==153 or topic2_id==167:
            topic2=topics.find_element(By.XPATH,'./dt/span')
        else:
            topic2=topics.find_element(By.XPATH,'./dt/a')

        # 保存二级标题
        id_list.append(topic2_id)
        name_list.append(topic2.text)
        pre_id_list.append(i)

        topic3s=topics.find_elements(By.XPATH,'./dd/a')
        for topic3 in topic3s:
            topic3_name_list.append(topic3.text)
            topic3_preid_list.append(topic2_id)
        topic2_id += 1
    i += 1
wd.quit()

# topic3_number: 1752  topic1+2_number:197
# 保存3级标题
topic3_id+=len(id_list)

for i in range(len(topic3_name_list)):
    id_list.append(topic3_id)
    name_list.append(topic3_name_list[i])
    pre_id_list.append(topic3_preid_list[i])
    topic3_id+=1


data_dict={
    'id':id_list,
    'name':name_list,
    'preid':pre_id_list
}
df=pd.DataFrame(data_dict)
connection = create_engine(
        "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format('root', '123456', '127.0.0.1', '3306', 'test', 'utf8mb4'))
df.to_sql('jd',connection,if_exists='replace',index=False)
print('succeed')