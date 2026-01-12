import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found! Check your .env file.")

INPUT_PLAYERS = [
    { "id": "829936647138312202", "name": "Norizzyan", "points": 65 },
    { "id": "796432517954535494", "name": "Aggu", "points": 50 },
    { "id": "1059842437876547594", "name": "Xavi bin laden", "points": 45 },
    { "id": "707962986639261787", "name": "Swarit", "points": 39 },
    { "id": "1033349487915176026", "name": "Kathan", "points": 38 },
    { "id": "1075743496176148530", "name": "Mo_420", "points": 36 },
    { "id": "706044918904258694", "name": "Msn10911", "points": 36 },
    { "id": "1260194272246763522", "name": "Pablo Escobar", "points": 32 },
    { "id": "835080516859985930", "name": "Mr.x", "points": 31 },
    { "id": "691565022341758978", "name": "Dyz", "points": 27 },
    { "id": "1281518063425945622", "name": "Peter", "points": 26 },
    { "id": "839193011723829308", "name": "Toofani kanjdo", "points": 24 },
    { "id": "1032040532840550401", "name": "Omii", "points": 21 },
    { "id": "726168837158076477", "name": "Gaurav", "points": 17 },
    { "id": "789233118962778192", "name": "lll.han", "points": 17 },
    { "id": "940833565917192254", "name": "Gg boi", "points": 15 },
    { "id": "911953265816657960", "name": "Wushang", "points": 15 },
    { "id": "717332390623838211", "name": "Prateek", "points": 15 },
    { "id": "899662052757491715", "name": "Jack", "points": 15 },
    { "id": "690564323919265863", "name": "Totti", "points": 15 } ]


headers = {"Authorization": f"Bot {BOT_TOKEN}"}
updated_data = []

for player in INPUT_PLAYERS:
    user_id = player["id"]
    # We use v10 of the API
    url = f"https://discord.com/api/v10/users/{user_id}"
    response = requests.get(url, headers=headers)
    
    # Inside your loop in sync_discord.py
    if response.status_code == 200:
        data = response.json()
        user_id = data['id']
        
        # Avatar Logic (Animated vs Static)
        av_hash = data.get('avatar')
        av_ext = "gif" if av_hash and av_hash.startswith("a_") else "png"
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{av_hash}.{av_ext}?size=256" if av_hash else None

        # Banner Logic (Animated vs Static)
        b_hash = data.get('banner')
        b_ext = "gif" if b_hash and b_hash.startswith("a_") else "png"
        banner_url = f"https://cdn.discordapp.com/banners/{user_id}/{b_hash}.{b_ext}?size=600" if b_hash else None

        updated_data.append({
            "id": user_id,
            "name": data.get("global_name") or data["username"],
            "username": data["username"],
            "avatar": avatar_url,
            "banner_url": banner_url, # New field
            "banner_color": data.get("accent_color"),
            "points": player["points"],
            "bio": data.get("bio", "No bio available."),
            "badges": data.get("public_flags", 0)
        })
        print(f"Synced {data['username']}")

with open("players.json", "w") as f:
    json.dump(updated_data, f, indent=2)