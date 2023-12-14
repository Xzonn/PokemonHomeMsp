import os
import math
import re
from PIL import Image

with open("MSP顺序.txt", "r", -1, "utf8") as reader:
  lines = reader.read().split("\n")
  header = lines[0].split("\t")

msp_data = [
  dict(zip(header, i.split("\t"))) for i in lines[1:] if i
]

with open("PH对照表.txt", "r", -1, "utf8") as reader:
  lines = reader.read().split("\n")
  header = lines[0].split("\t")

_ = [
  dict(zip(header, i.split("\t"))) for i in lines[1:] if i
]
ph_data = {
  i["神奇宝贝百科编号"]: i for i in _
}

total = len(msp_data)
width_n = 40
height_n = math.ceil(total / width_n)
icon_width, icon_height = 112, 112
css_width, css_height = 56, 56

IMAGE_TYPES = ["Normal", "Shiny"]

def draw_icon(icon: Image, base: Image, width: int, height: int, left: int, top: int):
  if icon.width != width or icon.height != height:
    new_icon_width = max(width, icon.width)
    new_icon_height = max(height, icon.height)
    new_icon = Image.new("RGBA", (new_icon_width, new_icon_height))
    l = (new_icon_width - icon.width) // 2
    t = (new_icon_height - icon.height) // 2
    new_icon.paste(icon, (l, t))
    icon = new_icon.resize((width, height), Image.Resampling.BICUBIC)
  base.paste(icon, (left, top))

files = {}
for image_type in IMAGE_TYPES:
  image = Image.new("RGBA", (width_n * icon_width, height_n * icon_height))
  files[image_type] = image

css_output = (
  f".sprite-icon {{ display: inline-block; width: {css_width}px; height: {css_height}px; background: url(//media.52poke.com/wiki/a/a2/MSP_Normal.webp) 9999px 9999px no-repeat; vertical-align: middle; background-size: {width_n * css_width}px {height_n * css_height}px; }}\n"
  f".sprite-icon-shiny {{ display: inline-block; width: {css_width}px; height: {css_width}px; background: url(//media.52poke.com/wiki/8/84/MSP_Shiny.webp) 9999px 9999px no-repeat; vertical-align: middle; background-size: {width_n * css_width}px {height_n * css_height}px; }}\n"
  "\n"
)

x, y = 0, 0
for i, msp_icon in enumerate(msp_data):
  id_52poke = msp_icon["神奇宝贝百科编号"]
  css_class = f".sprite-icon-{id_52poke}"
  if re.search(r"^\d\d\d(?:\D.*)?$", id_52poke):
    css_class += f", .sprite-icon-0{id_52poke}"
  if id_52poke == "128PC":
    css_class += ", .sprite-icon-128P, .sprite-icon-0128P"
  css_output += f"{css_class} {{ background-position: -{x * css_width}px -{y * css_width}px; }}\n"

  for image_type in IMAGE_TYPES:
    file_path = None
    _ = f"Addition/{image_type}/{id_52poke}.png"
    if os.path.exists(_):
      file_path = _
    elif id_52poke in ph_data:
      _ = "poke_capture_" + ph_data[id_52poke]["文件名"] + ".png"
      if image_type == "Shiny":
        _ = _.replace("_n.png", "_r.png")
      _ = f"PH/{image_type}/{_}"
      if os.path.exists(_):
        file_path = _
    if not file_path:
      continue
    icon = Image.open(file_path)
    draw_icon(icon, files[image_type], icon_width, icon_height, x * icon_width, y * icon_height)
  
  x += 1
  if x >= width_n:
    x = 0
    y += 1

with open(f"Msp.css", "w", -1, "utf8") as writer:
  writer.write(css_output.replace("-0px", "0"))

for image_type in files:
  files[image_type].save(f"MSP_{image_type}.webp", quality=50, method=6, lossless=False)