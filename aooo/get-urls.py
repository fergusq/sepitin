import unidecode
import re

with open("index/novellit.tsv", "r") as f:
    for line in f:
        [name, url] = line.strip().split("\t")
        number = url[len("/works/"):]
        if "podfic" in name.lower():
            continue
            
        name = name.replace("&#39;", "'").replace("&#34;", "\"")

        included_words = []
        words = name.split(" ")
        for word in words:
            if len("".join(included_words) + word) > 22:
                break

            included_words.append(word)
        
        name = " ".join(included_words)


        name = unidecode.unidecode(name)
        name = re.sub(r"[^a-zA-Z0-9 ]", "", name).replace(" ", "%20")
        download_url = f"https://archiveofourown.org/downloads/{number}/{name}.html"
        print(download_url)