import pws_chk

class PipelineWithoutEmail:
    def __init__(self):
        self.checks = []

    def step(self, func, name=None):
        self.checks.append((func, name or func.__name__))
        return func

    def run(self, password):
        results = {}
        for func, key_name in self.checks:
            results[key_name] = func(password)
        return results

#pipeline do sprowadzania pliku
pipe_no_personal = PipelineWithoutEmail()

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