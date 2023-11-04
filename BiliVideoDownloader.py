from tqdm import tqdm  
import requests  
import re  
import os  
import json  
import time
import random

requests.packages.urllib3.disable_warnings()
_usrname = os.getlogin()
print("  _     _ _         ____  _ _ _ _     _ _ _  __     ___     _              ____                      _                 _           ")
print(" | |   (_) |_ ___  | __ )(_) (_) |__ (_) (_) \ \   / (_) __| | ___  ___   |  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __ ")
print(" | |   | | __/ _ \ |  _ \| | | | '_ \| | | |  \ \ / /| |/ _` |/ _ \/ _ \  | | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|")
print(" | |___| | ||  __/ | |_) | | | | |_) | | | |   \ V / | | (_| |  __/ (_) | | |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   ")
print(" |_____|_|\__\___| |____/|_|_|_|_.__/|_|_|_|    \_/  |_|\__,_|\___|\___/  |____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   ")
print("Copyright 2023 Dogeliu","Version:2.1")

# 用户输入要获取的视频地址
_url = str(input("Please input video url: "))  
_headers = {  
    'referer': 'https://www.bilibili.com/',  
    "user-agent": "Chrome/80.0.3970.5"  
}

# 获取视频网页html并做一个假的进度条
_fake_progressbar = "bakabakabakabakabakabakabakabaka999999999"
for chunk in tqdm(_fake_progressbar):
    chunk = str(chunk) 
    _random_range = random.uniform(0.1,0.2) 
    time.sleep(_random_range)

_response = requests.get(url=_url, headers=_headers) #获取html源码，发送头文件防止被制裁

# 看看网页源代码?  
# print(_response.text)

# 提取html内需要的信息 
_title = re.findall('<h1 title="(.*?)"', _response.text)[0] # 提取视频标题 
_title = re.sub(r"[\/':()（）‘’、‘’*?<>|【】{} +-]", "", _title) # 如果标题里有[\/:*?<>|]特殊字符,直接删除   
print("The video title was:", _title)  
_html_data = re.findall("<script>window.__playinfo__=(.*?)</script>", _response.text)[0] # 找视频地址
_json_data = json.loads(_html_data)  
_json_dict = json.dumps(_json_data)  # 转换成json对象

# 提取视频画面和声音  
_video_url = _json_data["data"]["dash"]["video"][0]["baseUrl"]  
_audio_url = _json_data["data"]["dash"]["audio"][0]["baseUrl"]  
print("Successfully get video!")  
print("image url:", _video_url)  
print("audio url:", _audio_url) 

_video_content = requests.get(url=_video_url, headers=_headers).content  
_audio_content = requests.get(url=_audio_url, headers=_headers).content  

# 写入视频数据，大的要来了！
print("If you don't input something, video will save at C:/Users/Public/")  
_video_save_address = str(input("Please input the location where the downloaded video will be stored: "))  
if _video_save_address == "":  
    _video_save_address =  "C:/Users/",_usrname,"/Desktop/"
    _video_save_address = "".join(_video_save_address)  # 用join()函数连接每个元素
    str(_video_save_address)  
    with open(_video_save_address + _title + ".mp4", mode="wb") as f: # 创建mp4文件，写入数据 
        for chunk in tqdm(_video_content):  
            chunk = str(chunk)  
            chunk = chunk.encode()  
        f.write(_video_content)
    # 创建mp3文件，写入数据
    _video_save_address =  "C:/Users/",_usrname,"/Desktop/"
    _video_save_address = "".join(_video_save_address)  # 用join()函数连接每个元素
    str(_video_save_address)  
    with open(_video_save_address + _title + ".mp3", mode="wb") as f:  
        for chunk in tqdm(_audio_content):  
            chunk = str(chunk)  
            chunk = chunk.encode()  
        f.write(_audio_content)
else:  
    # 创建mp4文件，写入数据 
    with open(_video_save_address + "/" + _title + ".mp4", mode="wb") as f:  
        for chunk in tqdm(_video_content):  
            chunk = str(chunk)  
            chunk = chunk.encode()  
        f.write(_video_content)
    # 创建mp3文件，写入数据  
    with open(_video_save_address + "/" + _title + ".mp3", mode="wb") as f:  
        for chunk in tqdm(_audio_content):  
            chunk = str(chunk)
            chunk = chunk.encode()  
        f.write(_audio_content)

_command = "ffmpeg -i ",_video_save_address,_title,".mp4 -i ",_video_save_address,_title,".mp3 -c:v copy -c:v copy finalvideo.mp4"
print(_command)
_command = "".join(_command)  # 用join()函数连接每个元素
str(_command)
print(_command)
os.system(_command)
_video_mp4_file = _video_save_address,_title,".mp4"
_video_mp4_file = "".join(_video_mp4_file)
_video_mp3_file = _video_save_address,_title,".mp3"
_video_mp3_file = "".join(_video_mp3_file)
os.remove(_video_mp4_file) # 删除单有画面的mp4文件
os.remove(_video_mp3_file) # 删除单有画面的mp3文件
print("Video was successfully output at",_video_save_address)
# 完