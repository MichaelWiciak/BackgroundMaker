import praw
import datetime

# Reddit API credentials from .env file, so fetch them
from dotenv import load_dotenv
import os

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

# Get current UTC time
utc_now = datetime.datetime.now(datetime.UTC)
utc_time_str = utc_now.strftime("%Y-%m-%d %H:%M:%S UTC")

# Path to the image
image_path = 'Images/2560x1600/17092024_1.png'
image_title = 'This image was uploaded on ' + utc_time_str + ' by Michael Wiciak (bot). Code found at https://github.com/MichaelWiciak/BackgroundMaker'

# Submit an image post with the current time as the title
subreddit.submit_image(title=image_title, image_path=image_path)

print("Image posted successfully!")
