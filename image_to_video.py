from glob import glob
from typing import List, Tuple, Callable
import cv2
import re


def write_video(file_name: str, images: List[str], resolution: Tuple[int], FPS: int):
    # Initialize the video writer with MJPG codec and resolution
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    out = cv2.VideoWriter(file_name, fourcc, FPS, resolution)
    print(images)
    for image in images:
        # Read the image and resize it to resolution
        img = cv2.imread(image)
        if img is None:
            print(f"Warning: '{image}' could not be read.")
            continue
        if img.size != resolution:
            img = cv2.resize(img, resolution)

        # Write the image as a single frame
        out.write(img)

    # Release the video writer
    out.release()


def images_to_video(
    folder: str,
    input_format: str,
    FPS: int,
    resolution: Tuple[int],
    output_filename: str,
    sort_func: Callable[[str], List] = None,
):
    assert input_format.lower() in ["png", "jpg"]
    if sort_func is not None:
        image_files = sorted(glob(f"{folder}/*.{input_format.lower()}"), key=sort_func)
    else:
        image_files = glob(f"{folder}/*.{input_format.lower()}")
    write_video(output_filename, image_files, resolution, FPS)


if __name__ == "__main__":
    natural_sort_key = lambda filename: [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r"(\d+)", filename)
    ]
    images_to_video("image", "png", 60, (2048, 2048), "result.avi", natural_sort_key)
