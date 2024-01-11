# Steam-Ban-database

![kuva](https://github.com/Metroseksuaali/steam-ban-database/assets/13061405/f7b44999-5d30-4450-a151-8a77ca06c4df)
![kuva](https://github.com/Metroseksuaali/steam-ban-database/assets/13061405/8b4aa676-0a90-4ec1-9fb3-ebcdf8377f4d)


Important note: This program checks for Community ban and VAC Ban tags from steamAPI

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


When you open someones steam profile there is 2 ways that adress is displayed.
        ```https://steamcommunity.com/id/Metroseksuaali/ ``` This is meant to be pasted on URL box
        ```https://steamcommunity.com/profiles/76561199050865196/``` From this just get the number value ```76561199050865196``` And past it on steamid64 box



Notes:

To use the program, you will need a Steam API key, which you can obtain as mentioned above.
The database stores information locally in the steam_ids.json file.
he program uses the requests library for making HTTP requests to the Steam Web API.

Enjoy using the program and keep an eye on suspicious Steam users!
