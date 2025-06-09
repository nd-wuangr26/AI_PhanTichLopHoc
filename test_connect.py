import mysql.connector
from mysql.connector import Error

# Thông tin kết nối MySQL
DB_CONFIG = {
    'host': '127.0.0.1',  # Địa chỉ máy chủ MySQL
    'user': 'root',  # Tên người dùng (thay đổi nếu cần)
    'password': '123',  # Mật khẩu (thay đổi)
    'database': 'class_db'  # Tên database
}


def test_mysql_connection():
    """
    Kiểm tra kết nối tới MySQL server
    """
    try:
        # Thử kết nối tới MySQL server
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Đã kết nối thành công tới MySQL Server phiên bản {db_info}")

            # Lấy thông tin database
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            database = cursor.fetchone()[0]
            print(f"Bạn đang kết nối với database: {database}")

            # Kiểm tra các bảng trong database
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("\nCác bảng hiện có trong database:")
            for table in tables:
                print(f"- {table[0]}")

                # Hiển thị cấu trúc của từng bảng
                cursor.execute(f"DESCRIBE {table[0]};")
                columns = cursor.fetchall()
                print("  Cấu trúc bảng:")
                for column in columns:
                    print(f"    {column[0]}: {column[1]}")

            # Thử thêm một bản ghi mẫu vào bảng detections
            test_insert_data(cursor, connection)

            # Đóng cursor và kết nối
            cursor.close()
            connection.close()
            print("Kết nối MySQL đã đóng")

    except Error as e:
        print(f"Lỗi khi kết nối tới MySQL: {e}")


def test_insert_data(cursor, connection):
    """
    Thử thêm một bản ghi vào bảng detections
    """
    try:
        # Kiểm tra xem bảng detections có tồn tại không
        cursor.execute("SHOW TABLES LIKE 'detections';")
        if cursor.fetchone():
            from datetime import datetime

            # Chuẩn bị dữ liệu mẫu
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            study_count = 5
            sleep_count = 2
            other_count = 3

            # Thực hiện thêm dữ liệu
            query = """
            INSERT INTO detections (timestamp, study_count, sleep_count, other_count) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (current_time, study_count, sleep_count, other_count))
            connection.commit()

            print(f"\nĐã thêm dữ liệu mẫu vào bảng detections với ID: {cursor.lastrowid}")

            # Truy vấn và hiển thị dữ liệu vừa thêm
            cursor.execute(f"SELECT * FROM detections WHERE id = {cursor.lastrowid}")
            record = cursor.fetchone()
            print("Dữ liệu vừa thêm:")
            print(f"ID: {record[0]}")
            print(f"Thời gian: {record[1]}")
            print(f"Study count: {record[2]}")
            print(f"Sleep count: {record[3]}")
            print(f"Other count: {record[4]}")
            if len(record) > 5:
                print(f"Created at: {record[5]}")
        else:
            print("\nBảng 'detections' không tồn tại. Vui lòng chạy script tạo bảng trước.")

    except Error as e:
        print(f"Lỗi khi thêm dữ liệu mẫu: {e}")


if __name__ == "__main__":
    print("Bắt đầu kiểm tra kết nối đến MySQL...")
    test_mysql_connection()