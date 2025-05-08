from flask import Flask, render_template, Response
import cv2
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import time
from flask import jsonify
from collections import Counter
from my_model import load_model_and_predict

app = Flask(__name__)
camera = cv2.VideoCapture("test.mp4")


# Thông tin kết nối MySQL
DB_CONFIG = {
    'host': '127.0.0.1',  # Địa chỉ máy chủ MySQL
    'user': 'root',  # Tên người dùng (thay đổi nếu cần)
    'password': '123456',  # Mật khẩu (thay đổi)
    'database': 'class_db'  # Tên database
}

# Kết nối và trả về connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Lỗi khi kết nối MySQL: {e}")
    return None


# Hàm lưu dữ liệu vào database
def save_to_db(study_count, sleep_count, other_count):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            query = """
            INSERT INTO detections (timestamp, study_count, sleep_count, other_count) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (current_time, study_count, sleep_count, other_count))

            connection.commit()
            cursor.close()
            connection.close()
            print(f"Đã lưu dữ liệu tại {current_time}")
    except Error as e:
        print(f"Lỗi khi lưu vào database: {e}")


# Biến đếm và thời gian cho việc lưu dữ liệu
class DetectionCounter:
    def __init__(self):
        self.study_count = 0
        self.sleep_count = 0
        self.other_count = 0
        self.last_save_time = time.time()
        self.save_interval = 1  # Lưu dữ liệu mỗi 5 giây


counter = DetectionCounter()


# Hàm xử lý frame và dự đoán
def generate_frames():
    fps = camera.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps)  # số frame cần bỏ qua để đạt 1 FPS
    frame_count = 0

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame_count += 1
        if frame_count < frame_interval:
            continue  # bỏ qua frame, chưa đến 1s
        frame_count = 0  # reset đếm


        # Thực hiện inference
        labels = load_model_and_predict(frame)
        counts = Counter(labels)

        counter.study_count = counts.get("study", 0)
        counter.sleep_count = counts.get("sleep", 0)
        counter.other_count = counts.get("other", 0)

        # Lưu DB nếu đã đủ 5 giây
        current_time = time.time()
        if current_time - counter.last_save_time >= counter.save_interval:
            save_to_db(counter.study_count, counter.sleep_count, counter.other_count)
            counter.study_count = 0
            counter.sleep_count = 0
            counter.other_count = 0
            counter.last_save_time = current_time

        # Encode để hiển thị video
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def get_chart_data(condition_sql):
    conn = get_db_connection()
    if not conn:
        return {'labels': ['Lỗi kết nối'], 'counts': [1]}

    cursor = conn.cursor()
    query = f"""
        SELECT
            SUM(study_count),
            SUM(sleep_count),
            SUM(other_count)
        FROM detections
        WHERE {condition_sql};
    """
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    study, sleep, other = result
    total = (study or 0) + (sleep or 0) + (other or 0)

    if total == 0:
        return {'labels': ['Không có dữ liệu'], 'counts': [1]}

    return {
        'labels': ['Tập trung', 'Ngủ', 'Làm việc riêng'],
        'counts': [
            round((study or 0) / total * 100, 2),
            round((sleep or 0) / total * 100, 2),
            round((other or 0) / total * 100, 2)
        ]
    }

@app.route('/')
def index():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM detections ORDER BY id DESC")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('index.html', data=data)
    else:
        return "Lỗi kết nối database", 500


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stats')
def stats():
    # Trang hiển thị thống kê từ database
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM detections ORDER BY timestamp DESC LIMIT 50')
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(data)
    except Error as e:
        print(f"Lỗi khi truy vấn dữ liệu: {e}")
        return "Lỗi khi truy vấn cơ sở dữ liệu", 500


@app.route('/api/chart-day')
def chart_day():
    today = datetime.now().strftime('%Y-%m-%d')
    return jsonify(get_chart_data(f"DATE(timestamp) = '{today}'"))

@app.route('/api/chart-month')
def chart_month():
    year = datetime.now().year
    month = datetime.now().month
    return jsonify(get_chart_data(f"YEAR(timestamp) = {year} AND MONTH(timestamp) = {month}"))

@app.route('/api/chart-year')
def chart_year():
    year = datetime.now().year
    return jsonify(get_chart_data(f"YEAR(timestamp) = {year}"))

if __name__ == '__main__':
    app.run(debug=True)