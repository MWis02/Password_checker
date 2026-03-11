import pipeline

if __name__ == "__main__":
    password = input("Podaj hasło: ")
    name = input("Podaj imię: ")
    surname = input("Podaj nazwisko: ")
    email = input("Podaj email: ")
    results = pipeline.pipe.run(password, name, surname, email)

    if results['entropy_check'] == 0:
        print("Hasło nie może być puste.")
    elif results['dictionary_check'] or results['pattern_check']:
        print("Hasło zawiera łatwe do odgadnięcia wzorce.")
    else:
        for key, result in results.items():
            print(f"{key}: {result}")
