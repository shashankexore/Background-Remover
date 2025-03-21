# Background Remover

## About the Project
This project implements an advanced background removal tool using the `rembg` library. Users can select an image, and the system automatically removes the background while refining the extracted foreground. The goal is to provide a seamless and efficient background removal process for various applications, such as photo editing, object detection, and computer vision tasks.

## Features
- **Automatic Background Removal**: Uses the `rembg` library for precise background removal.
- **User-Friendly Interface**: A simple GUI built with Tkinter allows users to select and process images effortlessly.
- **Real-Time Preview**: Displays the processed image immediately after background removal.
- **Save Processed Images**: Users can save the output image after processing.
- **Custom Styling**: Visually appealing interface with intuitive buttons and canvases.

## Technologies Used
- **Python**: The programming language used for development.
- **rembg**: For accurate background removal.
- **Pillow (PIL)**: For handling image operations.
- **Tkinter**: Provides a graphical interface for image selection and preview.

## Installation
### Prerequisites
Ensure you have Python installed along with the necessary dependencies:

```sh
pip install rembg pillow tkinter
```

## Usage
1. Run the script:
   ```sh
   python script.py
   ```
2. A file selection dialog will appear. Choose an image file (JPG, PNG, BMP, etc.).
3. The script will process the image and remove the background.
4. The processed image will be displayed in the application window.
5. Users can save the processed image in PNG format.

## How It Works
1. **Image Selection**: The user selects an image via a GUI dialog.
2. **Background Removal**: The `rembg` library processes the image to extract the foreground.
3. **Display Output**: The refined foreground image is displayed in a separate window.
4. **Saving Processed Image**: Users can save the image after background removal.

## Possible Improvements
- Add interactive selection for defining foreground and background regions.
- Implement real-time processing for live camera feeds.
- Support batch processing for multiple images.

## Credits
Created by Shashank Singh [@shashankexore](https://github.com/shashankexore) and Anushka Banerjee [@anushka369](https://github.com/anushka369).

