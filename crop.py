import cv2

def crop_to_specific_size(input_path, output_path, width_cm=3, height_cm=4, dpi=300, slide_down=0.1, slide_up=0.2, resize_factor=0.4):
    # Load the image and resize it
    original_image = cv2.imread(input_path)
    resized_image = cv2.resize(original_image, None, fx=resize_factor, fy=resize_factor)

    # Convert the resized image to grayscale for face detection
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Load the Haarcascades face classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the resized image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        print("No faces detected in the image.")
        return

    # Assume the first face is the main subject
    x, y, w, h = faces[0]

    # Calculate the required pixel dimensions for the specified width and height at the specified DPI
    width_pixels = int(width_cm * dpi / 2.54)  # Convert cm to inches
    height_pixels = int(height_cm * dpi / 2.54)  # Convert cm to inches

    # Calculate the center of the detected face
    center_x, center_y = x + w // 2, y + h // 2

    # Calculate the cropping region to ensure the face is centered
    crop_x = max(center_x - width_pixels // 2, 0)

    # Calculate the cropping region for sliding down
    crop_y = min(center_y - height_pixels // 2 - int(height_pixels * slide_down), resized_image.shape[0] - height_pixels)

    # Adjust the top position based on the slide_up parameter
    crop_y += int(height_pixels * slide_up)

    # Crop the face to the specified width and height
    cropped_face = resized_image[crop_y:crop_y + height_pixels, crop_x:crop_x + width_pixels]

    # Set the DPI for the saved image
    dpi_value = (dpi, dpi)
    params = [int(cv2.IMWRITE_JPEG_QUALITY), 100]

    # Save the resized and cropped face with specified DPI
    cv2.imwrite(output_path, cropped_face, params=params)

# Example usage
input_image_path = "DSCF7526.jpg"
output_image_path = "y.jpg"
crop_to_specific_size(input_image_path, output_image_path)
