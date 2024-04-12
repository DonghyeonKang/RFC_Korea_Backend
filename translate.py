import googletrans

def translate(content):
    translator = googletrans.Translator()
    result = translator.translate(content, dest='ko')
    return result