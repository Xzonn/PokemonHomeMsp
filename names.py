import json
import os

l = filter(lambda x: x.startswith("poke_icon_"), os.listdir("input"))

with open("forms.csv", "r") as f:
  lines = map(lambda x: x.split(","), filter(lambda x: x, f.read().split("\n")[1:]))

form_data = {
  f"{int(x[0]):03d}-{int(x[1])}": x[2] for x in lines
}

g = open("forms2.csv", "w")
g.write("PokemonNo,FormNo,FormCode\n")

data = {
  "000": {
    "normal": "None.png"
  }
}
for i in l:
  names = i.split(".")[0].split("_")[2:]
  if names[5] == "b":
    continue
  if names[6] == "r":
    if not os.path.exists(f"input/poke_icon_{'_'.join(names[:6])}_n.png"):
      print(i, f"poke_icon_{'_'.join(names[:6])}_n.png")
  no, form, gender, isGiga, Alcremie, front, isShiny = names
  form_code = f"{int(no):03d}-{int(form)}"
  if form_code in form_data and form_data[form_code]:
    form_code = f"{int(no):03d}{form_data[form_code]}"
  elif int(form) == 0:
    form_code = f"{int(no):03d}"
  else:
    form_data[form_code] = f"-{int(form)}"
    g.write(f"{int(no)},{int(form)},\n")
  
  if gender == "fd":
    if os.path.exists(f"input/poke_icon_{no}_{form}_md_{isGiga}_{Alcremie}_{front}_{isShiny}.png"):
      form_code += "F"
  if isGiga == "g":
    form_code += "GM"
  elif int(no) == 869:
    form_code += ["S", "B", "L", "St", "C", "F", "R"][int(Alcremie)]
  if form_code == "000":
    form_code = "Egg"
  elif form_code == "000490E":
    form_code = "490E"
  
  if form_code not in data:
    data[form_code] = {}
  data[form_code]["normal" if isShiny == "n" else "shiny"] = i
  # print(",".join(names))

with open("form.json", "w", -1, "utf8") as f:
  json.dump(data, f, indent=1)

g.close()