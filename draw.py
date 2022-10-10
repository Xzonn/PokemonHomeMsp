import json
import math
from PIL import Image

with open("form.json", "r") as f:
  data = json.load(f)

total = len(data)
width_n = math.ceil(math.sqrt(total))
height_n = math.ceil(total / width_n)

normal = Image.new("RGBA", (width_n * 112, height_n * 112))
shiny = Image.new("RGBA", (width_n * 112, height_n * 112))

css = open("msp.css", "w", -1, "utf8")
css.write(f".sprite-icon {{ display: inline-block; width: 56px; height: 56px; background: url(normal.png) 9999px 9999px no-repeat; vertical-align: middle; background-size: {width_n * 112 // 2}px {height_n * 112 // 2}px; }}\n.sprite-icon-shiny {{ display: inline-block; width: 56px; height: 56px; background: url(shiny.png) 9999px 9999px no-repeat; vertical-align: middle; background-size: {width_n * 112 // 2}px {height_n * 112 // 2}px; }}\n\n")

no = 0
for k, v in data.items():
  y = no // width_n
  x = no - width_n * y
  left = x * 112
  top = y * 112
  css.write(f".sprite-icon-{k} {{ background-position: {-left // 2}{'px' if x else ''} {-top // 2}{'px' if y else ''}; }}\n")
  no += 1
  if "normal" in v:
    icon = Image.open(f"input/{v['normal']}")
    normal.paste(icon, (left, top))
  if "shiny" in v:
    icon = Image.open(f"input/{v['shiny']}")
    shiny.paste(icon, (left, top))

normal.save("normal.png")
shiny.save("shiny.png")
css.close()