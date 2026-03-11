import math

def entropy(x):
    r=0
    l=len(x)

    if any(znak.islower() for znak in x):
        r+=26 #małe litery
    if any(znak.isupper() for znak in x):
        r+=26 #duże litery
    if any(znak.isdigit() for znak in x):
        r+=10 #cyfry
    if any(not znak.isalnum() for znak in x):
        r+=32 #znaki specjalne (przyjmujemy 32 znaki specjalne)

    if r == 0  or l == 0:
        return 0
    else:
        e=math.log2(pow(r,l))
        if e < 28:
            ocena = "Bardzo Słabe"
        elif 28 <= e <= 35:
            ocena = "Słabe"
        elif 36 <= e <= 59:
            ocena = "Silne"
        elif 60 <= e <= 127:
            ocena = "Bardzo Silne"
        else:
            ocena = "Standard Wojskowy"
        return e, ocena

def dictionary_test(x): #sprawdzenie, czy hasło znajduje się w popularnych hasłach
    chk_x = x.lower()
    password_list = open("password_list.txt", "r")
    common_passwords = set(password_list.read().splitlines())
    if chk_x in common_passwords:
        return True
    return False

def pattern_test(x): #sprawdzenie, czy hasło zawiera łatwe do odgadnięcia wzorce
    x_lower = x.lower()

    # 1. Znane wzorce klawiaturowe i sekwencje
    patterns = [
        # sekwencje liczbowe
        "1234", "2345", "3456", "4567", "5678", "6789", "0123",
        # sekwencje liczbowe odwrócone
        "4321", "5432", "6543", "7654", "8765", "9876", "3210",
        # sekwencje klawiaturowe (wiersze)
        "qwer", "wert", "erty", "rtyu", "tyui", "yuio", "uiop",
        "asdf", "sdfg", "dfgh", "fghj", "ghjk", "hjkl",
        "zxcv", "xcvb", "cvbn", "vbnm",
        # sekwencje alfabetyczne
        "abcd", "bcde", "cdef", "defg", "efgh", "fghi",
        "ghij", "hijk", "ijkl", "jklm", "klmn", "lmno",
        "mnop", "nopq", "opqr", "pqrs", "qrst", "rstu",
        "stuv", "tuvw", "uvwx", "vwxy", "wxyz",
        # popularne wzorce
        "1111", "2222", "3333", "4444", "5555",
        "6666", "7777", "8888", "9999", "0000",
        "aaaa", "bbbb", "cccc",
        "abab", "1212", "admin", "pass", "login", "haslo"
    ]
    if any(p in x_lower for p in patterns):
        return True

    # 2. Wykrycie powtórzeń tego samego znaku (np. "aaa", "111")
    for i in range(len(x) - 2):
        if x[i] == x[i+1] == x[i+2]:
            return True

    # 3. Wykrycie sekwencji rosnącej/malejącej (np. "abc", "321")
    for i in range(len(x) - 2):
        if ord(x[i]) + 1 == ord(x[i+1]) and ord(x[i+1]) + 1 == ord(x[i+2]):
            return True
        if ord(x[i]) - 1 == ord(x[i+1]) and ord(x[i+1]) - 1 == ord(x[i+2]):
            return True

    return False

def regex_test(x, min_length=8):
    import re
    if len(x) < min_length:
        return False
    if (re.search(r'[a-z]', x) #sprawdzenie obecności małych liter
            and re.search(r'[A-Z]', x) #sprawdzenie obecności dużych liter
            and re.search(r'[0-9]', x) #sprawdzenie obecności cyfr
            and re.search(r'[^a-zA-Z0-9]', x)): #sprawdzenie obecności znaków specjalnych
        return True
    return False