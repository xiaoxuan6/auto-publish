import json
import os
import time

import dotenv
import requests
from playwright.sync_api import sync_playwright

if not os.path.exists('douyin_cookie.txt'):
    print('cookie 文件不存在！')
    exit(1)


def download_video(url, save_path):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"视频已成功保存到 {save_path}")
    else:
        print(f"请求失败，状态码: {response.status_code}")


dotenv.load_dotenv()
download_video(os.environ.get("VIDEO_URL"), 'video.mp4')

if not os.path.exists('video.mp4'):
    print('文件 video.mp4 不存在！')
    exit(1)

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=True)

context = browser.new_context()
with open("douyin_cookie.txt") as f:
    context.add_cookies(json.loads(f.read()))

page1 = context.new_page()
page1.goto('https://www.douyin.com/?recommend=1')
time.sleep(10)

page2 = context.new_page()
page2.goto('https://creator.douyin.com/creator-micro/content/upload?enter_from=dou_web')
time.sleep(15)

page2.wait_for_selector('.box-s0--3Jb4Q')
pwd = os.getcwd()
page2.on("filechooser", lambda file_chooser: file_chooser.set_files(f"{pwd}/video.mp4"))

ele = page2.query_selector('.upload-btn--9eZLd')
ele.hover()
ele.click()
page2.wait_for_timeout(1000 * 60)

content = page2.locator('.contentWrapper--2uqyj').text_content()
if content.startswith('检测通过'):
    # page2.fill('//*[@id="root"]/div/div/div[2]/div[1]/div[2]/div/div/div/div[1]/div/div/input', '测试')
    page2.query_selector('//*[@id="root"]/div/div/div[2]/div[1]/div[17]/button[1]').click()
    print('发布成功！')
else:
    print("视频未审核通过！")
    exit(1)

time.sleep(3)
browser.close()
playwright.stop()
