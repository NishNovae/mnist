from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os
import pymysql.cursors
import json

app = FastAPI()


@app.post("/files/")
async def file_list():
    conn = pymysql.connect(
        host = '172.18.0.1', port = 53306,
        user = 'mnist', password = '1234',
        database = 'mnistdb',
        cursorclass=pymysql.cursors.DictCursor
    )

    with conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)

        return result

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[-1] # "image/png" > "png"

    upload_dir = os.getcwd() + "/photo/"
    os.makedirs(upload_dir, exist_ok = True)
    print(f"[INFO] Checked and/or created path: {upload_dir}")

    import uuid
    file_full_path = os.path.join(upload_dir, f'{uuid.uuid4()}.{file_ext}')

    with open(file_full_path, "wb") as f:
        f.write(img)
        print(f"[INFO] Successfully wrote file to: {file_full_path}")

# save file path DB INSERT
# tablename: image_processing
# column: num ( auto-incremented, initial insert )
# column: filename, filepath, req_time ( initial insert ), req_user (n00)
# column: pred_model, pred_result, pred_time ( to be updated )

    sql = "INSERT INTO image_processing(file_name, file_path, request_time, request_user) VALUES (%s, %s, %s, %s)"
    conn = pymysql.connect(
        host = '172.18.0.1', port = 53306, 
        user = 'mnist', password = '1234', 
        database = 'mnistdb', cursorclass=pymysql.cursors.DictCursor
    )

    import jigeum.seoul
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (
                file_name, file_full_path, jigeum.seoul.now(), 'n10'
                )
            )
            conn.commit()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_full_path": file_full_path
    }

@app.get("/all")
def all():
    from mnist.db import select
    sql = "SELECT * FROM image_processing"
    result = select(query=sql, size=-1)
    return result

@app.get("/one")
def one():
    from mnist.db import select
    sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num LIMIT 1"
    result = select(query=sql, size=1)
    return result[0]

@app.get("/many/")
def many(size: int = -1):
    from mnist.db import get_conn
    sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
    conn = get_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchmany(size)

    return result
