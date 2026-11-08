# case_l — the recorder's `add` method is called through an instance attribute
class Recorder:
    def add(self, name, code, body, want_code):
        print("RECORD name=%s code=%r want=%r" % (name, code, want_code))


def main():
    r = Recorder()
    r.add("attribute-recorder", 0, "body", 1)


main()
