import pipeline

if __name__ == "__main__":
    password = input("Podaj hasło: ")
    results = pipeline.pipe.run(password)
    print(results)

    if results['entropy_check'] == 0:
        print("Hasło nie może być puste.")
    elif results['dictionary_check'] or results['pattern_check']:
        print("Hasło zawiera łatwe do odgadnięcia wzorce.")
    else:
        for name, result in results.items():
            print(f"{name}: {result}")