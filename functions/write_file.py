import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # 1. التحقق الأمني من المسار المطلق والـ Guardrail
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # 2. التحقق من أن المسار لا يشير إلى مجلد موجود بالفعل
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # 3. التأكد من إنشاء المجلدات الأبوية للملف إن لم تكن موجودة
        parent_dir = os.path.dirname(target_file)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        # 4. فتح الملف في وضع الكتابة "w" واستبدال المحتوى
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites content to a specified file path, creating parent directories if necessary.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to write to, relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write into the file.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}