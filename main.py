import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import xml.etree.ElementTree as ET
import chromedriver_autoinstaller

# 실행마다 chromedriver.exe가 실행되고 브라우저를 끄더라도 쌓임. 자주 사용하는 환경에는 관련하여 코드를 수정하여 사용할 필요가 있음
# import파일 selenium, pyinstaller
# xml에서 루트를 가져옴. user태그를 찾음. 속성을 element에 할당
element = ET.parse('src/userInfo.xml').getroot().find('user').attrib

bizNo = element.get('biz-number') # 사업자번호 할당
password = element.get('password') # 비밀번호 할당


chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver.exe'

if os.path.exists(driver_path):
    print(f"chrom driver is installed: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver})")
    chromedriver_autoinstaller.install(True)

"""
웹드라이버 콘솔창 안띄우기
venv - lib - site-package - selenium - webdriver - common - service.py 파일열기
class service -> def start -> try -> self.process = subprocess.popen()
파라미터 중 creationflags=0x8000000 수정
"""
driver = webdriver.Chrome('src/chromedriver.exe') # 웹드라이버 연결
driver.get('https://www.zeropay.or.kr/UI_HP_005.act') # 로그인 화면으로 이동
driver.find_element(By.ID, 'iptBizNo').send_keys(bizNo) # 사업자 등록번호
driver.find_element(By.ID, 'iptPassWord').send_keys(password) # 비밀번호
driver.find_element(By.ID, 'btnLogin').click() # 로그인 버튼 클릭

time.sleep(1)
driver.get('https://www.zeropay.or.kr/UI_HP_002_03_01.act') # 결제정보 확인 화면으로 이동
driver.find_element(By.ID, 'inq_btn').click() # 조회 버튼 클릭
time.sleep(1)
driver.execute_script('window.scrollTo(0, 1000);') # 스크롤 이동

sys.exit()
