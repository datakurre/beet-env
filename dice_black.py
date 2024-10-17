from beet import Context
from beet import Texture
from PIL import Image
from PIL import ImageDraw


# Function to draw a dice side with a specified number of dots (pips)
def draw_dice_side(pips, image_size=32, dot_size=6):
    # Create a new image with a white background
    img = Image.new("RGB", (image_size, image_size), color="black")
    draw = ImageDraw.Draw(img)

    # Predefined positions for the dots on the dice
    dot_positions = {
        1: [(image_size // 2, image_size // 2)],  # Center
        2: [
            (image_size * 1 // 4, image_size * 1 // 4),  # Top-left
            (image_size * 3 // 4, image_size * 3 // 4),  # Bottom-right
        ],
        3: [
            (image_size * 1 // 4, image_size * 1 // 4),  # Top-left
            (image_size // 2, image_size // 2),  # Center
            (image_size * 3 // 4, image_size * 3 // 4),  # Bottom-right
        ],
        4: [
            (image_size * 1 // 4, image_size * 1 // 4),  # Top-left
            (image_size * 3 // 4, image_size * 1 // 4),  # Top-right
            (image_size * 1 // 4, image_size * 3 // 4),  # Bottom-left
            (image_size * 3 // 4, image_size * 3 // 4),  # Bottom-right
        ],
        5: [
            (image_size * 1 // 4, image_size * 1 // 4),  # Top-left
            (image_size * 3 // 4, image_size * 1 // 4),  # Top-right
            (image_size * 1 // 4, image_size * 3 // 4),  # Bottom-left
            (image_size * 3 // 4, image_size * 3 // 4),  # Bottom-right
            (image_size // 2, image_size // 2),  # Center
        ],
        6: [
            (image_size * 1 // 4, image_size * 1 // 4),  # Top-left
            (image_size * 3 // 4, image_size * 1 // 4),  # Top-right
            (image_size * 1 // 4, image_size // 2),  # Middle-left
            (image_size * 3 // 4, image_size // 2),  # Middle-right
            (image_size * 1 // 4, image_size * 3 // 4),  # Bottom-left
            (image_size * 3 // 4, image_size * 3 // 4),  # Bottom-right
        ],
    }

    # Draw black dots (representing the pips of the dice)
    for pos in dot_positions.get(pips, []):
        x, y = pos
        draw.ellipse(
            (
                x - dot_size // 2,
                y - dot_size // 2,
                x + dot_size // 2,
                y + dot_size // 2,
            ),
            fill="white",
        )

    return img


def beet_default(ctx: Context):
    # Create dice textures for each side of the die
    dice_sides = {
        1: draw_dice_side(1),
        2: draw_dice_side(2),
        3: draw_dice_side(3),
        4: draw_dice_side(4),
        5: draw_dice_side(5),
        6: draw_dice_side(6),
    }

    # Example: Assigning each dice side to a different block texture in Minecraft
    ctx.assets["minecraft:block/dice_black/1"] = Texture(dice_sides[1])
    ctx.assets["minecraft:block/dice_black/2"] = Texture(dice_sides[2])
    ctx.assets["minecraft:block/dice_black/3"] = Texture(dice_sides[3])
    ctx.assets["minecraft:block/dice_black/4"] = Texture(dice_sides[4])
    ctx.assets["minecraft:block/dice_black/5"] = Texture(dice_sides[5])
    ctx.assets["minecraft:block/dice_black/6"] = Texture(dice_sides[6])
