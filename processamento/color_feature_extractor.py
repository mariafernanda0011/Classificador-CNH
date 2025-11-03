import colorgram
import argparse
import sys
from PIL import Image, ImageDraw, ImageFont


def get_colors(image_file, numcolors=6):
    # Extract dominant colors from an image.
    colors = colorgram.extract(image_file, numcolors)
    return colors

def save_palette(colors, swatchsize=100, outfile="palette.png"):
    num_colors = len(colors)
    image_palette = Image.new('RGB', (swatchsize * num_colors, swatchsize))
    print(image_palette)

    draw = ImageDraw.Draw(image_palette)
    font = ImageFont.truetype('font/lmmonoproplt10-bold.otf', 15)
    posx = 0
    count_color = 0
    for color in colors:
        txt = str(color.rgb.r) + "," + str(color.rgb.g) + "," + str(
            color.rgb.b)
        print(
            f"Color {count_color}: ({color.rgb.r},{color.rgb.g},{color.rgb.b})")
        
        draw.rectangle([posx, 0, posx + swatchsize, swatchsize],
                       fill=(color.rgb.r, color.rgb.g, color.rgb.b))
    
    draw.text((posx + 10, 0, posx + swatchsize), txt, font=font)
    posx = posx + swatchsize
    count_color = count_color + 1
    image_palette.show()
    image_palette.save(outfile, "PNG")


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    colors = get_colors(input_file)
    save_palette(colors, outfile=output_file)
