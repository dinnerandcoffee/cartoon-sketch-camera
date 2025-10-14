# src/capture.py
import argparse
import cv2
from pathlib import Path

def run(device="/dev/video0", out="data/output.avi", fps=20.0, gray=True, show=True):
    cap = cv2.VideoCapture(device)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video device: {device}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Width: {width}, Height: {height}")

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    # isColor: gray면 False, color면 True
    is_color = not gray
    writer = cv2.VideoWriter(out, fourcc, fps, (width, height), isColor=is_color)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if gray:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if show:
                    cv2.imshow("Gray Video", frame)
            else:
                if show:
                    cv2.imshow("Color Video", frame)

            writer.write(frame)

            if show and (cv2.waitKey(1) & 0xFF == ord("q")):
                break
    finally:
        cap.release()
        writer.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="/dev/video0")
    p.add_argument("--out", default="data/output.avi")
    p.add_argument("--fps", type=float, default=20.0)
    p.add_argument("--gray", action="store_true", default=True, help="grayscale (default)")
    p.add_argument("--color", dest="gray", action="store_false", help="color mode")
    p.add_argument("--no-show", dest="show", action="store_false", help="do not open window")
    args = p.parse_args()
    run(device=args.device, out=args.out, fps=args.fps, gray=args.gray, show=args.show)
