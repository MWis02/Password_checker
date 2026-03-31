import os
import pipeline_with_email
import pipeline_wihout_email
from pathlib import Path
import unicodedata
from datetime import datetime
from outputs import print_interactive_summary, build_batch_report

# Czyści ekran konsoli przed kolejnym ekranem komunikatów
clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    while True:
        clear_screen()
        print("\n" + "=" * 40)
        flag = input('Czy chcesz sprawdzić swoje hasło?\n 1: Tak\n 2: Wgraj dane z pliku\n 3: Zakończ program \nWybór: ')
        if flag == '1':
            clear_screen()
            flag_1 = input('Czy chcesz sprawdzić powiązanie hasła z mailem\n 1: Tak\n 2: Nie \nWybór: ')
            with_email = flag_1 == '1'

            password = input("\nPodaj hasło: ")
            if with_email:
                email = input("Podaj mail: ")
                results = pipeline_with_email.pipe.run(password, email)
            else:
                results = pipeline_wihout_email.pipe_no_personal.run(password)

            print_interactive_summary(results, with_email)

            # Dopisz wynik testu do wspólnego pliku raportów
            output_dir = Path('reports')
            output_dir.mkdir(parents=True, exist_ok=True)
            log_path = (output_dir / 'audit.txt').resolve()
            report = build_batch_report(password, results, with_email)
            with log_path.open('a', encoding='utf-8') as log_file:
                log_file.write(report)

        elif flag == '2':
            clear_screen()
            flag_1 = input('Czy twój plik zawiera adresy email, odzielony od hasła przecinkiem\n 1: Tak\n 2: Nie \nWybór: ')
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

            output_dir = Path('reports')
            output_dir.mkdir(parents=True, exist_ok=True)
            # Bardziej czytelny format daty: RRRR-MM-DD_HH-MM-SS
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            output_path = (output_dir / f'audit_{timestamp}.txt').resolve()

            try:
                with input_path.open('r', encoding='utf-8') as file, output_path.open('w', encoding='utf-8') as file_write:
                    for tmp in file:
                        line = tmp.strip()
                        if not line:
                            continue

                        if flag_1 == '1':
                            # Oczekiwany format: hasło,email (oddzielone przecinkiem)
                            parts = [p.strip() for p in line.split(',', 1)]
                            if len(parts) != 2 or not parts[0] or not parts[1]:
                                print(f'Pomijam linię bez kompletu danych (hasło,email): {line}')
                                continue
                            password, email = parts
                            results = pipeline_with_email.pipe.run(password, email)
                            report = build_batch_report(password, results, True)
                        else:
                            # Linia zawiera tylko hasło
                            password = line
                            results = pipeline_wihout_email.pipe_no_personal.run(password)
                            report = build_batch_report(password, results, False)

                        file_write.write(report)

                print(f'Sprawdzono wszystkie hasła. Wyniki zapisano do: {output_path}')
            except PermissionError:
                print('Brak uprawnień do odczytu/zapisu wskazanego pliku.')
            except UnicodeDecodeError:
                print('Plik wejściowy nie jest w kodowaniu UTF-8.')
            except OSError as e:
                print(f'Błąd pliku: {e}')
        elif flag == '3':
            clear_screen()
            print("Dziękujemy za skorzystanie z programu. Do zobaczenia!")
            break
        else:
            print("Nieprawidłowy wybór. Proszę wybrać 1, 2 lub 3.")
