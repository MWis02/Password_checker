import inspect
import pws_chk

class PasswordPipeline:
    def __init__(self):
        self.checks = []

    def step(self, func, name=None):
        """Rejestruje funkcję w pipeline. Opcjonalnie można podać custom nazwę."""
        self.checks.append((func, name or func.__name__))
        return func

    def run(self, password, email):
        results = {}
        all_args = (password, email)
        for func, key_name in self.checks:
            num_params = len(inspect.signature(func).parameters)
            results[key_name] = func(*all_args[:num_params])
        return results

    def run_2(self, password):
        results = {}
        all_args = (password,)
        for func, key_name in self.checks:
            num_params = len(inspect.signature(func).parameters)
            results[key_name] = func(*all_args[:num_params])
        return results

#pipeline do sprawdzania osoby
pipe = PasswordPipeline()

@pipe.step #test regex
def regex_test(pw):
    return pws_chk.regex_test(pw)

@pipe.step #test wycieków
def pwnd_pswd(pw):
    return pws_chk.pwnd_pswd(pw)

@pipe.step #test słownikowy
def dictionary_check(pw):
    return pws_chk.dictionary_test(pw)

@pipe.step #test wzorców
def pattern_check(pw):
    return pws_chk.pattern_test(pw)

@pipe.step #test osobisty
def personal_test(pw, email):
    return pws_chk.personal_test(pw, email)

@pipe.step #test entropii
def entropy_check(pw):
    return pws_chk.entropy(pw)

#pipeline do sprowadzania pliku
pipe_no_personal = PasswordPipeline()

@pipe_no_personal.step
def regex_test(pw):
    return pws_chk.regex_test(pw)

@pipe_no_personal.step
def pwnd_pswd(pw):
    return pws_chk.pwnd_pswd(pw)

@pipe_no_personal.step
def dictionary_check(pw):
    return pws_chk.dictionary_test(pw)

@pipe_no_personal.step
def pattern_check(pw):
    return pws_chk.pattern_test(pw)

@pipe_no_personal.step
def entropy_check(pw):
    return pws_chk.entropy(pw)