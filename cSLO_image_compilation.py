import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os


def select_input_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    input_directory = filedialog.askdirectory()
    return input_directory




def find_image_files(input_directory):
    image_files = []

    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.tif') and ("BAF" in file or "IRAF" in file):
                image_files.append(os.path.join(root, file))

    return image_files


def list_mice(input_directory):
    mouse_list = [folder for folder in os.listdir(input_directory) if os.path.isdir(os.path.join(input_directory, folder))]
    return mouse_list


def compile_images(image_files):
    baf_images = [img for img in image_files if "BAF" in img]
    iraf_images = [img for img in image_files if "IRAF" in img]

    baf_images.sort()
    iraf_images.sort()

    if len(baf_images) != len(iraf_images):
        print("Unequal number of BAF and IRAF images. Cannot create pairs.")
        return

    pairs = list(zip(baf_images, iraf_images))

    images = []
    for baf_img, iraf_img in pairs:
        baf = Image.open(baf_img)
        iraf = Image.open(iraf_img)
        images.extend([baf, iraf])

    # Determine the dimensions for the final compilation image
    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)

    # Create a new blank image with the calculated dimensions
    compiled_image = Image.new('RGB', (max_width, total_height*2))

    # Paste each pair of images into the compiled image
    y_offset = 0
    for i in range(0, len(images), 2):
        compiled_image.paste(images[i], (0, y_offset))
        compiled_image.paste(images[i + 1], (max_width, y_offset))
        y_offset += images[i].height

    # Save the compiled image as a JPEG file
    output_directory = os.path.dirname(image_files[0]) if image_files else os.getcwd()
    compiled_image.save(os.path.join(output_directory, 'cSLO_compilation.jpg'))
    print("Compilation image saved as cSLO_compilation.jpg")

# Define the input directory where your images are located
input_directory = select_input_directory()


mouse_list = list_mice(input_directory)

print("List of mice:")
print(mouse_list)

image_files = find_image_files(input_directory)
print(f"Images found: {len(image_files)}")

compile_images(image_files)
