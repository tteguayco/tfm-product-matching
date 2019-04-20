
def word2features(product_title, i):
    '''
    A product title is received as a list of words (i.e. strings).
    '''
    word = product_title[i]

    features = {
        'word.lower()': word.lower(),
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'word.isalpha()': word.isalpha(),
        'word.containsdigit()': any(char.isdigit() for char in word),
        'word.containsNonAlphanumericChars()': not word.isalnum(),
    }
    
    # The word is not the beggining of a product title
    if i > 0:
        preceding_word = product_title[i-1]
        features.update({
            '-1:word.lower()': preceding_word.lower(),
            '-1:word.istitle()': preceding_word.istitle(),
            '-1:word.isupper()': preceding_word.isupper(),
        })
        
    # The word is the beginning of a product title
    else:
        features['BOT'] = True

    # The word is not the end of a product title
    if i < len(product_title) - 1:
        subsequent_word = product_title[i+1]
        features.update({
            '+1:word.lower()': subsequent_word.lower(),
            '+1:word.istitle()': subsequent_word.istitle(),
            '+1:word.isupper()': subsequent_word.isupper(),
        })
        
    # The word is not the end of a product title
    else:
        features['EOT'] = True

    return features

def title2features(product_title):
    return [word2features(product_title, i) for i in range(len(product_title))]
