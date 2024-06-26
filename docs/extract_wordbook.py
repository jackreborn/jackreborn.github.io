import os
import re
import json

base_dir = "./_posts"

wordbook = {
    "words": []
}



def scan_dir(dir):
    for sub_dir_name in os.listdir(dir):
        sub_dir = f'{dir}/{sub_dir_name}'
        if os.path.isdir(sub_dir):
            scan_dir(sub_dir)
        else:
           if sub_dir.endswith(".md"):
               with open(sub_dir, "r", encoding="utf-8") as file:
                   for line in file.readlines():
                       words_prefix = "Words: "
                       if line.startswith(words_prefix):
                        content = line[len(words_prefix):]
                        regex = re.compile(r"([\w]+)(\(.+?\)){0,1}")
                        for match in regex.finditer(content):
                            hint = match.group(2)
                            if hint:
                                hint = hint[1:-1]
                            word = {
                                "word":  match.group(1),
                                "hint": match.group(2)
                            }
                            wordbook["words"].append(word)


if __name__ == "__main__":
    scan_dir(base_dir)

    if not os.path.exists("./assets/"):
        os.mkdir("./assets")

    with open("./assets/wordbook.json", "a", encoding="utf-8") as file:
        json.dump(wordbook, file)