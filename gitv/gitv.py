import sys
from functions import create_file_as_submodule_and_push

def main():
    # Retrieve arguments
    args = sys.argv[1:]

    # Check command structure
    if len(args) < 3 or args[0] != "file":
        print("Usage: gitv file <file_relative_path> <github_token>")
        return

    file_name = args[1]
    github_token = args[2]

    # Call the function to transform or create the file as a submodule
    create_file_as_submodule_and_push(".", file_name, github_token)

if __name__ == "__main__":
    main()