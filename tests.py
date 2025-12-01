from functions.run_python_file import run_python_file


def _print_result(title, result):
    print(title)
    for line in result.splitlines():
        print(f"    {line}")


def main():
    cases = [
        ('run_python_file("calculator", "main.py"):\n', ("calculator", "main.py", None)),
        ('run_python_file("calculator", "main.py", ["3 + 5"]):\n', ("calculator", "main.py", ["3 + 5"])),
        ('run_python_file("calculator", "tests.py"):\n', ("calculator", "tests.py", None)),
        ('run_python_file("calculator", "../main.py"):\n', ("calculator", "../main.py", None)),
        ('run_python_file("calculator", "nonexistent.py"):\n', ("calculator", "nonexistent.py", None)),
        ('run_python_file("calculator", "lorem.txt"):\n', ("calculator", "lorem.txt", None)),
    ]

    for call_text, (wd, fp, args) in cases:
        print(call_text)
        if args is None:
            res = run_python_file(wd, fp)
        else:
            res = run_python_file(wd, fp, args)
        _print_result("Result:", res)
        print()


if __name__ == "__main__":
    main()
