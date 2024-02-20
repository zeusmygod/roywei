from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# 設置Chrome選項
options = Options()

# 創建webdriver實例
chrome = webdriver.Chrome(options=options)

# 網站的URL
url = "https://wroom.vision.com.tw/MainPage/SearchResult.aspx"

# 訪問網站
chrome.get(url)

area = input()
subject = input()
# 選擇城市
chrome.execute_script("document.getElementsByClassName('qry-city')[0].style.display = 'block'")
city = chrome.find_element(By.CLASS_NAME, 'qry-city')
select = Select(city)
select.select_by_visible_text('臺北市')

# 選擇區域
chrome.execute_script("document.getElementsByClassName('qry-area')[0].style.display = 'block'")
area_list = chrome.find_element(By.CLASS_NAME, 'qry-area')
select = Select(area_list)
select.select_by_visible_text(area)

# 選擇診所
chrome.execute_script("document.getElementsByClassName('qry-type')[0].style.display = 'block'")
clinic = chrome.find_element(By.CLASS_NAME, 'qry-type')
select = Select(clinic)
select.select_by_visible_text('診所')

# 選擇科別
chrome.execute_script("document.getElementsByClassName('qry-subj')[0].style.display = 'block'")
subject_list = chrome.find_element(By.CLASS_NAME, 'qry-subj')
select = Select(subject_list)
select.select_by_visible_text(subject)

# 點擊搜索按鈕
chrome.find_element(By.CLASS_NAME, 'ui-button-text').click()

# 等待搜索結果加載
# time.sleep(3)

page = 1
need_to_search = 10 #看你要找多少自己改
current = 0
all = []# 全部
while True:
    if current < need_to_search:
        # 11頁要重置
        if page > 10:
            page = 4

        # 獲取診所元素
        clinics = chrome.find_elements(By.XPATH, "//*[@title='候診訊息']")
        # 沒有候診
        if len(clinics) == 0:
            break

        # 遍歷診所元素
        for i in clinics:    
            if current > need_to_search:
                break

            # 創建新的webdriver實例
            newurl = i.get_attribute('href')
            newchrome = webdriver.Chrome(options=options)
            newchrome.get(newurl)

            
            information = []# 一間
            # 獲取診所信息
            head = newchrome.find_element(By.ID, 'dnn_ctr655_dnnTITLE_titleLabel')
            addr = newchrome.find_element(By.ID, 'dnn_ctr655_ViewVWWL_Clinics_mcsModuleCont_ctl00_lblCAddr')
            phone = newchrome.find_element(By.ID, 'dnn_ctr655_ViewVWWL_Clinics_mcsModuleCont_ctl00_lblCTel')
            service = newchrome.find_element(By.ID, 'dnn_ctr655_ViewVWWL_Clinics_mcsModuleCont_ctl00_lblServices')
            result = newchrome.find_elements(By.CLASS_NAME, 'clinic-room-info')

            if len(result):
                # print(head.text)
                # print(phone.text)
                # print(addr.text)
                # print(service.text)
                information.append(head.text)
                information.append(phone.text)
                information.append(addr.text)
                information.append(service.text)
                current += 1
            
            for j in result:
                if j.text:
                    # print(j.text)
                    information.append(j.text.split())
            if len(information) != 0:
                all.append(information)
            newchrome.close()

        page += 1
        # 翻頁
        chrome.find_element(By.XPATH, '//*[@id="dnn_ctr1089_ViewVNHI_Clinics_mcsModuleCont_ctl00_visClinicList_gvwClinicList"]/tbody/tr[11]/td/table/tbody/tr/td['+ str(page) +']/a').click()
    else:
        break

if len(all) == 0:
    print("")
else:
    print(all)
