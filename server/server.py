"""
실행방법은
uvicorn ./server.py:app --reload
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

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

@app.get("/videos/{video_index}")
async def download_video(video_index: int):
    # 해당 인덱스의 타깃 비디오 경로를 찾음
    target_video_path = os.path.join(video_folder, str(video_index), f"video_{video_index}.avi")
    
    if os.path.exists(target_video_path):
        return FileResponse(target_video_path, media_type='application/octet-stream', filename=f"video_{video_index}.avi")
    else:
        raise HTTPException(status_code=404, detail="Video not found")

@app.get("/images/{image_index}")
async def download_image(image_index: int):
    # 이미지 파일 경로를 생성
    image_file = f"image_{image_index}.jpg"
    target_image_path = os.path.join(image_folder, str(image_index), image_file)
    
    if os.path.exists(target_image_path):
        return FileResponse(target_image_path, media_type='image/jpeg', filename=image_file)
    else:
        raise HTTPException(status_code=404, detail="Image not found")

