from tqdm import tqdm  
import requests  
import re  
import os  
import json  
import time
import random
  
requests.packages.urllib3.disable_warnings()
print("  _     _ _         ____  _ _ _ _     _ _ _  __     ___     _              ____                      _                 _           ")
print(" | |   (_) |_ ___  | __ )(_) (_) |__ (_) (_) \ \   / (_) __| | ___  ___   |  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __ ")
print(" | |   | | __/ _ \ |  _ \| | | | '_ \| | | |  \ \ / /| |/ _` |/ _ \/ _ \  | | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|")
print(" | |___| | ||  __/ | |_) | | | | |_) | | | |   \ V / | | (_| |  __/ (_) | | |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   ")
print(" |_____|_|\__\___| |____/|_|_|_|_.__/|_|_|_|    \_/  |_|\__,_|\___|\___/  |____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   ")
print("Copyright 2023 Dogeliu","Version:2.1")                                                                                                                                   

_url = str(input("Please input video url: "))  
_headers = {  
    'referer': 'https://www.bilibili.com/',  
    "user-agent": "Chrome/80.0.3970.5"  
}  
  
_fake_progressbar = "bakabakabakabaka999999999999999999999999bakabakabakabaka9999999999999999999"
for chunk in tqdm(_fake_progressbar):
    chunk = str(chunk) 
    _random_range = random.uniform(0.1,0.3) 
    time.sleep(_random_range)

_response = requests.get(url=_url, headers=_headers)

print(_response)  
  
# 看看网页源代码?  
# print(_response.text)  
  
# 提取视频标题  
_title = re.findall('<h1 title="(.*?)"', _response.text)[0]  
# 如果标题里有[\/:*?<>|]特殊字符,直接删除  
# _title = re.sub(r"[\/':*?<>|]", "", _title)  
print("The video title was:", _title)  
_html_data = re.findall("<script>window.__playinfo__=(.*?)</script>", _response.text)[0]  
_json_data = json.loads(_html_data)  
_json_dict = json.dumps(_json_data)  # 转换成json对象  
# print(_json_dict)  
# 写入文件，以后写一个历史记录功能  
if os.path.isfile("C:/Users/Public/Documents/saves.json"):  
    with open("C:/Users/Public/Documents/saves.json", "w", encoding="utf-8") as f:  
        json.dump(_json_dict, f)  
  
# 提取视频画面和声音  
_video_url = _json_data["data"]["dash"]["video"][0]["baseUrl"]  
_audio_url = _json_data["data"]["dash"]["audio"][0]["baseUrl"]  
print("Successfully get video!")  
print("image url:", _video_url)  
print("audio url:", _audio_url)  
  
# 使用tqdm显示下载进度  
_video_content = requests.get(url=_video_url, headers=_headers).content  
_audio_content = requests.get(url=_audio_url, headers=_headers).content  
  
print("If you don't input something, video will save at C:/Users/Public/")  
_video_save_address = str(input("Please input the location where the downloaded video will be stored: "))  
if _video_save_address == "":  
    # 创建mp4文件，写入二进制数据  
    with open("C:/Users/Public/" + _title + ".mp4", mode="wb") as f:  
        for chunk in tqdm(_video_content):  
            chunk = str(chunk)  
            chunk = chunk.encode()  
        f.write(_video_content) 
    # 创建mp3文件，写入二进制数据  
    with open("C:/Users/Public/" + _title + ".mp3", mode="wb") as f:  
        for chunk in tqdm(_audio_content):  
            chunk = str(chunk)  
            chunk = chunk.encode()  
        f.write(_audio_content)
else:  
    # 创建mp4文件，写入二进制数据  
    with open(_video_save_address + "/" + _title + ".mp4", mode="wb") as f:  
        for chunk in tqdm(_video_content):  
            chunk = str(chunk)  
            chunk = chunk.encode()  
        f.write(_video_content)
    # 创建mp3文件，写入二进制数据  
    with open(_video_save_address + "/" + _title + ".mp3", mode="wb") as f:  
        for chunk in tqdm(_audio_content):  
            chunk = str(chunk)
            chunk = chunk.encode()  
        f.write(_audio_content)