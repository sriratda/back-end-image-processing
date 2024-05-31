from PIL import Image, ImageDraw
import requests
from io import BytesIO

def add_blue_background(input_image_url, output_image_path):
    # Download the image from the URL
    response = requests.get(input_image_url)
    
    if response.status_code != 200:
        print(f"Failed to download image from {input_image_url}. Status code: {response.status_code}")
        return
    
    # Open the downloaded image
    image = Image.open(BytesIO(response.content))

    # Create a new image with a blue background
    new_image = Image.new("RGB", image.size, "blue")

    # Paste the original image onto the new image
    new_image.paste(image, (0, 0), image)

    # Save the result
    new_image.save(output_image_path)

if __name__ == "__main__":
    input_image_url = "https://replicate.delivery/pbxt/9dUxJ8S12LJlPhxWXRzWsMMjFLFe1iEjVtmw3PfEMWc1kcVSA/output.png"
    output_image_path = "image_with_blue_background.jpg"

    add_blue_background(input_image_url, output_image_path)
