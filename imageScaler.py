import sys
import os
from PIL import Image

def main():
    # Take the path of the file to scale as the first command line argument
    # Take the resolution to scale the image to as the second command line argument in the format of 'num'x'num'
    # Take a path to where to save the scaled image as the third command line argument
    # Check if the number of arguments is correct
    if len(sys.argv) != 4:
        print("Usage: python imageScaler.py <image path> <resolution> <save path>")
        return
    
    # Get the path of the image file to scale
    image_path = sys.argv[1]
    # Check if the image_path exists
    if not os.path.exists(image_path):
        print("Invalid image path")
        return
    
    # Get the resolution to scale the image to
    resolution = sys.argv[2]
    # separate the resolution into width and height
    try:
        resolution = resolution.split('x')
        width = int(resolution[0])
        height = int(resolution[1])

    except:
        print("Invalid resolution")
        return
    
    # Check if the resolution is valid (positive integers) and less than 4k so that the image is not too large
    if width <= 0 or height <= 0 or width > 3840 or height > 2160:
        print("Invalid resolution")
        return

    # Get the path to save the scaled image
    save_path = sys.argv[3]
    # Check if the directory to save the scaled image exists
    if not os.path.exists(os.path.dirname(save_path)):
        print("Invalid save path")
        return
    
    # Scale the image to the given resolution and save it in the save_path
    scale_image(image_path, width, height, save_path)
    print(f"Image scaled and saved in {save_path}")


def scale_image(image_path, width, height, save_path):
    
    # Open the image
    image = Image.open(image_path)

    # print the original resolution of the image
    print(f"Original Resolution: {image.size}")

    # Scale the image to the given resolution
    image = image.resize((width, height))

    # Save the scaled image
    image.save(save_path)
    print(f"Scaled Resolution: {image.size}")


if __name__ == "__main__":
    main()