import cv2
import time
import os
import datetime
from pygame import mixer

# 웹캠 설정
cap = cv2.VideoCapture(0)
is_recording = False
capture_count = 0  # 촬영된 사진 수

capture_interval = 3  # 사진 촬영 간격 (초)

# 영상 녹화 배속 설정
fps = cap.get(cv2.CAP_PROP_FPS)
acc_fps = int(fps*1.5)

# 비디오 레코더 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter()

# 사진 촬영 사운드 설정
mixer.init()
shutter_sound = mixer.Sound('./sound/shutter_sound.mp3')

while True:
    index= 0 if capture_count == 0 else capture_count//4
    ret, frame = cap.read()
    if not ret:
        print("웹캠에서 영상을 받아올 수 없습니다.")
        break

    # 현재 프레임 표시
    cv2.imshow('frame', frame)

    # 키 입력 확인
    key = cv2.waitKey(1) & 0xFF

    # 'q'를 눌러 종료
    if key == ord('q'):
        break

    # 's'를 눌러 레코딩 시작
    if key == ord('s') and not is_recording:
        # last_capture_time = time.time()

        save_video_folder = f"./video/{index}" # 저장할 video 폴더명
        os.makedirs(save_video_folder,exist_ok=True) # 폴더 생성

        video_name = f"video_{index}.avi"
        save_video_path = f"{save_video_folder}/{video_name}"

        is_recording = True
        out = cv2.VideoWriter(save_video_path, fourcc, acc_fps, (frame.shape[1], frame.shape[0]))
        print("녹화 시작!")

    # 녹화 중이면 프레임 저장
    if is_recording:
        out.write(frame)

        save_image_folder = f"./image/{index}" # 저장할 image 폴더명
        os.makedirs(save_image_folder,exist_ok=True) # 폴더 생성

        # [이전코드]3초마다 촬영
        # if time.time() - last_capture_time > capture_interval:

        # 기능 변경 
        # c를 누르면 사진 촬영, 4장 촬영하면 녹화 종료
        if key == ord('c'):
            photo_name = f'picture_{datetime.datetime.now().strftime('%Hh-%Mmin-%Ssec')}_{capture_count%4}.jpg' #캡처 번호는 0,1,2,3으로 나온다.
            save_photo_path = f"{save_image_folder}/{photo_name}"
            cv2.imwrite(save_photo_path, frame)
            shutter_sound.play()
            print(f'{save_photo_path} 저장됨')

            # last_capture_time = time.time()
            capture_count += 1

            
            if capture_count % 4==0:  # 4장의 사진이 촬영되었으면
                print("4장의 사진이 촬영되었습니다. 녹화를 종료합니다.")
                is_recording = False
                out.release()  # 비디오 레코더 종료

# 모든 리소스 해제
cap.release()
cv2.destroyAllWindows()
if is_recording:
    out.release()  # 안전하게 비디오 레코더 종료
