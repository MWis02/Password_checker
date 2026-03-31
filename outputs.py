import typing


def _format_leaks(pwnd: int) -> str:
    return "\u2713 Brak wycieków" if pwnd == 0 else f"\u2717 Znalezione {pwnd}x"


def _format_personal(personal_ok: typing.Any) -> str:
    # personal_ok to krotka (data, distance) albo False/None
    if not personal_ok:
        return "\u2713 Brak dopasowań z loginem"
    data, distance = personal_ok
    if distance == 0:
        return f"\u2717 Zawiera dane osobowe ({data}) - dokładne dopasowanie"
    return f"\u2717 Zawiera dane osobowe ({data}) - odległość Levenshteina: {distance}"


def _unpack_common(results: dict, with_email: bool):
    entropy, grade, time = results['entropy_check']
    pwnd = results['pwnd_pswd']
    regex_ok = results['regex_test']
    dict_ok = not results['dictionary_check']
    pattern_ok = not results['pattern_check']
    personal_ok = results.get('personal_test') if with_email else None

    return entropy, grade, time, pwnd, regex_ok, dict_ok, pattern_ok, personal_ok


def print_interactive_summary(results: dict, with_email: bool) -> None:
    entropy, grade, time, pwnd, regex_ok, dict_ok, pattern_ok, personal_ok = _unpack_common(results, with_email)

    leaks_test = _format_leaks(pwnd)

    personal_test = _format_personal(personal_ok) if with_email else None

    print("\n" + "=" * 40)
    print("Podsumowanie audytu hasła")
    print("=" * 40)
    print(f"  Entropia:              {entropy:.2f} bitów")
    print(f"  Ocena:                 {grade}")
    print(f"  Czas łamania hasła:       {time}")
    print(f"  Regex (format):        {'\u2713 Poprawne z wzorcami haseł' if regex_ok else '\u2717 Brak poprawności'
                                        ' z wzorcami bezpieczeństwa'}")
    print(f"  Wycieki danych:        {leaks_test}")
    print(f"  Test słownikowy:       {'\u2713 Brak dopasowań z słownikiem' if dict_ok else 
                                            '\u2717 Hasło znajduję '
                                            'się w popularnych hasłach, w wzorcach '
                                        'słownikowych'}")
    print(f"  Test wzorców:          {'\u2713 Brak wzorców' if pattern_ok else '\u2717 Hasło '
                                            'zawiera łatwe do odganięcia wzorce np: aaa, abc, 123, 098 itp.'}\n")
    if with_email and personal_test is not None:
        print(f"  Test danych osobowych: {personal_test}")
    print("=" * 40)


def build_batch_report(password: str, results: dict, with_email: bool) -> str:
    entropy, grade, time, pwnd, regex_ok, dict_ok, pattern_ok, personal_ok = _unpack_common(results, with_email)

    leaks_txt = _format_leaks(pwnd)
    personal_txt = _format_personal(personal_ok) if with_email else None

    base_report = (
        "\n" + "=" * 40 + "\n"
        "Podsumowanie audytu hasła\n"
        + "=" * 40 + "\n"
        f"  Hasło:                 {password}\n"
        f"  Entropia:              {entropy:.2f} bitów\n"
        f"  Ocena:                 {grade}\n"
        f"  Czas łamania hasła:    {time}\n"
        f"  Regex (format):        {'\u2713 Poprawne z wzorcami haseł' if regex_ok else '\u2717 Brak poprawności'
                                    ' z wzorcami bezpieczeństwa'}\n"
        f"  Wycieki danych:        {leaks_txt}\n"
        f"  Test słownikowy:       {'\u2713 Brak dopasowań z słownikiem' if dict_ok else ''
                                        '\u2717 Hasło znajduję się w popularnych hasłach, w wzorcach '
                                        'słownikowych'}\n"
        f"  Test wzorców:          {'\u2713 Brak wzorców' if pattern_ok else '\u2717 Hasło '
                                        'zawiera ł2atwe do odganięcia wzorce np: aaa, abc, 123, 098 itp.'}\n"
    )

    if with_email and personal_txt is not None:
        base_report += f"  Test danych osobowych: {personal_txt}\n"

    return base_report

