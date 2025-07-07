import os
import json
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_data():
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    all_data = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    file_data = json.load(f)
                    # If it's a list of entries, extend
                    if isinstance(file_data, list):
                        all_data.extend(file_data)
                    else:
                        all_data.append(file_data)
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
    return all_data


def extract_features(entry):
    features = {}
    
    # Basic
    features['reaction_time'] = entry.get('reactionTime', -1)
    features['answer_length'] = len(entry.get('answer', ''))
    
    # Keystroke features
    keystrokes = entry.get('keystrokes', [])
    if len(keystrokes) >= 2:
        times = [k['time'] for k in keystrokes]
        intervals = [t2 - t1 for t1, t2 in zip(times[:-1], times[1:])]
        features['avg_key_interval'] = np.mean(intervals)
        features['std_key_interval'] = np.std(intervals)
    else:
        features['avg_key_interval'] = 0
        features['std_key_interval'] = 0

    # Mouse movement features
    mouse_movements = entry.get('mouseMovements', [])
    if len(mouse_movements) >= 2:
        positions = [(m['x'], m['y']) for m in mouse_movements]
        times = [m['time'] for m in mouse_movements]
        
        distances = [
            np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            for (x1, y1), (x2, y2) in zip(positions[:-1], positions[1:])
        ]
        time_deltas = [
            t2 - t1
            for t1, t2 in zip(times[:-1], times[1:])
        ]

        total_distance = sum(distances)
        avg_speed = np.mean([
            d / t if t > 0 else 0 for d, t in zip(distances, time_deltas)
        ])
        
        features['mouse_distance'] = total_distance
        features['mouse_avg_speed'] = avg_speed
        features['mouse_movements'] = len(mouse_movements)
    else:
        features['mouse_distance'] = 0
        features['mouse_avg_speed'] = 0
        features['mouse_movements'] = 0

    return features

def generate_dataset():
    raw_data = load_data()
    feature_rows = []
    
    for entry in raw_data:
        features = extract_features(entry)
        
        # ✅ Changed: use label from the JSON data if present
        features['label'] = entry.get('label', 0)
        feature_rows.append(features)

    df = pd.DataFrame(feature_rows)
    return df

if __name__ == "__main__":
    df = generate_dataset()
    
    # Save full dataset to CSV inside the data folder
    output_csv_path = os.path.join(DATA_DIR, "dataset.csv")
    df.to_csv(output_csv_path, index=False)
    
    # Display summary
    pd.set_option("display.max_rows", None)  # Optional: Show all rows
    print(df)
    print(f"\n✅ Total records: {len(df)}")
    print(f"📁 Saved to: {output_csv_path}")
