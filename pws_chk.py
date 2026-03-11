import math
import requests
import hashlib

def format_time(seconds):
    if seconds < 0.001:
        return "natychmiast"
    if seconds < 1:
        return f"{seconds:.3f} sekund"
    if seconds < 60:
        return f"{seconds:.1f} sekund"
    if seconds < 3600:
        return f"{seconds / 60:.1f} minut"
    if seconds < 86400:
        return f"{seconds / 3600:.1f} godzin"
    if seconds < 86400 * 365:
        return f"{seconds / 86400:.1f} dni"
    if seconds < 86400 * 365 * 1000:
        return f"{seconds / (86400 * 365):.1f} lat"
    if seconds < 86400 * 365 * 1e6:
        return f"{seconds / (86400 * 365 * 1000):.1f} tysięcy lat"
    if seconds < 86400 * 365 * 1e9:
        return f"{seconds / (86400 * 365 * 1e6):.1f} milionów lat"
    if seconds < 86400 * 365 * 1e12:
        return f"{seconds / (86400 * 365 * 1e9):.1f} miliardów lat"
    return f"{seconds / (86400 * 365 * 1e12):.1f} bilionów lat"

def entropy(pwd):
    r=0
    l=len(pwd)

    if any(znak.islower() for znak in pwd):
        r+=26 #małe litery
    if any(znak.isupper() for znak in pwd):
        r+=26 #duże litery
    if any(znak.isdigit() for znak in pwd):
        r+=10 #cyfry
    if any(not znak.isalnum() for znak in pwd):
        r+=32 #znaki specjalne (przyjmujemy 32 znaki specjalne)

    if r == 0  or l == 0:
        return 0
    else:
        e=math.log2(pow(r,l))
        if e < 28:
            grade = "Bardzo Słabe"
        elif 28 <= e <= 35:
            grade = "Słabe"
        elif 36 <= e <= 59:
            grade = "Silne"
        elif 60 <= e <= 127:
            grade = "Bardzo Silne"
        else:
            grade = "Standard Wojskowy"

        t = pow(r,l) / (3 * pow(10,11)) #przyblizony czas złamania hasła w sekundach, przez karte graficzna rtx 5090
        return e, grade, format_time(t)

def dictionary_test(pwd): #sprawdzenie, czy hasło znajduje się w popularnych hasłach
    chk_pwd = pwd.lower()
    with open("password_list.txt", "r") as password_list:
        common_passwords = set(p.lower() for p in password_list.read().splitlines())

    #Sprawdzenie czy całe hasło jest w słowniku
    if chk_pwd in common_passwords:
        return True

    #Sprawdzenie czy któreś słowo ze słownika jest częścią hasła
    for common in common_passwords:
        if len(common) >= 4 and common in chk_pwd:
            return True

    # Sprawdzenie czy jakaś część hasła jest w słowniku
    min_len = 4
    for i in range(len(chk_pwd)):
        for j in range(i + min_len, len(chk_pwd) + 1):
            substring = chk_pwd[i:j]
            if substring in common_passwords:
                return True

    return False

def pattern_test(pwd): #sprawdzenie, czy hasło zawiera łatwe do odgadnięcia wzorce
    pwd_lower = pwd.lower()

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
    if any(p in pwd_lower for p in patterns):
        return True

    # 2. Wykrycie powtórzeń tego samego znaku (np. "aaa", "111")
    for i in range(len(pwd) - 2):
        if pwd[i] == pwd[i + 1] == pwd[i + 2]:
            return True

    # 3. Wykrycie sekwencji rosnącej/malejącej (np. "abc", "321")
    for i in range(len(pwd) - 2):
        if ord(pwd[i]) + 1 == ord(pwd[i + 1]) and ord(pwd[i + 1]) + 1 == ord(pwd[i + 2]):
            return True
        if ord(pwd[i]) - 1 == ord(pwd[i + 1]) and ord(pwd[i + 1]) - 1 == ord(pwd[i + 2]):
            return True

    return False

def regex_test(pwd, min_length=8):
    import re
    if len(pwd) < min_length:
        return False
    if (re.search(r'[a-z]', pwd) #sprawdzenie obecności małych liter
            and re.search(r'[A-Z]', pwd) #sprawdzenie obecności dużych liter
            and re.search(r'[0-9]', pwd) #sprawdzenie obecności cyfr
            and re.search(r'[^a-zA-Z0-9]', pwd)): #sprawdzenie obecności znaków specjalnych
        return True
    return False

def pwnd_pswd(pwd):
    hash_sha1 = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    prefix = hash_sha1[:5]
    suffix = hash_sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    header = {
        'User-Agent': 'Password_checker'
    }
    
    try:
        # Przekazujemy nagłówki do zapytania
        response = requests.get(url, headers=header)

        if response.status_code != 200:
            return 0

        for linia in response.text.splitlines():
            finded_suffix, counted_data = linia.split(':')
            if finded_suffix == suffix:
                return int(counted_data)
        return 0

    except requests.exceptions.RequestException:
        return 0


def levenshtein(s, t): #algortym odleglosci skonczonych ciagow znakow
    m = len(s) #dlugosc danych do porwnania z haslem
    n = len(t) #dlugosc hasla

    d = [[0] * (n + 1) for _ in range(m + 1)] #macierz zer

    # Inicjalizacja pierwszej kolumny
    for i in range(m + 1):
        d[i][0] = i

    # Inicjalizacja pierwszego wiersza
    for j in range(n + 1):
        d[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                cost = 0
            else:
                cost = 1

            d[i][j] = min(
                d[i - 1][j] + 1,  # usuwanie
                d[i][j - 1] + 1,  # wstawianie
                d[i - 1][j - 1] + cost  # zamiana
            )

    return d[m][n]

def personal_test(pwd, email):
    pwd = pwd.lower()
    email_tmp = email.split('@')[0].lower() if '@' in email else email.lower()
    email_prefix = email_tmp.split('.')[0] if '.' in email_tmp else email_tmp

    data_to_check = [email_prefix]
    tolerance_limit = 3

    for data in data_to_check:
        if len(data) < tolerance_limit:
            continue

        if data in pwd:
            return data, 0

        distance = levenshtein(pwd, data)
        if distance <= tolerance_limit:
            return data, distance

    return False