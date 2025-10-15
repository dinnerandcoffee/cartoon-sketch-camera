import sys
import numpy as np
import cv2

# -----------------------------
# 카툰 필터 함수
# -----------------------------
def cartoon_filter(img):
    h, w = img.shape[:2]
    img2 = cv2.resize(img, (w // 2, h // 2))

    # 양방향 필터로 부드럽게 처리
    blr = cv2.bilateralFilter(img2, -1, 20, 7)
    # 에지 검출
    edge = 255 - cv2.Canny(img2, 80, 120)
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    # 윤곽선 유지 + 색 평탄화
    dst = cv2.bitwise_and(blr, edge)
    dst = cv2.resize(dst, (w, h), interpolation=cv2.INTER_NEAREST)

    return dst

# -----------------------------
# 연필 스케치 필터 함수
# -----------------------------
def pencil_sketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blr = cv2.GaussianBlur(gray, (0, 0), 3)
    dst = cv2.divide(gray, blr, scale=255)
    return dst

# -----------------------------
# 웹캠 열기
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Video open failed!')
    sys.exit()

cam_mode = 0  # 0: 기본, 1: 카툰, 2: 연필 스케치

# -----------------------------
# 메인 루프
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    if cam_mode == 1:
        frame = cartoon_filter(frame)
    elif cam_mode == 2:
        frame = pencil_sketch(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    # 화면 출력
    cv2.imshow('Camera Filter', frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC 종료
        break
    elif key == ord(' '):  # 스페이스바로 필터 전환
        cam_mode += 1
        if cam_mode == 3:
            cam_mode = 0

# -----------------------------
# 종료
# -----------------------------
cap.release()
cv2.destroyAllWindows()
