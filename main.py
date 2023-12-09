import cv2
import datetime
from pygame import mixer
import threading
import time
import os

# 카운트다운 함수
# test=2 실제=10
def countdown():
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)
    print("사진을 찍습니다.")

def record_video_and_capture_image():
    cap = cv2.VideoCapture(0)

    # 카메라 해상도 설정
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # 영상 저장을 위한 코덱 및 해상도 설정
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None
    video_count = 0
    is_recording = False

    # 사운드 설정
    mixer.init()
    shutter_sound = mixer.Sound("./sound/shutter_sound.mp3")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("카메라를 열 수 없습니다.")
            break

        cv2.imshow('영상 녹화 및 사진 촬영', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        

        # c를 누르면 사진 찍기 시작
        # 10초 간격으로 4번 연속 사진을 촬영한다. (test는 2초)
        # 시간:분:초 폴더를 생성하여 해당 폴더에 4개 사진을 추가한다.
        # 사진 이름 예시: Picture_1.png, Picture_2.png...
        elif key == ord('c'):
            img_count = 1
            # 폴더이름 지정(날짜) 및 생성
            img_folder = f"./image/{datetime.datetime.now().strftime('%Hh-%Mmin-%Ssec')}"
            os.makedirs(img_folder,exist_ok=True)

            for i in range(4):
                t = threading.Thread(target=countdown)
                t.start()
                while t.is_alive():
                    ret, frame = cap.read()
                    cv2.imshow('영상 녹화 및 사진 촬영', frame)
                    if cv2.waitKey(1) == ord('q'):  # 'q'를 누르면 종료
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                shutter_sound.play()

                img_name = f"Picture_{img_count}.png" # 이미지 이름
                img_savePath = f"{img_folder}/{img_name}" # 이미지 저장 경로

                # 사진 저장
                cv2.imwrite(img_savePath, frame)
                print(f"{img_savePath} 사진 저장 완료!")
                img_count += 1
        
        # 처음 r을 누르면 녹화가 시작하고
        # 녹화 중 다시 r을 누르면 녹화가 종료된다.
        elif key == ord('r'):
            if is_recording:
                print("녹화 종료")
                out.release()
                is_recording = False
            else:
                print("녹화 시작")

                # 영상 폴더 지정 및 생성
                video_folder = f"./video/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}" 
                os.makedirs(video_folder,exist_ok=True)
                
                video_name = f"Video_{video_count}.mp4" # 영상 파일 이름
                video_savePath = f"./{video_folder}/{video_name}" # 영상 저장 경로
                
                out = cv2.VideoWriter(video_savePath, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
                is_recording = True
                video_count += 1

        if is_recording:
            out.write(frame)

    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    record_video_and_capture_image()
