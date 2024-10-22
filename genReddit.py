import os
import sys
import time
import datetime
import shutil
import hashlib
import matplotlib
import praw
from dotenv import load_dotenv
from randimage import get_random_image

# Function to generate SHA-1 hash for an image
def generate_hash(file_path):
    hash_algo = hashlib.sha1()
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()[:8]

# Function to save time taken for image generation
def save_time(image_name, time_taken, width, height, num_images):
    with open("time.txt", "a") as file:
        file.write(f"{width}x{height}/{image_name}: {time_taken} seconds\n")
        file.write(f"Device: {os.uname()}\n")
        file.write(f"Date and Time: {time.ctime()}\n")
        file.write(f"Number of Images: {num_images}\n\n")

# Function to generate one image and save it
def generate_image_usingLibrary(image_name, width, height):
    img_size = (height, width)
    img = get_random_image(img_size)
    output_path = f"Images/{width}x{height}/{image_name}.png"
    matplotlib.image.imsave(output_path, img)
    print(f"Image {image_name}.png saved in {output_path}")
    print(f"Image size: {round(os.path.getsize(output_path)/1024/1024, 2)} MB")
    return output_path

# Function to ensure directory for images exists
def create_directory(width, height):
    directory = f"Images/{width}x{height}"
    os.makedirs(directory, exist_ok=True)
    print(f"Directory {directory} exists or was created.")

# Function to post images on Reddit
def post_to_reddit(image_path, subreddit, image_name, utc_time_str, image_hash):
    image_title = f"{utc_time_str} - {image_hash} - by Michael Wiciak (bot)"
    try:
        submission = subreddit.submit_image(title=image_title, image_path=image_path)
        if submission:
            print(f"Image '{image_name}' posted successfully!")
            return True
    except Exception as e:
        print(f"Error uploading '{image_name}': {e}")
    return False

# Main function combining everything
def main():
    # Validate and parse command-line arguments
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python <script_name>.py <image_name> <resolution> [num_images]")
        return
    
    image_name = sys.argv[1]
    if '.' in image_name:
        print("Invalid image name. Do not include the file extension.")
        return

    resolution = sys.argv[2].split('x')
    width, height = int(resolution[0]), int(resolution[1])
    
    if width <= 0 or height <= 0 or width > 3840 or height > 2532:
        print("Invalid resolution")
        return
    
    num_images = 1 if len(sys.argv) == 3 else int(sys.argv[3])
    
    # Create image directory
    create_directory(width, height)

    # Load Reddit API credentials from .env file
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )
    subreddit = reddit.subreddit('randimageMW')
    
    # Generate and post images
    start_time = time.time()
    for i in range(num_images):
        img_name = f"{image_name}_{i}" if num_images > 1 else image_name
        image_path = generate_image_usingLibrary(img_name, width, height)
        
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        utc_time_str = utc_now.strftime("%Y-%m-%d %H:%M:%S UTC")
        image_hash = generate_hash(image_path)
        
        if post_to_reddit(image_path, subreddit, img_name, utc_time_str, image_hash):
            uploaded_folder = f"Images/{width}x{height}/Uploaded"
            os.makedirs(uploaded_folder, exist_ok=True)
            shutil.move(image_path, os.path.join(uploaded_folder, f"{img_name}.png"))

    end_time = time.time()
    save_time(image_name, end_time - start_time, width, height, num_images)
    print(f"Finished generating and posting {num_images} images.")

if __name__ == "__main__":
    main()
