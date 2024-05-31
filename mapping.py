from PIL import Image

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

if __name__ == "__main__":
    input_picture_paths = ['img\outputOfModel.png', 'img\outputOfModel.png', 'img\outputOfModel.png',
                            'img\outputOfModel.png', 'img\outputOfModel.png', 'img\outputOfModel.png',
                            'img\outputOfModel.png', 'img\outputOfModel.png', 'img\outputOfModel.png']
    
    # Replace 'output_collage.jpg' with your desired output file path
    output_collage_path = 'img\output_collage.jpg'

    # Specify the target size in pixels for the resized images
    target_size = (471, 471)  # Adjust as needed

    # Resize and arrange the images in a 2x3 grid on a 4x6 inch white background
    resize_and_arrange_images(input_picture_paths, output_collage_path, target_size)
