from PIL import Image
import os

# Define the icon sizes required for a PWA application
icons = [
    {'size': (48, 48), 'name': 'maskable_icon_x48.png'},
    {'size': (72, 72), 'name': 'maskable_icon_x72.png'},
    {'size': (96, 96), 'name': 'maskable_icon_x96.png'},
    {'size': (128, 128), 'name': 'maskable_icon_x128.png'},
    {'size': (192, 192), 'name': 'maskable_icon_x192.png'},
    {'size': (192, 192), 'name': 'icon-192.png'},
    {'size': (192, 192), 'name': 'apple-touch-icon-192.png'},
    {'size': (192, 192), 'name': 'icon-maskable-192.png'},
    {'size': (384, 384), 'name': 'maskable_icon_x384.png'},
    {'size': (512, 512), 'name': 'maskable_icon_x512.png'},
    {'size': (512, 512), 'name': 'icon-512.png'},
    {'size': (512, 512), 'name': 'apple-touch-icon-512.png'},
    {'size': (512, 512), 'name': 'icon.png'},
    {'size': (512, 512), 'name': 'icon-maskable-512.png'},
    {'size': (512, 512), 'name': 'loading-animation.png'},
    {'size': (192, 192), 'name': 'icon-192.png'},
    {'size': (512, 512), 'name': 'maskable_icon.png'},
]

# Path to the source image
source_image_path = 'icon_generator/source_image.png'

# Output directory for the icons
output_directory = 'src/assets/icons'
output_directory_favicon = 'src/assets/'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Open the source image
try:
    with Image.open(source_image_path) as img:
        # Generate icons of different sizes
        for icon in icons:
            resized_img = img.resize(icon['size'])
            output_path = os.path.join(output_directory, icon['name'])
            resized_img.save(output_path)
        
        resized_img = img.resize((192, 192))
        output_path = os.path.join(output_directory_favicon, 'favicon.png')
        resized_img.save(output_path)
        print(f'Icon created: {output_path}')
        

except FileNotFoundError:
    print(f"Error: The source image was not found at '{source_image_path}'")
