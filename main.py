# Import necessary libraries
from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
from tkinter import filedialog

# Function to handle image upload
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        # Open the selected image file
        img = Image.open(file_path)
        # Resize the image to fit within a maximum size of 300x300 pixels
        img.thumbnail((300, 300))
        # Convert the image to a Tkinter-compatible format
        img_tk = ImageTk.PhotoImage(img)
        # Display the image on the label widget
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to prevent garbage collection
        image_label.image_path = file_path  # Store the file path for watermarking

# Function to calculate text size for watermark
def textsize(text, font):
    # Create a temporary image for text measurement (size 0x0)
    im = Image.new(mode="RGB", size=(0, 0))
    draw = ImageDraw.Draw(im)
    # Get the bounding box of the text to determine its size
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

# Function to apply watermark to the uploaded image
def apply_watermark():
    if not hasattr(image_label, 'image_path'):
        return  # No image uploaded

    watermark = watermark_text.get()  # Get the watermark text from the entry widget
    if not watermark:
        return  # No watermark text provided

    try:
        # Open the uploaded image
        img = Image.open(image_label.image_path)

        # Get image size
        width, height = img.size

        # Specify font and increase the font size for the watermark
        font_size = 48  # Font size for the watermark text
        font = ImageFont.truetype("arial.ttf", font_size)

        # Calculate text size using textbbox method
        text_width, text_height = textsize(watermark, font)

        # Calculate position for watermark to be centered
        x = (width - text_width) // 2  # Center horizontally
        y = (height - text_height) // 2  # Center vertically

        # Create drawing context
        draw = ImageDraw.Draw(img)

        # Apply the watermark to the image
        draw.text((x, y), watermark, font=font, fill=(255, 255, 255, 128))  # White text with some transparency

        # Resize image to fit within the label dimensions
        max_width = 600  # Max width of the label
        max_height = 300  # Max height of the label
        img.thumbnail((max_width, max_height), Image.LANCZOS)  # Resize using LANCZOS resampling

        # Convert the image to a format suitable for Tkinter display
        img_tk = ImageTk.PhotoImage(img)

        # Update the displayed image on the label widget
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to prevent garbage collection

        # Adjust label size to fit the image
        image_label.config(width=img_tk.width(), height=img_tk.height())

        # Save the watermarked image for later use
        image_label.watermarked_image = img

    except Exception as e:
        print(f"Error applying watermark: {e}")

# Function to save the watermarked image
def save_image():
    if not hasattr(image_label, 'watermarked_image'):
        return  # No watermarked image to save

    try:
        # Specify the file path to save
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            # Save the watermarked image to the specified file path
            image_label.watermarked_image.save(file_path)
            print(f"Image saved successfully to {file_path}")

    except Exception as e:
        print(f"Error saving image: {e}")

# Create the main window
window = Tk()
window.title("Image Watermarking Application")
window.geometry("600x590")  # Set the initial size of the window
window.config(background="lightgrey")  # Set the background color of the window

# Create and place the upload button
upload_button = Button(window, text='Upload', command=upload_image)
upload_button.pack(pady=10)

# Create a label to display the uploaded image
image_label = Label(window)
image_label.pack(pady=10)

# Add an entry widget for watermark text
watermark_text = Entry(window, width=40)
watermark_text.pack(pady=10)

# Add a button to apply the watermark
apply_watermark_button = Button(window, text='Apply Watermark', command=apply_watermark)
apply_watermark_button.pack(pady=10)

# Add a button to save the image
save_button = Button(window, text='Save Image', command=save_image)
save_button.pack(pady=10)

# Run the Tkinter main loop
window.mainloop()
