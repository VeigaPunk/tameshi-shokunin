RECORDED = []


def record(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    record("x", 0, "body", 0)
    record("y", 7, "body", 0)


if __name__ == "__main__":
    main()
    print(RECORDED)
