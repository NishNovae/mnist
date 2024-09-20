from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
# save file
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[-1] # "image/png"

    import os
    upload_dir = os.getcwd() + "/photo/"
    file_full_path = os.path.join(upload_dir, file_name)

    # creates directories, skips if exists
    os.makedirs(upload_dir, exist_ok = True)
    print(f"[INFO] Checked and/or created path: {upload_dir}")

    with open(file_full_path, "wb") as f:
        f.write(img)
        print(f"[INFO] Successfully wrote file to: {file_full_path}")

# save file path DB INSERT
# tablename: image_processing
# column: num ( auto-incremented, initial insert )
# column: filename, filepath, req_time ( initial insert ), req_user (n00)
# column: pred_model, pred_result, pred_time ( to be updated )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_full_path": file_full_path
    }

