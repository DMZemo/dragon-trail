import sys
import time
from tqdm import tqdm
import threading
import os
import random
import colorama
from colorama import Fore, Back, Style
import keyboard
import hashlib
import pandas as pd
import pygame
import logging

# KEEP FOR COPYING FOR EXPORTING TO EXE
# pyinstaller --onefile --add-data "Music;Music" --add-data "3207_Stats.xlsx;." --add-data "highscores.txt;." dragontrail3.4.py

logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


colorama.init(autoreset=True) #Makes it so that it resets color after each use

def get_resource_path(relative_path):
    """Gets the absolute path to a resource, handling PyInstaller."""
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error getting resource path: {e}")
        logging.exception(e)  # Log the exception with traceback
        return None

# HIGH SCORES ####################################################################
#### HIGH SCORES VARIABLES & FUNCTIONS ####################################################################

# --- 1. High Score Storage and Tabulation ---
high_scores = []  # Initialize an empty list to store high scores

def load_high_scores():
    """Loads high scores from a text file."""
    global high_scores
    file_path = os.path.join(os.path.dirname(__file__), "highscores.txt")  # Get relative path
    try:
        with open(file_path, 'r') as file:
            high_scores = [line.strip().split(',') for line in file.readlines()]
        print("High Scores loaded successfully")
        logging.debug("High Scores loaded successfully")
    except FileNotFoundError:
        print("High scores file not found. Creating a new one.")
        logging.debug("High scores file not found. Creating a new one.")
        # Create an empty highscores.txt file if it doesn't exist
        open(file_path, 'w').close()
    except Exception as e:
        print("Error Loading High Scores")
        logging.debug(f"Error Loading High Scores: {e}")

def save_high_scores():
    """Saves high scores to a file."""
    file_path = os.path.join(os.path.dirname(__file__), "highscores.txt")  # Get relative path
    with open(file_path, "w") as f:
        for name, score in high_scores:
            f.write(f"{name},{score}\n")
def add_high_score(name, score):
    """Adds a new high score to the list and saves."""
    high_scores.append((name, score))
    save_high_scores()

def display_high_scores():
    """Displays the high scores."""
    print("\nHigh Scores:")
    if high_scores:
        for i, (name, score) in enumerate(high_scores):
            print(f"{i + 1}. {name}: {score}")
    else:
        print("No high scores yet!")

# --- 3. Enemy HP to XP Conversion ---
def calculate_xp(hp):
    """Calculates experience points based on enemy HP."""
    return int(4.5 * hp)

# --- 4. Add XP to Score ---
def add_xp_to_score(xp):
    """Adds experience points to the player's score and saves high scores."""
    game_data["score"] += xp
    print(f"\nYou gained {xp} XP! Current score: {game_data['score']}")
    add_high_score(game_data["player"]["name"], game_data["score"]) # Save high score after XP gain


# Load High Scores
#load_high_scores(get_resource_path("highscores.txt"))

# MUSIC & AUDIO ####################################################################
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
        "mini_boss_fight": get_resource_path("Music/Machinations.mp3"),
    }
except Exception as e:
    print(f"Error loading music paths: {e}")

music_path = get_resource_path("Music")  # Path to the music directory

# Pygame Music Initialization (with error handling)
def init_pygame_mixer(retries=3):
    for attempt in range(retries):
        try:
            pygame.mixer.init()
            print("Pygame mixer initialized successfully.")
            return True
        except pygame.error as e:
            print(f"Error initializing Pygame mixer (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(1)  # Wait a bit before retrying
    print("Failed to initialize Pygame mixer after multiple attempts.")
    return False

if not init_pygame_mixer():
    print("Falling back to a different audio library or handling mechanism.")
    # Add fallback mechanism here if needed

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
                print("Please enter a number between 0 and 8.")
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

# UI ELEMENTS ####################################################################
#### ASCII ART, TEXT, & FUNCTIONS ####################################################################
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
Gather your starting resources and then TRAVEL to the next biome.
Along the way you will encounter random events and have to make choices.
There are all manner of encounters, from FLORA to FAUNA to HUMANOID.
All told there are 3,207 different encounters you could face.
They range from sentient plants that tickle your heels to dragons that will eat you whole.
Do your best to manage your supplies so you have HERBS and SUPPLIES to create POTIONS.
You can use these potions to heal yourself during combat.
You can also TRADE with merchants you encounter along the way.
HUNT or SCOUT for resources along the way.
REST to regain health and COOK to increase your food.
Make it to the Dragon and Defeat it to win the game!
"""

welcome_text = """
\nThere is a Dragon that has been terrorizing the continent.
It's lair is 1000 miles away.
You are brave enough to travel to the dragon and defeat it.
You will need to Travel, Hunt, Rest, and Cook along the way.
Take care along the road and get to the dragon in one piece, then defeat it.
Good luck along THE DRAGON TRAIL!!!
"""

def display_ascii_art(art_key, color=Fore.WHITE, style=Style.BRIGHT):
    print(color + ascii_art.get(art_key, "")) # Handle missing keys gracefully

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

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


# BIOMES VARIABLES & FUNCTIONS ########################################################
BIOMES = [
    "MARINE", "GLACIER", "TUNDRA", "TAIGA", "COLD_DESERT", "HOT_DESERT", 
    "TROPICAL_RAINFOREST", "WETLAND", "TROPICAL_SEASONAL_FOREST", "SAVANNA", 
    "GRASSLAND", "TEMPERATE_DECIDUOUS_FOREST", "TEMPERATE_RAINFOREST"
]

BIOME_CONNECTIONS = {
    "MARINE": ["MARINE", "WETLAND", "TROPICAL_RAINFOREST", "GLACIER", "TEMPERATE_RAINFOREST"], 
    "GLACIER": ["TUNDRA", "COLD_DESERT"], 
    "TUNDRA": ["GLACIER", "TAIGA", "COLD_DESERT"],
    "TAIGA": ["TUNDRA", "TEMPERATE_DECIDUOUS_FOREST", "GRASSLAND"], 
    "COLD_DESERT": ["TUNDRA", "GLACIER"], 
    "HOT_DESERT": ["SAVANNA", "GRASSLAND"], 
    "TROPICAL_RAINFOREST": ["TROPICAL_SEASONAL_FOREST", "WETLAND"],
    "WETLAND": ["TROPICAL_RAINFOREST", "TROPICAL_SEASONAL_FOREST", "GRASSLAND"], 
    "TROPICAL_SEASONAL_FOREST": ["TROPICAL_RAINFOREST", "SAVANNA"],
    "SAVANNA": ["HOT_DESERT", "TROPICAL_SEASONAL _FOREST", "GRASSLAND"],
    "GRASSLAND": ["SAVANNA", "TEMPERATE_DECIDUOUS_FOREST", "TAIGA"],
    "TEMPERATE_DECIDUOUS_FOREST": ["GRASSLAND", "TAIGA"],
    "TEMPERATE_RAINFOREST": ["TEMPERATE_DECIDUOUS_FOREST", "TROPICAL_RAINFOREST"] 
}

def get_next_biome(current_biome):
    """
    Randomly selects the next biome based on the current biome.
    """
    possible_biomes = BIOME_CONNECTIONS.get(current_biome, [])
    if not possible_biomes:
        return current_biome  # Stay in the current biome if no connections
    return random.choice(possible_biomes)

class Encounter:
    def __init__(self, encounter_type, difficulty_mod=0):
        self.encounter_type = encounter_type
        self.difficulty_mod = difficulty_mod

    def simulate(self, survival, progress):
        """Simulates the encounter and determines the outcome."""
        # Calculate difficulty based on progress
        if progress <= 0.25:
            base_difficulty = 5
        elif progress <= 0.50:
            base_difficulty = 10
        elif progress <= 0.75:
            base_difficulty = 15
        elif progress <= 0.90:
            base_difficulty = 20
        else:
            base_difficulty = 25

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

def load_encounter_data(excel_file_path):
    """Loads encounter data from an Excel file, handling potential errors."""
    try:
        df = pd.read_excel(excel_file_path)
        # Check for required columns
        required_cols = ['Biome', 'Encounter', 'Name', 'AC', 'HP', 'ATK', 'DPR']
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing columns in Excel file: {missing_cols}")
        
        # Check for NaN values in required columns
        #if df[required_cols].isnull().any().any():
            #raise ValueError("Encounter data contains NaN values in required columns.")
        
        # Fill NaN values with default values
        df.fillna({
            'Biome': 'Unknown',
            'Encounter': 'Unknown',
            'Name': 'Unknown',
            'AC': 0,
            'HP': '0',
            'ATK': 0,
            'DPR': '0'
        }, inplace=True)
        
        # Strip whitespace from string columns
        df['Biome'] = df['Biome'].str.strip()
        df['Encounter'] = df['Encounter'].str.strip()
        df['Name'] = df['Name'].str.strip()
        
        return df
    except FileNotFoundError:
        print(f"Error: Excel file not found at {excel_file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading the Excel file: {e}")
        return None

def get_random_encounter(biome, encounter_type, encounter_data):
    """Retrieves a random encounter based on biome and encounter type."""
    if encounter_data is None or encounter_data.empty:
        print("Encounter data is empty or None.")
        return None

    # Filter by biome and encounter type
    filtered_df = encounter_data[
        (encounter_data["Biome"].str.upper() == biome.upper()) & 
        (encounter_data["Encounter"].str.upper() == encounter_type.upper())
    ]

    if filtered_df.empty:
        print(f"No encounters found for biome: {biome} and encounter type: {encounter_type}")
        return None  # No encounters matching the criteria

    # Select a random row and return the encounter name and stats
    random_row = filtered_df.sample(n=1)
    encounter_name = random_row["Name"].iloc[0]
    encounter_stats = {
        "AC": int(random_row["AC"].iloc[0]),
        "HP": random_row["HP"].iloc[0],
        "ATK": int(random_row["ATK"].iloc[0]),
        "DPR": random_row["DPR"].iloc[0]
    }
    return encounter_name, encounter_stats

# Load encounter data from Excel
excel_file_name = "3207_Stats.xlsx"  # Name of your Excel file
excel_file_path = get_resource_path(excel_file_name)

if excel_file_path is None:
    print(f"Error: Could not locate Excel file '{excel_file_name}'. Exiting.")
    sys.exit(1)

encounter_data = load_encounter_data(excel_file_path)
if encounter_data is None:
    print(f"Error loading encounter data from '{excel_file_name}'. Exiting.")
    sys.exit(1)

encounter_data = load_encounter_data(excel_file_path)
if encounter_data is None or encounter_data.empty:
    print("Failed to load encounter data. Please check the Excel file and try again.")
    sys.exit(1)  # Exit the program if encounter data is not loaded properly

#### CONSTANTS ####################################################################
MONTHS = ["O'drahn 1 (June)", "O'drahn 2 (July)", "O'drahn 3 (August)", "O'drahn 4 (September)",
          "Remiscus 1 (October)", "Remiscus 2 (November)", "Remiscus 3 (December)", "Remiscus 4 (January)",
          "Demiscus 1 (February)", "Demiscus 2 (March)", "Demiscus 3 (April)", "Demiscus 4 (May)"]

######## TRAVEL CONSTANTS ####################################################################
MIN_MILES_PER_TRAVEL = 18
MAX_MILES_PER_TRAVEL = 30
MIN_DAYS_PER_TRAVEL = 1
MAX_DAYS_PER_TRAVEL = 3
TOTAL_MILES = 1000
current_biome = "MARINE"

######## COMBAT CONSTANTS ####################################################################
MAX_HEALTH_LEVEL = 100
PLAYER_AC = 16
DRAGON_AC = 20

######## RESOURCE CONSTANTS ####################################################################
MIN_DAYS_PER_REST = 1
MAX_DAYS_PER_REST = 3
FOOD_PER_HUNT = 5
MIN_DAYS_PER_HUNT = 1
MAX_DAYS_PER_HUNT = 4
WATER_SKIN_CAPACITY = 8  # lbs  
WATER_DRINK_AMOUNT = 1  #  lbs
WOOD_CORD_SIZE = 3  # lbs         
MAX_CARRY_CAPACITY = 150  #  lbs

# GAME DATA ####################################################################
game_data = {
    "time": {"day": 1, "month": MONTHS[0], "year": 0},
    "resources": {"food": 10, "water": 8, "waterskins": 1, "herbs": 1, "supplies": 10,
                  "wood": 3, "wood_cords": 1, "gold": 0},
    "journey": {"totalMilesTraveled": 0, "dragon_encountered": False, "current_biome": "MARINE", "mini_boss_defeated": False},
    "player": {"name": "", "health": 100, "survival": 0, "carry_weight": 0, "defend_cooldown": 0, "stun_splosion_cooldown": 0, "stunned": False},  # Initialize carry_weight
    "combat": {"potions": 0},
    "seed": 0,
    "last_encounter_day": 0, # Track the last day an encounter occurred
    "encounter_chance": 0.01, #Initial encounter chance (10%)
    "score": 0,
}

# PLAYER ATTACKS ####################################################################
# PLAYER_ATTACKS[0] = Melee Attack
# PLAYER_ATTACKS[1] = Ranged Attack
# PLAYER_ATTACKS[2] = Defend
# PLAYER_ATTACKS[3] = Magic Attack
# PLAYER_ATTACKS[4] = Stunsplosion

PLAYER_ATTACKS = [
    {'name': 'melee', 'damage_range': (10, 25), 'to_hit_bonus': 1, 'ascii_art': r"""
                      />
         ()          //---------------------------------------------(
         (*)OXOXOXOXO(*>                                             \
         ()          \\-----------------------------------------------)
                      \>
    """},
    {'name': 'ranged', 'damage_range': (10, 25), 'to_hit_bonus': 1, 'ascii_art': r"""
    llll                 
    │ lll                
    │   ll               
    │     l              
    │     ll             
    │      l             
    │------l  }=========>
    │      l             
    │     ll             
    │     l              
    │   ll               
    │ lll                
    llll                 
    """},
    {'name': 'defend', 'damage_range': (0, 0), 'to_hit_bonus': 0, 'ascii_art': r"""
       _________________________ 
      |<><><>     |  |    <><><>|
      |<>         |  |        <>|
      |           |  |          |
      |  (______ <\-/> ______)  |
      |  /_.-=-.\| " |/.-=-._\  | 
      |   /_    \(o_o)/    _\   |
      |    /_  /\/ ^ \/\  _\    |
      |      \/ | / \ | \/      |
      |_______ /((( )))\ _______|
      |      __\ \___/ /__      |
      |--- (((---'   '---))) ---|
      :           |  |          :     
       \<>        |  |       <>/      
        \<>       |  |      <>/       
         \<>      |  |     <>/       
          `\<>    |  |   <>/'         
            `\<>  |  |  <>/'         
              `\<>|  |<>/'         
                `-.__.-`                    
    """},
    {'name': 'magic', 'damage_range': (10, 45), 'to_hit_bonus': 7, 'ascii_art': r"""
        ✨ ✨ ✨
         \  |  /
          \ | /
          *\|/*
      ✨---✨---✨
          */|\*
          / | \
         /  |  \
        ✨ ✨ ✨
    """},
    {'name': 'stunsplosion', 'damage_range': (40, 50), 'to_hit_bonus': 10, 'ascii_art': r"""
      
      *****************      
    ** \!\*********/!/ **    
   *   ***************   *   
  *  *****%\░*!*░/%*****  *  
 *  * *░░░\%\*!*/%/░░░* *  * 
*  * *░░░**\%\!/%/**░░░* *  *
* * * ░░****\%X%/****░░ * * *
******««(≈≈≈≈≈÷≈≈≈≈≈)»»******
* * * ░░****/%X%\****░░ * * *
*  * *░░░**/%/¡\%\**░░░* *  *
 *  * *░░░/%/*¡*\%\░░░* *  * 
  *  *****%/░*¡*░\%*****  *  
   *   ***************   *   
    ** /¡/*********\¡\ **    
      *****************      
         ***********         
     
"""},
]

def handle_combat(enemy_name, enemy_ac, enemy_hp, atk_modifier, dpr_range, potions, xp_on_win):
    """Universal combat logic for encounters, mini-boss, and dragon."""
    player_hp = game_data["player"]["health"]

    print(f"\n{Fore.RED}Encounter Stats:{Style.RESET_ALL}\nName: {enemy_name}\nAC: {enemy_ac}\nHP: {enemy_hp}\nATK Modifier: {atk_modifier}\nDPR Range: {dpr_range}")
    input("Press Enter to start the encounter...")

    while enemy_hp > 0 and player_hp > 0:
        clear_screen()
        print_status(enemy_name, enemy_hp, player_hp, potions)
        player_choice = get_player_choice()

        if player_choice == 7:  # Flee
            flee_success = handle_flee(atk_modifier)
            if flee_success:
                return
            else:
                player_hp = handle_enemy_attack(player_hp, atk_modifier, dpr_range, enemy_name)
                input("Press Enter to continue...")  # Pause after enemy attack
        elif player_choice == 8:  # Toggle Music
            toggle_music()
        else:
            player_hp, enemy_hp, potions, player_defended = handle_player_turn(player_choice, player_hp, enemy_hp, potions, enemy_ac)
            input("Press Enter to continue...")  # Pause after player attack
            if enemy_hp > 0:
                enemy_hit, enemy_damage_rolled = roll_to_hit(atk_modifier, PLAYER_AC)
                if enemy_hit:
                    if player_defended:  # Apply defense only if player defended
                        reflected_damage = int(enemy_damage_rolled / 2)
                        enemy_hp -= reflected_damage
                        print(Fore.GREEN + f"You deflected {reflected_damage} damage! Enemy HP: {enemy_hp}" + Style.RESET_ALL)
                        input("Press Enter to continue...")  # Pause after enemy attack
                    player_hp = handle_enemy_attack(player_hp, atk_modifier, dpr_range, enemy_name, enemy_damage_rolled)
                    input("Press Enter to continue...")  # Pause after enemy attack
                else:
                    print(Fore.YELLOW + f"The {enemy_name} missed!" + Style.RESET_ALL)
                    input("Press Enter to continue...")  # Pause after enemy miss

        # Update cooldowns - Corrected cooldown update
        game_data["player"]["defend_cooldown"] = max(0, game_data["player"]["defend_cooldown"] - 1)
        game_data["player"]["stun_splosion_cooldown"] = max(0, game_data["player"]["stun_splosion_cooldown"] - 1)

    if enemy_hp <= 0:
        print(Fore.GREEN + f"You defeated the {enemy_name}!")
        print(Fore.GREEN + f"You gain {xp_on_win} XP!")
        add_xp_to_score(xp_on_win)
        input("Press Enter to continue...")
    else:
        print(Fore.RED + f"You were defeated by the {enemy_name}!")
        print(Fore.RED + "GAME OVER!")
        print(Fore.Red + "Your score is: " + str(game_data["score"]))
        handle_game_over()

def handle_player_turn(player_choice, player_hp, enemy_hp, potions, enemy_ac):
    """Handles player turn in combat."""
    player = game_data['player']
    potions = game_data["combat"]["potions"]
    
    if player_choice == 3:  # Defend
        if player["defend_cooldown"] == 0:
            print("You raise your shield.")
            player["defend_cooldown"] = 3  # Set cooldown for defend
            return player_hp, enemy_hp, potions, True  # Signal that player defended
        else:
            print(f"Defend is on cooldown for {player['defend_cooldown']} more turns.")
            return player_hp, enemy_hp, potions, False  # Signal that player did not defend
    elif player_choice == 6:  # Use Potion
        if potions > 0:
            potions -= 1
            health_restored = random.randint(33, 66)
            player_hp = min(player_hp + health_restored, MAX_HEALTH_LEVEL)
            print(Fore.GREEN + f"You drink a potion, restoring {health_restored} health!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "You have no potions left!" + Style.RESET_ALL)
    elif player_choice == 5:  # Stun-Splosion
        if potions >= 10:
            potions -= 10
            damage = random.randint(50, 70)
            enemy_hp -= damage
            print(PLAYER_ATTACKS[player_choice - 1]['ascii_art'])
            print(Fore.GREEN + f"You cast Stun-Splosion, dealing {damage} damage!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Not enough potions for Stun-Splosion!" + Style.RESET_ALL)
    else:
        # Ensure player_choice is within the valid range
        if 1 <= player_choice <= len(PLAYER_ATTACKS):
            attack_type = PLAYER_ATTACKS[player_choice - 1]['name']
            damage = player_attack(enemy_ac, attack_type)
            if damage > 0:
                enemy_hp -= damage
                print(PLAYER_ATTACKS[player_choice - 1]['ascii_art'])
                print(Fore.GREEN + f"You {attack_type}, dealing {damage} damage!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Your attack missed!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid attack type!" + Style.RESET_ALL)
    
    return player_hp, enemy_hp, potions, False

def handle_enemy_attack(player_hp, atk_modifier, dpr_range, enemy_name, enemy_damage_rolled=None):
    """Handles enemy turn in combat."""
    if enemy_damage_rolled is None:
        enemy_damage = enemy_attack(PLAYER_AC, atk_modifier, dpr_range)
    else:
        enemy_damage = enemy_damage_rolled
    player_hp -= enemy_damage
    print(Fore.RED + f"The {enemy_name} attacks, dealing {enemy_damage} damage!" + Style.RESET_ALL)
    return player_hp

def handle_flee(atk_modifier):
    """Handles player fleeing from combat."""
    flee_chance = 1 - (atk_modifier / 10)
    flee_roll = random.random()
    print(f"Flee chance: {flee_chance:.2f}, Flee roll: {flee_roll:.2f}")
    if flee_roll < flee_chance:
        print(Fore.GREEN + "You successfully flee from the encounter!" + Style.RESET_ALL)
        return True
    else:
        print(Fore.RED + "You failed to flee!" + Style.RESET_ALL)
        return False
    
def handle_boss_fight():
    """Handles the dragon boss fight using the unified combat system."""
    global current_menu
    current_menu = "boss_fight"
    play_music(current_menu)
    potions = game_data["combat"]["potions"]
    survival_value = game_data["player"]["survival"]
    
    # Dragon stats
    enemy_name = "Dragon"
    enemy_ac = DRAGON_AC
    enemy_hp = 180
    atk_modifier = max(0, 8 - survival_value) # Dragon attack bonus based on player survival
    dpr_range = (20, 40) # Dragon damage range
    xp_on_win = calculate_xp(180)

    print(Fore.RED + "\nYOU HAVE ARRIVED AT THE DRAGON'S LAIR!")
    display_ascii_art("dragonart", Fore.RED)
    
    #Potion Creation Dialog
    if game_data["resources"]["herbs"] > 0 or game_data["resources"]["supplies"] > 0:
        print("\nYou have a chance to prepare before the fight:")
        choice = input(f"You have {game_data['resources']['herbs']} herbs and {game_data['resources']['supplies']} supplies. Create potions? (y/n): ").lower()
        if choice == 'y':
            herbs_used = min(int(input(f"How many herbs do you want to use (up to {game_data['resources']['herbs']})? ")), game_data['resources']['herbs'])
            supplies_used = min(int(input(f"How many supplies do you want to use (up to {game_data['resources']['supplies']})? ")), game_data['resources']['supplies'])

            potions_created = herbs_used * (2 if supplies_used > 0 else 1) + supplies_used * (3 if herbs_used > 0 else 2)
            potions += potions_created
            game_data["resources"]["herbs"] -= herbs_used
            game_data["resources"]["supplies"] -= supplies_used
            game_data["combat"]["potions"] = potions
            print(f"You created {potions_created} potions!")

    handle_combat(enemy_name, enemy_ac, enemy_hp, atk_modifier, dpr_range, potions, xp_on_win)
    conclude_battle(0) #Dragon is defeated in handle_combat

def handle_mini_boss_fight():
    """Handles the mini-boss fight using the unified combat system."""
    global current_menu
    current_menu = "mini_boss_fight"
    play_music(current_menu)
    potions = game_data["combat"]["potions"]
    survival_value = game_data["player"]["survival"]
    
    # Mini-boss stats
    enemy_name = "Mini-Boss"
    enemy_ac = 15
    enemy_hp = 100
    atk_modifier = 5
    dpr_range = (10, 20)
    xp_on_win = calculate_xp(100)

    print(Fore.RED + "\nYOU HAVE ENCOUNTERED A MINI-BOSS!")

    #Potion Creation Dialog
    if game_data["resources"]["herbs"] > 0 or game_data["resources"]["supplies"] > 0:
        print("\nYou have a chance to prepare before the fight:")
        choice = input(f"You have {game_data['resources']['herbs']} herbs and {game_data['resources']['supplies']} supplies. Create potions? (y/n): ").lower()
        if choice == 'y':
            herbs_used = min(int(input(f"How many herbs do you want to use (up to {game_data['resources']['herbs']})? ")), game_data['resources']['herbs'])
            supplies_used = min(int(input(f"How many supplies do you want to use (up to {game_data['resources']['supplies']})? ")), game_data['resources']['supplies'])

            potions_created = herbs_used * (2 if supplies_used > 0 else 1) + supplies_used * (3 if herbs_used > 0 else 2)
            potions += potions_created
            game_data["resources"]["herbs"] -= herbs_used
            game_data["resources"]["supplies"] -= supplies_used
            game_data["combat"]["potions"] = potions
            print(f"You created {potions_created} potions!")

    handle_combat(enemy_name, enemy_ac, enemy_hp, atk_modifier, dpr_range, potions, xp_on_win)
    
def trigger_random_encounter(encounter_names_on_days, day):
    """Triggers a random encounter using the unified combat system."""
    current_biome = game_data["journey"]["current_biome"]
    encounter_chance = game_data.get("encounter_chance", 0)

    if random.random() < encounter_chance:
        encounter_result = get_random_encounter(current_biome, "TYPICAL", encounter_data)
        if encounter_result:
            encounter_name, encounter_stats = encounter_result
            print(Fore.RED + f"\nRandom Encounter: {encounter_name}!")
            encounter_names_on_days[day] = encounter_name

            # Extract stats
            ac = encounter_stats["AC"]
            hp_range_str = encounter_stats["HP"]
            atk_modifier = encounter_stats["ATK"]
            dpr_range_str = encounter_stats["DPR"]

            try:
                hp_range = tuple(map(int, hp_range_str.strip('()').split(','))) if ',' in hp_range_str else (int(hp_range_str), int(hp_range_str))
                dpr_range = tuple(map(int, dpr_range_str.strip('()').split(','))) if ',' in dpr_range_str else (int(dpr_range_str), int(dpr_range_str))
                enemy_hp = random.randint(*hp_range)
                xp_on_win = calculate_xp(enemy_hp)
            except (ValueError, KeyError, IndexError) as e:
                print(Fore.YELLOW + f"Error parsing encounter stats: {e}. Skipping encounter.")
                return

            handle_combat(encounter_name, ac, enemy_hp, atk_modifier, dpr_range, game_data["combat"]["potions"], xp_on_win)

            game_data["encounter_chance"] = 0.01
        else:
            print("No encounters found for this biome.")
        game_data["last_encounter_day"] = game_data["time"]["day"]
    else:
        game_data["encounter_chance"] = min(0.4, game_data.get("encounter_chance", 0.01) + 0.02)
        print(Fore.GREEN + "No random encounter this time. The chance of an encounter has increased.")

def simulate_encounter_fight(encounter_name, ac, hp_range, atk_modifier, dpr_range, potions):
    """Simulates a fight sequence with player choices."""
    initial_enemy_hp = random.randint(*hp_range)  # Store the initial HP
    enemy_hp = initial_enemy_hp
    player_hp = game_data["player"]["health"] # Get initial player HP from game_data

    print(f"\n{Fore.RED}Encounter Stats:{Style.RESET_ALL}\nName: {encounter_name}\nAC: {ac}\nHP: {enemy_hp}\nATK Modifier: {atk_modifier}\nDPR Range: {dpr_range}")
    input("Press Enter to start the encounter...")

    while enemy_hp > 0 and player_hp > 0:
        clear_screen()
        print_status(encounter_name, enemy_hp, player_hp, potions)

        # Player's turn
        player_choice = get_player_choice()

        if player_choice == 1:  # Sword Attack
            hit_success, _ = roll_to_hit(game_data['player']['survival'], ac)
            if hit_success:
                damage = random.randint(12, 24)
                enemy_hp -= damage
                print(PLAYER_ATTACKS[0]['ascii_art'])
                print(Fore.GREEN + f"You swing your sword, dealing {damage} damage!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Your attack missed!" + Style.RESET_ALL)
        elif player_choice == 2:  # Magic Attack
            hit_success, _ = roll_to_hit(game_data['player']['survival'], ac)
            if hit_success:
                damage = random.randint(8, 32)
                enemy_hp -= damage
                print(PLAYER_ATTACKS[1]['ascii_art'])
                print(Fore.GREEN + f"You unleash a spell, dealing {damage} damage!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Your spell missed!" + Style.RESET_ALL)
        elif player_choice == 3:  # Defend
            if game_data['player']['defend_cooldown'] == 0:
                print("You raise your shield.")
                game_data['player']['defend_cooldown'] = 3  # Set cooldown for defend
                # Reflect damage back to the enemy
                damage_reflected = random.randint(10, 20)
                enemy_hp -= damage_reflected
                print(Fore.GREEN + f"You reflect {damage_reflected} damage back to the enemy!" + Style.RESET_ALL)
                input("Press Enter to continue...")
                continue  # Skip the enemy's turn
            else:
                print(f"Defend is on cooldown for {game_data['player']['defend_cooldown']} more turns.")
                input("Press Enter to continue...")
                continue  # Skip the rest of the player's turn
        elif player_choice == 4:  # Use Potion
            if potions > 0:
                potions -= 1
                health_restored = random.randint(33, 66)
                player_hp = min(player_hp + health_restored, MAX_HEALTH_LEVEL)
                print(Fore.GREEN + f"You drink a potion, restoring {health_restored} health!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "You have no potions left!" + Style.RESET_ALL)
                input("Press Enter to continue...")
                continue  # Skip the rest of the player's turn
        elif player_choice == 5:  # Stun-Splosion
            if game_data['player']['stun_splosion_cooldown'] == 0:
                if potions >= 10:
                    potions -= 10
                    stun_damage = random.randint(40, 50)
                    enemy_hp -= stun_damage
                    print(Fore.GREEN + f"You cast Stun-Splosion, dealing {stun_damage} damage! Enemy stunned!" + Style.RESET_ALL)
                    game_data['player']['stun_splosion_cooldown'] = 5  # Set cooldown for Stun-Splosion
                    input("Press Enter to continue...")
                    continue  # Skip the enemy's turn
                else:
                    print(Fore.RED + "Not enough potions!" + Style.RESET_ALL)
                    input("Press Enter to continue...")
                    continue  # Skip the rest of the player's turn
            else:
                print(Fore.RED + f"Stun-Splosion is on cooldown for {game_data['player']['stun_splosion_cooldown']} more turns." + Style.RESET_ALL)
                input("Press Enter to continue...")
                continue  # Skip the rest of the player's turn
        elif player_choice == 6:  # Flee
            print(Fore.RED + "You attempt to flee from the encounter!")
            flee_chance = 1 - (atk_modifier / 10)
            flee_roll = random.random()
            print(f"Flee chance: {flee_chance:.2f}, Flee roll: {flee_roll:.2f}") #Added print statement for debugging
            if flee_roll < flee_chance:
                print(Fore.GREEN + "You successfully flee from the encounter!" + Style.RESET_ALL)
                input("Press Enter to continue...")
                return  # Successful flee
            else:
                print(Fore.RED + "You failed to flee! The enemy gets a max damage hit on you!" + Style.RESET_ALL)
                enemy_damage = max(dpr_range)  # Enemy deals max damage
                player_hp -= enemy_damage
                print(Fore.RED + f"The enemy deals {enemy_damage} damage to you!" + Style.RESET_ALL)
        elif player_choice == 7:  # Mute/Unmute Music
            toggle_music()  # Toggle music on mute/unmute
            input("Press Enter to continue...")
            continue  # Skip the enemy's turn

        input("Press Enter to continue...")
        clear_screen()

        # Enemy's turn
        if enemy_hp > 0:
            enemy_damage = enemy_attack(ac, atk_modifier, dpr_range)
            player_hp -= enemy_damage
            input("Press Enter to continue...")

    game_data["player"]["health"] = player_hp # Update the player's health

    if enemy_hp <= 0:
        print(Fore.GREEN + f"You defeated the {encounter_name}!")
        xp_gained = calculate_xp(initial_enemy_hp)  # Use initial_enemy_hp
        add_xp_to_score(xp_gained)  # Add XP to score
        print(Fore.GREEN + f"You gained {xp_gained} XP!")
        input("Press Enter to continue...")
        

    else:
        print(Fore.RED + f"You were defeated by the {encounter_name}!")
        input("Press Enter to continue...")
        handle_game_over()

    # Stop the fight music
    stop_music()

def get_player_choice():
    """Gets and returns the player's action choice."""
    player = game_data['player']
    
    print("\nYour Turn:")

    print("1. Attack (Sword)")

    print("2. Attack (Ranged)")
    
    # Display defend option with cooldown status
    defend_status = (f"{Fore.YELLOW}On Cooldown for {player['defend_cooldown']} more turns" 
                     if player['defend_cooldown'] > 0 else "Available")
    print(f"3. Defend (Reflect) - {defend_status}")

    print("4. Magic Bolt")

    # Display Stun-Splosion with cooldown status
    stun_status = (f"{Fore.YELLOW}On Cooldown for {player['stun_splosion_cooldown']} more turns" 
                   if player['stun_splosion_cooldown'] > 0 else "Available")
    print(f"5. Cast Stun-Splosion (10 Potions) - {stun_status}")

    print("6. Use Potion")

    print("7. Flee")

    print("8. Mute/Unmute Music")

    while True:
        try:
            player_choice = int(input("Choose your action (1-8): "))
            if 1 <= player_choice <= 8:  # Adjusted to 8 for valid choices
                return player_choice
            else:
                print(Fore.RED + "Invalid choice. Please choose a number between 1 and 8.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.")

def player_attack(enemy_ac, attack_type):
    """Simulates a player attack based on the attack type."""
    roll = roll_d20()
    total = roll + game_data["player"]["survival"]
    print(" ")
    print(f"\nPlayer attack roll: {roll} + Survival: {game_data['player']['survival']} = {total}")

    if total >= enemy_ac:
        if attack_type == "melee":
            damage = random.randint(15, 30)
            print(f"Hit with melee attack! Dealt {damage} damage.")
        elif attack_type == "magic":
            damage = random.randint(8, 45)
            print(f"Hit with spell attack! Dealt {damage} damage.")
        elif attack_type == "stunsplosion":
            if game_data["combat"]["potions"] >= 10:
                game_data["combat"]["potions"] -= 10
                damage = random.randint(50, 70)
                print(f"Hit with Stun-Splosion! Dealt {damage} damage and used 10 potions.")

            else:
                print("Not enough potions for Stun-Splosion!")
                return 0
        elif attack_type == "defend":
            damage = random.randint(10, 20)
            print(f"Deflected {damage} damage back to the enemy!")
        elif attack_type == "ranged":
            damage = random.randint(10, 25)
            print(f"Hit with ranged attack! Dealt {damage} damage.")
        else:
            print("Invalid attack type!")
            return 0
        return damage
    else:
        print("Miss!")
        return 0

def enemy_attack(ac, atk_modifier, dpr_range):
    """Simulates an enemy attack with a roll to hit."""
    roll = roll_d20()
    total = roll + atk_modifier
    print(" ")
    print(f"\nEnemy attack roll: {roll} + ATK Modifier: {atk_modifier} = {total}")

    if total >= ac:
        damage = random.randint(*dpr_range)
        print(Style.BRIGHT + Fore.RED + f"Enemy attack hits! Dealt {damage} damage.")
        return damage
    else:
        print(Style.BRIGHT + Fore.YELLOW + f"Enemy attack missed!")
        return 0

def print_status(enemy_name, enemy_hp, player_hp, potions):
    """Prints the current status of the encounter."""
    print(f"\n{Fore.RED}{enemy_name} HP: {enemy_hp}{Style.RESET_ALL} | {Fore.GREEN}Your HP: {player_hp}{Style.RESET_ALL} | Potions: {potions}")

# MINI-BOSS FUNCTIONS ####################################################################

def mini_boss_turn(mini_boss_health, player_health, mini_boss_cooldowns):
    """Handles the mini-boss's turn."""
    print("\nMini-Boss's Turn:")
    time.sleep(1)

    # Define mini-boss attacks (adjust damage and hit chance as needed)
    MINI_BOSS_ATTACKS = [
        {'name': 'slash', 'damage_range': (10, 20), 'to_hit_bonus': 1, 'ascii_art': "Mini-Boss slashes!"},
        {'name': 'kick', 'damage_range': (15, 25), 'to_hit_bonus': 2, 'ascii_art': "Mini-Boss kicks!"},
    ]

    # Choose a random attack (simple for now, can be improved later)
    attack_choice = random.choice(MINI_BOSS_ATTACKS)
    print(attack_choice['ascii_art'])

    # Roll to hit (simplified for mini-boss)
    hit_success = random.random() < 0.7  # 70% hit chance

    if hit_success:
        damage = random.randint(*attack_choice['damage_range'])
        player_health -= damage
        print(Fore.RED + f"The mini-boss's {attack_choice['name']} attack deals {damage} damage!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "The mini-boss's attack missed!" + Style.RESET_ALL)

    return mini_boss_health, player_health

def player_action(player_choice, mini_boss_health, player_health, potions, enemy_ac, atk_modifier, dpr_range):
    """Handles the player's action in the mini-boss fight."""
    player = game_data['player']

    if player_choice == 1:  # Sword Attack
        attack_type = PLAYER_ATTACKS[0]
        damage = player_attack(enemy_ac, attack_type)
        if damage > 0:
            mini_boss_health -= damage
            print(PLAYER_ATTACKS[0]['ascii_art'])
            print(Fore.GREEN + f"You swing your sword, dealing {damage} damage!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Your attack missed!" + Style.RESET_ALL)
    elif player_choice == 2:  # Ranged Attack
        attack_type = PLAYER_ATTACKS[3]
        damage = player_attack(enemy_ac, attack_type)
        if damage > 0:
            mini_boss_health -= damage
            print(PLAYER_ATTACKS[3]['ascii_art'])
            print(Fore.GREEN + f"You shoot an arrow, dealing {damage} damage!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Your attack missed!" + Style.RESET_ALL)
    elif player_choice == 3:  # Magic Attack
        attack_type = PLAYER_ATTACKS[1]
        damage = player_attack(enemy_ac, attack_type)
        if damage > 0:
            mini_boss_health -= damage
            print(PLAYER_ATTACKS[1]['ascii_art'])
            print(Fore.GREEN + f"You unleash a spell, dealing {damage} damage!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Your spell missed!" + Style.RESET_ALL)
    elif player_choice == 4:  # Defend
        if player['defend_cooldown'] == 0:
            print("You raise your shield.")
            player['defend_cooldown'] = 3
            # Reflect damage back to the enemy
            damage_reflected = random.randint(10, 20)
            mini_boss_health -= damage_reflected
            print(PLAYER_ATTACKS[2]['ascii_art'])
            print(Fore.GREEN + f"You reflect {damage_reflected} damage back to the enemy!" + Style.RESET_ALL)
        else:
            print(f"Defend is on cooldown for {player['defend_cooldown']} more turns.")
            return mini_boss_health, player_health, potions  # Return unchanged values
    elif player_choice == 5:  # Use Potion
        if potions > 0:
            potions -= 1
            health_restored = random.randint(33, 66)
            player_health = min(player_health + health_restored, MAX_HEALTH_LEVEL)
            print(Fore.GREEN + f"You drink a potion, restoring {health_restored} health!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "You have no potions left!" + Style.RESET_ALL)
            return mini_boss_health, player_health, potions  # Return unchanged values
    elif player_choice == 6:  # Stun-Splosion
        if player['stun_splosion_cooldown'] == 0:
            if potions >= 10:
                potions -= 10
                stun_damage = random.randint(40, 50)
                mini_boss_health -= stun_damage
                print(PLAYER_ATTACKS[4]['ascii_art'])
                print(Fore.GREEN + f"You cast Stun-Splosion, dealing {stun_damage} damage! Enemy stunned!" + Style.RESET_ALL)
                player['stun_splosion_cooldown'] = 5  # Set cooldown for Stun-Splosion
                return mini_boss_health, player_health, potions  # Return to skip enemy's turn
            else:
                print(Fore.RED + "Not enough potions!" + Style.RESET_ALL)
                return mini_boss_health, player_health, potions  # Return unchanged values
        else:
            print(Fore.RED + f"Stun-Splosion is on cooldown for {player['stun_splosion_cooldown']} more turns." + Style.RESET_ALL)
            return mini_boss_health, player_health, potions  # Return unchanged values
    elif player_choice == 7:  # Flee
        print(Fore.RED + "You attempt to flee from the encounter!")
        flee_chance = 1 - (atk_modifier / 10)
        flee_roll = random.random()
        print(f"Flee chance: {flee_chance:.2f}, Flee roll: {flee_roll:.2f}")  # Added print statement for debugging
        if flee_roll < flee_chance:
            print(Fore.GREEN + "You successfully flee from the encounter!" + Style.RESET_ALL)
            return mini_boss_health, player_health, potions  # Successful flee
        else:
            print(Fore.RED + "You failed to flee! The enemy gets a max damage hit on you!" + Style.RESET_ALL)
            enemy_damage = max(dpr_range)  # Enemy deals max damage
            player_health -= enemy_damage
            print(Fore.RED + f"The enemy deals {enemy_damage} damage to you!" + Style.RESET_ALL)

    # Decrement cooldowns at the end of the turn
    if player['defend_cooldown'] > 0:
        player['defend_cooldown'] -= 1
    if player['stun_splosion_cooldown'] > 0:
        player['stun_splosion_cooldown'] -= 1

    return mini_boss_health, player_health, potions

# DRAGON FUNCTIONS ####################################################################
# Constants for attack types
SLOW_ATTACK_COOLDOWNS = {
    'fire_breath': 3,
    'tail_feint': 3,
}
REGULAR_ATTACKS = [
    {'name': 'claw', 'damage_range': (15, 25), 'to_hit_bonus': 1, 'ascii_art': r"""                                                                              
                                                          :=#*                      ::::=*#                                     
                                                     .-:=*#*:                ::---=++==#+:=                 .:                  
                                                   ===:*#+==.               ::-  :-*%%= --             ::-+*+=.                 
                                                 =-=.*%=.-:             .=+-:=-*@@@#=.:+=-          .==::*= ::                  
                                              .+=- =%*:==.           -+=**.:+%@@@*:  -=.       .:: -===%%: .=-                  
                                          .-=+*=.=%%=:=:      .   ==*+. -*%@@@%+.    ::   .-=.:===-=*%@=.:=::                   
                                          :: .=*%@+ .*:     ::*==-*..-*%@@@@#-  :*---.    ==+*=-:-#@@@=::*:                     
                                      :=-=: .+@@%:   -+ ...=-:   .=#@@@@@@*:    :+.   ..:=*   :#@@@%+:.  =:                     
                          ..      .-==#   -*%@%= .:-+*==-     .=#@@@@@@@+.   +=:-  :-:=*:   :*@@@%-:.   :=                      
                      :-::.::-=-==:+. : .+@@@*===:.    -*=  =%@@@@@@%*=:   ==::   -+.     .+@@@@*+-:-= =-                     
                    -=.        == :.-+:*@@@%=+*=-:       -=:#@@@@@%=     -=-    .--:    -*@@@@*-.:+. .:             -:*%   
                  :*#=:        :=::#@@@@%#**++:          -%@@@@@%=    :-=+.    -:.:  :=#@@@@%=-*#==.             .==***    
                .-*=            =@@@%*-        ::     : :*%@@@@%:   .+=       =**=:. .*@@@@+  :-.            -==---%@*:  
           :=+==-:           :*::##-.-+***=:.  .#:   :%*+=%@%*=::.  :+  :+====:   .=#@@@@#. .=--:           =#: :*@#--      
         =*=:        :=     .++.=+-*+:    :+#*. +* :+@%:  ++.    :: -=-=+-    :-*%@@@@@%-  :%: . :-: -=:::++= .*@*: :        
       -*= .------.   :#:  :*+ .=**:       :%@- +@@@%=   --==-   +:=::=:.:*%@@@@@@@@@%= +====    =::--: .--.:+%%=  %     
      =*:.+-      =+-. *%*%@#+#%%#:       :#@@=:%@@@@:.-=::: :==**---==-+%@@@@@@@@@@@*: =:    .-=+-     :++%@@*..==.            
     :*=:+.       .*%: +@@@@@@%==-       =%@@@#%@@@@@#===+-   +*.         =@@@@@@#+-.  ==+.  .=:.==. :%%@@@%+:.:-.              
     :#=+:        -%%- ##*+*:#=:-      -%#*@@@@*++@*=:+:  .-+*#=-:         *@@%-       *.    -=    .=%@@@@*.  :=.               
     .*%+.      :*@@#:+*  ::.  ::    .#*:=%@@#-   #.=*:=*#%*+==:        ==:=*=      ==-=    .*=:-+%@@@@@#:  -=:                 
      .*=    :*%@%%%=+#:     :==    =#:=%@@#-      -#*=:                *@:*. :   :+=.    --== .=%@@@@%-  =-=:                  
       =-  :%%++*%%*%*.       .:  .*==#-:.        :#-            :    .*@+==  :*==++:  ::=:.::=%@@@@@%*= .=                     
       :- .%=:#%%%#+:         .: .*=*=           :#  :---::-=:   :%::+%%+++*. .#  :.::-==   -%@@@@@@%=  .=-                     
        =::--#                .: =+*.            *::*:       -=   %@@@%*=+::# -* :=-      -%@@@@@@*=.   --                      
        -:: %                  ..==              *+*         =@:  #@@@*.-:.=*=*. .==. .+=#@@@@@@*.   =:=+-                      
         =::#                  .-:               #=         =%%   %%#*..-=*=#=:=-=-  :%@@@@@@@@*.  :*:                          
          =:#                                  .*-        -%@%:  =%- :.-.  :-::=+:::*@@@@@@@@@*-   .+                           
           =%.                                :+:      :*%@%+== -@#*++-  :==    :-%@@*:.#@@@@#  :::::                           
            :=                               ==   .-=*%@@@@@%+-#%:       :=    *@@%+-..=*@@@#=  :=                              
                                           :=:.:=+**+++#@@@%**=:     :===-*==+%@@%=:    =#@* ::=#=                              
                                          :---==-:                .+=:.    .::-===:       #- :=  .                              
                                                                 :+.:=+=:             *:  @#  ::                                
                                                                 %*%*: .=+.    =:    -%: +@+-+:                                 
                                                                =@*:      +    =@*:*%*:  +*+:                                   
                                                             :+#*:        --   .%@@*.   +@*.                                    
                                                   :-::===+*+=:           -==: .%@@%###+:%=                                     
                                                    -=.             .:-+*%@*@: *@@#=+*=  +                                      
                                                      +*********#%%@@@@@@@@@%.*@*-     .:.                                      
                                                       .=***++=++*+++*#%@@@@#@#:                                                       
    THE DRAGON CLAW ATTACKS!                                                                                                          
    """},
    {'name': 'wing', 'damage_range': (20, 35), 'to_hit_bonus': 2, 'stun_chance': 0.25, 'ascii_art': r"""                                                                                                           
                       *#*****###@@%*                                                      *%@@##******%*                       
                          -%#%@%%%##%.:=*                                              *=:.#*#%%@@%*%=                          
                        #%*@#*#%%%*%-..::-*                                          *-::..-%*#%%#*#@#%*                        
                      *%#@***#%@%##%#                                                      #@*#%@%#***@*%*                      
                    =%#@**#*%%%#%@%**                                                      +%@@@#%%%****%#%=                    
                  :%#@#***#%#%**%@%#%                                                      %%@@%#*##%****#@*%:                  
                 @#%##****%#%**@*%@%@@                                                    %**@%#@**%#%***#*#%*@                 
               *###**#**#%#@#*#%%*#%**%                                                  %**##*@%###%%%###***#%%*               
              @#%#*****#%%%*#*##%**%@@%*                                                +**#%**%##*##%#%**#***#@*@              
            +%##****+**##@*=+*%###**%**#*                                              *#**%#**##%###*@*#***#***##%+            
           %#%**#***#*#%%**+**@%#**#+@#***                                            *##%@***##%@*=**#%%#+*#****#%#@           
          %*@*********%%##***#@@*****#@*@##                                          **#@@*#*=**@@#****##%#******##@*%          
         *#@**+******@#%##***#%@*******@@%*%                                        %%##@*****+*@%******%#@#**#*##**@##         
        *%%****#*#**##@#*****#%@********%#%@@-                                    :%##@@*****+**@%#******@##*#*******%##        
       :%%**********%*#******##%*********#%%##%                                  #%*#%#*********%*#******##@*=********%#:       
       @%#*********##@*******##%****+*****#@%##%*                              +%@%%@****+******@##*******@##*********#%@       
      *#%**********%**+******#%@*************@##%%*                          *%@**%*************@%#*******##%**********%#*      
     .%%#***********%***+****#%@*****+****+****@###%%*                    *%%#%#@****+**********@%#*+**+***%%*******+***%%:     
     %#%**********%#%**+*****#@@*+**+******+***=+#@%%**#@@%:        :%@@%%#*#@#*******+***+*****@@#*+******%#@*=********%#%     
    .%%*****+*+**+%%#****=****@%***+******+**+**++***%@%%%***@=  =@%%**#%@%**+*+++**+*******++*#@@****++****%%*++++*****#%#:    
    %#%***++*++++*%%=*********%##*+****++*++*+++*+*++++***%#%#*%@#*%%%++****++*+*++++**++*+*****#%+****-****%%*+**++*****##%    
    %%#***+*+**++*%%***+********#+*++++*+********+++++++=+=*%**%#**#*==+*++++=++*+*+**+*******+*******+*=***%#*+***++****#%%    
   -#@****+*+**++*#%*+*++**+*+*%%+++**+**++==+++++++=+=+===+@#*%@%%@+===++==+++=++++=+++**+*++*%%*+++++*++++%****++*++****@#=   
   +#%+++++***++**##*+++*+***++@%*=+++++===================+@@%@@*#%+==================+++++++=%@+++****+***##***++*+*=+++%#*   
   %#*+===++*+***###++++++*====*#%==========*%=:-#*==***===**@@@%%@@*===***==*#-:=%*==========##*===++++++++##***+**+====+*#%   
   %#*===+==++*++*##+==+=+======%%========*:             :%@#%%+=%%%@%:             :*========%%========+=+=*#*+*+*+======*#%   
   %#*=:====++++**##============***======%                 @%%%  %%%@                 %======+*#===-========*#**+++=+=====*#%   
   %#*===========*#%============+%@===+*#                                              #*+===@%+============%#*===========+#%   
   %*+===========+%%=============****=                                                    =***#=============%%+===========*#%   
   %**============%%+============+%%*                                                      +%%+============+%%============**%   
   **%============%**======**:   .+*#                                                      #**.   :**======**@============%+*   
   :*%+===========*#%=====*        *+@                                                    %+#        *=====##*============@*=   
    %**============%%===*@          ***                                                  ***          @*===%%============**%    
    **%============**+#               @+                                                =@               %+##=-==========%**    
     ##*===========+%@:                                                                                  :@%+===========*##     
     +*%+=========**%*%                                                                                  %+%**==========%**     
      **%=======*    @+*                                                                                *+@    *=======@**      
       %*#=====%      =%+                                                                              +%+      %=====#*%       
        %*%==+*         ::                                                                            ::         *+==%*%        
         #+@=*                                                                                                    *=@*%         
          #*%*                                                                                                    *%+#          
           =*%=                                                                                                  =%*=           
     THE DRAGON WING ATTACKS!                                                                                                                            
    """},
    {'name': 'tail_swipe', 'damage_range': (10, 20), 'to_hit_bonus': 1, 'ascii_art': r"""                                    
                                    @#                                     
                                  :@%%*                                       
                                 :%%%%%*          #-                                 
                                .%%%%%%%.       .**:                                              
                      %%        %%%##%%%#       *##:                                                 .%%%%%%=-::....:.:==*+==
                     =#%#      *%%%#*####=    :*##%                                                  %*      :==:-.....:.-:--
                     =#%%#     ###*******-  =****#-                                                          :. -.:..-=.+=:-=
                     :%%###:  .*#*****#******#**#*                                                          :.  -+.::=*:.=###
                      ###*#**********************                                                       *###=:  ....:.::=*+=+
                      ***********+=***********%:                                                     **#*#*+:   ...:=::=*==++
                       ********+=+*%**+*****%%     -*                                              =*####**-: .....:=*+*===*#
                        ****+*+==-=%+***+*=%    =++#                                              =*     == ....=+***+=**+*%@
                 +=      :=++==---**+++++++=+++++++                                                        .:.:==-=++=+**##%@
                 ++++===+++++==-:=+%++++++*+++++#                                                        =.:*=:-====+*@@%###@
                  +==+++++====-::=*@+*********@                                                       .===*::=##*+*%@@@@@###@
                  -=+=+===+++-:.::=#*+**+*#@=                                                  =-  ..::=--=*#+++*@@@@@@@@@#%%
                    +++==+++=-::::::+**%%:                                                      .-+**+--==#+***%@@@@@@@@@@%%%
                      .#****=.  ..::::=                                                     ...:+****##*##**###@@@@@@@@@@@@%%
                                  ....:-.                                                :.:-:-==++**#**###@@%#@@@@@@@@@@@@@@
                              .........:=*:                                           ..=.=*:--===**##@@@@@@@##@@@@@@@@@@@@@@
                             ...... :-:.:..--=--*    .                            .....:#-=##+***##%@@@@@@@@@##%@@@@@@@@@@@@@
                             : .. .   ....:.   ::::-:-=   -:                ......:.:-:-+#**#*####@@@@@@@@@@@%#%@@@@@@@@@@@@@
                               . .......   ....   ::+=  :==-+   :      :-=-.::==*#*-*++**#%@@@@@##@@@@@@@@@@@@%%%@@@@@@@@@@@@
                               . ......:.     .:.:             .....:-==-=+-==++#+#*+*#@@@@@@@@@##@@@@@@@@@@@@@%%#%@@@@@@@@*    
                                .::..:........  .....  .....=..+=::-:-=*=+*******#*##@@@@@@@@@@@##%@@@@@@@@@@@@@%%%%@@@@@+      
                                 ::::...:-::...::...-:=-:==:+=:=-----=+**%@@@@@@@@%##@@@@@@@@@@@%##@@@@@@@@@@@@@@@%%%%%-        
                                 .:=+%*===:::.-:::::::-#+=-===*###****##@@@@@@@@@@%##@@@@@@@@@@@@%##@@@@@@@@@@@@@@%%*           
                                  ::=#%=*%@@%*#@@@***#@@@@@#***#@@@@@%##@@@@@@@@@@@##@@@@@@@@@@@@@%##%@@@@@@@@@%*:              
                                   ..-+=*%@@@+@@@@@@*@@@@@@@%*@@@@@@@%##@@@@@@@@@@@###@@@@@@@@@@@@@@####@@@%*.                  
                                      ::=#%@@*%@@@@@*@@@@@@@##@@@@@@@@*#@@@@@@@@@@@@##%@@@@@@@@@@@@@@@#%#:                      
                                        .=*%@@*@@@@@%%@@@@@@@#@@@@@@@@%#%@@@@@@@@@@@@%###@@@@@@@@@@%*:                          
                                           -*%%*@@@@@#%@@@@@@%#@@@@@@@@@#%@@@@@@@@@@@@@%*##%%#*=.                               
                                              .+=#@@@@%#@@@@@@%*@@@@@@@@@%#%@@@@@@@@@@%*-.                                      
                                                     :*%*%@@@@@@#*%@@@@@@@@####*+    
     THE DRAGON TAIL SWIPES AT YOU!                                                                                                                        
    """},
    {'name': 'bite', 'damage_range': (25, 30), 'to_hit_bonus': 3, 'ascii_art': r"""                                                                                                           
    &x                x&;                                     
    .&&&               &&&                                    
     ;&&&&&            $&&&+                                  
      ;&&&&&&&          X&&&&&                                
       .&&&&&&&&&$       .&&&&&;                              
         &&&&&&&&&&&&&:          .                            
          x&&&&&&&&&&&&&&&&&&&&&&&&&&+                        
   :        &&&&&&&&&&&&&&&&&&&&&&&&&&&&               .&     
   ;&&&&$;   .&&&&&&&&&&&&&&&&&&&&&&&&&&&&;            x&&    
     ;&&&&&&&&&&&&&&&&&&&&&&&&&&&&   ;&&&&&&&          &&&X   
        x&&&&&&&&&&&&&&&&&&&&&&&&&;    ;&&&&&&&       &&&&&   
            x&&&&&&&&&&&&&&&&&&&&&&&&&$.  &&&&&&&X   &&&&&&:  
            .&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  
         $&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  
   .&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  
          .     x&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  
              &&&&&&&&&&&&&&&&&&&&$         &&&$&&&&&&&&&&&&  
           $&&&&&&&&&&&&&&&&&&&&&&&              && &&&&&&&+  
       :&&&&&&&&&&&:    &&&&&&&&&&&&&x .&&           ;  &&&   
    &&&&&&&x        &&  &&&&&& x&&&&&&&&&&+                   
            ;:  &&&&&x &&&&&&    &&&&&&&&&&&&&                
           &&          &&&&        &&&&&&&&&&&&&&$            
         .&&  &&&&&$  &&$  x:        $&&&&&&&&&&&&&&&:        
        :&&; &&&&&&x     &&&&;         .&&&&&&&&&&&&&         
        &&&   x&&&x    $&&&&&&x            &&&&&&&&&          
       &&&x X&;     .:  &&&&&&&&            ;&&&&&            
      .&&&. &&&&&&&&&&&  &&&&&&&&            ;&&&;            
      &&&&  X&&&&&&&&&&&  &&&&&&&&&           x&&.            
      &&&&;                 &&&&&&&&&          &$             
      &&&&& x&&&&&&&&&&&&&&  :&&&&&&&&&x                      
      ;&&&&  &&&&&&&&&&&&&&&:  :&&&&&&&&&;                    
     THE DRAGON BITES YOU!                                                                                                                                      
    """},
]

# Initialize cooldowns
dragon_cooldowns = {
    'fire_breath': 0,
    'tail_feint': 0,
}

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

def print_boss_status(dragon_health, player_health, potions):
    """Prints the current status of the dragon and player."""
    print(f"\n{Fore.CYAN}Dragon Health: {dragon_health} | Your Health: {player_health} | Potions: {potions}{Style.RESET_ALL}\n")

def get_player_action():
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

def player_move(choice, dragon_health, player_health, potions, survival_value):
    """Handles the player's action based on their choice."""
    hit_success = False
    player = game_data['player']

    if choice == 1:  # Sword Attack
        hit_success, _ = roll_to_hit(survival_value, DRAGON_AC)
        if hit_success:
            damage = random.randint(10, 25)
            dragon_health -= damage
            print(PLAYER_ATTACKS[0]['ascii_art'])
            print(Fore.GREEN + f"You swing your sword, dealing {damage} damage!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Your attack missed!" + Style.RESET_ALL)
    elif choice == 2:  # Magic Attack
        hit_success, _ = roll_to_hit(survival_value, DRAGON_AC)
        if hit_success:
            damage = random.randint(15, 30)
            dragon_health -= damage
            print(PLAYER_ATTACKS[1]['ascii_art'])
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
                return dragon_health, player_health, potions # Return to skip dragon's turn
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

def dragon_turn(dragon_health, player_health, survival_value, first_turn=False):
    """Handles the dragon's turn, incorporating the defend mechanic."""
    print("\nDragon's Turn:")
    time.sleep(1)

    # Dragon hit modifier based on survival value
    dragon_hit_modifier = max(0, 8 - survival_value)

    # Check for slow attack cooldowns
    if dragon_cooldowns['fire_breath'] > 0:
        dragon_cooldowns['fire_breath'] -= 1
        if dragon_cooldowns['fire_breath'] == 0:
            print("The dragon prepares to unleash its fiery breath!")
            damage = random.randint(30, 50)
            # Check if player is defending and reduce damage accordingly
            if game_data['player']['defend_cooldown'] > 0:
                damage_reduction = min(damage, 30)  # Reduce damage by up to 30
                damage -= damage_reduction
                print(Fore.GREEN + f"Your defense reduced the damage by {damage_reduction}!" + Style.RESET_ALL)
            player_health -= damage
            print(Fore.RED + f"The dragon breathes fire and deals {damage} damage!" + Style.RESET_ALL)
            return dragon_health, player_health

    if dragon_cooldowns['tail_feint'] > 0:
        dragon_cooldowns['tail_feint'] -= 1
        if dragon_cooldowns['tail_feint'] == 0:
            damage = random.randint(25, 40)
            if game_data['player']['defend_cooldown'] > 0:
                damage_reduction = min(damage, 30)
                damage -= damage_reduction
                print(Fore.GREEN + f"Your defense reduced the damage by {damage_reduction}!" + Style.RESET_ALL)
            player_health -= damage
            print(Fore.RED + f"The dragon feints and bites, dealing {damage} damage!" + Style.RESET_ALL)
            return dragon_health, player_health

    # Choose a random attack
    attack_choice = random.choice(REGULAR_ATTACKS)
    print(attack_choice['ascii_art'])  # Display ASCII art for the attack

    # Roll to hit
    hit_success, _ = roll_to_hit(dragon_hit_modifier + attack_choice.get('to_hit_bonus', 0), PLAYER_AC)

    if hit_success:
        damage = random.randint(*attack_choice['damage_range'])
        if game_data['player']['defend_cooldown'] > 0:
            damage_reduction = min(damage, 30)
            damage -= damage_reduction
            print(Fore.GREEN + f"Your defense reduced the damage by {damage_reduction}!" + Style.RESET_ALL)
        player_health -= damage
        print(Fore.RED + f"The dragon uses its {attack_choice['name']} attack, dealing {damage} damage!" + Style.RESET_ALL)

        # Check if attack has stun effect
        if 'stun_chance' in attack_choice and random.random() < attack_choice['stun_chance']:
            print(Fore.YELLOW + "You are stunned by the dragon's wing attack!" + Style.RESET_ALL)
            game_data['player']['defend_cooldown'] = 2  # Stun for 2 turns

    else:
        print(Fore.RED + "The dragon's attack missed!" + Style.RESET_ALL)

    # Manage cooldowns for the slow attacks
    if first_turn:
        if random.choice([True, False]):
            dragon_cooldowns['fire_breath'] = SLOW_ATTACK_COOLDOWNS['fire_breath']
        else:
            dragon_cooldowns['tail_feint'] = SLOW_ATTACK_COOLDOWNS['tail_feint']

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
        xp_gained = calculate_xp(180)  # Dragon HP is 180
        add_xp_to_score(xp_gained)
        print(Fore.GREEN + f"You gained {xp_gained} XP!")
        add_high_score(game_data["player"]["name"], game_data["score"])
        display_high_scores()

    else:
        handle_game_over()


# TIME FUNCTIONS ####################################################################
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
        # Consume food and water directly, bypassing modify_resource for this specific case
        if game_data["resources"]["food"] > 0:
            game_data["resources"]["food"] -= 1
        else:
            print(Fore.RED + "You are out of food!")

        if game_data["resources"]["water"] > 0:
            game_data["resources"]["water"] -= WATER_DRINK_AMOUNT
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

# RESOURCE MANAGEMENT FUNCTIONS ####################################################################
def randomize_item_costs(seed):
    """Randomizes item costs based on the provided seed."""
    random.seed(seed)
    return {
        "food": random.randint(1, 4),
        "water": random.randint(2, 6),
        "herbs": random.randint(3, 9),
        "supplies": random.randint(2, 8),
        "wood": random.randint(1, 5),
        "potion": random.randint(8, 12),
    }

def update_item_costs(seed):
    """Updates item costs based on the provided seed."""
    global item_costs
    item_costs = randomize_item_costs(seed)

# Initialize item costs based on the initial seed
update_item_costs(game_data["seed"])

item_weights = {
    "food": 1,
    "water": 1,
    "waterskins": 0.1,  # Weight of a waterskin
    "herbs": 0.1,
    "supplies": 1,
    "wood": 1,  # Weight of a single wood
    "potion": 0.1,
}

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

def collect_resource(resource_type, amount):
    """Collects a specified resource, handling special cases for water and wood."""
    handler = resource_handlers.get(resource_type)
    if handler:
        # Check carry capacity before collecting
        total_weight_after_collection = game_data["player"]["carry_weight"] + (amount * item_weights.get(resource_type, 0))
        if total_weight_after_collection > MAX_CARRY_CAPACITY:
            print(Fore.RED + "Not enough carry capacity for this much weight.")
            return

        handler(amount)  # Call the appropriate handler function
    else:
        print(f"Invalid resource type: {resource_type}")

def collect_water(amount):
    """Collects water, respecting waterskin capacity."""
    available_space = game_data["resources"]["waterskins"] * WATER_SKIN_CAPACITY - game_data["resources"]["water"]
    if available_space <= 0:
        print(Fore.RED + "You have no space left in your waterskins!")
        return
    amount = min(amount, available_space)
    modify_resource("water", amount)

def collect_wood(amount):
    """Collects wood, updating wood cords."""
    modify_resource("wood", amount)
    game_data["resources"]["wood_cords"] = game_data["resources"]["wood"] // WOOD_CORD_SIZE

def collect_wood_cords(amount):
    """Collects wood cords, ensuring the amount is a multiple of WOOD_CORD_SIZE."""
    if amount % WOOD_CORD_SIZE != 0:
        print(Fore.RED + f"Wood cords must be collected in multiples of {WOOD_CORD_SIZE} lbs.")
        return
    modify_resource("wood_cords", amount)
    modify_resource("wood", amount * WOOD_CORD_SIZE)

resource_handlers = {
    "water": collect_water,
    "wood": collect_wood,
    "wood_cords": collect_wood_cords,
    "food": lambda amount: modify_resource("food", amount),
    "herbs": lambda amount: modify_resource("herbs", amount),
    "supplies": lambda amount: modify_resource("supplies", amount),
    "waterskins": lambda amount: modify_waterskins(amount),
    "gold": lambda amount: modify_gold(amount),
}

def drink_water():
    """Allows the player to drink water, modifying health and water resources."""
    if game_data["resources"]["water"] < WATER_DRINK_AMOUNT:
        print(Fore.RED + "You don't have enough water to drink!")
        return
    modify_resource("water", -WATER_DRINK_AMOUNT)
    modify_health(1)
    space()

def convert_wood_to_cords(wood_weight):
    """Converts wood weight to full cords and returns the number of cords and remaining wood weight."""
    full_cords = wood_weight // WOOD_CORD_SIZE
    remaining_wood = wood_weight % WOOD_CORD_SIZE
    return full_cords, remaining_wood

def update_carry_weight():
    """Updates the player's carry weight based on current resources."""
    total_weight = sum(
        game_data["resources"][resource] * item_weights.get(resource, 1)
        for resource in ["food", "herbs", "supplies", "water", "waterskins", "wood"]
    )

    # Round the total weight to one decimal place
    rounded_weight = round(total_weight, 1)

    game_data["player"]["carry_weight"] = rounded_weight
    if rounded_weight > MAX_CARRY_CAPACITY:
        print(Fore.RED + f"Warning: You are over your carry capacity! ({rounded_weight:.1f} lbs > {MAX_CARRY_CAPACITY} lbs)")

def drop_excess_weight(resource_type):
    """Drops excess weight if the player is over the carry capacity."""
    over_capacity = game_data["player"]["carry_weight"] - MAX_CARRY_CAPACITY
    if resource_type in item_weights:
        dropped_amount = min(over_capacity // item_weights[resource_type], game_data["resources"][resource_type])
        if dropped_amount > 0:
            modify_resource(resource_type, -dropped_amount, f"Carry capacity exceeded: Dropped {dropped_amount} {resource_type}.", from_drop_excess=True)
    else:
        print(f"Warning: Cannot drop excess {resource_type} - no weight defined.")

def modify_resource(resource_type, amount, event_description=None, from_drop_excess=False):
    """Modifies the amount of a specified resource."""
    #Check for invalid resource type
    if resource_type not in game_data["resources"]:
        print(f"Invalid resource type: {resource_type}")
        return

    game_data["resources"][resource_type] = max(0, game_data["resources"][resource_type] + amount)
    update_carry_weight()

    if event_description:
        print(Fore.CYAN + f"Event: {event_description}")

    if game_data["player"]["carry_weight"] > MAX_CARRY_CAPACITY and not from_drop_excess:
        print(Fore.RED + "Warning: Carry capacity exceeded. Dropping excess resources.")
        drop_excess_weight(resource_type)

def modify_gold(amount):
    """Modifies the amount of gold the player has."""
    game_data["resources"]["gold"] += amount
    print(Fore.YELLOW + f"Gold modified by {amount}. Current gold: {game_data['resources']['gold']}")

def modify_waterskins(amount):
    """Modifies the number of waterskins the player has."""
    game_data["resources"]["waterskins"] += amount
    print(Fore.YELLOW + f"Waterskins modified by {amount}. Current waterskins: {game_data['resources']['waterskins']}")

def check_low_resources():
    """Checks for low resources and prints red alerts."""
    low_resource_alerts = []
    for resource, threshold in [("food", 3), ("water", 3), ("wood_cords", 1), ("herbs", 1), ("supplies", 1)]:
        if game_data["resources"][resource] <= threshold:
            low_resource_alerts.append(f"You are down to {game_data['resources'][resource]} {resource}!")

    if low_resource_alerts:
        print(Fore.RED + "\nLOW RESOURCES ALERT:")
        for alert in low_resource_alerts:
            print(alert)
        print(Fore.RED + "Consider gathering more resources before proceeding.")

#### PURCHASING FUNCTIONS ####################################################################
def handle_purchase():
    """
    Enhanced gear purchasing menu with music, carry capacity checks, screen refresh,
    and validation for waterskins, water, wood cords, and wood.
    Automatically ends purchasing if the player runs out of gold or reaches carry capacity.
    """
    global MAX_CARRY_CAPACITY
    global current_menu

    current_menu = "gear_shop"  # Set current menu for gear shop
    play_music(current_menu)  # Play music for gear shop
    display_ascii_art("gear_shop", Fore.WHITE + Style.BRIGHT)
    print("\nWelcome to the Gear Shop!")
    print("-" * 30)

    while True:
        # Display current stats and inventory
        update_carry_weight()
        print(f"Gold: {game_data['resources']['gold']} gp | Carry Weight: {game_data['player']['carry_weight']}/{MAX_CARRY_CAPACITY} lbs")
        print("-" * 30)
        print("Items Available:")
        print(f"1. Food ({item_costs['food']} gp/lb)")
        print(f"2. Water ({item_costs['water']} gp/waterskin, 8 lbs of water per waterskin)")
        print(f"3. Herbs ({item_costs['herbs']} gp each)")
        print(f"4. Supplies ({item_costs['supplies']} gp/lb)")
        print(f"5. Wood Cords ({item_costs['wood']} gp for 3 lbs of wood)")
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
            choice = input("What would you like to buy? (1-6 or enter cheat code): ").strip().lower()

            # Handle cheat codes
            if choice == 'bubblegum':
                clear_screen()
                print("You're a dirty little cheater aren't you? Here's a dragon to fight!")
                current_menu = "boss_fight"  # Start the boss fight
                handle_boss_fight()  # Trigger the boss fight immediately
                continue  # Skip to the next iteration
            elif choice == 'rowan':
                clear_screen()
                game_data['resources']['gold'] += 1000
                print("You're a dirty little cheater aren't you? Here's 1000 doge coins!")
                continue  # Skip to the next iteration
            elif choice == 'smudge':
                clear_screen()
                MAX_CARRY_CAPACITY = 1000  # Set a high carry capacity
                game_data['player']['carry_weight'] = 0  # Reset carry weight
                update_carry_weight()  # Update carry weight
                print("You're a dirty little cheater aren't you? Here's 1000 pocketses!")
                continue  # Skip to the next iteration
            elif choice == 'jillybean':
                clear_screen()
                game_data['journey']['totalMilesTraveled'] += 500
                print("You're a dirty little cheater aren't you? Here's 500 miles traveled!")
                check_mini_boss_encounter()
                continue  # Skip to the next iteration

            choice = int(choice)
            if choice == 6:  # Finish shopping
                clear_screen()
                print(Fore.YELLOW + "\nGood Luck to you Adventurer! And so your journey begins...")
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
            amount_to_trade = int(input(f"How much {resource_to_trade} would you like to trade? (1 {resource_to_trade} = {exchange_rate} {resource_to_gain}, enter 0 to cancel): "))
            if 0 <= amount_to_trade <= game_data["resources"][resource_to_trade]:
                if amount_to_trade == 0:
                    print(Fore.CYAN + "Trade canceled. Returning to menu...")
                    return
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

# PLAYER FUNCTIONS ####################################################################
def modify_health(amount, event_description=None):
    """Modifies health and prints a message. Handles multi-day health changes."""
    game_data["player"]["health"] += amount
    game_data["player"]["health"] = min(MAX_HEALTH_LEVEL, game_data["player"]["health"])
    if game_data["player"]["health"] <= 0:
        handle_game_over()

    if event_description:
        print(Fore.CYAN + f"Event: {event_description}")

# UTILITY FUNCTIONS ####################################################################
def convert_seed_to_int(seed):
    """Converts a seed string to a 9-digit integer."""
    hash_object = hashlib.md5(seed.encode())
    hex_dig = hash_object.hexdigest()
    int_val = int(hex_dig[:9], 16)  # Take the first 9 hex digits and convert to int
    print(f"Seed {int_val} selected. ")
    return int_val

def space():
    print("\n")

def roll_d20():
    """Rolls a d20 using the seed to affect randomness."""
    return random.randint(1, 20)

### MINI-GAME FUNCTION (moving target game) ####################################################################
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

# EVENT FUNCTIONS ####################################################################
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
        "effect": lambda: modify_resource("water", 32),
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
        "effect": lambda: (advance_days(1), modify_resource("water", 32)),
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
        "effect": lambda: modify_resource("water", 8), #Use modify_resource to handle waterskin capacity
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
        "effect": lambda: modify_resource(16),
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
    if random.random() < 0.23:      # 23% chance
        event = random.choice(environmental_events)
        print(Fore.CYAN + f"Event: {event['name']}")
        print(Fore.WHITE + event['description'])
        event["effect"]()
        space()

def trigger_scouting_event():
    if random.random() < 0.23:      # 23% chance
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

# TRAVEL FUNCTIONS ####################################################################
def check_mini_boss_encounter():
    """Checks and handles the mini-boss encounter."""
    if game_data['journey']['totalMilesTraveled'] >= 500 and not game_data['journey'].get('mini_boss_defeated', False):
        handle_mini_boss_fight()
        game_data['journey']['mini_boss_defeated'] = True
        handle_post_miniboss_merchant()

def travel_miles(amount):
    game_data["journey"]["totalMilesTraveled"] += amount
    game_data["journey"]["totalMilesTraveled"] = min(TOTAL_MILES, game_data["journey"]["totalMilesTraveled"])
    print(Fore.GREEN + f"Traveled an extra {amount} miles! Total miles traveled: {game_data['journey']['totalMilesTraveled']}")

def travel():
    """Handles the travel sequence, including random encounters and a detailed summary."""
    # Check if already at the goal
    if game_data['journey']['totalMilesTraveled'] >= TOTAL_MILES:
        print(Fore.GREEN + "You have already reached the dragon's lair. No further travel is needed!")
        return

    global current_biome
    current_biome = get_next_biome(current_biome)
    game_data["journey"]["current_biome"] = current_biome

    # Resource checks and input
    food = game_data["resources"]["food"]
    water = game_data["resources"]["water"]
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

    while True:
        try:
            days_to_travel = int(input(f"How many days would you like to travel? (1-{max_days}): "))
            if 1 <= days_to_travel <= max_days:
                break
            else:
                print(f"Please enter a number between 1 and {max_days}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Travel simulation
    total_miles_traveled = 0
    events = []
    encounter_names_on_days = {}  # Dictionary to store encounter names for each day

    for day in range(days_to_travel):
        advance_days(1)  # Advance the day

        miles_traveled = random.randint(MIN_MILES_PER_TRAVEL, MAX_MILES_PER_TRAVEL)
        total_miles_traveled += miles_traveled
        game_data["journey"]["totalMilesTraveled"] += miles_traveled

        # Environmental events
        if random.random() < 0.01:
            event = random.choice(environmental_events)
            print(Fore.CYAN + f"Day {day + 1} of Travel: Event - {event['name']}")
            print(Fore.WHITE + event['description'])
            event["effect"]()
            events.append(f"Day {day + 1}: {event['name']} - {event['description']}")
        else:
            print(Fore.CYAN + f"Day {day + 1} of Travel: Uneventful")
            events.append(f"Day {day + 1}: Uneventful")

        # Random encounters
        trigger_random_encounter(encounter_names_on_days, day + 1)

        input(Fore.CYAN + "Press Enter to continue to the next day...")
        clear_screen()

    # Travel summary
    print(f"Travel complete. You traveled {total_miles_traveled} miles.")
    print("Events during travel:")
    for day in range(1, days_to_travel + 1):
        event_description = events[day - 1].split(": ", 1)[1]  # Remove the redundant day information
        encounter_name = encounter_names_on_days.get(day)
        if encounter_name:
            print(f"Day {day}: {event_description}, Encounter: {encounter_name}")
        else:
            print(f"Day {day}: {event_description}")
    space()
    # Boss Encounter check
    check_mini_boss_encounter()

    input("Press Enter to continue...")
    clear_screen()

def handle_post_miniboss_merchant():
    """Handles the merchant encounter after the mini-boss fight."""
    print(Fore.YELLOW + "\nA weary traveler approaches, offering to trade...")
    handle_purchase() # Reuse existing purchase function

def handle_travel():
    # Check if already at the goal
    if game_data['journey']['totalMilesTraveled'] >= TOTAL_MILES:
        print(Fore.GREEN + "You have already reached the dragon's lair. No further travel is needed!")
        return

     # Check for mini-boss encounter
    if game_data['journey']['totalMilesTraveled'] >= 500 and not game_data['journey'].get('mini_boss_defeated', False):
        print(Fore.RED + "\nYou encounter a fearsome mini-boss!")
        handle_mini_boss_fight()
        game_data['journey']['mini_boss_defeated'] = True  # Flag the mini-boss as defeated
        handle_post_miniboss_merchant()  #New merchant after mini-boss

    
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

# HUNT FUNCTIONS ####################################################################
def handle_hunt():
    # Check if there are supplies available to hunt
    if game_data['resources']['supplies'] <= 0:
        print(Fore.RED + "You do not have enough supplies to hunt! Find supplies or trade to restock.")
        return

    # Available game types and their corresponding weapons
    wildgame_types = {
        "Small": {"weapon": "Snare", "bonus": 1},
        "Medium": {"weapon": "Tripwire", "bonus": 2},
        "Large": {"weapon": "Arrow", "bonus": 3}
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
        bonus = hunt_mini(wildgame_types[actual_game]["bonus"])
        if bonus > 0:
            food_gained = FOOD_PER_HUNT + bonus
            game_data['resources']["food"] += food_gained
            print(f"Success! You caught {actual_game} game!")
            print(f"You gained {food_gained} lbs of food! ({FOOD_PER_HUNT} + {bonus} bonus)")
            space()

            # Add ASCII art based on game type
            if actual_game == "Small":
                display_ascii_art("small_game", Fore.WHITE)
            elif actual_game == "Medium":
                display_ascii_art("med_game", Fore.WHITE)
            elif actual_game == "Large":
                display_ascii_art("large_game", Fore.WHITE)
        else:
            print("You failed to catch any prey and return empty-handed.")
            space()
    else:
        print("You chose the wrong weapon and failed to catch any prey.")
        space()
    
    # Time passage
    days_hunting = random.randint(MIN_DAYS_PER_HUNT, MAX_DAYS_PER_HUNT)
    advance_days(days_hunting)
    
    print(f"\nHunting took {days_hunting} days.")
    print(f"Current food supply: {game_data['resources']['food']} lbs")
    space()
    input("Press Enter to continue...")
    clear_screen()

def hunt_mini(game_bonus):
    modifier = 0

    def successful_hunt_strong(survival):
        nonlocal modifier
        modifier = int(random.randint(2, 3) * (1 + survival * 0.1)) + game_bonus
        game_data['resources']['food'] += modifier
        print(f"You gained {modifier} lbs of food!")

    def successful_hunt_weak(survival):
        nonlocal modifier
        modifier = int(random.randint(1, 2) * (1 + survival * 0.05)) + game_bonus
        game_data['resources']['food'] += modifier
        print(f"You gained {modifier} lbs of food, but could have done better!")

    def fail_hunt():
        print("You failed to catch any prey and return empty-handed.")

    handle_target_practice(
        "You found prey! TIME FOR HUNTING MINI-GAME",
        "Hit! You successfully catch your prey!",
        "Miss! The prey escaped, and you return empty-handed.",
        successful_hunt_strong,
        successful_hunt_weak,
        fail_hunt
    )
    return modifier

# SCOUT FUNCTIONS ####################################################################
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
        collect_resource(target_resource, amount)
    elif total_roll >= 15 + difficulty_modifier:  # Moderate Success
        amount = random.randint(4, 6)
        print(f"\nYou found some {target_resource}! You found {amount} {target_resource}!")
        collect_resource(target_resource, amount)
    elif total_roll >= 10 + difficulty_modifier:  # Minor Success
        amount = random.randint(2, 3)
        print(f"\nYou found a small amount of {target_resource}! You found {amount} {target_resource}!")
        collect_resource(target_resource, amount)
    else:  # Failure
        print("\nYour scouting efforts yielded nothing.")
        trigger_scouting_event()  # Add a chance of a random event on failure

    space()
    input("Press Enter to continue...")
    clear_screen()

def scout_mini(resource_type):
    modifier = 0

    def successful_scout_strong(survival):
        nonlocal modifier
        modifier = int(random.randint(4, 6) * (1 + survival * 0.1))
        print(f"You're in the zone while scouting and gain a modifier of {modifier}!")

    def successful_scout_weak(survival):
        nonlocal modifier
        modifier = int(random.randint(2, 4) * (1 + survival * 0.05))
        print(f"You do well enough scouting and gain a modifier of {modifier}.")

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
    return modifier

# REST FUNCTIONS ####################################################################
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

# COOK FUNCTIONS ####################################################################
def handle_cook():
    display_ascii_art("cook", Fore.YELLOW)

    # Check if there are herbs available to cook
    if game_data['resources']['herbs'] <= 0:
        print(Fore.RED + "You do not have enough herbs to cook! Find herbs or trade to restock.")
        return

    # Ask the player what they want to cook
    print(f"You have {game_data['resources']['herbs']} herbs and {game_data['resources']['supplies']} supplies.")
    print("1. Cook herbs for food")
    print("2. Cook herbs and supplies for potions")

    while True:
        try:
            choice = int(input("What would you like to cook? (1-2): "))
            if choice in [1, 2]:
                break
            else:
                print("Enter a valid choice (1 or 2).")
        except ValueError:
            print("Enter a valid number.")

    if choice == 1:
        # Ask the player how many herbs to use for food
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
        food_gained = herbs_to_cook * (random.randint(1, 4) + (game_data["player"]["survival"] // 2))  # 1d4 + 1/2(Survival) food per herb
        modify_resource("food", food_gained)
        modify_resource("herbs", -herbs_to_cook)
        print(Fore.GREEN + f"Used {herbs_to_cook} herbs to cook. Gained {food_gained} food.")
        print(f"Current food: {game_data['resources']['food']} lbs, Herbs remaining: {game_data['resources']['herbs']}.")

    elif choice == 2:
        # Check if there are enough supplies available to cook potions
        if game_data['resources']['supplies'] <= 0:
            print(Fore.RED + "You do not have enough supplies to cook potions! Find supplies or trade to restock.")
            return

        # Ask the player how many herbs and supplies to use for potions
        while True:
            try:
                herbs_to_cook = int(input(f"How many herbs would you like to use for potions? "))
                supplies_to_cook = int(input(f"How many supplies would you like to use for potions? "))
                if 0 < herbs_to_cook <= game_data['resources']['herbs'] and 0 < supplies_to_cook <= game_data['resources']['supplies']:
                    break
                else:
                    print("Enter a valid number of herbs and supplies.")
            except ValueError:
                print("Enter a valid number.")

        # Update potions, herbs, and supplies
        potions_gained = herbs_to_cook + supplies_to_cook  # 1 potion per herb and supply
        modify_resource("herbs", -herbs_to_cook)
        modify_resource("supplies", -supplies_to_cook)
        game_data['combat']['potions'] += potions_gained
        print(Fore.GREEN + f"Used {herbs_to_cook} herbs and {supplies_to_cook} supplies to cook. Gained {potions_gained} potions.")
        print(f"Current potions: {game_data['combat']['potions']}, Herbs remaining: {game_data['resources']['herbs']}, Supplies remaining: {game_data['resources']['supplies']}.")

    space()
    input("Press Enter to continue...")
    clear_screen()

# HELP FUNCTIONS ####################################################################
def handle_help():
    print(how_to_play)
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
    print(Fore.MAGENTA + Style.BRIGHT + f"High Scores:")
    display_high_scores()
    input("Press Enter to continue...")


# GAME LOGIC FUNCTIONS ####################################################################
def handle_game():
    global current_menu

    while True:
        check_win_condition()
        clear_screen()
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
        elif command == 'jillybean':
            clear_screen()
            game_data['journey']['totalMilesTraveled'] += 500
            print("You're a dirty little cheater aren't you? Here's 500 miles traveled!")
            check_mini_boss_encounter()
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

def handle_game_start():
    # Game Start
    display_ascii_art("title", Fore.RED)
    space()
    load_high_scores()

    # Ask for the player's name
    player_name = input("Name? (This will be used to create the world seed for your gameplay): ").strip()
    game_data["player"]["name"] = player_name

    # Set the seed based on the player's name
    game_data["seed"] = convert_seed_to_int(player_name)
    random.seed(game_data["seed"])  # Set the random seed
    print("Seed set successfully.")

    # Ask for the player's survival skill
    while True:
        try:
            survival_skill = int(input("Set your Survival Skill 0-8 \n(0 = Hard)---(4 = Medium)---(8 = Easy)\n"))
            if 0 <= survival_skill <= 8:
                game_data["player"]["survival"] = survival_skill
                set_carry_capacity(survival=survival_skill)
                break
            else:
                print("Please enter a number between 0 and 8.")
        except ValueError:
            print("Please enter a valid number.")

    update_item_costs(game_data["seed"])  # Update item costs based on the new seed

    space()
    input("Press Enter to continue...")
    clear_screen()

    print(Style.BRIGHT + welcome_text)
    space()
    display_ascii_art("dragonart", Fore.RED)
    space()
    print(Style.BRIGHT + how_to_play)
    input("Hit any key to start...")  # Pause before starting gear purchase
    clear_screen()

    # Start the game with gear purchasing
    print(Fore.YELLOW + "\nWelcome to the Journey Preparation Phase!")
    game_data["resources"]["gold"] = 50 + random.randint(1, 100)  # Random starting gold
    game_data["player"]["carry_weight"] = 0
    game_data["journey"]["current_biome"] = random.choice(BIOMES)
    update_carry_weight()

    print(Fore.CYAN + f"You start with {game_data['resources']['gold']} gold pieces to prepare for your journey.")
    print("Spend your gold wisely to gather essential resources.")

    handle_purchase()  # Call the updated purchase menu
    print(Fore.GREEN + "\nYour journey begins! Good luck!")

def check_win_condition():
    if game_data["time"]["year"] >= 1 or game_data["player"]["health"] < 1:   ########################################
        handle_game_over()
    if game_data["journey"]["totalMilesTraveled"] >= 1000:
        handle_boss_fight()

def handle_game_over():
    print(Fore.RED + "Game Over!")
    display_high_scores()
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
    "journey": {"totalMilesTraveled": 0, "dragon_encountered": False, "current_biome": "MARINE", "mini_boss_defeated": False},
    "player": {"name": "", "health": 100, "survival": 0, "carry_weight": 0, "defend_cooldown": 0, "stun_splosion_cooldown": 0, "stunned": False},  # Initialize carry_weight
    "combat": {"potions": 0},
    "seed": 0,
    "last_encounter_day": 0,  # Track the last day an encounter occurred
    "encounter_chance": 0.01,  # Initial encounter chance (1%)
    "score": 0,
}

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
    potions = game_data['combat']['potions']

    if miles_remaining == 0:
        print(Fore.GREEN + "You have reached the dragon's lair!")
        game_data["journey"]["dragon_encountered"] = True
    else:
        print(f"You have traveled {game_data['journey']['totalMilesTraveled']} miles with {miles_remaining} miles left to go.")

    # Convert wood weight to full cords and remaining wood weight
    full_cords, remaining_wood = convert_wood_to_cords(wood_weight)

    # Display game status
    print("Game Status:")
    print(Back.LIGHTBLACK_EX + Fore.LIGHTCYAN_EX + Style.BRIGHT + f"Name: {game_data['player']['name']}" + Style.RESET_ALL)
    print(Back.LIGHTYELLOW_EX + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + f"Seed: {game_data['seed']}" + Style.RESET_ALL)
    print(Back.RED + Fore.LIGHTWHITE_EX + Style.BRIGHT + f"Health: {game_data['player']['health']}" + Style.RESET_ALL)
    print(Back.LIGHTGREEN_EX + Fore.RED + Style.BRIGHT + f"Food: {food}" + Style.RESET_ALL)
    print(Back.LIGHTBLUE_EX + Fore.WHITE + Style.BRIGHT + f"Water: {water}" + Style.RESET_ALL)
    print(Back.GREEN + Fore.LIGHTBLACK_EX + Style.BRIGHT + f"Wood: {wood_weight} lbs ({full_cords} full cords and {remaining_wood} lbs remaining)" + Style.RESET_ALL)
    print(Back.LIGHTCYAN_EX + Fore.BLACK + Style.BRIGHT + f"Herbs: {herbs}" + Style.RESET_ALL)
    print(Back.LIGHTRED_EX + Fore.YELLOW + Style.BRIGHT + f"Supplies: {supplies}" + Style.RESET_ALL)
    print(Back.LIGHTMAGENTA_EX + Fore.LIGHTWHITE_EX + Style.BRIGHT + f"Potions: {potions}" + Style.RESET_ALL)
    print(Back.LIGHTYELLOW_EX + Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Score: {game_data['score']}" + Style.RESET_ALL)

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

if __name__ == "__main__":
    try:
        handle_game_start()
        handle_game()
    except KeyboardInterrupt:
        stop_music()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.exception(e)  # Log the exception with traceback
        stop_music()