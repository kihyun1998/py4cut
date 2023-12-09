import cv2
import datetime
from pygame import mixer
import time

def record_video_and_capture_image():
    cap = cv2.VideoCapture(0)

    # 카메라 해상도 설정
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # 영상 저장을 위한 코덱 및 해상도 설정
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None
    img_count = 0
    is_recording = False

    # 사운드 설정
    mixer.init()
    shutter_sound = mixer.Sound('shutter_sound.mp3')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("카메라를 열 수 없습니다.")
            break

        cv2.imshow('영상 녹화 및 사진 촬영', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            print("10초 후에 사진을 찍습니다.")
            for i in range(1000, 0, -1):  # 10초부터 1초까지 카운트다운
                if i%100==0:
                    print(i//100)
                time.sleep(0.01)  # 1초마다 화면 갱신
                ret, frame = cap.read()
                if not ret:
                    print("카메라를 열 수 없습니다.")
                    break
                cv2.imshow('영상 녹화 및 사진 촬영', frame)
                if cv2.waitKey(1) == ord('q'):  # 'q'를 누르면 종료
                    cap.release()
                    cv2.destroyAllWindows()
                    return
            shutter_sound.play()
            img_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_capture_{img_count}.png"
            cv2.imwrite(img_name, frame)
            print(f"{img_name} 사진 저장 완료!")
            img_count += 1
        elif key == ord('r'):
            if is_recording:
                print("녹화 종료")
                out.release()
                is_recording = False
            else:
                print("녹화 시작")
                out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
                is_recording = True

        if is_recording:
            out.write(frame)

    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    record_video_and_capture_image()
