import pws_chk

class PasswordPipeline:
    def __init__(self):
        self.checks = []

    def step(self, func):
        self.checks.append(func)
        return func

    def run(self, password):
        results = {}
        for check in self.checks:
            results[check.__name__] = check(password)
        return results

pipe = PasswordPipeline()

@pipe.step #test słownikowy
def dictionary_check(pw):
    return pws_chk.dictionary_test(pw)

@pipe.step #test wzorców
def pattern_check(pw):
    return pws_chk.pattern_test(pw)

@pipe.step #test entropii
def entropy_check(pw):
    return pws_chk.entropy(pw)