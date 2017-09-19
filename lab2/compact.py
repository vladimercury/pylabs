import re
with open('file.txt', 'r') as file:
    regex = re.compile('[\s,]+')
    words = []
    for row in file:
        words += regex.split(row)
    dictionary = dict()
    for word in words:
        word_hash = ''.join(sorted(word))
        if word_hash not in dictionary:
            dictionary[word_hash] = set()
        dictionary[word_hash].add(word)
    for key, value in sorted(dictionary.items()):
        if len(value) > 1:
            print(list(sorted(value)))