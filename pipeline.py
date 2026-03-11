import inspect
import pws_chk

class PasswordPipeline:
    def __init__(self):
        self.checks = []

    def step(self, func):
        self.checks.append(func)
        return func

    def run(self, password, email):
        results = {}
        all_args = (password,email)
        for check in self.checks:
            num_params = len(inspect.signature(check).parameters)
            results[check.__name__] = check(*all_args[:num_params])
        return results

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