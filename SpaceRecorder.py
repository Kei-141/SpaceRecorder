import os
import json
import requests
import time
import datetime
import schedule
import tweepy
import subprocess
import psutil
import pprint
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

# Twitter Options
AK = os.environ['AK']
AKS = os.environ['AKS']
AT = os.environ['AT']
ATS = os.environ['ATS']
tw_auth = tweepy.OAuthHandler(AK, AKS)
tw_auth.set_access_token(AT, ATS)
tw_api = tweepy.API(tw_auth)

bearer_token = os.environ['BT']
target_user = os.environ['target_id'] # Target User ID
search_url = "https://api.twitter.com/2/spaces/by/creator_ids"
params = {'user_ids'  : target_user}
headers = {"Authorization": "Bearer {}".format(bearer_token), "User-Agent": "v2SpacesLookupPython"}

def record_space(target_url):
    # Selenium Settings
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--autoplay-policy=no-user-gesture-required')
    driver = webdriver.Chrome(options=options)

    # Open Target URL
    wait = WebDriverWait(driver, 60)
    try:
        driver.get(target_url)
        join_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div[4]/div/div')))
        join_button.click()
    except:
        driver.quit()
        return

    # Record Sound
    print("Start recording...")
    p = subprocess.Popen(("rec", "record.mp3", "silence", "1", "0.5", "1%", "1", "5:00", "0.1%"))

    while True:
        poll = p.poll()
        print(poll)
        if poll != None:
            break
        time.sleep(10)

    p.terminate()
    driver.quit()
    try:
        p.wait(timeout=1)
    except subprocess.TimeoutExpired:
        p.kill()

    print("Record finished.")

    # Upload Data to Google Drive
    upload_drive()

def upload_drive():
    print("Start Uploading...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    gauth = GoogleAuth()
    gauth.CommandLineAuth()

    drive = GoogleDrive(gauth)

    f = drive.CreateFile()
    f['parents'] = [{'id': os.environ['folder_id']}]
    f.SetContentFile('/record.mp3')

    d_now = datetime.datetime.now()
    file_title = d_now.strftime('%Y-%m-%d-%H-%M-%S') + '.mp3'
    f['title'] = file_title
    f.Upload()
    print("Upload Finished.")
    file_id = f['id']
    file_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    tw_api.update_status(file_link)
    print("File Sharing Link Posted.")

def check_space():
    response = requests.request("GET", search_url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    json_response = response.json()

    try:
        space_id = json_response['data'][0]['id']
        space_state = json_response['data'][0]['state']
        if space_state == "live":
            target_url = f"https://twitter.com/i/spaces/{space_id}/peek"
            return target_url
        else:
            return None
    except:
        print('Space is NOT live.')
        return None

def main_job():
    print('Job Executing...')
    d_now = datetime.datetime.now()
    print(d_now.strftime('%Y-%m-%d %H:%M:%S'))
    target_url = check_space()
    if target_url != None:
        record_space(target_url)

def main():
    schedule.every(1).minutes.do(main_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()