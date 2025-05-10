import requests

# URL của API Nominatim với query tìm kiếm là "Da Nang, Vietnam"
url = "https://nominatim.openstreetmap.org/search?q=Da+Nang,+Vietnam&format=json"

# Đặt header User-Agent mặc định
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Gửi yêu cầu GET đến API với header User-Agent
response = requests.get(url, headers=headers)

# Kiểm tra nếu yêu cầu thành công
if response.status_code == 200:
    data = response.json()
    
    # Kiểm tra nếu có ít nhất một kết quả
    if data:
        lat = data[0].get('lat')
        lon = data[0].get('lon')
        if lat and lon:
            print(f"Latitude: {lat}, Longitude: {lon}")
        else:
            print("Không có tọa độ trong kết quả.")
    else:
        print("Không tìm thấy kết quả.")
else:
    print(f"Yêu cầu thất bại với mã lỗi: {response.status_code}")
