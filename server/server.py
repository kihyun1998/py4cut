"""
** 실행방법은
uvicorn ./server.py:app --reload

** ngrok 활성화 해야 public으로 작동한다.
ngrok http 8000

"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import os
import qrcode
import io

app = FastAPI()

# 'video' 및 'image' 폴더에 대한 경로 설정
video_folder = '../video'
image_folder = '../image'

@app.get("/videos/")
async def get_videos_list():
    # 모든 비디오 폴더 목록을 반환
    folders = os.listdir(video_folder)
    videos = [os.path.join(folder, "video.avi") for folder in folders if os.path.exists(os.path.join(video_folder, folder, "video.avi"))]
    return {"videos": videos}

"""
video 다운로드 API
"""
@app.get("/videos/{video_index}")
async def download_video(video_index: int):
    # 해당 인덱스의 타깃 비디오 경로를 찾음
    target_video_path = os.path.join(video_folder, str(video_index), f"video_{video_index}.avi")
    
    if os.path.exists(target_video_path):
        return FileResponse(target_video_path, media_type='application/octet-stream', filename=f"video_{video_index}.avi")
    else:
        raise HTTPException(status_code=404, detail="Video not found")

"""
이미지 다운로드 API
"""
@app.get("/images/{image_index}")
async def download_image(image_index: int):
    # 이미지 파일 경로를 생성
    image_file = f"image_{image_index}.jpg"
    target_image_path = os.path.join(image_folder, str(image_index), image_file)
    
    if os.path.exists(target_image_path):
        return FileResponse(target_image_path, media_type='image/jpeg', filename=image_file)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
"""
QR코드 생성 API
"""
@app.get("/qr/{video_index}")
async def get_video_qr(video_index: str):
    # 여기에서는 로컬 호스트와 포트를 사용했지만, 
    # 실제 배포 환경에 맞는 호스트 주소와 포트로 변경해야 합니다.
    video_url = f"https://68c3-118-37-47-3.ngrok-free.app/videos/{video_index}"
    qr_img = qrcode.make(video_url)
    img_bytes = io.BytesIO()
    qr_img.save(img_bytes)
    img_bytes.seek(0)
    return StreamingResponse(img_bytes, media_type="image/png")