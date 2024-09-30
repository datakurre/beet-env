from PIL import Image, ImageDraw

from beet import Context, Function, Texture


def beet_default(ctx: Context):
    # Create a simple function that runs when the data pack loads
    ctx.data["basic1:hello"] = Function(["say hello"], tags=["minecraft:load"])

    # Create an empty image of size 32x32
    img = Image.new("RGB", (32, 32))

    # Get the draw object to draw on the image
    draw = ImageDraw.Draw(img)

    # Define the rainbow colors (approximated)
    rainbow_colors = [
        (255, 0, 0),    # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (75, 0, 130),   # Indigo
        (148, 0, 211)   # Violet
    ]

    # Calculate the radius step based on the image size and number of colors
    center = (img.width // 2, img.height // 2)  # Center of the image
    max_radius = min(img.width, img.height) // 2  # Maximum radius
    radius_step = max_radius // len(rainbow_colors)  # Size of each ring

    # Draw concentric circles with decreasing radius for each color
    for i, color in enumerate(rainbow_colors):
        # Draw an ellipse (circle) with the calculated radius
        draw.ellipse(
            [
                (center[0] - (max_radius - i * radius_step), center[1] - (max_radius - i * radius_step)),
                (center[0] + (max_radius - i * radius_step), center[1] + (max_radius - i * radius_step))
            ],
            fill=color
        )

    # Assign the circular rainbow texture to the stone block in the resource pack
    ctx.assets["minecraft:block/stone"] = Texture(img)
