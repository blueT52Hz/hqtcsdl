import requests
import pandas as pd
from google.cloud import storage
import os

# Đường dẫn tới file Excel chứa danh sách ID các thành phố
input_file = "D:\\Ð án 2\\Data-hien\\vi-tri.xlsx"  # Thay bằng đường dẫn file của bạn
output_file = "D:\\Đề án 2\\data\\now_wea.xlsx"  # Thay bằng đường dẫn file xuất
bucket_name = "thoitiet1"  # Thay bằng tên bucket của bạn
blob_name = "Data-hien/now_wea.xlsx"  # Đường dẫn tệp trong bucket

# Đọc file Excel chứa danh sách ID các thành phố
city_data = pd.read_excel(input_file)
city_ids = city_data['id']  # Giả sử file có cột 'id' chứa City ID

# Thay API key của bạn tại đây
API_KEY = "c743baf8f7f6eef4f8398aae4ce721ef"
API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Danh sách lưu kết quả
results = []

# Gọi API cho từng City ID và lưu dữ liệu
for city_id in city_ids:
    try:
        # Gửi request tới API
        response = requests.get(API_URL, params={"id": city_id, "appid": API_KEY})
        response.raise_for_status()  # Kiểm tra lỗi
        data = response.json()

        # Lấy tất cả thông tin cần thiết
        results.append({
            "id": data.get("id", ""),
            "name": data.get("name", ""),
            "country": data.get("sys", {}).get("country", ""),
            "coord_lon": data.get("coord", {}).get("lon", ""),
            "coord_lat": data.get("coord", {}).get("lat", ""),
            "weather_main": data.get("weather", [{}])[0].get("main", ""),
            "weather_description": data.get("weather", [{}])[0].get("description", ""),
            "weather_icon": data.get("weather", [{}])[0].get("icon", ""),
            "base": data.get("base", ""),
            "temp": data.get("main", {}).get("temp", ""),
            "feels_like": data.get("main", {}).get("feels_like", ""),
            "temp_min": data.get("main", {}).get("temp_min", ""),
            "temp_max": data.get("main", {}).get("temp_max", ""),
            "pressure": data.get("main", {}).get("pressure", ""),
            "humidity": data.get("main", {}).get("humidity", ""),
            "sea_level": data.get("main", {}).get("sea_level", ""),
            "grnd_level": data.get("main", {}).get("grnd_level", ""),
            "visibility": data.get("visibility", ""),
            "wind_speed": data.get("wind", {}).get("speed", ""),
            "wind_deg": data.get("wind", {}).get("deg", ""),
            "wind_gust": data.get("wind", {}).get("gust", ""),
            "clouds_all": data.get("clouds", {}).get("all", ""),
            "dt": data.get("dt", ""),
            "sys_sunrise": data.get("sys", {}).get("sunrise", ""),
            "sys_sunset": data.get("sys", {}).get("sunset", ""),
            "timezone": data.get("timezone", ""),
            "cod": data.get("cod", ""),
        })
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for city ID {city_id}: {e}")
    except KeyError as e:
        print(f"Missing data for city ID {city_id}: {e}")

# Chuyển kết quả thành DataFrame
output_data = pd.DataFrame(results)

# Xuất dữ liệu ra file Excel
output_data.to_excel(output_file, index=False)
print(f"Dữ liệu đã được lưu vào {output_file}")

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
    print(f"Error uploading to Cloud Storage: {e}")
