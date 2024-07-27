def get_languages():
	import os
	return [ f.name for f in os.scandir(".") if f.is_dir() and f.name != ".git" and f.name != "build" ]

def clean_build(buildDir: str):
	import shutil, os

	if os.path.exists(buildDir):
		print("Cleaning old build.")
		shutil.rmtree(buildDir)

def main():
	import os, json
	BUILD_DIR = "build"

	clean_build(BUILD_DIR)
	os.mkdir(BUILD_DIR)

	print("Getting languages")
	languages = get_languages()
	print(f"Found {len(languages)} language(s)! [ {", ".join(languages)} ]")

	defs = {}

	for language in languages:
		language_data = build_language(language)
		defs[language] = language_data["__name"]
		del language_data["__name"]

		with open(os.path.join(BUILD_DIR, f"{language}.json"), "w+") as f:
			json.dump(language_data, f, indent=4)

	print("Finishing up.")

	with open(os.path.join(BUILD_DIR, "defs.json"), "w+") as f:
		json.dump(defs, f)

	print("Done!")

def build_language(language: str):
	import os, json, glob

	print(f"Building: {language}")

	langauge_data_path = os.path.join(language, f"{language}.json")
	if not os.path.exists(langauge_data_path):
		print(f"Missing '{language}.json'!")
		return
	
	with open(langauge_data_path) as f:
		language_data = json.load(f)

	for text in glob.glob(os.path.join(language, "*.txt")):
		entry = os.path.splitext(os.path.basename(text))[0]
		with open(text) as f:
			lines = f.readlines()
			flattened_text = '\n'.join(line.strip() for line in lines)

			language_data[entry] = flattened_text

	return language_data

	

if __name__ == "__main__":
	main()