import tkinter as tk
from tkinter import messagebox
import requests
import json

# SteamAPI class for handling Steam Web API calls
class SteamAPI:
    def __init__(self):
        self.api_key = None

    def set_api_key(self, api_key):
        self.api_key = api_key

    @staticmethod
    def extract_vanity_url(full_url):
        if not full_url:
            messagebox.showerror("Error", "Enter a Vanity URL.")
            return None

        if "https://steamcommunity.com/id/" not in full_url:
            messagebox.showerror("Error", "Invalid Vanity URL format. Use: https://steamcommunity.com/id/your_name")
            return None

        vanity_url = full_url.split("https://steamcommunity.com/id/")[1].split('/')[0]
        return vanity_url

    def resolve_vanity_url(self, vanity_url):
        if not self.api_key:
            messagebox.showerror("Error", "API Key is missing.")
            return None

        url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={self.api_key}&vanityurl={vanity_url}"
        response = requests.get(url)
        data = response.json()
        if data['response']['success'] == 1:
            return data['response']['steamid']
        else:
            messagebox.showerror("Error", "Invalid Vanity URL or other error occurred.")
            return None

    def get_steam_player_name(self, steam_id):
        if not self.api_key:
            messagebox.showerror("Error", "API Key is missing.")
            return None

        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.api_key}&steamids={steam_id}"
        response = requests.get(url)
        data = response.json()
        if data['response']['players']:
            player = data['response']['players'][0]
            personaname = player.get('personaname', 'Name not available')
            return steam_id, personaname
        return None, None

    def check_bans_for_id(self, steam_id):
        if not self.api_key:
            messagebox.showerror("Error", "API Key is missing.")
            return None

        url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={self.api_key}&steamids={steam_id}"
        response = requests.get(url)
        data = response.json()
        return data

    @staticmethod
    def save_api_key(api_key):
        with open("api_key.txt", "w") as file:
            file.write(api_key)

    @staticmethod
    def load_api_key():
        try:
            with open("api_key.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

# Function for adding a SteamID to the list
def add_steam_id(steam_api, steam_id_entry, listbox, steam_ids):
    steam_id = steam_id_entry.get().strip()
    if steam_id and steam_id not in steam_ids:
        steam_id64, personaname = steam_api.get_steam_player_name(steam_id)
        if personaname:
            steam_ids[steam_id] = personaname
            listbox.insert(tk.END, f"{personaname} ({steam_id})")
            steam_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "SteamID is not available.")
    else:
        messagebox.showerror("Error", "SteamID is already in the list or the field is empty.")

# Function for adding a Vanity URL to the list
def add_vanity_url(steam_api, vanity_url_entry, listbox, steam_ids):
    full_url = vanity_url_entry.get().strip()
    vanity_url = steam_api.extract_vanity_url(full_url)
    if vanity_url:
        steam_id64 = steam_api.resolve_vanity_url(vanity_url)
        if steam_id64:
            steam_id, personaname = steam_api.get_steam_player_name(steam_id64)
            if personaname:
                steam_ids[steam_id] = personaname
                listbox.insert(tk.END, f"{personaname} ({steam_id})")
                vanity_url_entry.delete(0, tk.END)

# Function for checking bans for the added SteamIDs
def check_bans(steam_api, listbox, status_listbox, steam_ids, percentage_label):
    status_listbox.delete(0, tk.END)
    banned_count = 0
    not_banned_count = 0

    for steam_id, personaname in steam_ids.items():
        ban_data = steam_api.check_bans_for_id(steam_id)
        if 'players' in ban_data:
            banned = any(player['VACBanned'] or player['CommunityBanned'] for player in ban_data['players'])
            status = "BANNED" if banned else "NOT BANNED"
            status_listbox.insert(tk.END, status)
            status_listbox.itemconfig(tk.END, fg="red" if banned else "green")

            if banned:
                banned_count += 1
            else:
                not_banned_count += 1

    total_count = len(steam_ids)
    banned_percentage = (banned_count / total_count) * 100
    not_banned_percentage = (not_banned_count / total_count) * 100

    percentage_label.config(text=f"Banned: {banned_percentage:.2f}% | Not Banned: {not_banned_percentage:.2f}%")

# Function for removing a selected SteamID from the list
def remove_selected_steam_id():
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Warning", "Select an item to remove.")
        return

    selected_index = int(selected_index[0])
    steam_id_item = listbox.get(selected_index)
    # Get SteamID from the selected item
    steam_id = steam_id_item.split(" (")[1].rstrip(")")

    if steam_id in steam_ids:
        del steam_ids[steam_id]  # Remove SteamID and associated name from the dictionary
        with open("steam_ids.json", "w") as file:
            json.dump(steam_ids, file)  # Save the updated dictionary to a JSON file

        listbox.delete(selected_index)  # Remove the item from Listbox
        status_listbox.delete(selected_index)  # Remove the status from the status_listbox
    else:
        messagebox.showerror("Error", "Item not found in the list.")

# Function to display the context menu
def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)

# Function to add an API key to the SteamAPI instance
def add_api_key(api_key_entry, steam_api):
    api_key = api_key_entry.get().strip()
    if api_key:
        steam_api.set_api_key(api_key)
        steam_api.save_api_key(api_key)  # Save the API key to a file
        api_key_entry.delete(0, tk.END)
        messagebox.showinfo("Info", "API Key added successfully.")
    else:
        messagebox.showerror("Error", "Enter an API Key.")

# Function to handle the main GUI and application logic
def main():
    root = tk.Tk()
    root.title("Steam Ban Checker")

    steam_api = SteamAPI()
    saved_api_key = steam_api.load_api_key()
    if saved_api_key:
        steam_api.set_api_key(saved_api_key)

    steam_ids = {}

    try:
        with open("steam_ids.json", "r") as file:
            saved_data = json.load(file)
            steam_ids.update(saved_data)
    except FileNotFoundError:
        pass

    frame = tk.Frame(root)
    frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    header_frame = tk.Frame(frame)
    header_frame.pack(side=tk.TOP, fill=tk.X)

    label_user = tk.Label(header_frame, text="USER")
    label_user.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    label_status = tk.Label(header_frame, text="STATUS")
    label_status.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    listbox_frame = tk.Frame(frame)
    listbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    context_menu = tk.Menu(listbox, tearoff=0)
    context_menu.add_command(label="Remove", command=remove_selected_steam_id)
    listbox.bind("<Button-3>", show_context_menu)  # Show context menu on right-click

    status_listbox = tk.Listbox(listbox_frame, fg="green", selectmode=tk.SINGLE)
    status_listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    for steam_id, personaname in steam_ids.items():
        listbox.insert(tk.END, f"{personaname} ({steam_id})")
        status_listbox.insert(tk.END, "NOT BANNED")

    api_key_frame = tk.Frame(root)
    api_key_frame.pack(side=tk.TOP, fill=tk.X)

    api_key_label = tk.Label(api_key_frame, text="Add Steam API Key:")
    api_key_label.pack(side=tk.LEFT, padx=(10, 0))

    api_key_entry = tk.Entry(api_key_frame)
    api_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    add_api_key_button = tk.Button(api_key_frame, text="Add", command=lambda: add_api_key(api_key_entry, steam_api))
    add_api_key_button.pack(side=tk.LEFT, padx=(0, 10))

    new_id_entry = tk.Entry(root)
    new_id_entry.pack(side=tk.TOP, fill=tk.X)
    add_steam_id_button = tk.Button(root, text="Add SteamID64",
                                    command=lambda: add_steam_id(steam_api, new_id_entry, listbox, steam_ids))
    add_steam_id_button.pack(side=tk.TOP)

    vanity_url_entry = tk.Entry(root)
    vanity_url_entry.pack(side=tk.TOP, fill=tk.X)
    add_vanity_url_button = tk.Button(root, text="Add URL",
                                      command=lambda: add_vanity_url(steam_api, vanity_url_entry, listbox, steam_ids))
    add_vanity_url_button.pack(side=tk.TOP)

    check_bans_button = tk.Button(root, text="Check Bans",
                                  command=lambda: check_bans(steam_api, listbox, status_listbox, steam_ids,
                                                             percentage_label))
    check_bans_button.pack(side=tk.TOP)

    percentage_label = tk.Label(root, text="Banned: 0.00% | Not Banned: 0.00%")
    percentage_label.pack(side=tk.TOP)

    def on_closing():
        with open("steam_ids.json", "w") as file:
            json.dump(steam_ids, file)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
