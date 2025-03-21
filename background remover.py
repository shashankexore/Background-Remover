import tkinter as tk
from tkinter import filedialog, Label, Button, Canvas
from rembg import remove
from PIL import Image, ImageTk
import io

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")])
    if not file_path:
        return
    
    image = Image.open(file_path)
    img_display = image.resize((300, 300))
    img_display = ImageTk.PhotoImage(img_display)
    image_canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
    image_canvas.image = img_display
    process_image(image, file_path)

def process_image(image, input_path):
    output = remove(image)
    img_io = io.BytesIO()
    output.save(img_io, format='PNG')
    img_io.seek(0)
    
    processed_img = Image.open(img_io)
    processed_img_display = processed_img.resize((300, 300))
    processed_img_display = ImageTk.PhotoImage(processed_img_display)
    output_canvas.create_image(0, 0, anchor=tk.NW, image=processed_img_display)
    output_canvas.image = processed_img_display
    
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        output.save(save_path, format='PNG')
        status_label.config(text=f"Saved: {save_path}")

def on_enter(e):
    e.widget.config(bg="#ff5722", fg="white")

def on_leave(e):
    e.widget.config(bg="#007bff", fg="white")

# GUI Setup
root = tk.Tk()
root.title("Background Remover")
root.geometry("900x600")
root.configure(bg="#ffeb3b")

header = Label(root, text="🖼️ Background Remover", font=("Arial", 18, "bold"), bg="#ffeb3b", fg="#333")
header.pack(pady=10)

btn_select = Button(root, text="📂 Select Image", command=select_image, font=("Arial", 12, "bold"), bg="#007bff", fg="white", padx=10, pady=5, borderwidth=2, relief="raised")

btn_select.pack(pady=10)
btn_select.bind("<Enter>", on_enter)
btn_select.bind("<Leave>", on_leave)

frame = tk.Frame(root, bg="#ffeb3b")
frame.pack(pady=10)

image_canvas = Canvas(frame, width=300, height=300, bg="#ff9800", highlightthickness=2, relief="ridge")
image_canvas.grid(row=0, column=0, padx=20, pady=10)

output_canvas = Canvas(frame, width=300, height=300, bg="#4caf50", highlightthickness=2, relief="ridge")
output_canvas.grid(row=0, column=1, padx=20, pady=10)

status_label = Label(root, text="", font=("Arial", 12, "bold"), fg="#d32f2f", bg="#ffeb3b")
status_label.pack(pady=10)

root.mainloop()
