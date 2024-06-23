from PIL import Image, ImageDraw, ImageOps
import numpy as np
import sys

# Define the dot size variable at the top
DOT_SIZE = 10

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
  image = scale_image(image, 1024 * 2)
  c, m, y, k = image.split()

  c_dots = apply_dots(c, dot_size, 0, 0, "c")
  m_dots = apply_dots(m, dot_size, 2, 0, "m")
  y_dots = apply_dots(y, dot_size, 0, 2, "y")
  k_dots = apply_dots(k, dot_size, 2, 2, "k")

  cmyk_halftone = Image.merge("CMYK", (c_dots, m_dots, y_dots, k_dots))
  rgb_halftone = cmyk_halftone.convert("RGB")
  rgb_halftone.save(output_path)

# Run the updated script
halftone_cmyk_effect(sys.argv[1], "./updated.png", DOT_SIZE)

# Return the path to the new processed image
"/updated.png"