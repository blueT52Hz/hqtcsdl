import requests
import pandas as pd
import time
from openpyxl import Workbook

# Thông tin API
api_key = 'V4MKPXP9GVLC9WXVQZ3T5TZHE'  # Thay bằng API key của bạn từ Visual Crossing

# Đường dẫn file Excel đầu vào và file Excel đầu ra
input_file = 'D:\\Đề án 2\\data\\City_ID.xlsx'  # File đầu vào chứa tên tỉnh thành
output_file = 'D:\\Đề án 2\\data\\history2.xlsx'  # File đầu ra để lưu dữ liệu thời tiết

# Phạm vi thời gian cần lấy dữ liệu
start_date = '2024-11-01'
end_date = '2024-11-15'

# Đọc danh sách tỉnh thành từ file Excel
locations_df = pd.read_excel(input_file)
locations = locations_df['TP'].tolist()  # Đọc tên tỉnh thành từ cột "Tinh_thanh"

# Danh sách lưu kết quả
results = []

# Lặp qua từng tỉnh thành để lấy dữ liệu
for location in locations:
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&key={api_key}&contentType=json"

    # Gửi yêu cầu đến API và xử lý lỗi 429
    while True:
        response = requests.get(url)
        
        # Kiểm tra mã trạng thái phản hồi
        if response.status_code == 200:
            data = response.json()
            for day in data['days']:
                # Lấy thông tin cho từng ngày và xử lý dữ liệu thiếu
                row = {
                    'Location': location,
                    'datetime': day.get('datetime', ''),
                    'tempmax': day.get('tempmax', ''),
                    'tempmin': day.get('tempmin', ''),
                    'temp': day.get('temp', ''),
                    'feelslikemax': day.get('feelslikemax', ''),
                    'feelslikemin': day.get('feelslikemin', ''),
                    'feelslike': day.get('feelslike', ''),
                    'dew': day.get('dew', ''),
                    'humidity': day.get('humidity', ''),
                    'precip': day.get('precip', ''),
                    'precipprob': day.get('precipprob', ''),
                    'precipcover': day.get('precipcover', ''),
                    'preciptype': ', '.join(day.get('preciptype', [])) if day.get('preciptype') else '',
                    'snow': day.get('snow', ''),
                    'snowdepth': day.get('snowdepth', ''),
                    'windgust': day.get('windgust', ''),
                    'windspeed': day.get('windspeed', ''),
                    'winddir': day.get('winddir', ''),
                    'pressure': day.get('pressure', ''),
                    'cloudcover': day.get('cloudcover', ''),
                    'visibility': day.get('visibility', ''),
                    'solarradiation': day.get('solarradiation', ''),
                    'solarenergy': day.get('solarenergy', ''),
                    'uvindex': day.get('uvindex', ''),
                    'severerisk': day.get('severerisk', ''),
                    'sunrise': day.get('sunrise', ''),
                    'sunset': day.get('sunset', ''),
                    'moonphase': day.get('moonphase', ''),
                    'conditions': day.get('conditions', ''),
                    'description': day.get('description', ''),
                    'icon': day.get('icon', ''),
                    'stations': ', '.join(day.get('stations', [])) if day.get('stations') else '',
                    'source': day.get('source', ''),
                    'name': day.get('name', '')
                }
                # Thêm kết quả vào danh sách
                results.append(row)
            
            print(f"Dữ liệu thời tiết cho {location} đã được lưu.")
            break
        elif response.status_code == 429:
            # Tạm dừng nếu gặp lỗi 429 và thử lại sau
            print("Quá nhiều yêu cầu, tạm dừng 60 giây...")
            time.sleep(30)  # Tăng thời gian tạm dừng nếu gặp lỗi 429
            break
        elif response.status_code == 401:
            print(f"Lỗi 401: Không hợp lệ API key cho {location}. Vui lòng kiểm tra lại API key của bạn.")
            break
        else:
            print(f"Lỗi khi lấy dữ liệu cho {location}: {response.status_code}")
            break

    # Giới hạn số lượng yêu cầu để tránh vượt quá hạn mức API
    time.sleep(30)  # Nghỉ 10 giây giữa mỗi yêu cầu
    break
# Chuyển kết quả thành DataFrame
weather_df = pd.DataFrame(results)

# Xuất dữ liệu ra file Excel
weather_df.to_excel(output_file, index=False)
print(f"Dữ liệu đã được lưu vào {output_file}")
