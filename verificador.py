import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python verificador.py <file1> <file2>")
        sys.exit(1)
    input_file = sys.argv[1]
    decompressed_file = sys.argv[2]

    with open(input_file, "r", encoding="ISO-8859-1") as f:
        original_data = f.read()

    with open(decompressed_file, "r", encoding="ISO-8859-1") as f:
        decompressed_data = f.read()

    if original_data == decompressed_data:
        print("ok")
    else:
        print("nok")

if __name__ == "__main__":
    main()
