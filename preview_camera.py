import argparse
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview the wrist camera view.")
    parser.add_argument("--camera-index", default="0")
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--save-path", type=Path)
    parser.add_argument(
        "--save-only",
        action="store_true",
        help="Capture one frame and save it without opening a preview window.",
    )
    args = parser.parse_args()

    index_or_path: int | str
    try:
        index_or_path = int(args.camera_index)
    except ValueError:
        index_or_path = args.camera_index

    cap = cv2.VideoCapture(index_or_path)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    cap.set(cv2.CAP_PROP_FPS, args.fps)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera: {args.camera_index}")

    last_frame = None
    default_save_path = Path("outputs/captured_images/fixed_start_view.png")
    print("Press q to quit, s to save one frame.")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError("Camera returned no frame.")

            last_frame = frame
            if args.save_only:
                save_path = args.save_path or default_save_path
                save_path.parent.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(save_path), frame)
                print(f"Saved {save_path}")
                break

            try:
                cv2.imshow("Fixed start wrist camera view", frame)
            except cv2.error as exc:
                save_path = args.save_path or default_save_path
                save_path.parent.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(save_path), frame)
                print(f"OpenCV preview is unavailable, saved one frame to {save_path}")
                print(exc)
                break

            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):
                save_path = args.save_path or default_save_path
                save_path.parent.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(save_path), frame)
                print(f"Saved {save_path}")
            elif key == ord("q"):
                break
    finally:
        if args.save_path and last_frame is not None:
            args.save_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(args.save_path), last_frame)
            print(f"Saved {args.save_path}")
        cap.release()
        try:
            cv2.destroyAllWindows()
        except cv2.error:
            pass


if __name__ == "__main__":
    main()
