from picamera import PiCamera
from datetime import datetime
import time
import numpy as np
import cv2
import os
import matplotlib
import matplotlib.pyplot as plt

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

DETECTION_PIXEL_THRESH = 1e6

def compute_hist(img):
    global prev_hist
    # compute histogram
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_flatten = hist.flatten()
    hist_x = np.array(range(256))

    # plot histogram
    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(111)
    ax.plot(hist_x, hist_flatten)
    fig.canvas.draw()

    image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image_from_plot = image_from_plot.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    cv2.imshow("hist", image_from_plot)
    cv2.waitKey(1)


def substract_and_erode(img, background_img):
    diff_img = cv2.absdiff(img, background_img)
    thresh, binary_img = cv2.threshold(diff_img, 60, 255, cv2.THRESH_BINARY)
    erode_kernel = np.ones((3, 3), np.uint8)
    img_erode = cv2.erode(binary_img, erode_kernel)
    cv2.imshow("diff_img", img_erode)
    cv2.waitKey(1)
    pixel_sum = img_erode.sum()
    if pixel_sum > DETECTION_PIXEL_THRESH:
        img_name = datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f") + ".png"
        img_path = os.path.join("/home/wanlin/Desktop/camera_images", img_name)
        print(f"write image to {img_path}")
        cv2.imwrite(img_path, img)

def run():
    with PiCamera() as camera:
        camera.resolution = (IMAGE_WIDTH, IMAGE_HEIGHT)
        camera.framerate = 12
        background_img = None
        while True:
            image = np.empty((IMAGE_HEIGHT * IMAGE_WIDTH * 3), dtype=np.uint8)
            camera.capture(image, "bgr")
            image = image.reshape((IMAGE_HEIGHT, IMAGE_WIDTH, 3))
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if background_img is None:
                background_img = image_gray
            substract_and_erode(image_gray, background_img)
            compute_hist(image_gray)
            cv2.imshow("camera", image_gray)
            cv2.waitKey(1)

if __name__ == "__main__":
    run()

