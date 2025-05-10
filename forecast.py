import pandas as pd
import requests
from google.cloud import storage
import os

# Đường dẫn tới file Excel chứa danh sách ID các thành phố
input_file = "D:\\Ð án 2\\Data-hien\\vi-tri.xlsx"  # Đường dẫn tới file chứa ID thành phố
output_file = "D:\\Đề án 2\\data\\du_doan.xlsx"  # Đường dẫn xuất dữ liệu ra file Excel
bucket_name = "thoitiet1"  # Thay bằng tên bucket của bạn
blob_name = "Data-hien/forecast.xlsx"  # Đường dẫn tệp trong bucket

# Đọc file Excel chứa danh sách ID các thành phố
df = pd.read_excel(input_file)

# Thay API key của bạn tại đây
API_KEY = "c743baf8f7f6eef4f8398aae4ce721ef"
API_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Hàm lấy dữ liệu thời tiết từ API cho mỗi thành phố
def get_weather_data(city_id):
    try:
        # Gửi yêu cầu API với các tham số đã chỉ định
        response = requests.get(API_URL, params={"id": city_id, "appid": API_KEY})
        response.raise_for_status()  # Kiểm tra lỗi
        weather_data = response.json()

        # Danh sách chứa các dự báo thời tiết trong 5 ngày
        forecasts = weather_data['list']
        weather_info_list = []

        # Trích xuất thông tin từ từng dự báo
        for forecast in forecasts:
            weather_info = {
                'city_id': city_id,  # ID thành phố
                'date': forecast['dt_txt'],  # Ngày và giờ dự báo
                'temp': forecast['main']['temp'],  # Nhiệt độ hiện tại (°C)
                'feels_like': forecast['main']['feels_like'],  # Nhiệt độ cảm nhận (°C)
                'temp_min': forecast['main']['temp_min'],  # Nhiệt độ tối thiểu (°C)
                'temp_max': forecast['main']['temp_max'],  # Nhiệt độ tối đa (°C)
                'pressure': forecast['main']['pressure'],  # Áp suất không khí (hPa)
                'humidity': forecast['main']['humidity'],  # Độ ẩm (%)
                'clouds': forecast['clouds']['all'],  # Tỷ lệ mây (%)
                'wind_speed': forecast['wind']['speed'],  # Tốc độ gió (m/s)
                'wind_deg': forecast['wind']['deg'],  # Hướng gió (độ)
                'wind_gust': forecast['wind'].get('gust', 'N/A'),  # Gió giật (m/s)
                'visibility': forecast.get('visibility', 'N/A'),  # Tầm nhìn (m)
                'weather_id': forecast['weather'][0]['id'],  # ID thời tiết
                'weather_main': forecast['weather'][0]['main'],  # Loại thời tiết
                'weather_description': forecast['weather'][0]['description'],  # Mô tả thời tiết
                'weather_icon': forecast['weather'][0]['icon'],  # Icon thời tiết
            }
            weather_info_list.append(weather_info)
        return weather_info_list
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi lấy dữ liệu cho thành phố ID {city_id}: {e}")
        return []

# Lưu trữ tất cả dữ liệu thời tiết
weather_data_list = []

# Lặp qua từng thành phố trong file Excel và lấy dữ liệu thời tiết
for city_id in df['id']:  # Giả sử cột chứa ID thành phố là 'id'
    weather_data = get_weather_data(city_id)
    weather_data_list.extend(weather_data)

# Tạo DataFrame từ dữ liệu thời tiết
weather_df = pd.DataFrame(weather_data_list)

# Xuất kết quả ra file Excel mới
weather_df.to_excel(output_file, index=False)
print(f"Đã xuất dữ liệu ra file: {output_file}")

# Kết nối Google Cloud Storage và tải file lên bucket
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'D:\Đề án 2\data\dean2-442908-652748bc53d2.json'  # Thay bằng đường dẫn tệp JSON key của bạn
client = storage.Client()

try:
    # Truy cập bucket
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Tải tệp lên bucket
    blob.upload_from_filename(output_file)
    print(f"Dữ liệu đã được tải lên Google Cloud Storage: gs://{bucket_name}/{blob_name}")
except Exception as e:
    print(f"Lỗi khi tải lên Google Cloud Storage: {e}")
