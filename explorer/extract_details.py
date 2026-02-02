import base64
import re
import string

# Minimal extraction of the body from the *memory* of what I saw in Step 720
# I will use a placeholder here and ask the user to re-paste ONLY if I can't find the file.
# BUT, I already wrote the file in Step 836? NO, that failed.
# I wrote it in Step 640? No.
# I will try to read /tmp/test_contract.rgba IF I successfully updated it.
# Check file size of /tmp/test_contract.rgba first.

def extract_strings(data):
    # Regex to find printable strings of length >= 4
    chars = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    regexp = b"[%s]{4,}" % chars
    
    found = []
    for match in re.finditer(regexp, data):
        found.append(match.group().decode('ascii'))
    return found

try:
    # Try reading the file we hope exists or I'll create a dummy one to verify the script 
    # Logic: I need the REAL data.
    # I will assume the user has the file locally at /tmp/test_contract.rgba or similar.
    # If not, I will ask user to confirm location.
    # BUT, I can just use the debug_contract.py logic which expects a file.
    
    path = '../sample_contract.rgba'
    with open(path, 'r') as f:
        content = f.read()
        
    # Extract body
    if '\n\n' in content:
        body = content.split('\n\n', 1)[1]
    else:
        body = content
        
    body = body.replace('-----BEGIN RGB CONSIGNMENT-----', '') \
               .replace('-----END RGB CONSIGNMENT-----', '') \
               .replace('-----BEGIN RGB CONTRACT-----', '') \
               .replace('-----END RGB CONTRACT-----', '')
    cleaned = ''.join(body.split())
    
    print(f"Body length: {len(cleaned)}")
    
    # Decode
    data = base64.b85decode(cleaned)
    print(f"Decoded {len(data)} bytes")
    
    strings = extract_strings(data)
    print("\n--- Extracted Strings ---")
    for s in strings:
        print(s)
        
except Exception as e:
    print(f"Error: {e}")
