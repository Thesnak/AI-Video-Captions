from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon(size=(512, 512)):
    """Create a modern, minimalist app icon for video captioning"""
    # Create a new image with a gradient background
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Create a gradient background
    for y in range(size[1]):
        r = int(255 * (1 - y / size[1]))
        g = int(200 * (1 - y / size[1]))
        b = int(100 * (1 - y / size[1]))
        for x in range(size[0]):
            draw.point((x, y), fill=(r, g, b, 255))
    
    # Draw video and caption symbol
    center_x, center_y = size[0] // 2, size[1] // 2
    
    # Video camera icon
    draw.polygon([
        (center_x - 100, center_y - 80),
        (center_x + 100, center_y - 80),
        (center_x + 100, center_y + 80),
        (center_x - 100, center_y + 80)
    ], outline=(255, 255, 255, 255), width=10)
    
    # Subtitle symbol
    draw.rectangle([
        (center_x - 150, center_y + 120),
        (center_x + 150, center_y + 200)
    ], fill=(255, 255, 255, 200))
    
    draw.text(
        (center_x, center_y + 160), 
        "Captions", 
        fill=(0, 0, 0, 255), 
        anchor="mm"
    )
    
    # Save icon
    os.makedirs('assets', exist_ok=True)
    image.save('assets/app_icon.png')
    image.save('assets/splash_screen.png')

def main():
    create_app_icon()
    print("Assets generated successfully!")

if __name__ == "__main__":
    main()