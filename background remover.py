import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def enhanced_grabcut(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        raise ValueError(f"Image not found or unable to load: {image_path}")

    height, width = image.shape[:2]

    # Create a mask
    mask = np.zeros(image.shape[:2], np.uint8)

    # Define a bounding box (this can be user-defined)
    rect = (10, 10, width - 20, height - 20)

    # Create background and foreground models
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    # Apply GrabCut
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

    # Modify the mask to create a binary mask
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Morphological operations to refine the mask
    kernel = np.ones((5, 5), np.uint8)
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel)
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)

    # Extract the foreground
    foreground = image * mask2[:, :, np.newaxis]

    return foreground

def main():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask the user to select an image file
    image_path = filedialog.askopenfilename(title='Select an image file', filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    
    if not image_path:
        print("No file selected. Exiting.")
        return

    try:
        # Perform background removal
        output_image = enhanced_grabcut(image_path)

        # Display the processed image
        cv2.imshow('Foreground', output_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
