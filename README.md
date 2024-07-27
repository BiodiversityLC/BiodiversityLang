# BiodiversityLang
Translations for Biodiversity.

## New Language
Duplicate an existing folder, rename it to a short internal letter code and ensure that the containing `.json` file is renamed to the same 2 letter code. Then edit the `__name` attribute to the name of the language and you can begin translating.

## Testing In-Game
To make sure everything is formatted correctly, the python script `build.py` handles converting the language translations into the format the mod reads.
For changes to existing languages, simply copying the `build` directory after running the script into the `lang` folder of the mod directory will update it.
For new languages it requires the mod `.dll` to be rebuilt (`defs.json` is contained inside the dll). As a workaround you can replace the contents of `en.json` in the `lang` folder with `<your language>.json` and test like that.