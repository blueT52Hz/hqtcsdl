import pandas as pd
from google.cloud import storage, bigquery
import datetime
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/content/dean2-442908-a629d330a67a.json"
# Thiết lập client cho GCS và BigQuery
gcs_client = storage.Client()
bq_client = bigquery.Client()

# Thông tin về bucket và file trên GCS
gcs_bucket_name = "thoitiet1"
hydropower_file = "Data/du_lieu_thuy_dien.xlsx"
weather_file = "Data/thoi_tiet_hien_tai.xlsx"
vitri_file="Data/vi-tri.xlsx"
song_file= "Data/ten_song_vietnam.xlsx"
loaithientai_file="Data/loai_thien_tai.xlsx"
lstt_file="Data/lich_su_thoi_tiet.xlsx"
khdieutiet_file="Data/ke_hoach_dieu_tiet_nuoc.xlsx"
dlthuydien_file="Data/du_lieu_thuy_dien.xlsx"
dlnuoc_file="Data/du_lieu_nuoc_tren_song.xlsx"
dlnuoc_file="Data/du_lieu_nuoc_tren_song.xlsx"
dieutietnuoc_file="Data/dieu_tiet_nuoc_thuy_dien.xlsx"
event_file="thoitiet1/Data/du_lieu_thien_tai.xlsx"
# Thông tin về bảng BigQuery
project_id = "dean2-442908"
dataset_id = "DataWareHouse"

# Schema cho bảng ViTri
vi_tri_table = "ViTri"
vi_tri_schema = [
    bigquery.SchemaField("Vi_tri_ID", "INTEGER"),
    bigquery.SchemaField("Ten_VT", "STRING"),
    bigquery.SchemaField("Vi_do", "FLOAT"),
    bigquery.SchemaField("Kinh_do", "FLOAT"),
]
# Schema cho bảng Song
song_table = "Song"
song_schema = [
    bigquery.SchemaField("Song_ID", "INTEGER"),
    bigquery.SchemaField("Ten_Song", "STRING"),
]

# Schema cho bảng LoaiThienTai
loai_thien_tai_table = "LoaiThienTai"
loai_thien_tai_schema = [
    bigquery.SchemaField("Loai_thien_tai_ID", "STRING"),
    bigquery.SchemaField("Ten_loai_tt", "STRING"),
]

# Bảng và schema cho dữ liệu thủy điện
hydropower_table = "TramThuyDien"
hydropower_schema = [
    bigquery.SchemaField("Tram_thuy_dien_ID", "STRING"),
    bigquery.SchemaField("Ten_tram", "STRING"),
    bigquery.SchemaField("Ten_VT", "INTEGER"),
]

# Bảng và schema cho dữ liệu thời tiết
weather_table = "ThoiTietHienTai"
weather_schema = [
    bigquery.SchemaField("Thoi_tiet_ID", "INTEGER"),
    bigquery.SchemaField("Vi_tri_ID", "INTEGER"),
    bigquery.SchemaField("Ngay_ghi", "DATETIME"),
    bigquery.SchemaField("Nhiet_do", "FLOAT"),
    bigquery.SchemaField("Nhiet_do_cao_nhat", "FLOAT"),
    bigquery.SchemaField("Nhiet_do_thap_nhat", "FLOAT"),
    bigquery.SchemaField("Do_am", "FLOAT"),
    bigquery.SchemaField("Toc_do_gio", "FLOAT"),
    bigquery.SchemaField("Ap_suat", "FLOAT"),
    bigquery.SchemaField("Tam_nhin_xa", "FLOAT"),
]

# Schema cho bảng lich_su_thoi_tiet
weather_history_table = "LS_ThoiTiet"
weather_history_schema = [
    bigquery.SchemaField("LS_thoi_tiet_ID", "INTEGER"),
    bigquery.SchemaField("Vi_tri_ID", "INTEGER"),
    bigquery.SchemaField("Ngay_ghi", "DATETIME"),
    bigquery.SchemaField("Nhiet_do", "FLOAT"),
    bigquery.SchemaField("Nhiet_do_cao_nhat", "FLOAT"),
    bigquery.SchemaField("Nhiet_do_thap_nhat", "FLOAT"),
    bigquery.SchemaField("Do_am", "FLOAT"),
    bigquery.SchemaField("Toc_do_gio", "FLOAT"),
    bigquery.SchemaField("Ap_suat", "FLOAT"),
    bigquery.SchemaField("Tam_nhin_xa", "FLOAT"),
]

# Schema cho bảng ke_hoach_dieu_tiet_nuoc
water_regulation_plan_table = "KeHoachDieuTietNuoc"
water_regulation_plan_schema = [
    bigquery.SchemaField("KH_dieu_tiet_ID", "STRING"),
    bigquery.SchemaField("Song_ID", "INTEGER"),
    bigquery.SchemaField("Ngay_bd_kh", "DATE"),
    bigquery.SchemaField("Ngay_kt_kh", "DATE"),
    bigquery.SchemaField("Muc_tieu_nuoc_vao", "FLOAT"),
    bigquery.SchemaField("Muc_tieu_luong_xa", "FLOAT"),
    bigquery.SchemaField("Muc_tieu_muc_nuoc_ho", "FLOAT"),
    bigquery.SchemaField("San_luong_dien_can_dat", "FLOAT"),
    bigquery.SchemaField("Muc_tieu_ngan_ngua_lu", "FLOAT"),
    bigquery.SchemaField("KH_xu_ly_khan_cap", "STRING"),
    bigquery.SchemaField("Ngay_ban_hanh", "DATE"),
]

# Schema cho bảng du_lieu_thuy_dien
hydropower_data_table = "DuLieuThuyDien"
hydropower_data_schema = [
    bigquery.SchemaField("Ma_do_ID", "STRING"),
    bigquery.SchemaField("Tram_thuy_dien_ID", "STRING"),
    bigquery.SchemaField("Thoi_gian_hoat_dong", "DATE"),
    bigquery.SchemaField("San_luong_dien", "FLOAT"),
    bigquery.SchemaField("Cong_suat_phat_dien", "FLOAT"),
]

# Schema cho bảng du_lieu_nuoc_tren_song
river_flow_data_table = "DuLieuNuocTrenSong"
river_flow_data_schema = [
    bigquery.SchemaField("Song_ID", "INTEGER"),
    bigquery.SchemaField("Vi_tri_ID", "INTEGER"),
    bigquery.SchemaField("Toc_do_dong", "FLOAT"),
    bigquery.SchemaField("Ngay_do", "DATE"),
    bigquery.SchemaField("Muc_Nuoc", "FLOAT"),
]

# Schema cho bảng DieuTietNuocThuyDien
water_management_table = "DieuTietNuocThuyDien"
water_management_schema = [
    bigquery.SchemaField("Ma_dieu_tiet", "STRING"),
    bigquery.SchemaField("Tram_thuy_dien_ID", "STRING"),
    bigquery.SchemaField("Muc_nuoc_ho_chua", "FLOAT"),
    bigquery.SchemaField("Luong_nuoc_vao", "FLOAT"),
    bigquery.SchemaField("Luong_nuoc_ra", "FLOAT"),
    bigquery.SchemaField("Nuoc_qua_tuabin", "FLOAT"),
    bigquery.SchemaField("Luong_nuoc_xa_qua_dap_tran", "FLOAT"),
    bigquery.SchemaField("Dung_tich_ho", "FLOAT"),
    bigquery.SchemaField("Dung_tich_ho_hien_tai", "FLOAT"),
    bigquery.SchemaField("Luong_nuoc_xa_khan", "FLOAT"),
    bigquery.SchemaField("Trang_thai_dap", "STRING"),
    bigquery.SchemaField("DB_luong_nuoc_vao", "FLOAT"),
    bigquery.SchemaField("DB_luong_nuoc_xa", "FLOAT"),
    bigquery.SchemaField("Song_ID", "INTEGER"),
]

# Schema cho bảng SuKien
disaster_event_table = "SuKien"
disaster_event_schema = [
    bigquery.SchemaField("Thien_tai_ID", "STRING"),
    bigquery.SchemaField("Loai_thien_tai_ID", "STRING"),
    bigquery.SchemaField("Ngay_BD", "DATE"),
    bigquery.SchemaField("Ngay_KT", "DATE"),
    bigquery.SchemaField("Vi_do", "FLOAT"),
    bigquery.SchemaField("Kinh_do", "FLOAT"),
    bigquery.SchemaField("Nguoi_chet_va_mat_tich", "INTEGER"),
    bigquery.SchemaField("Thiet_hai_kt", "INTEGER"),
    bigquery.SchemaField("Muc_do", "STRING"),
    bigquery.SchemaField("Vi_tri_ID", "INTEGER"),
]

# Tải dữ liệu từ GCS và xử lý tệp Excel
def process_and_upload_to_bq(file_name, table_name, schema, transform_func):
    # Tải file từ GCS

    bucket = gcs_client.bucket(gcs_bucket_name)
    blob = bucket.blob(file_name)
    local_file_path = f"/content/{os.path.basename(file_name)}"
    blob.download_to_filename(local_file_path)
    print(f"Tệp {file_name} đã được tải xuống.")

    # Đọc file Excel vào DataFrame
    df = pd.read_excel(local_file_path)

    # Chuyển đổi dữ liệu theo yêu cầu
    transformed_df = transform_func(df)

    # Tải dữ liệu lên BigQuery
    table_ref = f"{project_id}.{dataset_id}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_TRUNCATE",  # Ghi đè dữ liệu nếu bảng đã tồn tại
    )
    job = bq_client.load_table_from_dataframe(transformed_df, table_ref, job_config=job_config)
    job.result()
    print(f"Dữ liệu đã được tải lên BigQuery: {table_ref}")

# Hàm xử lý dữ liệu thủy điện
def transform_hydropower_data(df):
    return pd.DataFrame({
        "Tram_thuy_dien_ID": df["ID"].astype(str),
        "Ten_tram": df["Tên thủy điện"].astype(str),
        "Ten_VT": df["Vị trí hành chính"].astype(int),
    })
# Hàm xử lý dữ liệu ViTri
def transform_vi_tri_data(df):
    return pd.DataFrame({
        "Vi_tri_ID": df["id"].astype(int),
        "Ten_VT": df["name"].astype(str),
        "Vi_do": df["latitude"].astype(float),
        "Kinh_do": df["longitude"].astype(float),
    })
# Hàm xử lý dữ liệu Song
def transform_song_data(df):
    return pd.DataFrame({
        "Song_ID": df["Mã Sông"].astype(int),
        "Ten_Song": df["Tên Sông"].astype(str),
    })

# Hàm xử lý dữ liệu LoaiThienTai
def transform_loai_thien_tai_data(df):
    return pd.DataFrame({
        "Loai_thien_tai_ID": df["Mã Thiên tai "].astype(str),
        "Ten_loai_tt": df["Loại hình thiên tai"].astype(str),
    })
# Hàm xử lý dữ liệu thời tiết
def transform_weather_data(df):
    return pd.DataFrame({
        "Thoi_tiet_ID": df["id"].astype(int),
        "Vi_tri_ID": df["id_tp"].astype(int),
        "Ngay_ghi": pd.to_datetime(df["dt"], unit='s'),
        "Nhiet_do": df["temp"].astype(float) - 273.15,  # Chuyển từ Kelvin sang Celsius
        "Nhiet_do_cao_nhat": df["temp_max"].astype(float) - 273.15,
        "Nhiet_do_thap_nhat": df["temp_min"].astype(float) - 273.15,
        "Do_am": df["humidity"].astype(float),
        "Toc_do_gio": df["wind_speed"].astype(float),
        "Ap_suat": df["pressure"].astype(float),
        "Tam_nhin_xa": df["visibility"].astype(float),
    })
# Hàm xử lý dữ liệu lịch sử thời tiết
def transform_weather_history_data(df):
    return pd.DataFrame({
        "LS_thoi_tiet_ID": df["History_ID"].astype(int),
        "Vi_tri_ID": df["Location_ID"].astype(int),
        "Ngay_ghi": pd.to_datetime(df["datetime"]),
        "Nhiet_do": df["temp"].astype(float),
        "Nhiet_do_cao_nhat": df["tempmax"].astype(float),
        "Nhiet_do_thap_nhat": df["tempmin"].astype(float),
        "Do_am": df["humidity"].astype(float),
        "Toc_do_gio": df["windspeed"].astype(float),
        "Ap_suat": df["pressure"].astype(float),
        "Tam_nhin_xa": df["visibility"].astype(float),
    })

# Hàm xử lý dữ liệu kế hoạch điều tiết nước
def transform_water_regulation_plan_data(df):
    try:
        return pd.DataFrame({
            "KH_dieu_tiet_ID": df["Ma dinh danh cua ke hoach dieu tiet nuoc"].astype(str),
            "Song_ID": df["Ma Song"].astype(int),
            "Ngay_bd_kh": pd.to_datetime(df["Ngay bat dau thuc hien ke hoach dieu tiet"], errors='coerce').dt.date,
            "Ngay_kt_kh": pd.to_datetime(df["Ngay ket thuc du kien cua ke hoach dieu tiet"], errors='coerce').dt.date,
            "Muc_tieu_nuoc_vao": df["Muc tieu luong nuoc vao (m3/s)"].astype(float),
            "Muc_tieu_luong_xa": df["Muc tieu luong nuoc xa ra (m3/s)"].astype(float),
            "Muc_tieu_muc_nuoc_ho": df["Muc tieu muc nuoc cua ho chua (met)"].astype(float),
            "San_luong_dien_can_dat": df["Muc tieu san luong dien can dat (MW)"].astype(float),
            "Muc_tieu_ngan_ngua_lu": df["Muc tieu ngan ngua lu lut"].astype(float),
            "KH_xu_ly_khan_cap": df["Ke hoach xu ly tinh huong khan cap trong dieu tiet nuoc"].astype(str),
            "Ngay_ban_hanh": pd.to_datetime(df["Ngay dua ra ke hoach"], errors='coerce').dt.date,
        })
    except Exception as e:
        print("Lỗi trong quá trình chuyển đổi dữ liệu:", e)
        raise

# Hàm xử lý dữ liệu du_lieu_thuy_dien
def transform_hydropower_data(df):
    try:
        return pd.DataFrame({
            "Ma_do_ID": df["Mã đo"].astype(str),
            "Tram_thuy_dien_ID": df["ID"].astype(str),
            "Thoi_gian_hoat_dong": pd.to_datetime(df["Năm\nhoạt\nđộng"], errors='coerce').dt.date,
            "San_luong_dien": pd.to_numeric(df["Sản lượng\n(triệu KWh\n/năm)"], errors='coerce').astype(float),
            "Cong_suat_phat_dien": pd.to_numeric(df["Công suất\nPLM\n(MW)"], errors='coerce').astype(float),
        })
    except Exception as e:
        print("Lỗi trong quá trình chuyển đổi dữ liệu thủy điện:", e)
        raise

# Hàm xử lý dữ liệu du_lieu_nuoc_tren_song
def transform_river_flow_data(df):
    try:
        return pd.DataFrame({
            "Song_ID": df["River_ID"].astype(int),
            "Vi_tri_ID": df["Location_ID"].astype(int),
            "Toc_do_dong": df["Flow_Rate"].astype(float),
            "Ngay_do": pd.to_datetime(df["Measurement_Date"], errors='coerce').dt.date,
            "Muc_Nuoc": df["Water_Level"].astype(float),
        })
    except Exception as e:
        print("Lỗi trong quá trình chuyển đổi dữ liệu nước trên sông:", e)
        raise

def transform_water_management_data(df):
    try:
        return pd.DataFrame({
            "Ma_dieu_tiet": df["Mã định danh hồ nước"].astype(str),
            "Tram_thuy_dien_ID": df["Mã thủy điện"].astype(str),
            "Muc_nuoc_ho_chua": df["Mực nước tại hồ chứa (m)"].astype(float),
            "Luong_nuoc_vao": df["Lượng nước vào hồ (m³/s)"].astype(float),
            "Luong_nuoc_ra": df["Lượng nước ra hồ (m³/s)"].astype(float),
            "Nuoc_qua_tuabin": df["Lượng nước qua tua-bin (m³/s)"].astype(float),
            "Luong_nuoc_xa_qua_dap_tran": df["Lượng nước xả qua đập tràn (m³/s)"].astype(float),
            "Dung_tich_ho": df["Dung tích hồ chứa (m³)"].astype(float),
            "Dung_tich_ho_hien_tai": df["Dung tích hiện tại của hồ (m³)"].astype(float),
            "Luong_nuoc_xa_khan": df["Lượng nước xả khẩn cấp (m³/s)"].astype(float),
            "Trang_thai_dap": df["Trạng thái an toàn của đập"].astype(str),
            "DB_luong_nuoc_vao": df["Dự báo lượng nước vào (m³/s)"].astype(float),
            "DB_luong_nuoc_xa": df["Dự báo lượng nước ra (m³/s)"].astype(float),
            "Song_ID": df["Mã Sông"].astype(int),
        })
    except Exception as e:
        print("Lỗi trong quá trình chuyển đổi dữ liệu:", e)
        raise

# Hàm chuyển đổi dữ liệu cho bảng du_lieu_thien_tai
def transform_disaster_data(df):
    try:
        return pd.DataFrame({
            "Thien_tai_ID": df["Mã thiên tai"].astype(str),
            "Loai_thien_tai_ID": df["Mã Loại Thiên Tai"].astype(str),
            "Ngay_BD": pd.to_datetime(df["Thời gian bắt đầu"], errors='coerce').dt.date,
            "Ngay_KT": pd.to_datetime(df["Thời gian kết thúc"], errors='coerce').dt.date,
            "Vi_do": df["Vĩ độ"].astype(float),
            "Kinh_do": df["Kinh độ"].astype(float),
            "Nguoi_chet_va_mat_tich": df["Người chết và mất tích"].astype(int),
            "Thiet_hai_kt": df["Tổng thiệt hại (tỷ đồng)"].astype(int),
            "Muc_do": df["Mức độ nghiêm trọng"].astype(str),
            "Vi_tri_ID": df["Địa điểm xảy ra"].astype(int),
        })
    except Exception as e:
        print("Lỗi trong quá trình chuyển đổi dữ liệu:", e)
        raise

# Xử lý và tải dữ liệu vitri lên BigQuery
process_and_upload_to_bq(vitri_file, vi_tri_table, vi_tri_schema, transform_vi_tri_data)
# Xử lý và tải dữ liệu Song lên BigQuery
process_and_upload_to_bq(song_file, song_table, song_schema, transform_song_data)

# Xử lý và tải dữ liệu LoaiThienTai lên BigQuery
process_and_upload_to_bq(loaithientai_file, loai_thien_tai_table, loai_thien_tai_schema, transform_loai_thien_tai_data)

# Xử lý và tải dữ liệu thủy điện lên BigQuery
process_and_upload_to_bq(hydropower_file, hydropower_table, hydropower_schema, transform_hydropower_data)

# Xử lý và tải dữ liệu thời tiết lên BigQuery
process_and_upload_to_bq(weather_file, weather_table, weather_schema, transform_weather_data)

# Xử lý và tải dữ liệu lịch sử thời tiết lên BigQuery
process_and_upload_to_bq(lstt_file, weather_history_table, weather_history_schema, transform_weather_history_data)

# Xử lý và tải dữ liệu kế hoạch điều tiết nước lên BigQuery
process_and_upload_to_bq(khdieutiet_file, water_regulation_plan_table, water_regulation_plan_schema, transform_water_regulation_plan_data)

# Xử lý và tải dữ liệu thủy điện lên BigQuery
process_and_upload_to_bq(dlthuydien_file, hydropower_data_table, hydropower_data_schema, transform_hydropower_data)

# Xử lý và tải dữ liệu nước trên sông lên BigQuery
process_and_upload_to_bq(dlnuoc_file, river_flow_data_table, river_flow_data_schema, transform_river_flow_data)

# Chạy quy trình xử lý và tải dữ liệu
process_and_upload_to_bq(dieutietnuoc_file, water_management_table, water_management_schema, transform_water_management_data)

# Chạy quy trình xử lý và tải dữ liệu
process_and_upload_to_bq(event_file, disaster_event_table, disaster_event_schema, transform_disaster_data)