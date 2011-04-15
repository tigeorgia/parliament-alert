def en_or_ka(english,text):
    en = english.split("|")
    key = text.split(" ")[0]
    if key in en:
        return "en"
    else:
        return "ka"
