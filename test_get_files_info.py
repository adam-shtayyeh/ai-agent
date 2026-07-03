from functions.get_files_info import get_files_info

def main():
    print(f"Result for current directory:\n{get_files_info('calculator', '.')}\n")
    print(f"Result for 'pkg' directory:\n{get_files_info('calculator', 'pkg')}\n")
    print(f"Result for '/bin' directory:\n{get_files_info('calculator', '/bin')}\n")
    print(f"Result for '../' directory:\n{get_files_info('calculator', '../')}\n")

if __name__ == "__main__":
    main()