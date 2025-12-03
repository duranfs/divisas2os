import pickle
import sys

ticket = 'errors/127.0.0.1.2025-11-27.18-33-03.a76485e9-7ee1-43b9-9ee5-20ce6d1a9115'

with open(ticket, 'rb') as f:
    data = pickle.load(f)
    
print("Claves disponibles:", list(data.keys()))
print("\n" + "="*80)

for key in ['output', 'traceback', 'layer']:
    if key in data:
        print(f"\n{key}:")
        print(data[key])
