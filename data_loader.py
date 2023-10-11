import os
import uuid
import psycopg2
from minio import Minio

# Параметры подключения к PostgreSQL
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')

# Подключение к PostgreSQL
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = conn.cursor()

# Подключение к Minio
minio_client = Minio(
    endpoint=f"{os.getenv('MINIO_HOST')}:{os.getenv('MINIO_PORT')}",
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    secure=False
)

def load_hosts():
    cursor.execute("""
        INSERT INTO host (host_id, name, phone, email, contract_id)
        VALUES
           (1, 'Василий Иванов', '+7 123 456 7890', 'vasiliy@example.com', NULL),
           (2, 'Елена Петрова', '+7 987 654 3210', 'elena@example.com', NULL),
           (3, 'Александр Смирнов', '+7 456 789 0123', 'alexander@example.com', NULL),
           (4, 'Мария Кузнецова', '+7 321 654 0987', 'maria@example.com', NUll),
           (5, 'Иван Соколов', '+7 789 012 3456', 'ivan@example.com', NULL);
    """)
    conn.commit()


# Загрузка данных в таблицы
def load_accomodations():
    cursor.execute("""
    INSERT INTO accommodation (accommodation_id, host_id, name, address, price_category_id, rooms, accommodation_type_id)
    VALUES
       (1, 1, 'Уютный пансионат', 'Адрес коттеджа 1', 1, 3, 1),
       (2, 2, 'Комфортабельный санаторий', 'Адрес апартаментов 1', 2, 2, 2),
       (3, 3, 'Новая гостиница', 'Адрес гостевого дома 1', 3, 4, 3),
       (4, 4, 'VIP отель', 'Адрес виллы 1', 4, 5, 4),
       (5, 5, 'Гостевой дом с бассейном', 'Адрес отеля 1', 5, 3, 5);
    """)
    conn.commit()

def load_photos():
    bucket_name = "photos"
    for i in range(1,11):
        object_uuid = str(uuid.uuid4())
        photo_path = os.path.join("test_data", "photos", f"{i}.jpg")
        minio_client.fput_object(bucket_name, object_uuid, photo_path)
        cursor.execute(f"""
        INSERT INTO metadata (object_uuid, content_type, file_name, bucket_name)
        VALUES ('{object_uuid}', 'jpg', '{photo_path}', '{bucket_name}')
        """)
        conn.commit()
        cursor.execute(f"""
        INSERT INTO accommodation_photo (accommodation_id, object_uuid)
        VALUES ({(i+1) // 2}, '{object_uuid}')
        """)
        conn.commit()



if __name__ == "__main__":
    # Загрузка данных
    load_hosts()
    load_accomodations()
    load_photos()
