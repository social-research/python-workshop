import string
import urllib.request

STOP_WORDS = ['a', 'about', 'across', 'after', 'an', 'and', 'any', 'are', 'as', 'at',
              'be', 'because', 'but', 'by', 'did', 'do', 'does', 'for', 'from',
              'get', 'has', 'have', 'if', 'in', 'is', 'it', 'its',
              'many', 'more', 'much', 'no', 'not', 'of', 'on', 'or', 'out',
              'so', 'some', 'than', 'the', 'this', 'that', 'those', 'through', 'to',
              'very', 'what', 'where', 'whether', 'which', 'while', 'who', 'with']


def get_text(fname):
    """Open file given as either directory location or url by fname
    and return text as a string.
    """
    if fname.startswith('http://') or fname.startswith('https://'):
        txt = ''
        for line in urllib.request.urlopen(fname):
            txt += line.decode("utf-8")
    else:
        with open(fname) as f:
            txt = f.read()
    return txt


def get_tokens(fname):
    """Read given text file and return a list with all words in lowercase
    in the order they appear in the text. Common contractions are expanded
    and hyphenated words are combined in one word.
    """
    # Open file
    txt = get_text(fname)

    # Remove paragraphs and format consistently
    txt = txt.strip().replace('\n', ' ').replace("’", "'")

    # Get rid of possessives and expand contractions
    txt = txt.replace("'s", '').replace("'ve", ' have').replace("'re", ' are')
    txt = txt.replace("can't", 'can not').replace("n't", ' not')

    # Remove punctuation and convert to lower-case
    exclude = set(string.punctuation) | {"”", "“", "…", '–'}
    txt = ''.join(ch.lower() for ch in txt if ch not in exclude)

    # Break into words
    wrds = txt.split()

    return wrds


def get_word_counts(tokens):
    """Take tokens and return a dictionary where keys are words
    and values are counts of the number of time the word is repeated.
    """
    # Create dictionary with word:count
    word_counts = {}

    for i in tokens:
        if i not in STOP_WORDS:
            if i not in word_counts:
                word_counts[i] = 1
            else:
                word_counts[i] += 1

    # Get the words with counts in decreasing order of popularity
    # Note this produces a list of tuples
    sorted_word_counts = sorted(word_counts.items(), key=lambda i: i[1], reverse=True)

    return sorted_word_counts
