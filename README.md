用于 [神奇宝贝百科](https://wiki.52poke.com/) 创建 [MediaWiki:Gadget-msp.css](https://wiki.52poke.com/wiki/MediaWiki:Gadget-msp.css)、[MSP_Normal.webp](https://s0.52poke.wiki/wiki/a/a2/MSP_Normal.webp)、[MSP_Shiny.webp](https://s0.52poke.wiki/wiki/8/84/MSP_Shiny.webp)。

## 用法

1. clone 本项目，安装依赖项。
2. 提取《Pokémon HOME》的 romfs，将`romfs:/pokemon/icon_pokemon/bin/icon_pokemon.arc`中包含的宝可梦小图标导出为 png 格式，非异色图标放入`PH/Normal/`文件夹中，异色图标放入`PH/Shiny/`文件夹中。
3. 将所有不包含于《Pokémon HOME》的图标按照神奇宝贝百科的编号导出为 png 格式，非异色图标放入`Addition/Normal/`文件夹中，异色图标放入`Addition/Shiny/`文件夹中。
4. 运行`main.py`。