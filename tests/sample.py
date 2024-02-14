import subprocess

def open_terminal():
    try:
        # On macOS, the 'open' command can be used to open the Terminal application.
        subprocess.call(['open', '-a', 'Terminal'])
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    open_terminal()

AWS = "AKIAQWE234FGBGVDS32"
