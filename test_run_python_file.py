from functions.run_python_file import run_python_file


def main():
    print("Result: run main.py (no args)")
    print(run_python_file("calculator", "main.py"))

    print("\nResult: run main.py with expression")
    print(run_python_file("calculator",  "main.py", ["3 + 5"]))

    print("\nResult: run tests.py")
    print(run_python_file("calculator", "tests.py"))

    print("\nResult: outside working directory")
    print(run_python_file("calculator", "../main.py"))

    print("\nResult: nonexistent file")
    print(run_python_file("calculator", "nonexistent.py"))

    print("\nResult: not a Python file")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()
