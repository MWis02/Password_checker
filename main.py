import pipeline

if __name__ == "__main__":
    while True:
        print("\n" + "=" * 40)
        flag = input('Czy chcesz sprawdzić swoje hasło?\n 1: tak\n 2: nie\nWybór: ')
        if flag == '1':
            password = input("\nPodaj hasło: ")
            email = input("Podaj login: ")
            results = pipeline.pipe.run(password, email)

            entropy, grade, time = results['entropy_check']
            pwnd = results['pwnd_pswd']
            regex_ok = results['regex_test']
            dict_ok = not results['dictionary_check']
            pattern_ok = not results['pattern_check']
            personal_ok = results['personal_test']

            leaks_txt = "✓ Brak wycieków" if pwnd == 0 else f"✗ Znalezione {pwnd}x"

            print("\n" + "=" * 40)
            print("Podsumowanie audytu hasła")
            print("=" * 40)
            print(f"  Entropia:              {entropy:.2f} bitów")
            print(f"  Ocena:                 {grade}")
            print(f"  Czas złamania hasła:   {time}")
            print(f"  Regex (format):        {'✓ Poprawne z wzorcami haseł' if regex_ok else '✗ Brak poprawności z wzorcami bezpieczeństwa'}")
            print(f"  Wycieki danych:        {leaks_txt}")
            print(f"  Test słownikowy:       {'✓ Brak dopasowań z słownikiem' if dict_ok else '✗'}")
            print(f"  Test wzorców:          {'✓ Brak wzorców' if pattern_ok else '✗'}")
            if not personal_ok:
                print(f"  Test danych osobowych: ✓ Brak dopasowań z loginem")
            else:
                data, distance = personal_ok
                if distance == 0:
                    print(f"  Test danych osobowych: ✗ Zawiera dane osobowe ({data}) - dokładne dopasowanie")
                else:
                    print(f"  Test danych osobowych: ✗ Zawiera dane osobowe ({data}) - odległość Levenshteina: {distance}")
            print("=" * 40)
        elif flag == '2':
            print("Dziękujemy za skorzystanie z programu. Do zobaczenia!")
            break
        else:
            print("Nieprawidłowy wybór. Proszę wybrać 1 lub 2.")