from src.camera_filter import *

if __name__ == "__main__":
    # 프로그램 시작
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Video open failed!')
        sys.exit()

    cam_mode = 0  # 0: 기본, 1: 카툰, 2: 연필 스케치

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if cam_mode == 1:
            frame = cartoon_filter(frame)
        elif cam_mode == 2:
            frame = pencil_sketch(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        cv2.imshow('Camera Filter', frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == ord(' '):
            cam_mode = (cam_mode + 1) % 3

    cap.release()
    cv2.destroyAllWindows()
