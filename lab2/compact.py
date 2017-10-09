import re
with open('file.txt', 'r') as file:
    regex = re.compile('[\W]+')
    words = []
    for row in file:
        words += regex.split(row)
    dictionary = dict()
    for word in words:
        word_hash = ''.join(sorted(word))
        if word_hash not in dictionary:
            dictionary[word_hash] = set()
        dictionary[word_hash].add(word)
    dictionary = {key: value for key,value in dictionary.items() if len(value) > 1}
    for key, value in sorted(dictionary.items()):
        print(key + ":", list(sorted(value)), sep=" \t")