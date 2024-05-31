from flask import Flask, send_file, render_template, url_for, request, redirect, jsonify
from werkzeug.utils import secure_filename
import replicate
import os
import cv2
from flask_cors import CORS
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import base64

os.environ['REPLICATE_API_TOKEN'] = 'r8_X2gjDZWF6YNkHfYmoAmLOjIy5E2e98w3gnt9W'

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/')
def index():
       # Replace 'image1.png' and 'image2.png' with the actual filenames and 'img' with the correct directory
    image1_filename = 'outputOfModel.png'
    image2_filename = 'output_collage.jpg'
    
    image1_path = os.path.join('img', image1_filename)
    image2_path = os.path.join('img', image2_filename)

    # Check if the image files exist
    if os.path.exists(image1_path) and os.path.exists(image2_path):
        return render_template('index.html', image1_path=image1_path, image2_path=image2_path)
    else:
        return 'Image not found'

@app.route('/image')
def get_image1():
    # Replace 'image1.png' with the actual filename and 'img' with the correct directory
    image1_filename = 'outputOfModel.png'
    image1_path = os.path.join('img', image1_filename)

    # Check if the image file exists
    if os.path.exists(image1_path):
        return send_file(image1_path, mimetype='image/png')
    else:
        return 'Image not found'

@app.route('/image1')
def get_image2():
    # Replace 'image2.png' with the actual filename and 'img' with the correct directory
    image2_filename = 'output_collage.jpg'
    image2_path = os.path.join('img', image2_filename)

    # Check if the image file exists
    if os.path.exists(image2_path):
        return send_file(image2_path, mimetype='image/jpg')
    else:
        return 'Image not found'


@app.route('/image2')
def get_image3():
    # Replace 'image2.png' with the actual filename and 'img' with the correct directory
    image2_filename = 'test1.jpg'
    image2_path = os.path.join('img', image2_filename)

    # Check if the image file exists
    if os.path.exists(image2_path):
        return send_file(image2_path, mimetype='image/jpg')
    else:
        return 'Image not found'


@app.route("/", methods=["POST", "GET"])
def upload_image():
    if request.method == 'POST':
        print("JSON Body:", request.form['size'])
        if 'image' not in request.files:
            return jsonify({'error': 'No image part in the request'}), 400
        input = request.files["image"]
        sizeImage = float(request.form["size"])
        print("Size:", sizeImage)
        input.save("img/test1.jpg")
        model("img/test1.jpg", sizeImage)
        base64_string1 = encode_image_to_base64("img/outputOfModel.png")
        base64_string2 = encode_image_to_base64("img/output_collage.jpg")
        return jsonify({
            'message': 'Files uploaded and processed successfully',
            'image1_base64': base64_string1,
            'image2_base64': base64_string2
        })
    else:
        # Assuming you want to handle GET differently or just return a simple message
        return jsonify({'message': 'Send a POST request with an image'}), 200
    #     model("img/test1.jpg")
    #     return redirect('/')
    # else:
    #     return render_template("index.html")
  

def model(inputImage, sizeImage):
    # Example usage
    input_image_path = inputImage
    output_path = "img/cropped_id_picture.jpg"

    # Crop to specific width (3 cm) and height (4 cm) with slide_down=0.1 and slide_up=0.1
    crop_to_specific_size(input_image_path, output_path, sizeImage)


    image = open(output_path, "rb")

    output1 = replicate.run(
        "tencentarc/gfpgan:297a243ce8643961d52f745f9b6c8c1bd96850a51c92be5f43628a0d3e08321a",
        input={
            "img": image,
            "scale": 2,
            "version": "v1.4"
        }
    )

    output2 = replicate.run(
        "lucataco/remove-bg:95fcc2a26d3899cd6c2691c900465aaeff466285a65c14638cc5f36f34befaf1",
        input={
        "image": output1
        }
    )

    # delete_image()

    input_image_url = output2
    output_image_path = "img/outputOfModel.png"

    add_blue_background(input_image_url, output_image_path)

    input_picture_paths = ['img\outputOfModel.png', 'img\outputOfModel.png', 'img\outputOfModel.png',
                            'img\outputOfModel.png', 'img\outputOfModel.png', 'img\outputOfModel.png',
                            'img\outputOfModel.png', 'img\outputOfModel.png', 'img\outputOfModel.png']
    
    # Replace 'output_collage.jpg' with your desired output file path
    output_collage_path = 'img\output_collage.jpg'

    # Specify the target size in pixels for the resized images

    if sizeImage == 1.0:
        target_size = (421, 421)  # Adjust as needed
    else:
        target_size = (471, 471)

    

    # Resize and arrange the images in a 2x3 grid on a 4x6 inch white background
    resize_and_arrange_images(input_picture_paths, output_collage_path, target_size)


    print(output2)

def encode_image_to_base64(filepath):
    """Helper function to encode an image file to a base64 string."""
    with open(filepath, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def delete_image():
    image_filename = 'cropped_id_picture.jpg'  # Retrieve filename from request
    folder_path = 'img'  # Replace with your actual folder path
    image_path = os.path.join(folder_path, image_filename)

    os.remove(image_path)

def resize_and_arrange_images(input_paths, output_path, target_size):
    # Create a blank white background of 4x6 inch size
    new_img = Image.new("RGB", (4*300, 6*300), "white")

    # Calculate the width and height for each individual image in the 2x3 grid
    img_width = new_img.width // 2
    img_height = new_img.height // 3

    for i, input_path in enumerate(input_paths):
        with Image.open(input_path) as img:
            # Resize the image while maintaining its aspect ratio
            img.thumbnail(target_size)

            # Calculate the position to paste the resized image
            col = i % 3
            row = i // 3
            x = col * img_width + (img_width - img.width) // 2
            y = row * img_height + (img_height - img.height) // 2

            # Paste the resized image onto the white background
            new_img.paste(img, (x, y))

    # Save the result
    new_img.save(output_path, dpi=(300, 300))



def crop_to_specific_size(input_path, output_path, sizeImage, dpi=300):
    # Define size parameters based on sizeImage
    # if sizeImage == 1:
    width_cm, height_cm = 2.8, 3.5
    # elif sizeImage == 1.5:
    #     width_cm, height_cm = 3, 4
    # else:  # Default to largest size
    # width_cm, height_cm = 4.2, 5.5

    slide_down = 0.1
    slide_up = 0.2
    resize_factor = 0.4

    # Load the image
    original_image = cv2.imread(input_path)
    if original_image is None:
        print(f"Failed to load image at path: {input_path}")
        return

    resized_image = cv2.resize(original_image, None, fx=resize_factor, fy=resize_factor)
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        print("No faces detected in the image.")
        return

    x, y, w, h = faces[0]
    width_pixels = int(width_cm * dpi / 2.54)
    height_pixels = int(height_cm * dpi / 2.54)
    center_x = x + w // 2
    center_y = y + h // 2
    crop_x = max(center_x - width_pixels // 2, 0)
    crop_y = min(center_y - height_pixels // 2 - int(height_pixels * slide_down), resized_image.shape[0] - height_pixels)
    crop_y += int(height_pixels * slide_up)
    cropped_face = resized_image[crop_y:crop_y + height_pixels, crop_x:crop_x + width_pixels]

    if cropped_face.size == 0:
        print("Cropping resulted in an empty image.")
        return

    cv2.imwrite(output_path, cropped_face, [int(cv2.IMWRITE_JPEG_QUALITY), 100])




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
    new_image.save(output_image_path,format='JPEG')


if __name__ == "__main__":
    app.run(debug=True)
