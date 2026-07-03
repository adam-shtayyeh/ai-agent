from functions.get_file_content import get_file_content

def main():
    # 1. فحص ملف لوريم والتأكد من البتر وضغط حجم المخرجات في الطباعة
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    print("-" * 40)

    # 2. طباعة الحالات الأخرى المطلوبة
    print(get_file_content("calculator", "main.py"))
    print("-" * 40)
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("-" * 40)
    print(get_file_content("calculator", "/bin/cat"))
    print("-" * 40)
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()
