from functions.get_file_content import get_file_content
# from config import MAX_CHARS
MAX_CHARS = 10000

def main():
    print("Result for lorem.txt:")
    content = get_file_content("calculator", "lorem.txt")
    print(f"Length: {len(content)}")
    print(content[-120:])  # show truncation message

    print("\nResult for main.py:")
    print(get_file_content("calculator", "main.py"))

    print("\nResult for pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\nResult for /bin/cat:")
    print(get_file_content("calculator", "/bin/cat"))

    print("\nResult for missing file:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    main()
