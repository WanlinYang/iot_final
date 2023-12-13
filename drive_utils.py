from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

FOLDER_NAME = "437_IoT"

def get_folder_id(folder_name):
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for f in file_list:
        if f["title"] == FOLDER_NAME:
            folder_id = f["id"]
            return folder_id
    return None

def upload_image_to_drive(img_path, folder_id):
    filename = img_path.split("/")[-1]
    metadata = {
        "parents": [{"id": folder_id}],
        "title": filename,
        "mimeType": "image/png",
    }
    f = drive.CreateFile()
    f.SetContentFile(img_path)
    f.Upload()

def test_upload():
    folder_id = get_folder_id(FOLDER_NAME)
    print("folder_id", folder_id)
    upload_image_to_drive("/home/wanlin/Desktop/camera_images/test.png", folder_id)

if __name__ == "__main__":
    test_upload()
