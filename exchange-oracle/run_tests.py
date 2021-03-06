import os  # pragma: no cover
import subprocess  # pragma: no cover


def main():  # pragma: no cover
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    subprocess.call(["coverage", "run", "-m", "pytest", "-rw"])
    print("\n\nTests completed, checking coverage...\n\n")

    subprocess.call(["coverage", "combine", "--append"])
    subprocess.call(["coverage", "report", "-m"])


if __name__ == "__main__":  # pragma: no cover
    main()
