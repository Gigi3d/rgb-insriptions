import json
import random

CONTRACT_TYPES = ["RGB21 (UDA)", "RGB20 (Fungible)", "RGB25 (Collectible)"]
DESCRIPTIONS = [
    "A unique digital asset representing an ancient artifact.",
    "Standard fungible token for utility access.",
    "A collectible trading card series, 1st edition.",
    "Membership token for the RGB Vanguard.",
    "Digital land deed on the Bitcoin Network."
]

def generate_mock():
    registry = []
    
    # Generate 20 mock items
    for i in range(20):
        # Create a fake hash-like ID
        hex_id = ''.join(random.choices('0123456789abcdef', k=64))
        
        c_type = "RGB21 (UDA)" # Default to UDA as requested primarily
        if i % 3 == 0: c_type = "RGB20 (Fungible)"
        
        entry = {
            "rgb_number": i,
            "inscription_id": f"{hex_id}i0",
            "contract_type": c_type,
            "description": random.choice(DESCRIPTIONS),
            "supply": 1 if "UDA" in c_type else 1000000,
            "created_at": "2024-05-21T10:00:00Z"
        }
        registry.append(entry)
    
    # Sort descending so #19 is first
    registry.sort(key=lambda x: x['rgb_number'], reverse=True)
    
    with open('index.json', 'w') as f:
        json.dump(registry, f, indent=2)
    
    print(f"Generated {len(registry)} rich mock inscriptions in index.json")

if __name__ == "__main__":
    generate_mock()
