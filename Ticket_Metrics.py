import json
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from cryptography.fernet import Fernet

zendesk_user = '' 
zendesk_pwd =  b''
encrypt_key = b''

def get_ticket_metrics(ticket):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.get('https://totvssuporte.zendesk.com/api/v2/tickets/' + str(ticket) + '/metrics') 
    ticket_metrics = json.loads(driver.find_element_by_xpath("/html/body/pre").text)
    
    ticket_id = str(ticket_metrics['ticket_metric']['ticket_id'])
    replies = str(ticket_metrics['ticket_metric']['replies'])
    reopens = str(ticket_metrics['ticket_metric']['reopens'])
    assignee_updated_at = str(ticket_metrics['ticket_metric']['assignee_updated_at'])
    requester_updated_at = str(ticket_metrics['ticket_metric']['requester_updated_at'])
    reply_time_in_minutes = str(ticket_metrics['ticket_metric']['reply_time_in_minutes']['business'])
    first_resolution_time_in_minutes = str(ticket_metrics['ticket_metric']['first_resolution_time_in_minutes']['business'])
    full_resolution_time_in_minutes = str(ticket_metrics['ticket_metric']['full_resolution_time_in_minutes']['business'])
    requester_wait_time_in_minutes = str(ticket_metrics['ticket_metric']['requester_wait_time_in_minutes']['business'])
    latest_comment_added_at = str(ticket_metrics['ticket_metric']['latest_comment_added_at'])
    
    info = ticket_id + ',' +  replies  + ',' +  reopens  + ',' +  assignee_updated_at  + ',' + requester_updated_at + ',' + reply_time_in_minutes  + ',' +  first_resolution_time_in_minutes  + ',' +  full_resolution_time_in_minutes  + ',' +  requester_wait_time_in_minutes + ',' + latest_comment_added_at
    
    return info

options = webdriver.ChromeOptions();
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path="./files/driver/chromedriver.exe", options=options)
driver.get('https://totvssuporte.zendesk.com/agent/tickets/')
user_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/form/div[1]/div/input")))
user_box.click()
user_box.send_keys(zendesk_user)
pwd_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/form/div[2]/div/input")))
pwd_box.send_keys(Fernet(encrypt_key).decrypt(zendesk_pwd).decode() + Keys.ENTER)
time.sleep(10)

ticket_list = []

driver.get('https://totvssuporte.zendesk.com/api/v2/search/export?query=group:43377508+created>2020-12-01&page[size]=200&filter[type]=ticket')
#driver.get('https://totvssuporte.zendesk.com/api/v2/search/export?query=group:43377508&page[size]=100&filter[type]=ticket')
export_result = json.loads(driver.find_element_by_xpath("/html/body/pre").text)

for ticket in export_result["results"]:
    ticket_list.append(ticket["id"])

while export_result['meta']['has_more'] == True:
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.get(export_result['links']['next'])
    export_result = json.loads(driver.find_element_by_xpath("/html/body/pre").text)
    for ticket in export_result["results"]:
        ticket_list.append(ticket["id"])

text_file = open("./files/data/Ticket_Metrics.csv", 'w')
text_file.write('ticket_id,replies,reopens,assignee_updated_at,requester_updated_at,reply_time_in_minutes,first_resolution_time_in_minutes,full_resolution_time_in_minutes,requester_wait_time_in_minutes,latest_comment_added_at\n')
text_file.close()

for ticket in ticket_list:
    text_file = open("./files/data/Ticket_Metrics.csv", 'a')
    text_file.writelines(get_ticket_metrics(ticket) + '\n')
    text_file.close()

driver.quit()







