import os
import json
import random
import time

# Path to your data folder
DATA_DIR = "../data"
NUM_BOT_SESSIONS = 30  # number of bot sessions to create

def generate_bot_session():
    # Simulated very fast reaction time (bots are super quick)
    reaction_time = random.randint(100, 300)

    # Simulated keystrokes with near-zero delays
    keystrokes = []
    current_time = 1000  # starting timestamp in ms
    for key in "automate":
        delay = random.randint(5, 15)  # ultra-fast typing
        current_time += delay
        keystrokes.append({
            "key": key,
            "time": current_time
        })

    # Simulated straight-line or jumpy mouse movements
    mouse_movements = []
    x, y = random.randint(100, 200), random.randint(100, 200)
    for _ in range(30):
        x += random.randint(1, 5)
        y += random.randint(1, 5)
        timestamp = int(time.time() * 1000)
        mouse_movements.append({
            "x": x,
            "y": y,
            "time": timestamp
        })

    # Return the full session dictionary with label = 1 (bot)
    return {
        "prompt": "Are you a bot?",
        "answer": "yes",
        "reactionTime": reaction_time,
        "keystrokes": keystrokes,
        "mouseMovements": mouse_movements,
        "label": 1
    }

# Create and save bot sessions
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

for i in range(NUM_BOT_SESSIONS):
    bot_session = generate_bot_session()
    file_path = os.path.join(DATA_DIR, f"bot_session_{i+1}.json")
    with open(file_path, "w") as f:
        json.dump(bot_session, f, indent=2)

print(f"✅ Successfully created {NUM_BOT_SESSIONS} bot sessions in '{DATA_DIR}' folder.")
