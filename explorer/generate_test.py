import base64

# Create synthetic data with embedded JPEG
# JPEG Magic: FF D8 FF
fake_image = b'\xFF\xD8\xFF' + b'\x00' * 50 # Valid JPEG header + 50 bytes
padding = b'\x00' * 100 # Padding to ensure image isn't at start
binary_data = padding + fake_image + padding

# Encode using Python's b85encode (which uses the RFC1924 charset)
encoded_body = base64.b85encode(binary_data).decode('ascii')

contract = f"""-----BEGIN RGB CONSIGNMENT-----
Id: rgb:fake-id
Type: contract
Contract: rgb:test-valid-contract

{encoded_body}

-----END RGB CONSIGNMENT-----
"""

with open('/tmp/test_valid.rgba', 'w') as f:
    f.write(contract)
print("Created /tmp/test_valid.rgba")
