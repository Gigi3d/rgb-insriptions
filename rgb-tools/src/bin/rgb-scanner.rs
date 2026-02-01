use anyhow::{Context, Result};
use clap::Parser;
use glob::glob;
use serde::Serialize;
use std::fs;

const RGB_ARMOR_START: &str = "-----BEGIN RGB CONTRACT-----";
const RGB_ARMOR_END: &str = "-----END RGB CONTRACT-----";

#[derive(Parser)]
#[command(name = "rgb-scanner")]
#[command(about = "Scans files for RGB inscriptions and indexes them")]
struct Cli {
    /// Glob pattern to scan (default: "*.html")
    #[arg(default_value = "*.html")]
    pattern: String,

    /// Output JSON path (default: index.json)
    #[arg(long, default_value = "index.json")]
    json: String,
}

#[derive(Serialize)]
struct RegistryEntry {
    rgb_number: usize,
    inscription_id: String,
}

fn main() -> Result<()> {
    let args = Cli::parse();

    println!("Scanning files matching: {}...", args.pattern);

    let mut rgb_count = 0;
    let mut registry = Vec::new();

    // Sort logic would ideally be block height, but simulating with consistent alphabetical order here
    let mut paths: Vec<_> = glob(&args.pattern)
        .context("Failed to read glob pattern")?
        .filter_map(Result::ok)
        .collect();
    paths.sort();

    for path in paths {
        let content = fs::read_to_string(&path);

        // Skip binary or unreadable files gracefully
        if let Ok(text) = content {
            if let (Some(start_idx), Some(end_idx)) =
                (text.find(RGB_ARMOR_START), text.find(RGB_ARMOR_END))
            {
                if start_idx < end_idx {
                    let id = path.display().to_string();
                    registry.push(RegistryEntry {
                        rgb_number: rgb_count,
                        inscription_id: id.clone(), // In real app, this would be an extracted hash
                    });

                    println!("[FOUND] RGB #{} -> Inscription {}", rgb_count, id);
                    rgb_count += 1;
                }
            }
        }
    }

    // Write JSON registry
    let json_output = serde_json::to_string_pretty(&registry)?;
    fs::write(&args.json, json_output).context("Failed to write JSON output")?;

    println!("\n--- Scan Complete ---");
    println!("Total RGB Inscriptions found: {}", registry.len());
    println!("Registry written to: {}", args.json);

    Ok(())
}
