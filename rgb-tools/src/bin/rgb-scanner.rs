use anyhow::{Context, Result};
use ascii85;
use base64::{engine::general_purpose, Engine as _};
use clap::Parser;
use glob::glob;
use serde::Serialize;
use std::fs;
use z85;

const RGB_ARMOR_START: &str = "-----BEGIN RGB CONTRACT-----";
const RGB_ARMOR_END: &str = "-----END RGB CONTRACT-----";
const RGB_CONSIGNMENT_START: &str = "-----BEGIN RGB CONSIGNMENT-----";
const RGB_CONSIGNMENT_END: &str = "-----END RGB CONSIGNMENT-----";

#[derive(Parser)]
#[command(name = "rgb-scanner")]
#[command(about = "Scans files for RGB inscriptions and indexes them")]
struct Cli {
    #[arg(default_value = "*.html")]
    pattern: String,
    #[arg(long, default_value = "index.json")]
    json: String,
    #[arg(long)]
    analyze: bool,
}

#[derive(Serialize)]
struct RegistryEntry {
    rgb_number: usize,
    inscription_id: String,
    contract_id: Option<String>,
    schema_id: Option<String>,
    contract_type: Option<String>,
    checksum: Option<String>,
    version: Option<String>,
}

#[derive(Serialize)]
struct AnalysisResult {
    id: String,
    consignment_id: Option<String>,
    schema: Option<String>,
    contract_type: Option<String>,
    checksum: Option<String>,
    version: Option<String>,
    image_base64: Option<String>,
    strings: Vec<String>,
    valid: bool,
    error: Option<String>,
}

fn main() -> Result<()> {
    let args = Cli::parse();
    if args.analyze {
        analyze_file(&args.pattern)?;
        return Ok(());
    }
    scan_directory(&args)?;
    Ok(())
}

fn scan_directory(args: &Cli) -> Result<()> {
    eprintln!("Scanning files matching: {}...", args.pattern);
    let mut rgb_count = 0;
    let mut registry = Vec::new();
    let mut paths: Vec<_> = glob(&args.pattern)
        .context("Failed to read glob pattern")?
        .filter_map(Result::ok)
        .collect();
    paths.sort();
    for path in paths {
        let content = fs::read_to_string(&path);
        if let Ok(text) = content {
            let is_rgb = (text.contains(RGB_ARMOR_START) && text.contains(RGB_ARMOR_END))
                || (text.contains(RGB_CONSIGNMENT_START) && text.contains(RGB_CONSIGNMENT_END));
            if is_rgb {
                // Extract Metadata for Index
                let mut contract_id = None;
                let mut schema_id = None;
                let mut contract_type = None;
                let mut checksum = None;
                let mut version = None;

                // Simple header scan
                let normalized = text
                    .replace("\r\n", "\n")
                    .replace("\r", "\n")
                    .replace("\\n", "\n");
                let parts: Vec<&str> = normalized.splitn(2, "\n\n").collect();

                for line in parts[0].lines() {
                    if let Some((k, v)) = line.split_once(':') {
                        let val = v.trim().to_string();
                        match k.trim() {
                            "Contract" => contract_id = Some(val),
                            "Schema" => schema_id = Some(val),
                            "Type" => contract_type = Some(val),
                            "Check-SHA256" => checksum = Some(val),
                            "Version" => version = Some(val),
                            _ => {}
                        }
                    }
                }

                if contract_id.is_none() {
                    for line in parts[0].lines() {
                        if let Some((k, v)) = line.split_once(':') {
                            if k.trim() == "Id" {
                                contract_id = Some(v.trim().to_string());
                            }
                        }
                    }
                }

                registry.push(RegistryEntry {
                    rgb_number: rgb_count,
                    inscription_id: path.display().to_string(),
                    contract_id,
                    schema_id,
                    contract_type,
                    checksum,
                    version,
                });
                eprintln!("[FOUND] RGB #{} -> {}", rgb_count, path.display());
                rgb_count += 1;
            }
        }
    }
    let json_output = serde_json::to_string_pretty(&registry)?;
    fs::write(&args.json, json_output).context("Failed to write JSON output")?;
    eprintln!("\n--- Scan Complete ---");
    eprintln!("Total RGB Inscriptions found: {}", registry.len());
    Ok(())
}

fn analyze_file(path: &str) -> Result<()> {
    let content = match fs::read_to_string(path) {
        Ok(c) => c,
        Err(e) => {
            return output_analysis(AnalysisResult {
                id: "Unknown".to_string(),
                consignment_id: None,
                schema: None,
                contract_type: None,
                checksum: None,
                version: None,
                image_base64: None,
                strings: Vec::new(),
                valid: false,
                error: Some(e.to_string()),
            });
        }
    };
    let normalized = content
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\\n", "\n");

    let parts: Vec<&str> = normalized.splitn(2, "\n\n").collect();
    let header_chunk = parts[0];
    let body_chunk = if parts.len() > 1 { parts[1] } else { "" };

    let mut id = "rgb1unknown".to_string();
    let mut consignment_id = None;
    let mut schema = None;
    let mut contract_type = None;
    let mut checksum = None;
    let mut version = None;

    for line in header_chunk.lines() {
        let trimmed = line.trim();
        if trimmed.is_empty() {
            continue;
        }
        if let Some((key, val)) = trimmed.split_once(':') {
            let key = key.trim();
            let val = val.trim().to_string();
            match key {
                "Contract" => id = val,
                "Id" => {
                    if val.starts_with("rgb:csg") {
                        consignment_id = Some(val);
                    } else if id == "rgb1unknown" {
                        id = val;
                    }
                }
                "Schema" => schema = Some(val),
                "Type" => contract_type = Some(val),
                "Check-SHA256" => checksum = Some(val),
                "Version" => version = Some(val),
                _ => {}
            }
        }
    }

    let body = body_chunk
        .replace(RGB_ARMOR_START, "")
        .replace(RGB_ARMOR_END, "")
        .replace(RGB_CONSIGNMENT_START, "")
        .replace(RGB_CONSIGNMENT_END, "")
        .replace(|c: char| c.is_whitespace(), "");

    let bytes = if let Ok(decoded) = z85::decode(&body) {
        decoded
    } else if let Some(decoded) = decode_base85_rfc1924(&body) {
        decoded
    } else if let Ok(decoded) = ascii85::decode(&body) {
        decoded
    } else if let Ok(decoded) = general_purpose::STANDARD.decode(&body) {
        decoded
    } else {
        return output_analysis(AnalysisResult {
            id,
            consignment_id,
            schema,
            contract_type,
            checksum,
            version,
            image_base64: None,
            strings: Vec::new(),
            valid: true,
            error: Some("Failed to decode".to_string()),
        });
    };

    let limit = bytes.len();
    let mut image_b64 = None;
    for i in 0..limit.saturating_sub(4) {
        if bytes[i] == 0xFF && bytes[i + 1] == 0xD8 && bytes[i + 2] == 0xFF {
            let b64 = general_purpose::STANDARD.encode(&bytes[i..]);
            image_b64 = Some(format!("data:image/jpeg;base64,{}", b64));
            break;
        }
        if bytes[i] == 0x89 && bytes[i + 1] == 0x50 && bytes[i + 2] == 0x4E && bytes[i + 3] == 0x47
        {
            let b64 = general_purpose::STANDARD.encode(&bytes[i..]);
            image_b64 = Some(format!("data:image/png;base64,{}", b64));
            break;
        }
    }

    let strings = extract_strings(&bytes);
    output_analysis(AnalysisResult {
        id,
        consignment_id,
        schema,
        contract_type,
        checksum,
        version,
        image_base64: image_b64,
        strings,
        valid: true,
        error: None,
    })
}

fn extract_strings(data: &[u8]) -> Vec<String> {
    let mut strings = Vec::new();
    let mut current_string = String::new();
    for &b in data {
        if b >= 32 && b <= 126 {
            current_string.push(b as char);
        } else {
            if current_string.len() >= 4 {
                strings.push(current_string.clone());
            }
            current_string.clear();
        }
    }
    if current_string.len() >= 4 {
        strings.push(current_string);
    }
    strings
}

fn output_analysis(result: AnalysisResult) -> Result<()> {
    let json = serde_json::to_string(&result)?;
    println!("{}", json);
    Ok(())
}

fn decode_base85_rfc1924(input: &str) -> Option<Vec<u8>> {
    let charset =
        b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~";
    let mut lookup = [0xffu8; 256];
    for (i, &c) in charset.iter().enumerate() {
        lookup[c as usize] = i as u8;
    }
    let mut acc: u64 = 0;
    let mut count = 0;
    let mut out = Vec::with_capacity(input.len());
    for &b in input.as_bytes() {
        let val = lookup[b as usize];
        if val == 0xff {
            if b.is_ascii_whitespace() {
                continue;
            }
            return None;
        }
        acc = acc * 85 + (val as u64);
        count += 1;
        if count == 5 {
            if acc > u32::MAX as u64 {
                return None;
            }
            out.push((acc >> 24) as u8);
            out.push((acc >> 16) as u8);
            out.push((acc >> 8) as u8);
            out.push(acc as u8);
            acc = 0;
            count = 0;
        }
    }
    if count > 0 {
        let mut val = acc;
        for _ in 0..(5 - count) {
            val = val * 85 + 84;
        }
        if val > u32::MAX as u64 {
            return None;
        }
        if count > 1 {
            out.push((val >> 24) as u8);
        }
        if count > 2 {
            out.push((val >> 16) as u8);
        }
        if count > 3 {
            out.push((val >> 8) as u8);
        }
        if count > 4 {
            out.push(val as u8);
        }
    }
    Some(out)
}
