import cv2
import numpy as np

def get_mask(img:np.ndarray) -> np.ndarray:
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of black color in HSV
    lower_val = np.array([0,0,0])
    upper_val = np.array([50,100,100])

    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv, lower_val, upper_val)

    # invert mask to get black symbols on white background
    mask_inv = cv2.bitwise_not(mask)

    return mask_inv

def get_mask_from_gray(img:np.ndarray, lower_val:int = 0,upper_val:int = 100) -> np.ndarray:
    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(img, lower_val, upper_val)
    mask = cv2.bitwise_not(mask)

    return mask