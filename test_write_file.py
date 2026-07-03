from functions.write_file import write_file


def main():
    # 1. فحص تعديل ملف موجود بالفعل
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    # 2. فحص إنشاء ملف جديد مع مجلد فرعي غير موجود مسبقاً
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    # 3. فحص محاولة اختراق والكتابة خارج المجلد المسموح به
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    main()