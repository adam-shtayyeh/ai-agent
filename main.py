import os
import sys
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="AI Agent Chatbot")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("Error: OPENROUTER_API_KEY not found in environment variables. Please check your .env file.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # إعداد قائمة الرسائل الابتدائية
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # بدء حلقة الـ Agent (بحد أقصى 20 محاولة للوصول للحل)
    for i in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0,
        )

        if response.usage is None:
            raise RuntimeError("Error: API request failed or usage metadata is missing.")

        if args.verbose:
            print(f"\n[Iteration {i + 1}]")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message

        # 1. إلحاق رد الـ Assistant (سواء كان نصاً أو طلباً لاستدعاء أداة) بالـ history فوراً
        messages.append(message)

        # 2. الفحص: هل طلب النموذج استدعاء أدوات؟
        if message.tool_calls:
            for tool_call in message.tool_calls:
                # تنفيذ الدالة والحصول على ديكشنري يحمل الـ role: tool
                result_message = call_function(tool_call, verbose=args.verbose)

                if not result_message.get("content"):
                    raise ValueError("Error: Function returned an empty content string.")

                if args.verbose:
                    print(f"-> {result_message['content']}")

                # إلحاق رسالة الـ Tool بقائمة الـ messages حتى يراها الموديل في الدورة القادمة
                messages.append(result_message)
        else:
            # إذا لم يطلب أدوات، فهذا هو الرد النهائي للمستخدم
            if args.verbose:
                print("\nFinal response:")
            print(message.content)
            # الخروج من الحلقة بنجاح
            break
    else:
        # إذا انتهت الـ 20 دورة دون الوصول لرد نهائي
        print("Error: Maximum number of iterations reached without a final response.")
        sys.exit(1)


if __name__ == "__main__":
    main()
