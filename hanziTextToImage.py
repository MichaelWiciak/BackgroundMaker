import hashlib
from PIL import Image, ImageDraw, ImageFont

def sha1_to_chinese(sha1):
    # Translate each character of SHA1 hash to Chinese.
    chinese_translation = ""
    for char in sha1:
        # Use a simple translation method, or an API for a better translation.
        chinese_char = chr(ord(char) + 12000)  # Simplified character conversion
        chinese_translation += chinese_char
    return chinese_translation

def add_text_to_image(image_path, sha1_hash):
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Convert SHA1 hash to Chinese
    chinese_text = sha1_to_chinese(sha1_hash)

    # print the Chinese text
    print(f"Chinese text: {chinese_text}")

    # Start with a large font size and dynamically reduce
    font_size = 300
    font_path = "/Library/Fonts/HanyiSentyPagoda Regular.ttf"  # Adjust the path to your font file

    
    # Calculate position to center the text
    x = (image.size[0]) // 2
    y = (image.size[1]) // 2

    # print the position
    print(f"Position: ({x}, {y})")

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Add the text to the image
    draw.text((x, y), chinese_text, font=font, fill="black")

    # Save the modified image
    output_path = image_path.replace(".png", "_with_text.png")
    image.save(output_path)
    print(f"Image saved at: {output_path}")

# Example usage
image_path = "Images/2560x1600/Blood.png"
sha1_hash = "7dc84205"
add_text_to_image(image_path, sha1_hash)
