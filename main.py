import os
import pipeline_with_email
import pipeline_wihout_email
from pathlib import Path
import unicodedata
from datetime import datetime
from typing import Pattern
from outputs import print_interactive_summary, build_batch_report
from regex_patterns import (
    BATCH_WITH_EMAIL_RE,
    EMAIL_RE,
    MENU_MAIN_RE,
    MENU_YES_NO_RE,
    PASSWORD_RE,
    PATH_RE,
)

# Czyści ekran konsoli przed kolejnym ekranem komunikatów
clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def normalize_input(value: str) -> str:
    return ''.join(ch for ch in value if unicodedata.category(ch) != 'Cf').strip()


def prompt_with_regex(prompt: str, pattern: Pattern[str], error_message: str, sanitizer=normalize_input) -> str:
    while True:
        value = sanitizer(input(prompt))
        if pattern.fullmatch(value):
            return value
        print(f'Błąd wejścia: {error_message}')

if __name__ == "__main__":
    while True:
        clear_screen()
        print("\n" + "=" * 40)
        flag = prompt_with_regex(
            'Czy chcesz sprawdzić swoje hasło?\n 1: Tak\n 2: Wgraj dane z pliku\n 3: Zakończ program \nWybór: ',
            MENU_MAIN_RE,
            'dozwolone wartości to: 1, 2 lub 3.'
        )
        if flag == '1':
            clear_screen()
            flag_1 = prompt_with_regex(
                'Czy chcesz sprawdzić powiązanie hasła z mailem\n 1: Tak\n 2: Nie \nWybór: ',
                MENU_YES_NO_RE,
                'dozwolone wartości to: 1 lub 2.'
            )
            with_email = flag_1 == '1'

            password = input("\nPodaj hasło: ")
            if not PASSWORD_RE.fullmatch(password):
                print('Błąd wejścia: hasło nie może być puste.')
                continue

            if with_email:
                email = prompt_with_regex(
                    'Podaj mail: ',
                    EMAIL_RE,
                    'niepoprawny format adresu e-mail (przykład: user@example.com).'
                )
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
            flag_1 = prompt_with_regex(
                'Czy twój plik zawiera adresy email, odzielony od hasła przecinkiem\n 1: Tak\n 2: Nie \nWybór: ',
                MENU_YES_NO_RE,
                'dozwolone wartości to: 1 lub 2.'
            )
            route_raw = input('Podaj ścieżkę do pliku: ')
            route = normalize_input(route_raw).strip('"')
            input_path = Path(route).expanduser()

            if not route:
                print('Błąd wejścia: nie podano ścieżki do pliku.')
                continue

            if not PATH_RE.fullmatch(route):
                print('Błąd wejścia: ścieżka zawiera niedozwolone znaki.')
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
                            # Oczekiwany format: hasło, email (oddzielone przecinkiem)
                            match = BATCH_WITH_EMAIL_RE.fullmatch(line)
                            if not match:
                                print(f'Błąd wejścia: pomijam linię o niepoprawnym formacie (hasło,email): {line}')
                                continue
                            password = match.group('password').strip()
                            email = match.group('email').strip()
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
