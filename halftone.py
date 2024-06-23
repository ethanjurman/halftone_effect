from PIL import Image, ImageDraw, ImageOps
import numpy as np
import sys

IMAGE = './image.png'
OUTPUT = './updated.png'
DOT_SIZE = 10
OUTPUT_SIZE = 2048
SHIFT_SIZE = 2

if (len(sys.argv) > 1):
  IMAGE = sys.argv[1]
if (len(sys.argv) > 2):
  OUTPUT = sys.argv[2]
if (len(sys.argv) > 3):
  DOT_SIZE = int(sys.argv[3])
if (len(sys.argv) > 4):
  OUTPUT_SIZE = int(sys.argv[4])
if (len(sys.argv) > 5):
  SHIFT_SIZE = int(sys.argv[5])

def apply_dots(channel, dot_size, shift_x, shift_y, channel_name):
  width, height = channel.size
  halftone_channel = Image.new("L", (width, height), 255)
  draw = ImageDraw.Draw(halftone_channel)
  pixels = np.array(channel)
  
  for y in range(shift_y, height - dot_size, dot_size):
    for x in range(shift_x, width - dot_size, dot_size):
      block = pixels[y:y + dot_size, x:x + dot_size]
      avg_brightness = np.mean(block)
      radius = (1 - avg_brightness / 255) * (dot_size / 1.6)
      bbox = [x, y, x + 2 * radius, y + 2 * radius]
      draw.ellipse(bbox, fill=0) if avg_brightness > 10 else draw.rectangle(bbox, fill=0)
  
  return halftone_channel

def scale_image(image, target_width=1024):
  width, height = image.size
  if width < target_width:
    scaling_factor = target_width / width
    new_height = int(height * scaling_factor)
    image = image.resize((target_width, new_height), Image.ADAPTIVE)
  return image

def halftone_cmyk_effect(image_path, output_path, dot_size):
  image = Image.open(image_path).convert("CMYK")
  image = scale_image(image, OUTPUT_SIZE)
  c, m, y, k = image.split()

  c_dots = apply_dots(c, dot_size, 0, 0, "c")
  m_dots = apply_dots(m, dot_size, SHIFT_SIZE, 0, "m")
  y_dots = apply_dots(y, dot_size, 0, SHIFT_SIZE, "y")
  k_dots = apply_dots(k, dot_size, SHIFT_SIZE, SHIFT_SIZE, "k")

  cmyk_halftone = Image.merge("CMYK", (c_dots, m_dots, y_dots, k_dots))
  rgb_halftone = cmyk_halftone.convert("RGB")
  rgb_halftone.save(output_path)

# Run the updated script
halftone_cmyk_effect(IMAGE, OUTPUT, DOT_SIZE)

# Return the path to the new processed image
"/updated.png"