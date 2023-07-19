from nonebot import get_driver
from nonebot.rule import to_me
from nonebot import on_command
from .config import Config
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent,Message, MessageSegment, MessageEvent
import requests
from bs4 import BeautifulSoup
from nonebot.rule import fullmatch

url = "https://kumamate.net/vip/" 
response = requests.get(url)
content = response.content.decode('utf-8') # 将网页内容解码为Unicode字符串

response = requests.get(url) # 发送GET请求

soup = BeautifulSoup(response.content, 'html.parser') # 解析HTML内容

# 找到包含整数的标签，并提取整数
common_score_str = soup.find('span', {'class': 'vipborder'}).text
common_score = str(common_score_str)

# 获取更新时间
soup = BeautifulSoup(content, 'html.parser')
paragraph = soup.find('p', {'class': 'data_hinto'})
time_str = paragraph.text.split(' ')[0] # 使用空格分割字符串，并提取第一个元素
new_time = time_str[55:]

vipexp_elements = soup.find_all(class_="vipexp")

# 选择第二个元素（索引为1）
second_vipexp_element = vipexp_elements[3]
for element in vipexp_elements:
    # 找到当前元素中的所有<br>标签
    br_tags = element.find_all('br')
    
    # 遍历每个<br>标签，将其替换为换行符
    for br_tag in br_tags:
        br_tag.replace_with("\n")

weather = on_command("斗vip", aliases={"任斗vip", "乱斗vip","斗vip分","任斗vip分","乱斗vip分","斗vip分数","任斗vip分数","乱斗vip分数"}, priority=10, block=True)


@weather.handle()
async def _():
    await weather.send("目前大乱斗VIP分数线为" + common_score +"分。")
    await weather.send("分数更新时间：" + new_time + "（日本时间）")
    await weather.send("民间段位：" + "\n" + second_vipexp_element.text) 


global_config = get_driver().config
config = Config.parse_obj(global_config)

