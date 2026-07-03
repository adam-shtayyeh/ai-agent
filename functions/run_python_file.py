import os
import subprocess


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        # 1. التحقق الأمني من المسار
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 2. التحقق من وجود الملف وأنه ملف عادي
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # 3. التحقق من امتداد الملف
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        # 4. بناء أمر التشغيل
        command = ["python", target_file]
        if args:
            command.extend(args)

        # 5. تشغيل السكربت باستخدام subprocess
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # 6. بناء المخرجات النصية الموجهة للـ LLM
        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory using an optional list of arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the Python file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "description": "Optional list of string arguments to pass to the script.",
                    "items": {
                        "type": "string"
                    }
                },
            },
            "required": ["file_path"],
        },
    },
}