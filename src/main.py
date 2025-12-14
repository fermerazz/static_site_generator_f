import sys
from copystatic import copy_static
from gencontent import generate_pages_recursively

if len(sys.argv) > 1:
    basepath =sys.argv[1]
else:
    basepath = "/"

def main():
    copy_static("static", "docs")
    generate_pages_recursively(basepath, "content", "template.html", "docs")

if __name__ == "__main__":
    main()