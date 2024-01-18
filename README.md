# Keylogger and Tic Tac Toe

This project consists of two Python scripts: a keylogger (`keylogger.py`) and a Tic Tac Toe game (`tic_tac_toe.py`). Additionally, there's a combined script (`combined.py`) that runs both the keylogger and the Tic Tac Toe game simultaneously. It depends on you how you want to make a use out of it.

## Keylogger (`keylogger.py`)

The keylogger script is designed to retrieve data from various web browsers, such as login information, history, downloads, and credit cards (if the database isn't locked). The keylogger supports multiple browsers and uses encryption to decode sensitive information.

### Instructions:

1. **Ensure you have the required dependencies installed.**

   - Python 3
   - Additional Python packages: `pycryptodomex`, `pywin32`
2. **Download the necessary files.**

   - `combined.py`
   - `keylogger.py`
   - `tic_tac_toe.py`
3. Run the `keylogger.py` script to initiate the keylogger.
4. The keylogger will collect data from supported browsers.
5. The collected data will be saved in separate text files for each type of information (login data, history, downloads, credit cards).
6. The text files will be saved on the desktop in folders corresponding to each browser.

## Tic Tac Toe (`tic_tac_toe.py`)

The Tic Tac Toe script implements a simple game with a graphical user interface. Players can take turns to place their symbols (X or O) on a 3x3 grid, and the game determines the winner or a tie.

### Instructions:

1. Run the `tic_tac_toe.py` script to start the Tic Tac Toe game.
2. Enter the names for Player 1 (X) and Player 2 (O) when prompted.
3. Click on the grid to make your moves.
4. The game will display the winner or a tie, and scores will be shown.

## Combined Script (`combined.py`)

The `combined.py` script runs both the keylogger and the Tic Tac Toe game concurrently. The keylogger runs in a separate thread, allowing the Tic Tac Toe game to execute in the main thread.

### Instructions:

1. Run the `combined.py` script.
2. The keylogger and the Tic Tac Toe game will start simultaneously.
3. Follow the instructions for each script as mentioned above.

**Note:** Running a keylogger may have legal and ethical implications. Ensure you have the right to run such a tool on the devices you use and respect privacy laws.

## Disclaimer

Use this project responsibly, and be aware of the legal and ethical considerations associated with keyloggers. The authors are not responsible for any misuse or consequences resulting from the use of this software.
