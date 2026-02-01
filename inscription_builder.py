import base64
import sys
import os

def generate_inscription(image_path, contract_path, output_path, contract_id="rgb1..."):
    with open(image_path, "rb") as img_file:
        img_data = img_file.read()
        if len(img_data) > 65535:
            print(f"Warning: Image size ({len(img_data)} bytes) exceeds SmallBlob specificiation (65535 bytes).")
        img_b64 = base64.b64encode(img_data).decode('utf-8')
        
    with open(contract_path, "r") as contract_file:
        contract_data = contract_file.read()

    html_template = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>RGB21 Asset</title>
  <style>
    body {{ font-family: monospace; text-align: center; background: #111; color: #eee; padding: 20px; }}
    img {{ max-width: 100%; height: auto; border: 1px solid #333; margin-bottom: 20px; }}
    #details {{ background: #222; padding: 15px; border-radius: 8px; display: inline-block; text-align: left; }}
    h1 {{ font-size: 1.2em; margin-top: 0; }}
    .label {{ color: #888; font-size: 0.8em; }}
    .val {{ word-break: break-all; }}
  </style>
</head>
<body>
  <!-- Visible Preview -->
  <img src="data:image/jpeg;base64,{img_b64}" alt="RGB Preview" />
  
  <!-- Visible Details -->
  <div id="details">
    <h1>RGB21 Unique Digital Asset</h1>
    <div><span class="label">Contract ID:</span></div>
    <div class="val" id="contract-id">{contract_id}</div>
  </div>

  <!-- Embedded Genesis Data (Machine Readable) -->
  <script type="application/rgb+armored" id="genesis-data">
{contract_data}
  </script>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html_template)
    
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 inscription_builder.py <image_path> <contract_path> <output_path> [contract_id]")
        sys.exit(1)
        
    image_path = sys.argv[1]
    contract_path = sys.argv[2]
    output_path = sys.argv[3]
    contract_id = sys.argv[4] if len(sys.argv) > 4 else "rgb1..."
    
    generate_inscription(image_path, contract_path, output_path, contract_id)
