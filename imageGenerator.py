import sys
from randimage import get_random_image, show_array
import matplotlib
import os
import time

def main():
    # The command line arguments should be the name of the image file to generate, the resolution of the image as 'num'x'num'
    # And a optional number, which is the number of images to generate
    # Check if the number of arguments is correct  
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python imageGenerator.py <image name> <resolution>")
        return
    
    # If the argument is 4, check if the last argument is a positive integer and
    # set the number of images to generate to that number
    num_images = 1
    if len(sys.argv) == 4:
        try:
            num_images = int(sys.argv[3])
        except:
            print("Invalid number of images")
            return
    else:
        num_images = 1

    
    # Get the name of the image file to generate
    image_name = sys.argv[1]
    # Check the image_name does not have a file extension
    if '.' in image_name:
        print("Invalid image name")
        print("Don't include the file extension")
        return

    # Get the resolution of the image
    resolution = sys.argv[2]

    # separate the resolution into width and height
    resolution = resolution.split('x')
    width = int(resolution[0])
    height = int(resolution[1])

    # Check if the resolution is valid (positive integers) and less than 4k so that the image is not too large
    if width <= 0 or height <= 0 or width > 3840 or height > 2532:
        print("Invalid resolution")
        return
    
    # Create a directory for the resolution
    create_directory(width, height)

    # If the number of images to generate is 1, generate one image
    # If the number of images to generate is more than 1, generate that number of images
    if num_images == 1:
        generateOneImage(image_name, width, height)
    else:
        generateMultipleImages(image_name, width, height, num_images)
    

    

def save_time(image_name, time_taken, width, height, num_images):
    with open("time.txt", "a") as file:
        file.write(f"{width}x{height}/{image_name}: {time_taken}\n")
        # Also write device information and date and time
        file.write(f"Device: {os.uname()}\n")
        file.write(f"Date and Time: {time.ctime()}\n")
        # Also write how many images it generated
        file.write(f"Number of Images: {num_images}\n")
        file.write("\n")


def generateOneImage(image_name, width, height):
    # Generate the image with the given resolution and record how long it took
    start = time.time()
    generate_image_usingLibrary(image_name, width, height)
    end = time.time()
    print(f"Time taken to generate Image: {end - start} seconds")

    # Save the time taken to generate the image in a file called 'time.txt'
    # if the file does not exist, create it
    # if the file exists, append the time to the file
    # write in the format of "image_name: time_taken" in seconds
    save_time(image_name, end - start, width, height, 1)


def generateMultipleImages(image_name, width, height, num_images):
    # Generate the image with the given resolution and record how long it took
    start = time.time()
    for i in range(num_images):
        generate_image_usingLibrary(image_name + f"_{i}", width, height)
    end = time.time()
    print(f"Time taken to generate {num_images} Images: {end - start} seconds")

    # Save the time taken to generate the image in a file called 'time.txt'
    # if the file does not exist, create it
    # if the file exists, append the time to the file
    # write in the format of "image_name: time_taken" in seconds
    save_time(image_name, end - start, width, height, num_images)

# Generate the image with the given resolution
def generate_image_usingLibrary(image_name, width, height):
    img_size = (height,width)
    img = get_random_image(img_size)  #returns numpy array
    matplotlib.image.imsave(f"Images/{width}x{height}/{image_name}.png", img) #saves the image in the directory
    print(f"Image {image_name}.png saved in Images/{width}x{height}")
    # Print the image size in megabytes, round it to 2 decimal places
    print(f"Image size: {round(os.path.getsize(f'Images/{width}x{height}/{image_name}.png')/1024/1024, 2)} MB")



# Check if the directory of that resolution exists, if not, create it
# If it created a new directory, give a message
# If the directory already exists, give a message
def create_directory(width, height):
    directory = f"Images/{width}x{height}"
    try:
        os.mkdir(directory)
        print(f"Created directory {directory}")
    except FileExistsError:
        print(f"Directory {directory} already exists")
    


if __name__ == "__main__":
    main()