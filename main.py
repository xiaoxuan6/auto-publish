import json
import os
import random
import time

import dotenv
import requests
from playwright.sync_api import sync_playwright

if not os.path.exists('douyin_cookie.txt'):
    print('cookie 文件不存在！')
    exit(1)


def download_video(save_path):
    urls = (
        "https://api.shenke.love/api/gzl.php",
        "https://api.shenke.love/api/mnsp.php?msg=xjj&type=video",
        "https://api.yujn.cn/api/heisis.php",
        'https://api.yujn.cn/api/xjj.php',
        'https://api.yujn.cn/api/zzxjj.php',
        'https://api.yujn.cn/api/manzhan.php',
        'https://qtkj.love/api/ycyy.php',
        'https://qtkj.love/api/tmxl.php',
        'https://qtkj.love/api/slxl.php',
        'https://qtkj.love/api/ndym.php',
        'https://qtkj.love/api/llxl.php',
        'https://qtkj.love/api/kdbz.php',
        'https://qtkj.love/api/hbss.php',
        'https://qtkj.love/api/gjzs.php'
    )

    url = random.choice(urls)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"视频已成功保存到 {save_path}")
    else:
        print(f"请求失败，状态码: {response.status_code}")


dotenv.load_dotenv()
download_video('video.mp4')
if not os.path.exists('video.mp4'):
    print('文件 video.mp4 不存在！')
    exit(1)

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)

context = browser.new_context()
with open("douyin_cookie.txt") as f:
    context.add_cookies(json.loads(f.read()))

page1 = context.new_page()
page1.goto('https://www.douyin.com/?recommend=1')
time.sleep(10)

page2 = context.new_page()
page2.goto('https://creator.douyin.com/creator-micro/content/upload?enter_from=dou_web')
time.sleep(10)

page2.wait_for_selector('.box-s0--3Jb4Q')
pwd = os.getcwd()
page2.on("filechooser", lambda file_chooser: file_chooser.set_files(f"{pwd}/video.mp4"))

ele = page2.query_selector('.upload-btn--9eZLd')
ele.hover()
ele.click()
page2.wait_for_timeout(1000 * 30)

ele2 = page2.query_selector('//*[@id="root"]/div/div/div[2]/div[1]/div[13]/div[1]/div/div[2]/div/input')
ele2.hover()
ele2.click()

ele3 = page2.query_selector('//*[@id="root"]/div/div/div[2]/div[1]/div[15]/div/label[2]/input')
ele3.hover()
ele3.click()

page2.query_selector('//*[@id="root"]/div/div/div[2]/div[1]/div[17]/button[1]').click()
time.sleep(3)
print('发布成功！')

browser.close()
playwright.stop()
