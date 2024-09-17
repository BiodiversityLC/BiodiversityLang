import os
import json
import glob
import shutil
from typing import Optional, Dict, Any

def get_languages() -> list:
    """Retrieve all language directories, excluding .git and build."""
    return [f.name for f in os.scandir(".") if f.is_dir() and f.name not in [".git", "build"]]

def clean_build(buildDir: str):
    """Remove the build directory if it exists and recreate it."""
    if os.path.exists(buildDir):
        print("Cleaning old build.")
        shutil.rmtree(buildDir)

def build_language(language: str) -> Optional[Dict[str, Any]]:
    """Build a single language JSON by combining the main JSON and all .txt files."""
    print(f"Building: {language}")
    language_data_path = os.path.join(language, f"{language}.json")
    
    if not os.path.exists(language_data_path):
        print(f"Missing '{language}.json'!")
        return None
    
    try:
        with open(language_data_path, 'r', encoding='utf-8') as f:
            language_data = json.load(f)
    except Exception as e:
        print(f"Error reading '{language_data_path}': {e}")
        return None
    
    txt_files = glob.glob(os.path.join(language, "*.txt"))
    for text_file in txt_files:
        entry = os.path.splitext(os.path.basename(text_file))[0]
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                # Strip each line and join with newline character
                flattened_text = '\n'.join(line.strip() for line in lines)
                language_data[entry] = flattened_text
                print(f"Added entry '{entry}' from '{text_file}'")
                
        except Exception as e:
            print(f"Error reading '{text_file}': {e}")
            continue
        
    return language_data

def main():
    BUILD_DIR = "build"
    
    clean_build(BUILD_DIR)
    os.mkdir(BUILD_DIR)
    
    print("Getting languages")
    languages = get_languages()
    print(f"Found {len(languages)} language(s)! [ {', '.join(languages)} ]")
    
    defs: Dict[str, str] = {}
    for language in languages:
        language_data = build_language(language)
        if language_data is None:
            print(f"Skipping language '{language}' due to previous errors.")
            continue
        
        # Use '__name' key if it exists, else fallback to language identifier
        defs[language] = language_data.get("__name", language)
        language_data.pop("__name", None)
        
        # Write the language JSON with proper encoding and without ASCII escaping
        output_path = os.path.join(BUILD_DIR, f"{language}.json")
        try:
            with open(output_path, "w", encoding='utf-8') as f:
                 json.dump(language_data, f, indent=4, ensure_ascii=False)
            print(f"Successfully wrote {output_path}")
        except Exception as e:
            print(f"Error writing {output_path}: {e}")
            
    print("Finishing up.")
    
    # Write the defs.json file
    defs_path = os.path.join(BUILD_DIR, "defs.json")
    try:
        with open(defs_path, "w", encoding='utf-8') as f:
            json.dump(defs, f, ensure_ascii=False, indent=4)
        print(f"Successfully wrote {defs_path}")
    except Exception as e:
        print(f"Error writing {defs_path}: {e}")
        
    print("Done!")




if __name__ == "__main__":
	main()
