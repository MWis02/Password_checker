import pipeline
from pathlib import Path
import unicodedata

if __name__ == "__main__":
    while True:
        print("\n" + "=" * 40)
        flag = input('Czy chcesz sprawdzić swoje hasło?\n 1: tak\n 2: nie\n 3: wgraj dane z pliku \nWybór: ')
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
        elif flag == '3':
            route_raw = input('Podaj ścieżkę do pliku: ')
            route = ''.join(ch for ch in route_raw if unicodedata.category(ch) != 'Cf').strip().strip('"')
            input_path = Path(route).expanduser()

            if not route:
                print('Nie podano ścieżki do pliku.')
                continue

            if not input_path.is_absolute():
                input_path = (Path.cwd() / input_path).resolve()

            if not input_path.exists() or not input_path.is_file():
                print(f'Nie znaleziono pliku: {input_path}')
                continue

            output_path = Path('audit.txt').resolve()

            try:
                with input_path.open('r', encoding='utf-8') as file, output_path.open('w', encoding='utf-8') as file_write:
                    for tmp in file:
                        password = tmp.strip()
                        if not password:
                            continue

                        results = pipeline.pipe_no_personal.run_2(password)
                        entropy, grade, time = results['entropy_check']
                        pwnd = results['pwnd_pswd']
                        regex_ok = results['regex_test']
                        dict_ok = not results['dictionary_check']
                        pattern_ok = not results['pattern_check']

                        leaks_txt = "✓ Brak wycieków" if pwnd == 0 else f"✗ Znalezione {pwnd}x"

                        report = (
                            "\n" + "=" * 40 + "\n"
                            "Podsumowanie audytu hasła\n"
                            + "=" * 40 + "\n"
                            f"  Hasło:                 {password}\n"
                            f"  Entropia:              {entropy:.2f} bitów\n"
                            f"  Ocena:                 {grade}\n"
                            f"  Czas złamania hasła:   {time}\n"
                            f"  Regex (format):        {'✓ Poprawne z wzorcami haseł' if regex_ok else '✗ Brak poprawności z wzorcami bezpieczeństwa'}\n"
                            f"  Wycieki danych:        {leaks_txt}\n"
                            f"  Test słownikowy:       {'✓ Brak dopasowań z słownikiem' if dict_ok else '✗ Hasło znajduję się w popularnych hasłach, w wzorcach słownikowych'}\n"
                            f"  Test wzorców:          {'✓ Brak wzorców' if pattern_ok else '✗ Hasło zawiera łatwe do odganięcia wzorce np: aaa, abc, 123, 098 itp.'}\n"
                        )
                        file_write.write(report)

                print(f'Sprawdzono wszystkie hasła. Wyniki zapisano do: {output_path}')
            except PermissionError:
                print('Brak uprawnień do odczytu/zapisu wskazanego pliku.')
            except UnicodeDecodeError:
                print('Plik wejściowy nie jest w kodowaniu UTF-8.')
            except OSError as e:
                print(f'Błąd pliku: {e}')
        else:
            print("Nieprawidłowy wybór. Proszę wybrać 1, 2 lub 3.")
