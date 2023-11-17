import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
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


def compile_images(image_files, mouse_list, input_directory):
    # Determining the size of the compilation document
    print("Determining size of compiled document. 0%", end='\r')
    max_width = 0
    max_height = 0
    for i, image_path in enumerate(image_files):
        current_image = Image.open(image_path)
        if max_width < current_image.width:
            max_width = current_image.width
        if max_height < current_image.height:
            max_height = current_image.height
        percent_done = round(100 * i / len(image_files))
        print(f"Determining size of compiled document. {percent_done}%", end='\r')
    print(f"Determining size of compiled document. 100%")

    compilation_width = int(max_width * len(image_files) / 2)   # Divide by 2 because we have two rows (BAF/IRAF)
    y_offset = 500
    compilation_height = int((max_height * 2) + y_offset)
    background_color = (255, 255, 255)
    compiled_image = Image.new('RGB', (compilation_width, compilation_height), background_color)

    # Creating a title for the document
    draw = ImageDraw.Draw(compiled_image)
    title = "[Your experiment name here]"
    text_color = (0, 0, 0)
    font = ImageFont.truetype("arial.ttf", 120)
    draw.text((30, 20), title, fill=text_color, font=font)


    current_image_number = 0
    total_images = len(image_files)

    for i, mouse in enumerate(mouse_list):
        current_mouse_files = []
        for image in image_files:
            if mouse in os.path.basename(image):
                current_mouse_files.append(image)
        if len(current_mouse_files) != 4:
            print(f"Unexpected number of files in mouse {mouse}. Number of files: {len(current_mouse_files)}")

        x_offset = i * max_width * 2
        # y_offset is defined above when making the compiled image

        font = ImageFont.truetype("arial.ttf", 100)
        draw.text((x_offset + 30, y_offset - 200), mouse, fill=text_color, font=font)

        for image_path in current_mouse_files:
            image = Image.open(image_path)
            if "OD" in os.path.basename(image_path):
                if "BAF" in os.path.basename(image_path):
                    compiled_image.paste(image, (x_offset, y_offset))
                if "IRAF" in os.path.basename(image_path):
                    compiled_image.paste(image, (x_offset, y_offset + max_height))
            elif "OS" in os.path.basename(image_path):
                if "BAF" in os.path.basename(image_path):
                    compiled_image.paste(image, (x_offset + max_width, y_offset))
                if "IRAF" in os.path.basename(image_path):
                    compiled_image.paste(image, (x_offset + max_width, y_offset + max_height))
            else:
                continue
            current_image_number += 1
            percent_done = round(100 * current_image_number / total_images)
            print(f"Inserting images into compilation document. {percent_done}%", end='\r')

    print(f"Inserting images into compilation document. 100%")

    completed_file_path = os.path.join(input_directory, 'cSLO_compilation.jpg')
    compiled_image.save(completed_file_path)

    print("Compilation image saved as cSLO_compilation.jpg")

    return completed_file_path

# Define the input directory where your images are located
input_directory = select_input_directory()


mouse_list = list_mice(input_directory)

print("List of mice:")
print(mouse_list)

image_files = find_image_files(input_directory)
print(f"Images found: {len(image_files)}")


completed_file_path = compile_images(image_files, mouse_list, input_directory)

# Opening the final product
if os.name == 'nt':  # Check if the operating system is Windows
    os.startfile(completed_file_path)
