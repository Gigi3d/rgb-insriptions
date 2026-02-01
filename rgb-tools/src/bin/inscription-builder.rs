use anyhow::{Context, Result};
use base64::{engine::general_purpose, Engine as _};
use clap::Parser;
use std::fs;
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "inscription-builder")]
#[command(about = "Generates an HTML inscription for RGB21 assets")]
struct Cli {
    /// Path to the thumbnail image
    #[arg(short, long)]
    image: PathBuf,

    /// Path to the armored contract file (.rgba)
    #[arg(short, long)]
    contract: PathBuf,

    /// Output HTML file path
    #[arg(short, long)]
    output: PathBuf,

    /// Contract ID to display
    #[arg(long, default_value = "rgb1...")]
    contract_id: String,
}

fn main() -> Result<()> {
    let args = Cli::parse();

    // 1. Process Image
    let img_data = fs::read(&args.image).context("Failed to read image file")?;
    if img_data.len() > 65_535 {
        eprintln!(
            "Warning: Image size ({} bytes) exceeds SmallBlob specification (65535 bytes).",
            img_data.len()
        );
    }
    let img_b64 = general_purpose::STANDARD.encode(&img_data);

    // 2. Process Contract
    let contract_data =
        fs::read_to_string(&args.contract).context("Failed to read contract file")?;

    // 3. Generate HTML
    let html_content = format!(
        r#"<!DOCTYPE html>
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
</html>"#,
        img_b64 = img_b64,
        contract_id = args.contract_id,
        contract_data = contract_data
    );

    // 4. Write Output
    fs::write(&args.output, html_content).context("Failed to write output file")?;
    println!("Successfully generated {}", args.output.display());

    Ok(())
}
