"""Simple Prefix Tree, or Trie, implementation, e.g. for finding valid
scrabble words.
"""

def make_trie(words):
    res = {}
    for word in words:
        d = res
        for c in word:
            d = d.setdefault(c, {})
        d["."] = None
    return res

def find_words(trie, letters, prefix=""):
    if "." in trie:
        yield prefix
    for i, c in enumerate(letters):
        if c in trie:
            rest = letters[:i] + letters[i+1:]
            for res in find_words(trie[c], rest, prefix + c):
                yield res

words = ["cat", "cats", "act", "car", "carts", "cash"]
trie = make_trie(words)
print(trie)
print(set(find_words(trie, "acst")))

# http://www.3zsoftware.com/download/
with open("sowpods.txt") as words:
    trie = make_trie(map(str.strip, words))
    res = set(find_words(trie, "SMOKEJACK"))
    print(len(res))

