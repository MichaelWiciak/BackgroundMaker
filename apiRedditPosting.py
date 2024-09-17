import praw
import datetime
import os
import shutil
from dotenv import load_dotenv


import hashlib

def generate_hash(file_path):
    hash_algo = hashlib.sha1()

    # Open the image file in binary mode
    with open(file_path, "rb") as file:
        # Read the file in chunks to avoid memory issues with large files
        while chunk := file.read(4096):
            hash_algo.update(chunk)

    # Return the first 8 characters of the hash (adjust as necessary)
    return hash_algo.hexdigest()[:8]

def main():
    # Load Reddit API credentials from .env file
    load_dotenv()

    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    username = os.getenv('REDDIT_USERNAME')
    password = os.getenv('REDDIT_PASSWORD')
    user_agent = os.getenv('REDDIT_USER_AGENT')

    # Create a Reddit instance
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

    # Specify subreddit
    subreddit = reddit.subreddit('randimageMW')


    # Path to the folder containing images
    image_folder = 'UploadToRedditBatch'

    # Loop through all the files in the folder
    counter = 0
    for image_file in os.listdir(image_folder):
        if counter == 2:
            break
        # Make sure we only upload images (you can add other formats if needed but at the moment it only deals with .png) 
        if image_file.lower().endswith(('.png')):
            # Full path to the image
            image_path = os.path.join(image_folder, image_file)
            
            # get new utc time for each image
            utc_now = datetime.datetime.now(datetime.timezone.utc)
            utc_time_str = utc_now.strftime("%Y-%m-%d %H:%M:%S UTC")
            # Calculate the hash of the image
            image_hash = generate_hash(image_path)
            image_title = f"{image_hash} Image uploaded on {utc_time_str} by Michael Wiciak (bot)."
            
            try:
                # Submit the image
                submission = subreddit.submit_image(title=image_title, image_path=image_path)
                
                if submission:
                    print(f"Image '{image_file}' posted successfully!")
                    
                    # Move the file to a 'Uploaded' folder instead of deleting (optional safety step)
                    uploaded_folder = os.path.join(image_folder, 'Uploaded')
                    os.makedirs(uploaded_folder, exist_ok=True)
                    shutil.move(image_path, os.path.join(uploaded_folder, image_file))
                    
                else:
                    print(f"Failed to upload image '{image_file}'. Skipping deletion.")

            except Exception as e:
                print(f"Error uploading '{image_file}': {e}")
                continue  # Move to the next image if there's an error

        else:
            # Print that it found a file that doesnt meet the criteria, it has the following extension and file path
            print(f"Found a file that doesn't meet the criteria. It has the following extension: {os.path.splitext(image_file)[1]} and file path: {image_path}")

        counter += 1

    print(f"Processed {counter} images.")
    print("Done!")


if __name__ == '__main__':
    main()