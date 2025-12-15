import datetime
import math
import os
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

today = datetime.datetime.now().strftime("%Y%m%d")
total = len(msp_data)
width_n = 40
height_n = math.ceil(total / width_n)
icon_width, icon_height = 112, 112
css_width, css_height = 56, 56

IMAGE_TYPES = ["Normal", "Shiny"]

def draw_icon(icon: Image.Image, base: Image.Image, width: int, height: int, left: int, top: int):
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
  f".sprite-icon, .sprite-icon-shiny {{ display: inline-block; font-size: {css_width}px; width: 1em; height: 1em; background-repeat: no-repeat; background-size: {width_n}em auto; vertical-align: middle; }}\n"
  f".sprite-icon {{ background-image: url(//media.52poke.com/wiki/a/a2/MSP_Normal.webp?v={today}); }}\n"
  f".sprite-icon-shiny {{ background-image: url(//media.52poke.com/wiki/8/84/MSP_Shiny.webp?v={today}); }}\n"
  "\n"
)

x, y = 0, 0
for i, msp_icon in enumerate(msp_data):
  id_52pokes = msp_icon["神奇宝贝百科编号"].split("|")
  id_52poke = id_52pokes[0]
  css_class = ""
  for id  in id_52pokes:
    css_class += f", .sprite-icon-{id}"
    if re.search(r"^\d\d\d(?:\D.*)?$", id):
      css_class += f", .sprite-icon-0{id}"
  css_class = css_class[2:]

  css_output += f"{css_class} {{ background-position: -{x}em -{y}em; }}\n".replace("-0em", "0")

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
    if not file_path and image_type == "Shiny":
      _ = f"Addition/Normal/{id_52poke}.png"
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