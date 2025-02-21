# Background Remover
## Enhanced GrabCut Background Removal

## About the Project
This project implements an advanced background removal technique using OpenCV's GrabCut algorithm. It allows users to select an image file, automatically identifies the foreground, and removes the background while refining the extracted foreground using morphological operations. The goal is to produce cleaner, more accurate extractions for various applications such as photo editing, object detection, and computer vision tasks.

## Features
- **Automatic Background Removal**: Uses OpenCV's GrabCut algorithm to identify and separate the foreground.
- **Morphological Refinement**: Applies opening and closing operations to enhance mask accuracy.
- **User-Friendly Interface**: Utilizes Tkinter to allow users to select an image file interactively.
- **Real-Time Preview**: Displays the processed image immediately after background removal.

## Technologies Used
- **Python**: The programming language used for development.
- **OpenCV**: For image processing and background removal.
- **NumPy**: To handle array manipulations efficiently.
- **Tkinter**: Provides a graphical interface for image selection.

## Installation
### Prerequisites
Ensure you have Python installed along with the necessary dependencies:

```sh
pip install opencv-python numpy
```

## Usage
1. Run the script:
   ```sh
   python script.py
   ```
2. A file selection dialog will appear. Choose an image file (JPG, PNG, BMP, etc.).
3. The script will process the image, remove the background, and refine the foreground using morphological operations.
4. The final output image will be displayed in a new window.

## How It Works
1. **Image Selection**: The user selects an image via a GUI dialog.
2. **Initial Processing**: OpenCV loads the image and applies a rough bounding box for GrabCut.
3. **GrabCut Algorithm**: OpenCV’s GrabCut algorithm segments the foreground from the background.
4. **Morphological Processing**: Closing and opening operations refine the extracted mask to remove noise and enhance the result.
5. **Display Output**: The refined foreground image is displayed in a separate window.

## Possible Improvements
- Add interactive selection for defining foreground and background regions.
- Implement real-time processing for live camera feeds.
- Allow saving the processed image after background removal.

## Credits
Created by Shashank Singh[@shashankexore](https://github.com/shashankexore) and Anushka Banerjee [@anushka369](https://github.com/anushka369).
