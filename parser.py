import re
hello = ['привет', 'здравствуй', 'здравствуйте', 'hello', 'приветствую']

class Request:
    artist = ''
    album = ''
    date = 0

    def show(self):
        return 'sample text'


key_words = ['последний', 'последние', 'последняя',
             'топ', 'лучший', 'лучшие', 'лучшая',
             'трек', 'песня', 'трэк',
             'альбом', 'сингл']


# the Levenstein distance algorithm
def distance(a: object, b: object) -> object:
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def main_func(s):
    user_request = Request()
    s = re.sub(r'[^\w\s]', '', s)
    s_splitted = s.split()
    for _ in range(len(s_splitted)):
        s_splitted[_] = s_splitted[_].lower()
        if represents_int(s_splitted[_]):
            if 1990 < s_splitted < 2016:
                user_request.date = int(s_splitted[_])
                s_splitted.pop(_)
    return s_splitted

def check_hello(s):
    i = 0
    for _ in range(len(hello)):
        if hello[_] in main_func(s):
            print('Добрейший вечерочек!')
            break

user_string = input()
check_hello(user_string)
