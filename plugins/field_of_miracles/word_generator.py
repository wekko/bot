try:
    import wikipedia
    loaded = True
except:
    loaded = False

import re

if __name__ == "__main__":
    if not loaded:
        print("NO WIKIPEDIA MODULE.\nPlease, install module 'wikipedia'.")

    else:
        wikipedia.set_lang("ru")
        wikipedia.set_rate_limiting(False)

        while True:
            try:
                p = wikipedia.page(wikipedia.random())
            except Exception as e:
                continue

            if p.summary.count(" — ") < 1:
                continue

            v = p.summary.split(" — ", 1)

            v[0] = re.sub(r"\(.+\)", "", v[0])
            v[1] = v[1][0].upper() + v[1][1:].replace("\n", "")

            if "," in v[0] or v[0].count(" ") > 2 or len(v[0]) < 12 or len(v[1]) > 120:
                continue

            print(f"    (\"{v[1].strip()}\", \"{v[0].strip().lower()}\"),")
