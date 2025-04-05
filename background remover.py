import tkinter as tk
from tkinter import filedialog, Label, Button, Canvas, Entry, colorchooser, Radiobutton, StringVar
from rembg import remove
from PIL import Image, ImageTk, ImageColor
import io

selected_bg_color = "#ffffff"
selected_bg_image = None
processed_image_output = None
original_image = None
fg_image = None
fg_offset = [0, 0]
drag_data = {"x": 0, "y": 0}

def select_image():
    global original_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")])
    if not file_path:
        return
    original_image = Image.open(file_path).convert("RGBA")
    display_image(original_image, image_canvas)
    process_image(original_image)

def process_image(image):
    global selected_bg_image, processed_image_output, fg_image, fg_offset

    output = remove(image)

    if bg_mode.get() == "color":
        bg = Image.new("RGBA", output.size, selected_bg_color)
        bg.paste(output, (0, 0), output)
        processed_image_output = bg
        display_image(bg, output_canvas)
    elif bg_mode.get() == "photo" and selected_bg_image:
        bg = selected_bg_image.copy().convert("RGBA")
        out_w, out_h = output.size

        bg_ratio = bg.width / bg.height
        fg_ratio = out_w / out_h

        if bg_ratio > fg_ratio:
            new_height = out_h
            new_width = int(bg_ratio * new_height)
        else:
            new_width = out_w
            new_height = int(new_width / bg_ratio)

        bg = bg.resize((new_width, new_height), Image.Resampling.LANCZOS)
        bg_crop = bg.crop((0, 0, out_w, out_h))

        # Set initial position of foreground image
        fg_image = output
        fg_offset = [0, 0]

        render_canvas(bg_crop, output, fg_offset)

        processed_image_output = bg_crop.copy()
        processed_image_output.paste(output, tuple(fg_offset), output)

    else:
        processed_image_output = output
        display_image(output, output_canvas)

    status_label.config(text="✅ Image processed. Drag foreground if needed, then save.")

def render_canvas(bg_img, fg_img, offset):
    global output_canvas, fg_tk, bg_tk

    # Convert images for Tkinter
    bg_tk = ImageTk.PhotoImage(bg_img.resize((300, 300), Image.Resampling.LANCZOS))
    fg_scaled = fg_img.resize((300, 300), Image.Resampling.LANCZOS)
    fg_tk = ImageTk.PhotoImage(fg_scaled)

    output_canvas.delete("all")
    output_canvas.create_image(0, 0, anchor=tk.NW, image=bg_tk, tags="bg")
    output_canvas.create_image(offset[0], offset[1], anchor=tk.NW, image=fg_tk, tags="fg")

    output_canvas.tag_bind("fg", "<ButtonPress-1>", start_drag)
    output_canvas.tag_bind("fg", "<B1-Motion>", do_drag)
    output_canvas.tag_bind("fg", "<ButtonRelease-1>", stop_drag)

def start_drag(event):
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def do_drag(event):
    dx = event.x - drag_data["x"]
    dy = event.y - drag_data["y"]
    drag_data["x"] = event.x
    drag_data["y"] = event.y

    fg_offset[0] += dx
    fg_offset[1] += dy

    output_canvas.move("fg", dx, dy)

def stop_drag(event):
    # Nothing needed here right now
    pass

def save_image():
    global processed_image_output, fg_image, selected_bg_image, fg_offset

    if bg_mode.get() == "photo" and selected_bg_image and fg_image:
        output = selected_bg_image.copy().convert("RGBA")
        out_w, out_h = fg_image.size

        output = output.resize((out_w, out_h), Image.Resampling.LANCZOS)
        fg_paste = fg_image.copy()
        output.paste(fg_paste, tuple(fg_offset), fg_paste)
        processed_image_output = output

    if not processed_image_output:
        status_label.config(text="⚠️ No processed image to save.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        processed_image_output.save(save_path, format='PNG')
        status_label.config(text=f"✅ Saved: {save_path}")

def display_image(pil_image, canvas):
    max_size = 300
    w, h = pil_image.size
    scale = min(max_size / w, max_size / h)
    new_w, new_h = int(w * scale), int(h * scale)
    img_display = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    tk_image = ImageTk.PhotoImage(img_display)
    canvas.delete("all")
    canvas.create_image((max_size - new_w)//2, (max_size - new_h)//2, anchor=tk.NW, image=tk_image)
    canvas.image = tk_image

def set_bg_color(color_code):
    global selected_bg_color
    selected_bg_color = color_code
    custom_color_entry.delete(0, tk.END)
    custom_color_entry.insert(0, color_code)

def choose_custom_color():
    color_code = colorchooser.askcolor(title="Choose Background Color")[1]
    if color_code:
        set_bg_color(color_code)

def apply_custom_color():
    color_code = custom_color_entry.get()
    try:
        ImageColor.getrgb(color_code)
        set_bg_color(color_code)
    except ValueError:
        status_label.config(text="❌ Invalid hex color code")

def select_bg_photo():
    global selected_bg_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")])
    if not file_path:
        return
    selected_bg_image = Image.open(file_path).convert("RGBA")
    status_label.config(text=f"✅ Background photo selected")

def toggle_bg_options():
    if bg_mode.get() == "color":
        bg_options_frame.pack(pady=10)
        bg_photo_button.pack_forget()
    elif bg_mode.get() == "photo":
        bg_options_frame.pack_forget()
        bg_photo_button.pack(pady=10)
    else:
        bg_options_frame.pack_forget()
        bg_photo_button.pack_forget()

def on_enter(e):
    e.widget.config(bg="#ff5722", fg="white")

def on_leave(e):
    e.widget.config(bg="#007bff", fg="white")

# GUI Setup
root = tk.Tk()
root.title("Background Remover")
root.geometry("960x800")
root.configure(bg="#e1edfc")

bg_mode = StringVar(value="transparent")

header = Label(root, text="Background Remover", font=("Arial", 18, "bold"), bg="white", fg="black")
header.pack(pady=10)

btn_select = Button(root, text="📂 Select Image", command=select_image, font=("Arial", 12, "bold"), bg="#007bff", fg="white", padx=10, pady=5, borderwidth=2, relief="raised")
btn_select.pack(pady=10)
btn_select.bind("<Enter>", on_enter)
btn_select.bind("<Leave>", on_leave)

# Background mode selection
mode_frame = tk.Frame(root, bg="#e1edfc")
mode_frame.pack(pady=5)

Label(mode_frame, text="Choose Output Background:", font=("Arial", 12, "bold"), bg="#e1edfc").pack(anchor="w")
Radiobutton(mode_frame, text="Transparent", variable=bg_mode, value="transparent", command=toggle_bg_options, bg="#e1edfc").pack(anchor="w")
Radiobutton(mode_frame, text="Custom Color", variable=bg_mode, value="color", command=toggle_bg_options, bg="#e1edfc").pack(anchor="w")
Radiobutton(mode_frame, text="Custom Photo", variable=bg_mode, value="photo", command=toggle_bg_options, bg="#e1edfc").pack(anchor="w")

# Custom background color options
bg_options_frame = tk.Frame(root, bg="#e1edfc")

Label(bg_options_frame, text="Pick a Color:", font=("Arial", 12), bg="#e1edfc").grid(row=0, column=0, sticky="w", pady=5)

colors = ["#ffffff", "#000000", "#ff0000", "#00ff00", "#0000ff", "#cccccc"]
color_buttons_frame = tk.Frame(bg_options_frame, bg="#e1edfc")
color_buttons_frame.grid(row=0, column=1, columnspan=6, sticky="w")

for idx, col in enumerate(colors):
    btn = Button(color_buttons_frame, bg=col, width=2, height=1, relief="flat", borderwidth=0, command=lambda c=col: set_bg_color(c))
    btn.grid(row=0, column=idx, padx=1)

Button(bg_options_frame, text="🎨 Color Picker", command=choose_custom_color).grid(row=1, column=0, pady=5, sticky="w")
custom_color_entry = Entry(bg_options_frame, width=10)
custom_color_entry.grid(row=1, column=1, padx=5, pady=5)
Button(bg_options_frame, text="Apply", command=apply_custom_color).grid(row=1, column=2, pady=5)

# Background image selection button
bg_photo_button = Button(root, text="🖼️ Select Background Photo", command=select_bg_photo, font=("Arial", 12), bg="#007bff", fg="white")

# Image Display
frame = tk.Frame(root, bg="#e1edfc")
frame.pack(pady=10)

image_canvas = Canvas(frame, width=300, height=300, bg="#5188cc", highlightthickness=2, relief="ridge")
image_canvas.grid(row=0, column=0, padx=20, pady=10)

output_canvas = Canvas(frame, width=300, height=300, bg="#5188cc", highlightthickness=2, relief="ridge")
output_canvas.grid(row=0, column=1, padx=20, pady=10)

# Save Button
save_button = Button(root, text="💾 Save Image", command=save_image, font=("Arial", 12, "bold"), bg="#28a745", fg="white", padx=10, pady=5)
save_button.pack(pady=10)

status_label = Label(root, text="", font=("Arial", 12, "bold"), fg="#d32f2f", bg="#e1edfc")
status_label.pack(pady=10)

toggle_bg_options()
root.mainloop()
