
def get_float_from_string(text):

    if text:
        words = text.split(' ')
        for word in words:
            try:
                return float(word)
            except:
                continue
    return None
