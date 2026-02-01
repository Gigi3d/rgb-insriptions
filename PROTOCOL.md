# RGB Inscription Indexing Protocol ("The RGB Sequence")

## Goal Description
To establish a "Number Theory" for RGB Inscriptions, effectively creating a sequential index (RGB #0, RGB #1, ...) for every valid RGB Genesis Contract inscribed on the Bitcoin blockchain.

This transforms the collection of disparate inscriptions into a cohesive, ordered collection, similar to how Ordinals theory numbers Satoshis.

## Standard definition: "What is a Valid RGB Inscription?"

To be indexed, an inscription must meet the **Detection Criteria**:

### Criteria A: HTML Container (Preferred)
The inscription is an HTML file containing a script tag with the specific MIME type:
```html
<script type="application/rgb+armored" id="genesis-data">
-----BEGIN RGB CONTRACT-----
...
-----END RGB CONTRACT-----
</script>
```

### Criteria B: Raw Text (Legacy/Direct)
The inscription content body *starts* directly with the RGB Armor Header:
`-----BEGIN RGB CONTRACT-----`

## Indexing Logic
The **RGB Number** is assigned based on the **First valid appearance** on the Bitcoin blockchain.

1.  **Ordering Rule**:
    *   Primary Sort: Block Height (Ascending)
    *   Secondary Sort: Transaction Index in Block (Ascending)
    *   Tertiary Sort: Inscription Index in Transaction (Ascending)
    
    *note: This follows the canonical Ordinals inscription numbering order.*

2.  **Validity Rule**:
    *   The content MUST parse as a valid RGB Contract Genesis (checksum verification).
    *   Duplicates: If exactly the same Contract ID is inscribed twice, only the **first** one gets an RGB Number (Canonical Instance).

## Implementation Plan

### 1. Protocol Specification
Define the exact Regex and Parsing rules.
*   **Magic Bytes**: `2d 2d 2d 2d 2d 42 45 47 49 4e 20 52 47 42 20 43 4f 4e 54 52 41 43 54 2d 2d 2d 2d 2d` (ASCII for `-----BEGIN RGB CONTRACT-----`)

### 2. The Scanner (Indexer)
A script that connects to an Ordinals-aware node (e.g., `ord` server or API like Hiro/Unisat) and filters the stream.

See `rgb_scanner_mock.py` for a reference implementation.
