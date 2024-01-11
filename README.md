# Steam-Ban-database

Important note: This program checks for all kinds of bans in steam not purely vac bans. 

Startup and Installation:

Make sure you have Python installed on your computer.

Download this program and save it to your desired directory.

Open a command prompt (CMD) or terminal and navigate to the directory where the program is saved using the cd path\to\program_directory command.


Install the required libraries for the program by running the command:

    pip install -r requirements.txt

How to Use the Program:

Obtain a Steam API key:
        Visit the Steam Developer website.
        Log in to your Steam account.
        Accept the Steam Web API Terms of Use.
        Fill in the required information and submit to generate your API key.

 Launch the program by running the following command in the CMD or terminal:


    python main.py

OR

    py main.py
    
Alternatively, you can use the command py main.py.

The program will open a graphical user interface (GUI) where you can add Steam users for tracking.

Add SteamID64 or Vanity URL addresses through the GUI.

Press the "Check Bans" button to see if the added users have VAC bans.

The program will save the added users locally, allowing you to check their status later.

You can remove users from the GUI and storage.

Program Overview:

This simple Python program allows you to save Steam users locally, enabling you to track suspicious accounts while gaming. The program utilizes the Steam Web API to check for VAC bans.

Notes:

To use the program, you will need a Steam API key, which you can obtain as mentioned above.
The database stores information locally in the steam_ids.json file.
he program uses the requests library for making HTTP requests to the Steam Web API.

Enjoy using the program and keep an eye on suspicious Steam users!
