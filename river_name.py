from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# Đường dẫn tới chromedriver, hãy thay đổi theo máy bạn
CHROMEDRIVER_PATH = "D:\\Đề án 2\\chromedriver-win64\\chromedriver.exe"

# Tạo một driver Chrome
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Mở trang web
url = "https://quyhoachvietnam.com/ban-do-song-ngoi-viet-nam/"
driver.get(url)

# Đợi một chút để trang web tải đầy đủ
time.sleep(5)

# Tìm các phần tử chứa tên sông
try:
    # Thay đổi selector phù hợp nếu cấu trúc HTML thay đổi
    river_elements = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div/article/div/div/ul/li') 
    # Lấy danh sách tên sông
    rivers = [elem.text for elem in river_elements if elem.text.strip()]
#//*[@id="main-content"]/div[1]/article/div/div[2]/ul[2]/li[1]/text()
#//*[@id="main-content"]/div[1]/article/div/div[2]/ul[2]/li[5]/text()
#//*[@id="main-content"]/div[1]/article/div/div[2]/ul[3]/li[1]/text()
    # Đóng driver
    driver.quit()

    # Lưu vào file Excel
    df = pd.DataFrame(rivers, columns=["Tên Sông"])
    output_path = "D:\\Đề án 2\\ten_song_vietnam2.xlsx"
    df.to_excel(output_path, index=False)  # Loại bỏ 'encoding' ở đây
    print(f"File Excel đã được lưu tại {output_path}")

except Exception as e:
    print("Có lỗi xảy ra:", e)
    driver.quit()
