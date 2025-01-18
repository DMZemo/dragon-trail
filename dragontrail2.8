import sys
import time
from tqdm import tqdm
import threading
import os
import random
import colorama
from colorama import Fore, Back, Style
import keyboard
import pygame

colorama.init(autoreset=True) #Makes it so that it resets color after each use

#
#
#
#
#

def get_resource_path(relative_path):
    """
    Constructs the absolute path to the resource, ensuring no path duplication.
    Handles both development and PyInstaller bundled environments.
    """
    try:
        if getattr(sys, 'frozen', False):
            # If the application is run as a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # If the application is run in a normal Python environment
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Normalize paths to prevent duplication
        normalized_path = os.path.normpath(os.path.join(base_path, relative_path))
        
        # Validate the constructed path
        if not os.path.exists(normalized_path):
            raise FileNotFoundError(f"Resource not found: {normalized_path}")
        
        return normalized_path
    except Exception as e:
        print(f"Error resolving resource path: {e}")
        raise

# Music tracks (organized in a dictionary)
try:
    music_tracks = {
        "main_menu": get_resource_path("Music/Earth Prelude.mp3"),
        "travel": get_resource_path("Music/Earth Prelude.mp3"),
        "hunt": get_resource_path("Music/Lotus.mp3"),
        "scout": get_resource_path("Music/Lotus.mp3"),
        "rest": get_resource_path("Music/Evening.mp3"),
        "cook": get_resource_path("Music/Evening.mp3"),
        "boss_fight": get_resource_path("Music/Machinations.mp3"),
        "gear_shop": get_resource_path("Music/Earth Prelude.mp3"),
    }
    print("Music paths loaded successfully.")
except Exception as e:
    print(f"Error loading music paths: {e}")

# Pygame Music Initialization (with error handling)
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing Pygame mixer: {e}")
    sys.exit(1)  # Exit if Pygame initialization fails

music_muted = False  # Global variable to track music state
current_music_track = None  # Track the currently playing music


def play_music(menu_name):
    """Plays music for the specified menu, always reloading if needed."""
    global current_music_track, music_muted
    if not music_muted:
        track = music_tracks.get(menu_name)
        if track:
            if track != current_music_track:  # Check if the track is different
                try:
                    pygame.mixer.music.load(track)  # Load the new track
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    current_music_track = track
                    print(f"Playing music for {menu_name}...")
                except pygame.error as e:
                    print(f"Error playing music for {menu_name}: {e}")
            else:
                print(f"Already playing music for {menu_name}.")
        else:
            print(f"No music track found for {menu_name}.")


def stop_music():
    """Stops the music."""
    pygame.mixer.music.stop()
    print("Music stopped.")
    global current_music_track
    current_music_track = None


def toggle_music():
    """Toggles the music on or off."""
    global music_muted
    music_muted = not music_muted
    if music_muted:
        stop_music()
        print("Music muted.")
    else:
        play_music(current_menu)  # Resume playing music for the current menu

# ASCII art (moved to a dictionary for better organization)
ascii_art = {
    "writtenby": r"""                                                                                                   
    DM.ZEMO-DM.ZEMO-DM.ZEMO-DM.ZEMO-DM.ZEMO-DM.ZEMO-DM.ZEMO-DM.ZEMO
      DDDDDD  MMM   MMM    ZZZZZZZZ EEEEEEEE  MMM   MMM   OOOOOOO
      DD   D  M  M M  M         ZZ  EE        M  M M  M   O     O
      DD   D  M   M   M       ZZ    EEEEE     M   M   M   O     O
      DD   D  M       M     ZZ      EE        M       M   O     O
      DDDDDD  M       M [] ZZZZZZZZ EEEEEEEE  M       M   OOOOOOO
    DM.ZEMO-DM.ZEMO-DM.ZEMO-DM.ZEMO-DM.ZEMO-DM.ZEMO-DM.ZEMO-DM.ZEMO
    """,

    "title": r"""
███████████ █████                                            
░█░░░███░░░█░░███                                             
░   ░███  ░  ░███████    ██████                               
    ░███     ░███░░███  ███░░███                              
    ░███     ░███ ░███ ░███████                               
    ░███     ░███ ░███ ░███░░░                                
    █████    ████ █████░░██████                               
   ░░░░░    ░░░░ ░░░░░  ░░░░░░                                
                                                              
                                                              
                                                              
 ██████████                                                   
░░███░░░░███                                                  
 ░███   ░░███ ████████   ██████    ███████  ██████  ████████  
 ░███    ░███░░███░░███ ░░░░░███  ███░░███ ███░░███░░███░░███ 
 ░███    ░███ ░███ ░░░   ███████ ░███ ░███░███ ░███ ░███ ░███ 
 ░███    ███  ░███      ███░░███ ░███ ░███░███ ░███ ░███ ░███ 
 ██████████   █████    ░░████████░░███████░░██████  ████ █████
░░░░░░░░░░   ░░░░░      ░░░░░░░░  ░░░░░███ ░░░░░░  ░░░░ ░░░░░ 
                                  ███ ░███                    
                                 ░░██████                     
                                  ░░░░░░                      
 ███████████                      ███  ████                   
░█░░░███░░░█                     ░░░  ░░███                   
░   ░███  ░  ████████   ██████   ████  ░███                   
    ░███    ░░███░░███ ░░░░░███ ░░███  ░███                   
    ░███     ░███ ░░░   ███████  ░███  ░███                   
    ░███     ░███      ███░░███  ░███  ░███                   
    █████    █████    ░░████████ █████ █████                  
   ░░░░░    ░░░░░      ░░░░░░░░ ░░░░░ ░░░░░                   """,

    "status": r"""
     █████████   █████               █████                      
     ███░░░░░███ ░░███               ░░███                       
    ░███    ░░░  ███████    ██████   ███████   █████ ████  █████ 
    ░░█████████ ░░░███░    ░░░░░███ ░░░███░   ░░███ ░███  ███░░  
     ░░░░░░░░███  ░███      ███████   ░███     ░███ ░███ ░░█████ 
     ███    ░███  ░███ ███ ███░░███   ░███ ███ ░███ ░███  ░░░░███
     ░░█████████   ░░█████ ░░████████  ░░█████  ░░████████ ██████ 
      ░░░░░░░░░     ░░░░░   ░░░░░░░░    ░░░░░    ░░░░░░░░ ░░░░░░  """,
    
    "travel": r"""
     ███████████                                          ████ 
    ░█░░░███░░░█                                         ░░███ 
    ░   ░███  ░  ████████   ██████   █████ █████  ██████  ░███ 
        ░███    ░░███░░███ ░░░░░███ ░░███ ░░███  ███░░███ ░███ 
        ░███     ░███ ░░░   ███████  ░███  ░███ ░███████  ░███ 
        ░███     ░███      ███░░███  ░░███ ███  ░███░░░   ░███ 
        █████    █████    ░░████████  ░░█████   ░░██████  █████
        ░░░░░    ░░░░░      ░░░░░░░░    ░░░░░     ░░░░░░  ░░░░░ """,

"hourglasses": r"""
    --------------------------------------------------------------------
      \°°°°°°°/  \°°°°°°°/  \       /  \       /  \       /  \       /  
       \°°°°°/    \°°°°°/    \°°°°°/    \     /    \     /    \     /   
        \°°°/      \°°°/      \°°°/      \°°°/      \   /      \   /    
         \°/        \°/        \°/        \°/        \°/        \ /     
          0          0          0          0          0          0      
         / \        / \        / \        / \        / \        /°\     
        /   \      /   \      /   \      /   \      /°°°\      /°°°\    
       /     \    /     \    /     \    /°°°°°\    /°°°°°\    /°°°°°\   
      /       \  /       \  /°°°°°°°\  /°°°°°°°\  /°°°°°°°\  /°°°°°°°\  
    --------------------------------------------------------------------""",

    "hunt": r"""
    █████   █████                        █████   
    ░░███   ░░███                        ░░███    
     ░███    ░███  █████ ████ ████████   ███████  
     ░███████████ ░░███ ░███ ░░███░░███ ░░░███░   
     ░███░░░░░███  ░███ ░███  ░███ ░███   ░███    
     ░███    ░███  ░███ ░███  ░███ ░███   ░███ ███
    █████   █████ ░░████████ ████ █████  ░░█████ 
    ░░░░░   ░░░░░   ░░░░░░░░ ░░░░ ░░░░░    ░░░░░  """,

    "small_game": r"""
     __    __
    / \\..// \
      ( oo )  
       \__/ 
     _/-  -\_
    (   ()   )
     \  /\  /
     /`|  |`\
    You Catch Multiple Rabbits!""",

    "med_game" : r"""
        _____  
    ^..^     \9
    (oo)_____/ 
       WW  WW 
    You Catch Multiple Boar!""",

    "large_game": r"""
      __.------~~~-.
    ,'/             `\
    " \  ,..__ | ,_   `\_,
       >/|/   ~~\||`\(`~,~'
       | `\     /'|   \_;
       "   "   "  "    
    You Catch Multiple Deer!""",

    "scout": r"""
    █████████                                █████   
    ███░░░░░███                              ░░███    
    ░███    ░░░   ██████   ██████  █████ ████ ███████  
    ░░█████████  ███░░███ ███░░███░░███ ░███ ░░░███░   
     ░░░░░░░░███░███ ░░░ ░███ ░███ ░███ ░███   ░███    
     ███    ░███░███  ███░███ ░███ ░███ ░███   ░███ ███
    ░░█████████ ░░██████ ░░██████  ░░████████  ░░█████ 
      ░░░░░░░░░   ░░░░░░   ░░░░░░    ░░░░░░░░    ░░░░░  """,

    "mount": r"""
          /\
         /**\
        /****\   /\
       /      \ /**\
      /  /\    /    \        /\    /\  /\      /\            /\/\/\  /\
     /  /  \  /      \      /  \/\/  \/  \  /\/  \/\  /\  /\/ / /  \/  \
    /  /    \/ /\     \    /    \ \  /    \/ /   /  \/  \/  \  /    \   \
   /  /      \/  \/\   \  /      \    /   /    \
__/__/_______/___/__\___\__________________________________________________""",

    "rest": r"""
    ███████████                     █████   
    ░░███░░░░░███                   ░░███    
     ░███    ░███   ██████   █████  ███████  
     ░██████████   ███░░███ ███░░  ░░░███░   
     ░███░░░░░███ ░███████ ░░█████   ░███    
     ░███    ░███ ░███░░░   ░░░░███  ░███ ███
    █████   █████░░██████  ██████   ░░█████ 
    ░░░░░   ░░░░░  ░░░░░░  ░░░░░░     ░░░░░  """,

    "cook": r"""
      █████████                    █████     
      ███░░░░░███                  ░░███      
     ███     ░░░   ██████   ██████  ░███ █████
    ░███          ███░░███ ███░░███ ░███░░███ 
    ░███         ░███ ░███░███ ░███ ░██████░  
    ░░███     ███░███ ░███░███ ░███ ░███░░███ 
    ░░█████████ ░░██████ ░░██████  ████ █████
     ░░░░░░░░░   ░░░░░░   ░░░░░░  ░░░░ ░░░░░ """,


    "dragonart": r"""
                         _====-_      _-====__
                    _--^^^#####/      \#####^^^--_
                 _-^##########/ (    ) \##########^-_
                -############/  |\^^/|  \############-
              _/############/   (@::@)   \############\_
             -#############(     \||/     )#############-
            -###############\    (oo)    /###############-
           -#################\  / "" \  /#################-
          -###################\/((()))\/###################-
         _#/|##########/\######\ (()) /#####/\##########|\#_
         |/ |#/\#/\#/\/  \#/\#/ \ () /\#/\#/  \/\#/\#/\#| \|
          \ |/  V  V      V  V   \VV/  V  V      V  V  \| /
    """,

    "gear_shop": r"""               
    \\\~///
   \|/   \|/  /``````````````\
    | *,* | <<  Get Yur Gear!|  
     \__0/    \,,,,,,,,,,,,,,/""",

    "main_menu": r"""
           /│\           
        ▓▓▓▓▓▓▓▓▓        
     ▓▓▓░░░░░░░░░▓▓▓     
   ▓▓░░░    N    ░░░▓▓   
  ▓░░   *   │   *   ░░▓  
 ▓░         │         ░▓ 
<▓░W────────+────────E░▓> WHAT WOULD YOU LIKE TO DO?
 ▓░         │         ░▓ 
  ▓░░   *   │   *   ░░▓  
   ▓▓░░░    S    ░░░▓▓   
     ▓▓▓░░░░░░░░░▓▓▓     
        ▓▓▓▓▓▓▓▓▓        
           \│/               
    """

}

how_to_play = """
\nHOW TO PLAY:

"""

welcome_text = """
\nThere is a Dragon that has been terrorizing the town.
It's lair is 1000 miles away.
You are assembling a party of adventurers to travel to the dragon and defeat it.
You will need to Travel, Hunt, Rest, and Cook along the way.
Take care along the road and get to the dragon in one piece, then defeat it.
Good luck along THE DRAGON TRAIL!!!
"""

# CONSTANTS (Grouped for better readability)
MONTHS = ["O'drahn 1 (June)", "O'drahn 2 (July)", "O'drahn 3 (August)", "O'drahn 4 (September)",
          "Remiscus 1 (October)", "Remiscus 2 (November)", "Remiscus 3 (December)", "Remiscus 4 (January)",
          "Demiscus 1 (February)", "Demiscus 2 (March)", "Demiscus 3 (April)", "Demiscus 4 (May)"]

# Travel Constants
MIN_MILES_PER_TRAVEL = 18
MAX_MILES_PER_TRAVEL = 30
MIN_DAYS_PER_TRAVEL = 1
MAX_DAYS_PER_TRAVEL = 3
TOTAL_MILES = 1000

# Health and Resource Constants
MAX_HEALTH_LEVEL = 100
PLAYER_AC = 16
DRAGON_AC = 20
MIN_DAYS_PER_REST = 1
MAX_DAYS_PER_REST = 3
FOOD_PER_HUNT = 5
MIN_DAYS_PER_HUNT = 1
MAX_DAYS_PER_HUNT = 4
WATER_SKIN_CAPACITY = 8  # lbs     ###THESE SHOULD BE CUT??
WATER_DRINK_AMOUNT = 1  #  lbs
WOOD_CORD_SIZE = 3  # lbs          #### THESE SHOULD BE CUT??
MAX_CARRY_CAPACITY = 150  #  lbs
current_biome = "Marine"

def set_carry_capacity(survival):
    """
    Dynamically sets the maximum carry capacity based on the survival skill level.

    Args:
        survival: An integer representing the player's survival skill (0-8).
    """
    global MAX_CARRY_CAPACITY  # Declare MAX_CARRY_CAPACITY as global to modify it

    if not 0 <= survival <= 8:
        raise ValueError("Survival skill must be an integer between 0 and 8.")

    # Define carry capacity based on survival skill
    carry_capacities = {
        8: 130,
        7: 125,
        6: 120,
        5: 110,
        4: 100,
        3: 90,
        2: 80,
        1: 70,
        0: 55,
    }

    MAX_CARRY_CAPACITY = carry_capacities[survival]
    print(f"Carry capacity set to {MAX_CARRY_CAPACITY} lbs based on survival skill {survival}.")

BIOMES = [
    "Marine", "Glacier", "Tundra", "Taiga", "Cold Desert", "Hot Desert", 
    "Tropical Rainforest", "Wetland", "Tropical Seasonal Forest", "Savanna", 
    "Grassland", "Temperate Deciduous Forest", "Temperate Rainforest"
]

BIOME_CONNECTIONS = {
    "Marine": ["Marine", "Wetland", "Tropical Rainforest", "Glacier", "Temperate Rainforest"], 
    "Glacier": ["Tundra", "Cold Desert"], 
    "Tundra": ["Glacier", "Taiga", "Cold Desert"],
    "Taiga": ["Tundra", "Temperate Deciduous Forest", "Grassland"], 
    "Cold Desert": ["Tundra", "Glacier"], 
    "Hot Desert": ["Savanna", "Grassland"], 
    "Tropical Rainforest": ["Tropical Seasonal Forest", "Wetland"],
    "Wetland": ["Tropical Rainforest", "Tropical Seasonal Forest", "Grassland"], 
    "Tropical Seasonal Forest": ["Tropical Rainforest", "Savanna"],
    "Savanna": ["Hot Desert", "Tropical Seasonal Forest", "Grassland"],
    "Grassland": ["Savanna", "Temperate Deciduous Forest", "Taiga"],
    "Temperate Deciduous Forest": ["Grassland", "Taiga"],
    "Temperate Rainforest": ["Temperate Deciduous Forest", "Tropical Rainforest"] 
}

# Game Data (Organized into meaningful sections)
game_data = {
    "time": {"day": 1, "month": MONTHS[0], "year": 0},
    "resources": {"food": 10, "water": 8, "waterskins": 1, "herbs": 1, "supplies": 10,
                  "wood": 3, "wood_cords": 1, "gold": 0},
    "journey": {"totalMilesTraveled": 0, "dragon_encountered": False, "current_biome": "Marine"},
    "player": {"health": 100, "survival": 0, "carry_weight": 0, "defend_cooldown": 0, "stun_splosion_cooldown": 0},  #Initialize carry_weight
    "combat": {"potions": 0}}


# Item costs
item_costs = {
    "food": 1,
    "water": 2,
    "herbs": 3,
    "supplies": 2,
    "wood": 1,
}

item_weights = {
    "food": 1,
    "waterskin": 0.1,  # Weight of a waterskin
    "herbs": 0.1,
    "supplies": 1,
    "wood": 1, # Weight of a single wood
}

def space():
    print("\n")

def roll_d20():
    return random.randint(1, 20)

def display_ascii_art(art_key, color=Fore.WHITE, style=Style.BRIGHT): #this may create issues with style=Style.BRIGHT, idk why color is bright but style is dim
    print(color + ascii_art.get(art_key))


def check_low_resources():
    """Checks for low resources and prints red alerts."""
    low_resource_alerts = []
    if game_data["resources"]["food"] <= 3:
        low_resource_alerts.append(f"You are down to {game_data['resources']['food']} food!")
    if game_data["resources"]["water"] <= 3:
        low_resource_alerts.append(f"You are down to {game_data['resources']['water']} water!")
    if game_data["resources"]["wood_cords"] <= 1:
        low_resource_alerts.append(f"You are down to {game_data['resources']['wood_cords']} wood cord!")
    if game_data["resources"]["herbs"] <= 1:
        low_resource_alerts.append(f"You are down to {game_data['resources']['herbs']} herb!")
    if game_data["resources"]["supplies"] <= 1:
        low_resource_alerts.append(f"You are down to {game_data['resources']['supplies']} supply!")

    if low_resource_alerts:
        print(Fore.RED + "\nLOW RESOURCES ALERT:")
        for alert in low_resource_alerts:
            print(alert)
        print(Fore.RED + "Consider gathering more resources before proceeding.")

def handle_game():
    global current_menu

    while True:
        check_win_condition()
        space()
        display_ascii_art("main_menu", Fore.LIGHTYELLOW_EX, Style.BRIGHT)
        command = input("What would you like to do? \n (1) Status\n (2) Travel\n (3) Hunt\n (4) Scout\n (5) Rest\n (6) Cook\n (7) Help\n (8) Credits\n (9) Quit\n").strip().lower()

        # Handle cheat codes
        if command == 'bubblegum':
            print("You're a dirty little cheater aren't you? Here's a dragon to fight!")
            current_menu = "boss_fight"  # Start the boss fight
            handle_boss_fight()  # Trigger the boss fight immediately
            continue  # Skip to the next iteration
        elif command == 'rowan':
            game_data['resources']['gold'] += 1000
            print("You're a dirty little cheater aren't you? Here's 1000 doge coins!")
            continue  # Skip to the next iteration
        elif command == 'smudge':
            game_data['player']['carry_weight'] = 1000
            print("You're a dirty little cheater aren't you? Here's 1000 pocketses!")
            continue  # Skip to the next iteration

        # Determine the menu based on the command
        if command == '1':
            current_menu = "status"
        elif command == '2':
            current_menu = "travel"
        elif command == '3':
            current_menu = "hunt"
        elif command == '4':
            current_menu = "scout"
        elif command == '5':
            current_menu = "rest"
        elif command == '6':
            current_menu = "cook"
        elif command == '7':
            current_menu = "help"
        elif command == '8':
            current_menu = "credits"
        elif command == '9':
            handle_game_over()
            break  # Exit the loop if the game is over
        elif game_data["journey"]["dragon_encountered"] and command == '0':
            current_menu = "boss_fight"
        else:
            print("Invalid command.")
            continue  # Skip to the next iteration if the command is invalid

        # Now set the music *after* determining the menu
        play_music(current_menu)

        # Execute the corresponding game function
        if command == '1':
            update_game_status()
        elif command == '2':
            travel()
            trigger_environmental_event()
        elif command == '3':
            handle_hunt()
        elif command == '4':
            handle_scout()
            trigger_environmental_event()
        elif command == '5':
            handle_rest()
        elif command == '6':
            handle_cook()
        elif command == '7':
            handle_help()
        elif command == '8':
            display_ascii_art("writtenby", Fore.LIGHTMAGENTA_EX, Style.BRIGHT)
        elif game_data["journey"]["dragon_encountered"] and command == '0':
            handle_boss_fight()


# Utility Functions
# Resource Management Functions
def collect_resource(resource_type, amount):
    if resource_type == "water":
        available_space = game_data["resources"]["waterskins"] * WATER_SKIN_CAPACITY - game_data["resources"]["water"]
        if available_space <= 0:
            print(Fore.RED + "You have no space left in your waterskins!")
            return
        amount = min(amount, available_space)
    elif resource_type == "wood":
        if amount % WOOD_CORD_SIZE != 0:
            print(Fore.RED + "Invalid amount. Wood must be collected in 3-lb increments.")
            return
    # Check carry capacity before collecting
    total_weight_after_collection = game_data["player"]["carry_weight"] + (amount * item_weights.get(resource_type, 0))
    if total_weight_after_collection > MAX_CARRY_CAPACITY:
        print(Fore.RED + "Not enough carry capacity for this much wood.")
        return

    modify_resource(resource_type, amount)

def collect_water(amount):
    if game_data['resources']['waterskins'] <= game_data['resources']['water'] // WATER_SKIN_CAPACITY:
        print(Fore.RED + "You need at least one empty waterskin to collect water!")
        return

    if game_data['resources']['water'] + amount <= game_data['resources']['waterskins'] * WATER_SKIN_CAPACITY:
        game_data['resources']['water'] += amount
        update_carry_weight()
        print(Fore.GREEN + f"Collected {amount} lbs of water.")
    else:
        print(Fore.RED + f"Not enough waterskin space to collect {amount} lbs of water.")


def collect_wood(amount):
    # Ensure wood is collected in multiples of WOOD_CORD_SIZE
    if amount % WOOD_CORD_SIZE != 0:
        print(Fore.RED + "Invalid amount. Wood must be collected in 3-lb increments.")
        return

    game_data['resources']['wood'] += amount
    game_data['resources']['wood_cords'] = game_data['resources']['wood'] // WOOD_CORD_SIZE
    update_carry_weight()
    print(Fore.GREEN + f"Collected {amount} lbs of wood.")


def drink_water():
    if game_data["resources"]["water"] < WATER_DRINK_AMOUNT:
        print(Fore.RED + "You don't have enough water to drink!")
        return
    modify_resource("water", -WATER_DRINK_AMOUNT)
    modify_health(1)
    space()


def get_next_biome(current_biome):
    """
    Randomly selects the next biome based on the current biome.
    """
    possible_biomes = BIOME_CONNECTIONS.get(current_biome, [])
    if not possible_biomes:
        return current_biome  # Stay in the current biome if no connections
    return random.choice(possible_biomes)

def convert_wood_to_cords(wood_weight):
    """Converts wood weight to full cords and returns the number of cords and remaining wood weight."""
    full_cords = wood_weight // WOOD_CORD_SIZE
    remaining_wood = wood_weight % WOOD_CORD_SIZE
    return full_cords, remaining_wood

def update_carry_weight():
    total_weight = 0
    total_weight += game_data["resources"]["food"] * item_weights["food"]
    total_weight += game_data["resources"]["herbs"] * item_weights["herbs"]
    total_weight += game_data["resources"]["supplies"] * item_weights["supplies"]
    total_weight += game_data["resources"]["water"]
    total_weight += game_data["resources"]["waterskins"] * item_weights["waterskin"]
    total_weight += game_data["resources"]["wood"]

    # Round the total weight to one decimal place
    rounded_weight = round(total_weight, 1)

    game_data["player"]["carry_weight"] = rounded_weight
    if rounded_weight > MAX_CARRY_CAPACITY:
        print(Fore.RED + f"Warning: You are over your carry capacity! ({rounded_weight:.1f} lbs > {MAX_CARRY_CAPACITY} lbs)")


def drop_excess_weight(resource_type):
    over_capacity = game_data["player"]["carry_weight"] - MAX_CARRY_CAPACITY
    if resource_type in item_weights:
        dropped_amount = min(over_capacity // item_weights[resource_type], game_data["resources"][resource_type])
        if dropped_amount > 0:
            modify_resource(resource_type, -dropped_amount, f"Carry capacity exceeded: Dropped {dropped_amount} {resource_type}.", from_drop_excess=True)
    else:
        print(f"Warning: Cannot drop excess {resource_type} - no weight defined.")

def modify_resource(resource_type, amount, event_description=None, from_drop_excess=False):
    original_amount = game_data["resources"][resource_type]
    game_data["resources"][resource_type] += amount
    game_data["resources"][resource_type] = max(0, game_data["resources"][resource_type])
    update_carry_weight()

    if event_description:
        print(Fore.CYAN + f"Event: {event_description}")

    if game_data["player"]["carry_weight"] > MAX_CARRY_CAPACITY and not from_drop_excess:
        print(Fore.RED + "Warning: Carry capacity exceeded. Dropping excess resources.")
        drop_excess_weight(resource_type)

def modify_health(amount, event_description=None):
    """Modifies health and prints a message. Handles multi-day health changes."""
    game_data["player"]["health"] += amount
    game_data["player"]["health"] = min(MAX_HEALTH_LEVEL, game_data["player"]["health"])
    if game_data["player"]["health"] <= 0:
        handle_game_over()

    if event_description:
        print(Fore.CYAN + f"Event: {event_description}")

def travel_miles(amount):
    game_data["journey"]["totalMilesTraveled"] += amount
    game_data["journey"]["totalMilesTraveled"] = min(TOTAL_MILES, game_data["journey"]["totalMilesTraveled"])
    print(Fore.GREEN + f"Traveled an extra {amount} miles! Total miles traveled: {game_data['journey']['totalMilesTraveled']}")

def modify_gold(amount):
    game_data["resources"]["gold"] += amount
    print(Fore.YELLOW + f"Gold modified by {amount}. Current gold: {game_data['resources']['gold']}")

def modify_waterskins(amount):
    game_data["resources"]["waterskins"] += amount
    print(Fore.YELLOW + f"Waterskins modified by {amount}. Current waterskins: {game_data["resources"]["waterskins"]}")

class Encounter:
    def __init__(self, encounter_type, difficulty_mod=0):
        self.encounter_type = encounter_type
        self.difficulty_mod = difficulty_mod

    def simulate(self, survival, progress):
        """Simulates the encounter and determines the outcome."""
        # Calculate difficulty based on progress
        if progress <= 0.25:
            base_difficulty = 10
        elif progress <= 0.50:
            base_difficulty = 15
        elif progress <= 0.75:
            base_difficulty = 20
        elif progress <= 0.90:
            base_difficulty = 25
        else:
            base_difficulty = 30

        difficulty = base_difficulty + self.difficulty_mod

        # Roll for outcome
        d20_roll = roll_d20()
        total_roll = d20_roll + survival

        print(Fore.YELLOW + f"You roll a d20: {d20_roll} + Survival Skill ({survival}) = {total_roll}")
        print(Fore.YELLOW + f"The difficulty of the {self.encounter_type} encounter is {difficulty}.")

        # Determine success or failure
        if total_roll >= difficulty:
            self.on_success()
        else:
            self.on_failure()

    def on_success(self):
        """Override this method in child classes to handle success logic."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def on_failure(self):
        """Override this method in child classes to handle failure logic."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class FloraEncounter(Encounter):
    def __init__(self):
        super().__init__(encounter_type="Flora", difficulty_mod=0)

    def on_success(self):
        herbs_found = random.randint(5, 10)
        print(Fore.GREEN + f"You successfully forage the area and find {herbs_found} herbs!")
        modify_resource("herbs", herbs_found)

    def on_failure(self):
        print(Fore.RED + "You fail to find any useful plants and waste precious time.")
        modify_health(-5)


class FaunaEncounter(Encounter):
    def __init__(self, subtype):
        difficulty_mod = 0  # Adjust as needed for different fauna subtypes
        super().__init__(encounter_type=f"Fauna ({subtype})", difficulty_mod=difficulty_mod)

    def on_success(self):
        if "wild_beast" in self.encounter_type:
            food_gained = random.randint(10, 20)
            print(Fore.GREEN + f"You defeat the wild beast and gain {food_gained} lbs of food!")
            modify_resource("food", food_gained)

    def on_failure(self):
        print(Fore.RED + "The wild beast wounds you before escaping!")
        modify_health(-10)


class HumanoidEncounter(Encounter):
    def __init__(self, subtype):
        difficulty_mod = 0  # Adjust as needed for different humanoid subtypes
        super().__init__(encounter_type=f"Humanoid ({subtype})", difficulty_mod=difficulty_mod)

    def on_success(self):
        if "bandit" in self.encounter_type:
            supplies_gained = random.randint(1, 3)
            gold_gained = random.randint(10, 30)
            print(Fore.GREEN + f"You defeat the bandit and gain {supplies_gained} supplies and {gold_gained} gold!")
            modify_resource("supplies", supplies_gained)
            modify_gold(gold_gained)

    def on_failure(self):
        print(Fore.RED + "The bandit overpowers you and steals some of your resources!")
        modify_resource("supplies", -2)
        modify_gold(-10)
        modify_health(-15)


def simulate_attack(encounter_type, subtype=None):
    """Simulates an encounter based on the type."""
    progress = game_data["journey"]["totalMilesTraveled"] / TOTAL_MILES
    survival = game_data["player"]["survival"]

    if encounter_type == "flora":
        encounter = FloraEncounter()
    elif encounter_type == "fauna" and subtype:
        encounter = FaunaEncounter(subtype)
    elif encounter_type == "humanoid" and subtype:
        encounter = HumanoidEncounter(subtype)
    else:
        print("Invalid encounter type!")
        return

    encounter.simulate(survival, progress)

# Example usage (assuming modify_resource and modify_health are defined elsewhere):
#simulate_attack("flora")
#simulate_attack("fauna", "wild_beast")
#simulate_attack("humanoid", "bandit")


def space():
    print("\n")

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def roll_d20():
    return random.randint(1, 20)

def display_ascii_art(art_key, color=Fore.WHITE, style=Style.BRIGHT):
    print(color + ascii_art.get(art_key, "")) # Handle missing keys gracefully

### MINI-GAME FUNCTION (moving target game) ###
def calculate_speed(survival):
    """Calculate speed of target minigame based on survival level."""
    return max(0.001, 0.001 + (survival * 0.015))  # 0 is hardest, 8 is easiest

def handle_target_practice(intro_text, result_text_success, result_text_failure, strong_success_action, weak_success_action, failure_action, roll_modifier=0):
    """
    A mini-game where the player attempts to time their input to hit a moving target.
    
    Args:
        intro_text (str): Text to display when the mini-game starts.
        result_text_success (str): Text to display on a successful hit.
        result_text_failure (str): Text to display on a miss.
        strong_success_action (callable): Function to execute on a strong success.
        weak_success_action (callable): Function to execute on a weak success.
        failure_action (callable): Function to execute on a failure.
        roll_modifier (int): Modifier to be applied to a roll in the success actions.
        
    """
    bar_length = 15  # Length of the progress bar
    target_center = random.randint(1, bar_length - 3)  # Center position for the target (3 spaces wide)
    indicator_position = 0  # Starting position of the moving indicator
    running = True  # Indicator movement control

    # Calculate speed based on survival
    speed = calculate_speed(game_data['player']['survival'])

    # Instructions
    clear_screen()
    print(intro_text)
    print("=" * len(intro_text))
    print("Press Enter to start!")
    input()  # Wait for player to press Enter

    # Indicator movement logic
    def move_indicator():
        """Moves the indicator back and forth across the bar."""
        nonlocal indicator_position, running
        direction = 1  # 1 for right, -1 for left (ping-pong movement)
        while running:
            # Create the bar and mark the target
            bar = ['-'] * bar_length
            bar[target_center] = 'X'  # Center target marker (bullseye)
            bar[target_center - 1] = 'x'  # Left target marker
            bar[target_center + 1] = 'x'  # Right target marker
            bar[indicator_position] = '^'  # Moving indicator

            # Display the bar
            clear_screen()
            print("[" + ''.join(bar) + "]")
            print("Press space to hit the target!")
            time.sleep(speed)

            # Move the indicator
            indicator_position += direction
            if indicator_position >= bar_length:  # Bounce back at the right end
                indicator_position = bar_length - 1
                direction = -1
            elif indicator_position < 0:  # Bounce back at the left end
                indicator_position = 0
                direction = 1

    # Start the indicator thread
    indicator_thread = threading.Thread(target=move_indicator)
    indicator_thread.daemon = True  # Ensure thread closes when main program exits
    indicator_thread.start()

    # Capture player input
    try:
        while running:
            if keyboard.is_pressed("space"):  # Detect spacebar press
                hit_position = indicator_position  # Store the hit position
                running = False  # Stop the indicator movement
                clear_screen()  # Clear the screen to show the result
                
                # Display the hit location
                bar = ['-'] * bar_length
                bar[target_center] = 'X'  # Center target marker (bullseye)
                bar[target_center - 1] = 'x'  # Left target marker
                bar[target_center + 1] = 'x'  # Right target marker
                bar[hit_position] = '0'  # Mark the hit position
                print("[" + ''.join(bar) + "]")
                print(f"You hit at position {hit_position + 1}!")  # +1 for human-readable position
                
                # Determine success
                if target_center - 1 <= hit_position <= target_center + 1:  # Check for hits
                    if hit_position == target_center:  # Bullseye
                        print("\033[92m" + result_text_success + " (Bullseye!)\033[0m")
                        strong_success_action(roll_modifier)  # Strong success
                    else:  # Weak success
                        print("\033[93m" + result_text_success + " (Weak Success!)\033[0m")
                        weak_success_action(roll_modifier)  # Weak success
                else:
                    print("\033[91m" + result_text_failure + "\033[0m")  # Red text for miss
                break
    except KeyboardInterrupt:
        running = False
        print("\nMini-game interrupted.")
    finally:
        indicator_thread.join()  # Ensure the thread ends cleanly

    # Pause briefly before returning to the main game
    time.sleep(2)

def travel_mini():
    def successful_travel_strong(survival):
        miles_traveled = int(random.randint(15, 25) * (1 + survival * 0.1))
        game_data['journey']['totalMilesTraveled'] += miles_traveled
        print(f"You successfully traveled {miles_traveled} miles!")

    def successful_travel_weak(survival):
        miles_traveled = int(random.randint(10, 15) * (1 + survival * 0.05))
        game_data['journey']['totalMilesTraveled'] += miles_traveled
        print(f"You traveled {miles_traveled} miles, but could have gone further.")

    def fail_travel():
        print("You got lost and wasted time traveling. No miles gained.")

    handle_target_practice(
        "TRAVELING MINI-GAME",
        "Hit! You successfully navigate the terrain!",
        "Miss! You get lost and waste time.",
        successful_travel_strong,
        successful_travel_weak,
        fail_travel
    )


def hunt_mini():
    def successful_hunt_strong(survival):
        food_gained = int(random.randint(10, 20) * (1 + survival * 0.1))
        game_data['resources']['food'] += food_gained
        print(f"You gained {food_gained} lbs of food!")

    def successful_hunt_weak(survival):
        food_gained = int(random.randint(5, 10) * (1 + survival * 0.05))
        game_data['resources']['food'] += food_gained
        print(f"You gained {food_gained} lbs of food, but could have done better!")

    def fail_hunt():
        modify_resource("food", -2, "Hunting Failure: Lost some food") #Penalty for failure
        print("You failed to catch any prey and lost some food.")

    handle_target_practice(
        "You found prey! TIME FOR HUNTING MINI-GAME",
        "Hit! You successfully catch your prey!",
        "Miss! The prey escaped, and you return empty-handed.",
        successful_hunt_strong,
        successful_hunt_weak,
        fail_hunt
    )


def scout_mini(resource_type):
    amount_gained = 0

    def successful_scout_strong(survival):
        nonlocal amount_gained
        amount_gained = int(random.randint(4, 6) * (1 + survival * 0.1))
        print(f"You're in the zone while scouting and find {amount_gained} {resource_type}!")

    def successful_scout_weak(survival):
        nonlocal amount_gained
        amount_gained = int(random.randint(2, 4) * (1 + survival * 0.05))
        print(f"You do well enough scouting and gather {amount_gained} {resource_type}.")

    def fail_scout():
        print(f"Your scouting efforts yielded nothing.")

    if resource_type not in game_data['resources']:
        print("Invalid resource type for scouting!")
        return 0

    handle_target_practice(
        f"SCOUTING MINI-GAME: {resource_type.upper()}",
        f"Hit! You spot the {resource_type} you need!",
        f"Miss! Your scouting yielded no {resource_type}.",
        successful_scout_strong,
        successful_scout_weak,
        fail_scout
    )
    return amount_gained


def rest_mini():
    def successful_rest_strong(survival):
        health_restored = int(random.randint(10, 15) * (1 + survival * 0.1))
        max_health = game_data['player'].get('max_health', 100)
        game_data['player']['health'] = min(game_data['player']['health'] + health_restored, max_health)
        print(f"You restored {health_restored} health during your rest!")

    def successful_rest_weak(survival):
        health_restored = int(random.randint(5, 10) * (1 + survival * 0.05))
        max_health = game_data['player'].get('max_health', 100)
        game_data['player']['health'] = min(game_data['player']['health'] + health_restored, max_health)
        print(f"You restored {health_restored} health, but it wasn't enough.")

    def fail_rest():
        modify_health(-5, "Rest Failure: Lost some health") #Penalty for failure
        print("You had trouble resting and lost some health.")

    handle_target_practice(
        "RESTING MINI-GAME",
        "Hit! You feel well-rested and rejuvenated!",
        "Miss! Your rest was restless and ineffective.",
        successful_rest_strong,
        successful_rest_weak,
        fail_rest
    )



# GAME EVENT FUNCTIONS

environmental_events = [
    {
        "name": "Storm",
        "description": "A violent storm disrupts your journey, causing delays and minor injuries.",
        "effect": lambda: (advance_days(1), modify_health(-5)),
    },
    {
        "name": "Wild Animal Encounter",
        "description": "You are attacked by a wild animal! Fight it off or suffer injuries.",
        "effect": lambda: (simulate_attack("fauna", "wild_beast")),
    },
    {
        "name": "Pleasant Weather",
        "description": "The weather is perfect, and you feel rejuvenated. If you use the weather to your advantage, you can travel further.",
        "effect": lambda: (modify_health(5), travel_mini)
    },
    {
        "name": "Bandit Ambush",
        "description": "Bandits attack and steal some of your supplies!",
        "effect": lambda: (modify_resource("supplies", -1), simulate_attack("humanoid","bandit"))
    },
    {
        "name": "Abandoned Supplies",
        "description": "You find an abandoned campsite with some useful supplies.",
        "effect": lambda: modify_resource("supplies", 3),
    },
    {
        "name": "Shortcut",
        "description": "You discover a hidden path that saves time on your journey.",
        "effect": lambda: travel_miles(50),
    },
     {
        "name": "Gold Discovery",
        "description": "You stumble upon a small pouch containing extra gold!",
        "effect": lambda: modify_gold(random.randint(5, 15)),
    },
    {
        "name": "Slain Bandits",
        "description": "You spot bandits in the brush, fat and drunk from rest. You get the jump on them and they flee leaving behind some gold.",
        "effect": lambda: modify_gold(random.randint(10, 50))
    },
    {
        "name": "Herbalist Encounter",
        "description": "You meet an herbalist selling herbs!",
        "effect": lambda: handle_herbalist_encounter(),
    },
    {
        "name": "Random Trader",
        "description": "You encounter a random trader selling resources.",
        "effect": lambda: handle_trade(trader_type=random.choice(["food_for_supplies", "supplies_for_food", "gold_for_food", "gold_for_water"])),
    },
    {
        "name": "Waterfall",
        "description": "You find a freshwater waterfall! You can collect water here.",
        "effect": lambda: collect_water(32),
    },
    {
        "name": "Water Merchant",
        "description": "You encounter a water merchant selling waterskins.",
        "effect": lambda: handle_water_merchant(),
    },
    {
        "name": "You Find an Empty Waterskin",
        "description": "You find an empty waterskin!",
        "effect": lambda: modify_resource("waterskins", int(random.randint(2, 3))),
    },
    {
        "name": "Stumbled Upon Wood",
        "description": "You stumble upon a pile of wood!",
        "effect": lambda: modify_resource("wood", random.randint(3, 9)),
    },
    {
        "name": "Lost Trail",
        "description": "You lose the trail and wander for hours before finding your way again.",
        "effect": lambda: advance_days(1),
    },
    {
        "name": "Hidden Cache",
        "description": "You discover a hidden cache of supplies left by a previous traveler.",
        "effect": lambda: modify_resource("supplies", random.randint(2, 5)),
    },
    {
        "name": "River Crossing",
        "description": "You find a river. Crossing it costs time and energy, but you refill your waterskins.",
        "effect": lambda: (advance_days(1), collect_water(32)),
    },
    {
        "name": "Ancient Ruins",
        "description": "You stumble upon ancient ruins. Searching them yields valuable trinkets.",
        "effect": lambda: modify_gold(random.randint(15, 30)),
    },
    {
        "name": "Wild Berries",
        "description": "You find a bush full of wild berries, enough to supplement your food supply.",
        "effect": lambda: modify_resource("food", random.randint(3, 7)),
    },
    {
        "name": "Expensive Merchant",
        "description": "A merchant offers goods at steep prices.",
        "effect": lambda: handle_trade(trader_type=random.choice(["food_for_supplies", "supplies_for_food", "gold_for_food", "gold_for_water"]), fair=False),
    },
]

scouting_events = [
    {
        "name": "Gentle Rain",
        "description": "A mild snap rainstorm happens while you're scouting, granting you easy clean water.",
        "effect": lambda: collect_water(8), #Use collect_water to handle waterskin capacity
    },
    {
        "name": "Wild Animal Encounter",
        "description": "You are attacked by a wild animal! Fight it off or suffer injuries.",
        "effect": lambda: simulate_attack("fauna", "wild_beast"),
    },
    {
        "name": "Pleasant Weather",
        "description": "The weather is perfect, and you feel rejuvenated.",
        "effect": lambda: modify_health(5),
    },
    {
        "name": "Abandoned Supplies",
        "description": "You find an abandoned campsite with some useful supplies.",
        "effect": lambda: modify_resource("supplies", random.randint(1,3)),
    },
    {
        "name": "Gold Discovery",
        "description": "You stumble upon a small pouch containing extra gold!",
        "effect": lambda: modify_gold(random.randint(10, 20)),
    },
    {
        "name": "You Find Empty Waterskins",
        "description": "You find empty waterskins!",
        "effect": lambda: modify_waterskins(int(random.randint (2,3))),
    },
    {
        "name": "Mushroom Grove",
        "description": "You find a grove of edible mushrooms. Some are highly nutritious.",
        "effect": lambda: modify_resource("food", random.randint(4, 6)),
    },
    {
        "name": "Abandoned Camp",
        "description": "An abandoned camp yields useful items.",
        "effect": lambda: (modify_resource("supplies", random.randint(1, 3)), modify_gold(random.randint(5, 15))),
    },
    {
        "name": "Bird Flock",
        "description": "A flock of birds alerts you to a water source nearby.",
        "effect": lambda: collect_water(16),
    },
    {
        "name": "Herbal Trove",
        "description": "You discover a patch of rare herbs, useful for potions.",
        "effect": lambda: modify_resource("herbs", random.randint(2, 5)),
    },
    {
        "name": "Natural Trap",
        "description": "You stumble into a natural trap. Escaping costs health and time.",
        "effect": lambda: (modify_health(-10), advance_days(1)),
    },
    {
        "name": "Stray Animal",
        "description": "You find a stray animal that seems lost. It might lead you to something valuable.",
        "effect": lambda: modify_resource("food", random.randint(3, 6)),
    },

]

def trigger_environmental_event():
    if random.random() < 0.02:      # 2% chance
        event = random.choice(environmental_events)
        print(Fore.CYAN + f"Event: {event['name']}")
        print(Fore.WHITE + event['description'])
        event["effect"]()
        space()

def trigger_scouting_event():
    if random.random() < 0.07:      # 7% chance
        event = random.choice(scouting_events)
        print(Fore.CYAN + f"Event: {event['name']}")
        print(Fore.WHITE + event['description'])
        event["effect"]()
        space()

def handle_herbalist_encounter():
    print("\nHerbalist Encounter:")
    print("The herbalist offers 3 herbs for 1 gold piece.")
    while True:
        try:
            herbs_to_buy = int(input("How many herbs would you like to buy? (multiples of 3): "))
            if herbs_to_buy >= 0 and herbs_to_buy % 3 == 0:
                break
            else:
                print("Invalid amount. Please enter a multiple of 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    gold_cost = herbs_to_buy // 3
    if game_data['resources']['gold'] >= gold_cost:
        game_data['resources']['gold'] -= gold_cost
        game_data['resources']["herbs"] += herbs_to_buy
        print(f"You bought {herbs_to_buy} herbs for {gold_cost} gold.")
    else:
        print("You don't have enough gold.")
    space()

def handle_water_merchant():
    print("\nWater Merchant Encounter:")
    print("The merchant offers to sell you waterskins.")
    while True:
        try:
            waterskins_to_buy = int(input("How many waterskins would you like to buy? (8 gold per waterskin): "))
            if waterskins_to_buy >= 0:
                break
            else:
                print("Invalid amount. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    gold_cost = waterskins_to_buy * 8
    if game_data['resources']['gold'] >= gold_cost:
        game_data['resources']['gold'] -= gold_cost
        game_data['resources']["waterskins"] += waterskins_to_buy
        print(f"You bought {waterskins_to_buy} waterskins for {gold_cost} gold.")
    else:
        print("You don't have enough gold.")
    space()





# COMBAT FUNCTIONS

def handle_boss_fight():
    """Simulates the epic boss fight against the dragon."""
    global current_menu
    current_menu = "boss_fight"  # Set the current menu
    play_music(current_menu)  # Play music for the boss fight
    dragon_health = 180  
    player_health = game_data['player']['health']
    game_data['journey']['dragon_encountered'] = True
    potions = create_potions()

    print(Fore.RED + "\nYOU HAVE ARRIVED AT THE DRAGON'S LAIR!")
    print(Fore.GREEN + f"\nYou quickly make {potions} POTIONS out of your Herbs, Food, and Supplies")
    display_ascii_art("dragonart", Fore.RED)

    survival_value = game_data["player"]["survival"]

    while dragon_health > 0 and player_health > 0:
        print_status(dragon_health, player_health, potions)

        player_choice = get_player_choice()

        if player_choice == 6:  # Flee
            print(Fore.RED + "Coward! The Dragon strikes you down as you flee!")
            player_health = 0  # Fleeing results in defeat
        elif player_choice == 7:  # Mute/Unmute Music
            toggle_music()  # Toggle music on mute/unmute
            continue  # Skip the dragon's turn
        else:
            result = player_action(
                player_choice, dragon_health, player_health, potions, survival_value
            )
            if isinstance(result, bool) and result is False:  # Check if the action was invalid
                print(Fore.RED + "You cannot perform that action. Please choose a valid option.")
            else:
                dragon_health, player_health, potions = result  # Unpack the valid result

                if player_health > 0 and dragon_health > 0:
                    dragon_health, player_health = dragon_turn(dragon_health, player_health, survival_value)

    conclude_battle(dragon_health)

def create_potions():
    """Calculates and returns the number of potions available."""
    game_data['combat']['potions'] = (
        game_data['resources']['herbs'] + 
        (game_data['resources']['food'] // 8) + 
        (game_data['resources']['supplies'] // 8)
    )
    return game_data['combat']['potions']

def get_survival_value():
    """Prompts the player to input a survival value and ensures it's valid."""
    while True:
        try:
            survival_value = int(input("Enter your survival value (0-8): "))
            if 0 <= survival_value <= 8:
                game_data['player']['survival'] = survival_value
                return survival_value
            else:
                print(Fore.YELLOW + "Survival value must be between 0 and 8.")
        except ValueError:
            print(Fore.YELLOW + "Invalid input.")

def print_status(dragon_health, player_health, potions):
    """Prints the current status of the dragon and player."""
    print(f"\n{Fore.CYAN}Dragon Health: {dragon_health} | Your Health: {player_health} | Potions: {potions}{Style.RESET_ALL}\n")

def get_player_choice():
    """Gets and returns the player's action choice."""
    player = game_data['player']
    
    print("\nYour Turn:")
    print("1. Attack (Sword)")
    print("2. Attack (Magic)")
    
    # Display defend option with cooldown status
    defend_status = (f"{Fore.YELLOW}On Cooldown for {player['defend_cooldown']} more turns" 
                     if player['defend_cooldown'] > 0 else "Available")
    print(f"3. Defend (Reflect) - {defend_status}")
    
    print("4. Use Potion")
    
    # Display Stun-Splosion with cooldown status
    stun_status = (f"{Fore.YELLOW}On Cooldown for {player['stun_splosion_cooldown']} more turns" 
                   if player['stun_splosion_cooldown'] > 0 else "Available")
    print(f"5. Cast Stun-Splosion (10 Potions) - {stun_status}")
    
    print("6. Flee")
    print("7. Mute/Unmute Music")

    while True:
        try:
            player_choice = int(input("Choose your action (1-7): "))
            if 1 <= player_choice <= 7:  # Adjusted to 7 for valid choices
                return player_choice
            else:
                print(Fore.RED + "Invalid choice. Please choose a number between 1 and 7.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.")

def roll_to_hit(modifier, target_ac):
    """Rolls a d20 to determine if the hit is successful."""
    roll = random.randint(1, 20)
    total = roll + modifier
    print(f"Rolled a d20: {roll} + Modifier: {modifier} = Total: {total}")
    return total >= target_ac, roll  # Return whether it hit and the roll

def player_action(choice, dragon_health, player_health, potions, survival_value):
    """Handles the player's action based on their choice."""
    hit_success = False
    player = game_data['player']

    if choice == 1:  # Sword Attack
        hit_success, _ = roll_to_hit(survival_value, DRAGON_AC)
        if hit_success:
            damage = random.randint(10, 25)
            dragon_health -= damage
            print(Fore.GREEN + f"You swing your sword, dealing {damage} damage!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Your attack missed!" + Style.RESET_ALL)
    elif choice == 2:  # Magic Attack
        hit_success, _ = roll_to_hit(survival_value, DRAGON_AC)
        if hit_success:
            damage = random.randint(15, 30)
            dragon_health -= damage
            print(Fore.GREEN + f"You unleash a spell, dealing {damage} damage!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Your spell missed!" + Style.RESET_ALL)
    elif choice == 3:  # Defend
        if player['defend_cooldown'] == 0:
            print("You raise your shield.")
            player['defend_cooldown'] = 3  # Set cooldown for defend
        else:
            print(f"Defend is on cooldown for {player['defend_cooldown']} more turns.")
            return False  # Invalid action
    elif choice == 4:  # Use Potion
        if potions > 0:
            potions -= 1
            health_restored = random.randint(33, 66)
            player_health = min(player_health + health_restored, MAX_HEALTH_LEVEL)
            print(Fore.GREEN + f"You drink a potion, restoring {health_restored} health!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "You have no potions left!" + Style.RESET_ALL)
            return False  # Invalid action
    elif choice == 5:  # Stun-Splosion
        if player['stun_splosion_cooldown'] == 0:
            if potions >= 10:
                potions -= 10
                stun_damage = random.randint(40, 50)
                dragon_health -= stun_damage
                print(Fore.GREEN + f"You cast Stun-Splosion, dealing {stun_damage} damage! Dragon stunned!" + Style.RESET_ALL)
                player['stun_splosion_cooldown'] = 5  # Set cooldown for Stun-Splosion
            else:
                print(Fore.RED + "Not enough potions!" + Style.RESET_ALL)
                return False  # Invalid action
        else:
            print(Fore.RED + f"Stun-Splosion is on cooldown for {player['stun_splosion_cooldown']} more turns." + Style.RESET_ALL)
            return False  # Invalid action
    elif choice == 6:  # Flee
        damage = random.randint(10, 20)
        player_health -= damage
        print(Fore.RED + f"Coward! The dragon deals {damage} damage as you futilely attempt to flee!" + Style.RESET_ALL)

    return dragon_health, player_health, potions

def dragon_turn(dragon_health, player_health, survival_value):
    """Handles the dragon's turn."""
    print("\nDragon's Turn:")
    time.sleep(1)

    # Dragon hit modifier based on survival value
    dragon_hit_modifier = max(0, 8 - survival_value)  # Mapping of survival to dragon hit modifier
    hit_success, damage_roll = roll_to_hit(dragon_hit_modifier, PLAYER_AC)

    if hit_success:
        damage = random.randint(20, 40)
        if game_data['player']['defend_cooldown'] > 0:  # Check for defend cooldown
            deflected_damage = damage // 2
            dragon_health -= deflected_damage
            print(Fore.GREEN + f"You deflect {deflected_damage} damage back to the dragon!" + Style.RESET_ALL)
            print(Fore.GREEN + "You take no damage due to your defense!" + Style.RESET_ALL)
        else:
            player_health -= damage
            print(Fore.GREEN + f"The dragon attacks and deals {damage} damage!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "The dragon's attack missed!" + Style.RESET_ALL)

    # Cooldown management for defend and Stun-Splosion
    if game_data['player']['defend_cooldown'] > 0:
        game_data['player']['defend_cooldown'] -= 1
    
    if game_data['player']['stun_splosion_cooldown'] > 0:
        game_data['player']['stun_splosion_cooldown'] -= 1

    return dragon_health, player_health

def conclude_battle(dragon_health):
    """Determines the outcome of the battle."""
    if dragon_health <= 0:
        print(Fore.GREEN + "\nYOU HAVE DEFEATED THE DRAGON! YOU WIN!!!")
        display_ascii_art("dragonart", Fore.GREEN)
    else:
        handle_game_over()

def handle_purchase():
    """
    Enhanced gear purchasing menu with music, carry capacity checks, screen refresh,
    and validation for waterskins, water, wood cords, and wood.
    Automatically ends purchasing if the player runs out of gold or reaches carry capacity.
    """
    global current_menu
    current_menu = "gear_shop" #Set current menu for gear shop
    play_music(current_menu) #Play music for gear shop
    display_ascii_art("gear_shop", Fore.WHITE + Style.BRIGHT)
    print("\nWelcome to the Gear Shop!")
    print("-" * 30)

    while True:
        # Display current stats and inventory
        update_carry_weight()
        print(f"Gold: {game_data['resources']['gold']} gp | Carry Weight: {game_data['player']['carry_weight']}/{MAX_CARRY_CAPACITY} lbs")
        print("-" * 30)
        print("Items Available:")
        print("1. Food (1 gp/lb)")
        print("2. Water (2 gp/waterskin, 8 lbs of water per waterskin)")
        print("3. Herbs (3 gp each)")
        print("4. Supplies (2 gp/lb)")
        print("5. Wood Cords (3 gp for 3 lbs of wood)")
        print("6. Finish Shopping")
        print(Fore.GREEN + Style.BRIGHT + f"""Your Current Resources: 
        Food: {game_data['resources']['food']} lbs, 
        Water: {game_data['resources']['water']} lbs, 
        Waterskins: {game_data['resources']['waterskins']}, 
        Herbs: {game_data['resources']['herbs']}, 
        Supplies: {game_data['resources']['supplies']}, 
        Wood: {game_data['resources']['wood']} lbs,
        Wood Cords: {game_data['resources']['wood_cords']}\n""")

        if game_data["resources"]["gold"] <= 0:
            print(Fore.RED + "\nYou've run out of gold! Shopping is complete.")
            break  # Exit the loop if no gold remains

        if game_data['player']['carry_weight'] >= MAX_CARRY_CAPACITY:
            print(Fore.RED + "\nYou've reached your carry capacity! Shopping is complete.")
            break  # Exit the loop if carry capacity is reached

        try:
            # Get player choice
            choice = int(input("What would you like to buy? (1-6): "))
            if choice == 6:  # Finish shopping
                print(Fore.YELLOW + "\nShopping complete! Beginning your journey...")
                break  # Exit the loop if the player chooses to finish shopping

            # Map choice to item type and cost
            item_type = {1: "food", 2: "water", 3: "herbs", 4: "supplies", 5: "wood"}[choice]
            item_cost = item_costs[item_type]
            item_weight = item_weights[item_type] if item_type != "water" else WATER_SKIN_CAPACITY

            # Ask how many items to purchase
            while True:
                try:
                    quantity = int(input(f"How many {item_type} would you like to buy? (Enter 0 to cancel): "))
                    if quantity == 0:
                        print(Fore.CYAN + "Purchase canceled. Returning to menu...")
                        break  # Return to the menu
                    elif quantity > 0:
                        break
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            # If the user cancels, restart the menu
            if quantity == 0:
                continue

            # Calculate total cost and total weight
            total_cost = item_cost * quantity
            total_weight = item_weight * quantity

            if item_type == "water":  # Adjust weight and cost for waterskins
                total_cost = 2 * quantity  # Cost includes both waterskin and water
                total_weight = WATER_SKIN_CAPACITY * quantity  # Water weight per waterskin

            elif item_type == "wood":  # Adjust for wood cords
                total_cost = 3 * quantity
                total_weight = WOOD_CORD_SIZE * quantity

            # Check affordability and carry capacity
            if game_data["resources"]["gold"] < total_cost:
                print(Fore.RED + "You don't have enough gold to make this purchase.")
                input(Fore.CYAN + "Press Enter to continue...")
                clear_screen()
                continue

            if game_data['player']['carry_weight'] + total_weight > MAX_CARRY_CAPACITY:
                print(Fore.RED + "This purchase exceeds your carry capacity. Choose fewer items.")
                input(Fore.CYAN + "Press Enter to continue...")
                clear_screen()
                continue

            # Finalize purchase
            game_data["resources"]["gold"] -= total_cost
            if item_type == "food":
                modify_resource("food", quantity)
            elif item_type == "water":
                modify_resource("waterskins", quantity)  # Add waterskins
                modify_resource("water", WATER_SKIN_CAPACITY * quantity)  # Add full water to each waterskin
            elif item_type == "herbs":
                modify_resource("herbs", quantity)
            elif item_type == "supplies":
                modify_resource("supplies", quantity)
            elif item_type == "wood":
                modify_resource("wood", WOOD_CORD_SIZE * quantity)  # Add wood
                modify_resource("wood_cords", quantity)  # Add wood cords

            # Success message
            print(Fore.GREEN + f"Purchase successful! You bought {quantity} {item_type}(s) for {total_cost} gp.")

        except (ValueError, KeyError):
            print("Invalid choice. Please enter a valid number (1-6).")

        input(Fore.CYAN + "Press Enter to continue...")
        clear_screen()


def handle_game_start():

    # Game Start
    display_ascii_art("title", Fore.RED)
    space()
    game_data["player"]["survival"] = int(input("Set your Survival Skill 0-8 \n(0 = Hard)---(4 = Medium)---(8 = Easy)\n"))
    set_carry_capacity(survival=game_data["player"]["survival"])
    space()
    input("Press Enter to continue...")
    clear_screen()
    print(Style.BRIGHT + welcome_text)
    space()
    display_ascii_art("dragonart", Fore.RED)
    input("Hit any key to start...") #Pause before starting gear purchase
    clear_screen()

    # Start the game with gear purchasing
    """
    Starts the game with a streamlined gear purchasing process.
    Automatically allocates gold and sets up the player's inventory.
    """
    print(Fore.YELLOW + "\nWelcome to the Journey Preparation Phase!")
    game_data["resources"]["gold"] = 50 + random.randint(1, 100)  # Random starting gold
    game_data["player"]["carry_weight"] = 0
    game_data["journey"]["current_biome"] = random.choice(BIOMES)
    update_carry_weight()

    print(Fore.CYAN + f"You start with {game_data['resources']['gold']} gold pieces to prepare for your journey.")
    print("Spend your gold wisely to gather essential resources.")

    handle_purchase()  # Call the updated purchase menu
    print(Fore.GREEN + "\nYour journey begins! Good luck!")


def travel():
    # Check if already at the goal
    if game_data['journey']['totalMilesTraveled'] >= TOTAL_MILES:
        print(Fore.GREEN + "You have already reached the dragon's lair. No further travel is needed!")
        return
    
    global current_biome
    current_biome = get_next_biome(current_biome)
    game_data["journey"]["current_biome"] = current_biome
    
    """Allows the player to decide how many days to travel."""
    food = game_data["resources"]["food"]
    water = game_data["resources"]["water"]
    
    # Calculate the maximum number of days the player can travel
    max_days_food = (food - 2) if food > 2 else 0
    max_days_water = (water - 2) if water > 2 else 0
    max_days = min(max_days_food, max_days_water)
    
    if max_days <= 0:
        print("You do not have enough resources to travel.")
        return
    clear_screen()
    display_ascii_art("travel", Fore.BLUE)
    display_ascii_art("hourglasses", Fore.BLUE)
    print(f"You have {food} food and {water} water.")
    print(f"You can travel for up to {max_days} days.")
    
    days_to_travel = int(input(f"How many days would you like to travel? (1-{max_days}): "))
    if days_to_travel < 1 or days_to_travel > max_days:
        print("Invalid number of days.")
        return
    
    # Resolve traveling
    travel_mini()
    events = []
    total_miles_traveled = 0
    for day in range(days_to_travel):
        game_data["resources"]["food"] -= 1
        game_data["resources"]["water"] -= 1
        
        # Advance days
        advance_days(1)
        
        # Calculate miles traveled for the day
        miles_traveled = random.randint(MIN_MILES_PER_TRAVEL, MAX_MILES_PER_TRAVEL)
        total_miles_traveled += miles_traveled
        game_data["journey"]["totalMilesTraveled"] += miles_traveled
        
        # Simulate random events during travel
        event = random.choice(environmental_events)
        event["effect"]()
        events.append(f"Day {day + 1}: {event['name']} - {event['description']}")
    
    print(f"Travel complete. You traveled {total_miles_traveled} miles.")
    # Present a truncated list of events
    print("Events during travel:")
    for event in events:
        print(event)


def handle_travel():
    # Check if already at the goal
    if game_data['journey']['totalMilesTraveled'] >= TOTAL_MILES:
        print(Fore.GREEN + "You have already reached the dragon's lair. No further travel is needed!")
        return
    
    global current_biome
    current_biome = get_next_biome(current_biome)
    game_data["journey"]["current_biome"] = current_biome

    # Calculate travel distance
    miles_traveled = random.randint(MIN_MILES_PER_TRAVEL, MAX_MILES_PER_TRAVEL)
    if game_data['journey']['totalMilesTraveled'] + miles_traveled >= TOTAL_MILES:
        miles_traveled = TOTAL_MILES - game_data['journey']['totalMilesTraveled']
        game_data['journey']['totalMilesTraveled'] += miles_traveled
        print(Fore.GREEN + "You have reached the dragon's lair!")
        display_ascii_art("dragonart", Fore.RED)
    else:
        game_data['journey']['totalMilesTraveled'] += miles_traveled

    # Time passage
    days_traveled = random.randint(MIN_DAYS_PER_TRAVEL, MAX_DAYS_PER_TRAVEL)
    advance_days(days_traveled)

    # Display travel details
    display_ascii_art("travel", Fore.BLUE)
    display_ascii_art("hourglasses", Fore.BLUE)
    print(f"Traveled {days_traveled} days and {miles_traveled} miles. Total miles traveled: {game_data['journey']['totalMilesTraveled']}")
    space()

def handle_hunt():
    # Check if there are supplies available to hunt
    if game_data['resources']['supplies'] <= 0:
        print(Fore.RED + "You do not have enough supplies to hunt! Find supplies or trade to restock.")
        return

    # Available game types and their corresponding weapons
    wildgame_types = {
        "Small": {"weapon": "Snare", "bonus": 6},
        "Medium": {"weapon": "Tripwire", "bonus": 12},
        "Large": {"weapon": "Arrow", "bonus": 18}
    }
    
    # Randomly select the actual game present
    actual_game = random.choice(list(wildgame_types.keys()))

    clear_screen()
    display_ascii_art("hunt", Fore.RED)
    print("""\n
          <-<-<-<-<-<-<-<->->->->->->->->
          ..........SPOT.WILDGAME........
          ...(Choose.the.right.weapon)...
          <-<-<-<-<-<-<-<->->->->->->->->
          """)
    print("You begin searching for signs of game...")
    space()
    
    # Roll for survival check
    survival_roll = roll_d20()
    total_check = survival_roll + game_data['player']['survival']
    
    print(f"\nYou rolled a {survival_roll} + {game_data['player']['survival']} = {total_check}")
    
    # Process the survival check results
    game_hint = ""
    if total_check >= 20:
        print(f"You find clear signs! You're certain there is {actual_game} game in the area!")
        game_hint = actual_game
    elif total_check >= 16:
        # 75% chance of accurate information
        if random.random() < 0.75:
            print(f"You think you see signs of {actual_game} game...")
            game_hint = actual_game
        else:
            false_game = random.choice([g for g in wildgame_types.keys() if g != actual_game])
            print(f"You think you see signs of {false_game} game...")
            game_hint = false_game
    elif total_check >= 13:
        wrong_game = random.choice([g for g in wildgame_types.keys() if g != actual_game])
        print(f"You can tell there definitely isn't any {wrong_game} game here.")
    else:
        print("You find no clear signs of game.")
    
    # Weapon selection
    print("\nChoose your hunting method:")
    print("1. Snare (for Small game)")
    print("2. Tripwire (for Medium game)")
    print("3. Arrow (for Large game)")
    space()
    
    weapon_choices = {
        "1": "Snare",
        "2": "Tripwire",
        "3": "Arrow"
    }
    
    while True:
        choice = input("\n Select your weapon (1-3): ")
        if choice in weapon_choices:
            selected_weapon = weapon_choices[choice]
            break
        print("Please enter a valid choice (1-3)")
    
    # Deduct supplies for hunting
    game_data['resources']['supplies'] -= 1
    print(Fore.YELLOW + f"Used 1 supply for hunting. Supplies remaining: {game_data['resources']['supplies']}.")

    # Process hunting results
    print("\nHunting Results:")
    if selected_weapon == wildgame_types[actual_game]["weapon"]:
        hunt_mini()
        bonus = wildgame_types[actual_game]["bonus"]
        food_gained = FOOD_PER_HUNT + bonus
        game_data['resources']["food"] += food_gained
        print(f"Success! You caught {actual_game} game!")
        print(f"You gained {food_gained} lbs of food! ({FOOD_PER_HUNT} + {bonus} bonus)")
        space()

    # Add ASCII art based on game type
    if actual_game == "Small" and selected_weapon == wildgame_types[actual_game]["weapon"]:
        display_ascii_art("small_game", Fore.WHITE)
    elif actual_game == "Medium" and selected_weapon == wildgame_types[actual_game]["weapon"]:
        display_ascii_art("med_game", Fore.WHITE)
    elif actual_game == "Large" and selected_weapon == wildgame_types[actual_game]["weapon"]:
        display_ascii_art("large_game", Fore.WHITE)
    else:
        game_data['resources']['food'] += 1
        print("You only find some berries and edible flowers.")
        print("You gained 1 lb of food.")
        space()
    
    # Time passage
    days_hunting = random.randint(MIN_DAYS_PER_HUNT, MAX_DAYS_PER_HUNT)
    advance_days(days_hunting)
    
    print(f"\nHunting took {days_hunting} days.")
    print(f"Current food supply: {game_data['resources']['food']} lbs")
    space()
    input("Press Enter to continue...")
    clear_screen()


def handle_scout():
    clear_screen()
    display_ascii_art("scout", Fore.GREEN)
    display_ascii_art("mount", Fore.GREEN)
    print("\nYou are scouting the area. Choose your focus:")
    print("1. Wood (Easiest)")
    print("2. Water (Medium)")
    print("3. Food (Hard)")
    print("4. Herbs (Hardest)")

    # Check resource availability before scouting
    if game_data['resources']["food"] < 2 or game_data['player']['health'] < 2:
        print(Fore.RED + "You do not have enough food or health to scout! You need at least 2 food and 2 health.")
        return

    # Deduct resource costs
    modify_resource("food", -1)

    while True:
        try:
            choice = int(input("Enter your choice (1-4): "))
            if 1 <= choice <= 4:
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    target_resource = {1: "wood", 2: "water", 3: "food", 4: "herbs"}[choice]
    difficulty_modifier = {1: 0, 2: 1, 3: 2, 4: 4}[choice]  # Difficulty affects success threshold

    print(f"\nYou focus your search on {target_resource}.")

    # Roll and calculate total (plus minigame modifier)
    d20_roll = roll_d20()
    survival = game_data['player']['survival']
    modifier = scout_mini(target_resource)
    total_roll = d20_roll + survival + modifier
    print(f"\nYou rolled a {d20_roll} + Survival Skill ({survival}) + Minigame Modifier ({modifier}) = {total_roll}")

    # Determine success level
    if total_roll >= 20 + difficulty_modifier:  # High Success
        amount = random.randint(6, 8)
        print(f"\nYou found a plentiful supply of {target_resource}! You found {amount} {target_resource}!")
        if target_resource == "wood":
            collect_wood(amount)
        elif target_resource == "water":
            collect_water(amount)
        elif target_resource == "food":
            modify_resource("food", amount)
        elif target_resource == "herbs":
            modify_resource("herbs", amount)

    elif total_roll >= 15 + difficulty_modifier:  # Moderate Success
        amount = random.randint(4, 6)
        print(f"\nYou found some {target_resource}! You found {amount} {target_resource}!")
        if target_resource == "wood":
            collect_wood(amount)
        elif target_resource == "water":
            collect_water(amount)
        elif target_resource == "food":
            modify_resource("food", amount)
        elif target_resource == "herbs":
            modify_resource("herbs", amount)

    elif total_roll >= 10 + difficulty_modifier:  # Minor Success
        amount = random.randint(2, 3)
        print(f"\nYou found a small amount of {target_resource}! You found {amount} {target_resource}!")
        if target_resource == "wood":
            collect_wood(amount)
        elif target_resource == "water":
            collect_water(amount)
        elif target_resource == "food":
            modify_resource("food", amount)
        elif target_resource == "herbs":
            modify_resource("herbs", amount)

    else:  # Failure
        print("\nYour scouting efforts yielded nothing.")
        trigger_scouting_event()  # Add a chance of a random event on failure

    space()
    input("Press Enter to continue...")
    clear_screen()

def collect_water(amount):
    if game_data['resources']['waterskins'] <= game_data['resources']['water'] // WATER_SKIN_CAPACITY:
        print(Fore.RED + "You need at least one empty waterskin to collect water!")
        return

    if game_data['resources']['water'] + amount <= game_data['resources']['waterskins'] * WATER_SKIN_CAPACITY:
        game_data['resources']['water'] += amount
        update_carry_weight()
        print(Fore.GREEN + f"Collected {amount} lbs of water.")
    else:
        print(Fore.RED + f"Not enough waterskin space to collect {amount} lbs of water.")

def collect_wood(amount):
    game_data['resources']['wood'] += amount
    game_data['resources']['wood_cords'] = game_data['resources']['wood'] // WOOD_CORD_SIZE
    update_carry_weight()
    print(Fore.GREEN + f"Collected {amount} lbs of wood.")


def handle_rest():
    display_ascii_art("rest", Fore.MAGENTA)
    # Check if there is enough food and wood to rest
    if game_data['resources']['food'] <= 0:
        print(Fore.RED + "You do not have enough food to rest! Hunt or cook to gather more food.")
        return  # Exit the function if food is insufficient
    if game_data['resources']['wood_cords'] <= 0:
        print(Fore.RED + "You do not have enough wood to rest! Find wood or trade to restock.")
        return #Exit the function if wood is insufficient

    # Proceed with resting
    if game_data['player']['health'] < MAX_HEALTH_LEVEL:
        days_resting = random.randint(MIN_DAYS_PER_REST, MAX_DAYS_PER_REST)

        # Spend one food and one wood cord per day rested
        for _ in range(days_resting):
            if game_data['resources']['food'] > 0 and game_data['resources']['wood_cords'] > 0:
                game_data['resources']['food'] -= 1
                game_data['resources']['wood_cords'] -= 1
            else:
                print(Fore.RED + "You ran out of food or wood while resting!")
                break  # Stop resting if food or wood runs out

        # Restore health based on days rested
        game_data['player']['health'] += (6 * days_resting)
        game_data['player']['health'] = min(MAX_HEALTH_LEVEL, game_data['player']["health"])  # Cap health at maximum level

        # Advance the days after resting
        advance_days(days_resting)

        print(f"Rested for {days_resting} days. Health: {game_data['player']['health']}, Food remaining: {game_data['resources']['food']} lbs, Wood Cords remaining: {game_data['resources']['wood_cords']}")
    else:
        print("You are already at full health.")
    space()
    input("Press Enter to continue...")
    clear_screen()


def handle_cook():
    display_ascii_art("cook", Fore.YELLOW)

    # Check if there are herbs available to cook
    if game_data['resources']['herbs'] <= 0:
        print(Fore.RED + "You do not have enough herbs to cook! Find herbs or trade to restock.")
        return

    # Ask the player how many herbs to use
    print(f"You have {game_data['resources']['herbs']} herbs.")
    while True:
        try:
            herbs_to_cook = int(input(f"How many herbs would you like to use for cooking? 1 herb = (+1d4+ 1/2[Survival]) Food: "))
            if 0 < herbs_to_cook <= game_data['resources']['herbs']:
                break
            else:
                print("Enter a valid number of herbs.")
        except ValueError:
            print("Enter a valid number.")

    # Update food and herbs
    food_gained = herbs_to_cook * (random.randint(1,4)+ (game_data["player"]["survival"] // 2) ) #1d4 + 1/2(Survival) food per herb
    modify_resource("food", food_gained)
    modify_resource("herbs", -herbs_to_cook)
    print(Fore.GREEN + f"Used {herbs_to_cook} herbs to cook. Gained {food_gained} food.")
    print(f"Current food: {game_data['resources']['food']} lbs, Herbs remaining: {game_data['resources']['herbs']}.")
    space()
    input("Press Enter to continue...")
    clear_screen()


# Game Logic Functions
def check_win_condition():
    if game_data["time"]["year"] >= 1 or game_data["player"]["health"] < 1:   ########################################
        handle_game_over()
    if game_data["journey"]["totalMilesTraveled"] >= 1000:
        handle_boss_fight()

def handle_game_over():
    print(Fore.RED + "Game Over!")
    choice = input("Do you want to restart? (y/n): ").lower()
    if choice == 'y':
        reset_game()
    else:
        sys.exit()

def reset_game():
    """Resets the game to its initial state."""
    global game_data
    game_data = {
    "time": {"day": 1, "month": MONTHS[0], "year": 0},
    "resources": {"food": 10, "water": 8, "waterskins": 1, "herbs": 1, "supplies": 10,
                  "wood": 3, "wood_cords": 1, "gold": 0},
    "journey": {"totalMilesTraveled": 0, "dragon_encountered": False, "current_biome": "Marine"},
    "player": {"health": 100, "survival": 0, "carry_weight": 0, "defend_cooldown": 0, "stun_splosion_cooldown": 0},  #Initialize carry_weight
    "combat": {"potions": 0}}

def animate_progress_bar(miles_traveled, total_miles, duration=1):
    """
    Animate a progress bar showing miles traveled toward the goal.

    Args:
        miles_traveled (int): Miles already traveled.
        total_miles (int): Total miles required to reach the goal.
        duration (int): Time duration for the progress animation in seconds.
    """
    progress_percent = int((miles_traveled / total_miles) * 100)
    with tqdm(total=100, desc="Miles Progress", ascii=False) as pbar:
        for i in range(progress_percent + 1):
            pbar.update(1)  # Increment progress bar by 1%
            time.sleep(duration / 100)

def update_game_status():
    """
    Displays the game status, ensures no negative resource values,
    and presents relevant information about the player's progress and inventory.
    """
    # Ensure no negative resource values
    for resource in game_data["resources"]:
        game_data["resources"][resource] = max(0, game_data["resources"][resource])

    # Calculate miles remaining
    miles_remaining = max(0, TOTAL_MILES - game_data["journey"]["totalMilesTraveled"])

    clear_screen()

    # Display status ASCII art
    print(Back.BLACK + ascii_art["status"])
    print(f"It is the {game_data['time']['day']} day of {game_data['time']['month']}, year {game_data['time']['year']}")
    print(f"Current Biome: {game_data['journey']['current_biome']}")
    check_low_resources()

    # Extract resource values
    food = game_data['resources']['food']
    water = game_data['resources']['water']
    wood_weight = game_data['resources']['wood']
    herbs = game_data['resources']['herbs']
    supplies = game_data['resources']['supplies']

    if miles_remaining == 0:
        print(Fore.GREEN + "You have reached the dragon's lair!")
        game_data["journey"]["dragon_encountered"] = True
    else:
        print(f"You have traveled {game_data['journey']['totalMilesTraveled']} miles with {miles_remaining} miles left to go.")

    # Convert wood weight to full cords and remaining wood weight
    full_cords, remaining_wood = convert_wood_to_cords(wood_weight)

    # Display game status
    print("Game Status:")
    print(f"Health: {game_data['player']['health']}")
    print(f"Food: {food}")
    print(f"Water: {water}")
    print(f"Wood: {wood_weight} lbs ({full_cords} full cords and {remaining_wood} lbs remaining)")
    print(f"Herbs: {herbs}")
    print(f"Supplies: {supplies}")

    # Display waterskin status
    water_level = game_data['resources']['water']
    waterskins = game_data['resources']["waterskins"]
    print("Waterskins:")
    for i in range(waterskins):
        fullness = min(water_level, WATER_SKIN_CAPACITY)  # Handle multiple waterskins
        water_level -= fullness
        representation = ""
        for j in range(WATER_SKIN_CAPACITY):
            if j < fullness:
                representation += "█"  # Full section
            else:
                representation += "░"  # Empty section
        print(f"Waterskin {i+1}: [{representation}] ({fullness}/8 lbs)")

    # Additional information
    print(f"Gold: {game_data['resources']['gold']} gp")
    print(f"Carry Weight: {game_data['player']['carry_weight']} lbs / {MAX_CARRY_CAPACITY} lbs")

    # Display progress bar
    animate_progress_bar(game_data['journey']["totalMilesTraveled"], TOTAL_MILES)
    space()
    input("Press Enter to continue...")
    clear_screen()


def handle_help():
    print("""
          COMMANDS:
          1) Status - Shows your current status with resources, health, and travel progress
          2) Travel - Travel along the trail to the dragon's lair, consuming 1 Food & 1 Water per day
          3) Hunt - Hunt for wildgame Food using Supplies 
          4) Scout - Consume food to Scout for Wood, Food, Water, or Herbs
          5) Rest - Use 1 Wood Cord to set a campfire and recover Health
          6) Cook - Cook herbs to create Food
          7) Help - Shows this help message
          8) Credits - Shows game credits
          9) Quit - Exits the game
          """)
    space()

def add_day():
    """Advances the game by one day, adjusting resources and health."""
    if game_data["resources"]["food"] > 0:
        modify_resource("food", -1)
    else:
        print(Fore.RED + "You are out of food!")

    # Health loss events on specific days
    if game_data['time']['day'] in (14, 18):
        modify_health(-1, "Health event due to poor conditions.")

    # Advance the day and handle month transitions
    advance_time()


def advance_days(days):
    """
    Advances the game by a specified number of days, updating resources and checking conditions.
    """
    for _ in range(days):
        # Consume food and water
        if game_data["resources"]["food"] > 0:
            modify_resource("food", -1)
        else:
            print(Fore.RED + "You are out of food!")

        if game_data["resources"]["water"] > 0:
            modify_resource("water", -WATER_DRINK_AMOUNT)
        else:
            print(Fore.RED + "You are out of water!")

        # Recalculate carry weight after consumption
        update_carry_weight()

        # Handle day and month progression
        game_data['time']['day'] += 1
        if game_data['time']['day'] > 30:  # Handle month transitions
            game_data['time']['day'] = 1
            month_index = MONTHS.index(game_data['time']['month'])
            game_data['time']['month'] = MONTHS[(month_index + 1) % len(MONTHS)]
            if month_index == len(MONTHS) - 1:
                game_data['time']['year'] += 1

        # Check if health drops to 0
        if game_data['player']['health'] <= 0:
            handle_game_over()


def advance_time():
    """Advances the game time, handling day and month transitions."""
    game_data['time']['day'] += 1

    if game_data['time']['day'] > 30:
        game_data['time']['day'] = 1
        month_index = MONTHS.index(game_data['time']['month'])
        game_data['time']['month'] = MONTHS[(month_index + 1) % len(MONTHS)]

        if month_index == len(MONTHS) - 1:
            game_data['time']['year'] += 1

# Helper function for handling trades
def handle_trade(trader_type, fair=True):
    """
    Handles trading logic for both fair and steep traders.

    Args:
        trader_type (str): The type of trade (e.g., 'food_for_supplies').
        fair (bool): If True, applies fair trading rates; otherwise, applies steep rates.
    """
    # Set exchange rates
    if trader_type == "food_for_supplies":
        exchange_rate = random.randint(3, 5) if fair else random.randint(1, 2)
        print(f"The trader offers {exchange_rate} supplies for every 1 food you trade.")
        resource_to_trade = "food"
        resource_to_gain = "supplies"
    elif trader_type == "supplies_for_food":
        exchange_rate = random.randint(3, 5) if fair else random.randint(1, 2)
        print(f"The trader offers {exchange_rate} food for every 1 supply you trade.")
        resource_to_trade = "supplies"
        resource_to_gain = "food"
    elif trader_type == "gold_for_food":
        exchange_rate = random.randint(10, 20) if fair else random.randint(5, 10)
        print(f"The trader offers {exchange_rate} food for every 1 gold you trade.")
        resource_to_trade = "gold"
        resource_to_gain = "food"
    elif trader_type == "gold_for_water":
        exchange_rate = random.randint(5, 10) if fair else random.randint(2, 5)
        print(f"The trader offers {exchange_rate} water for every 1 gold you trade.")
        resource_to_trade = "gold"
        resource_to_gain = "water"
    else:
        print(Fore.RED + "Invalid trader type.")
        return

    # Check if the player has enough resources to trade
    if game_data['resources'][resource_to_trade] < 1:
        print(Fore.RED + f"You do not have enough {resource_to_trade} to trade.")
        return

    # Handle trading logic
    while True:
        try:
            amount_to_trade = int(input(f"How much {resource_to_trade} would you like to trade? (1 {resource_to_trade} = {exchange_rate} {resource_to_gain}): "))
            if 0 < amount_to_trade <= game_data["resources"][resource_to_trade]:
                break
            else:
                print(f"Enter a valid number of {resource_to_trade} items to trade.")
        except ValueError:
            print("Enter a valid number.")

    # Calculate resources gained
    resources_gained = amount_to_trade * exchange_rate

    # Special handling for water (check waterskin capacity)
    if resource_to_gain == "water":
        available_space = game_data["resources"]["waterskins"] * WATER_SKIN_CAPACITY - game_data["resources"]["water"]
        if resources_gained > available_space:
            print(Fore.RED + f"Not enough waterskin space to hold {resources_gained} water. You can only hold {available_space}.")
            resources_gained = available_space

    # Complete the trade
    modify_resource(resource_to_trade, -amount_to_trade)
    modify_resource(resource_to_gain, resources_gained)
    print(Fore.GREEN + f"Traded {amount_to_trade} {resource_to_trade} for {resources_gained} {resource_to_gain}.")
    space()

# Fair Trader Function
def handle_trader():
    print(Fore.CYAN + "You encounter a trader on the road!")
    trader_type = random.choice(["food_for_supplies", "supplies_for_food", "gold_for_food", "gold_for_water"])
    handle_trade(trader_type, fair=True)

# Steep Trader Function
def handle_steep_trader():
    print(Fore.CYAN + "You encounter a trader with steep prices on the road!")
    trader_type = random.choice(["food_for_supplies", "supplies_for_food", "gold_for_food", "gold_for_water"])
    handle_trade(trader_type, fair=False)


if __name__ == "__main__":
    try:
        handle_game_start()
        handle_game()
    except KeyboardInterrupt:
        stop_music()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        stop_music()
