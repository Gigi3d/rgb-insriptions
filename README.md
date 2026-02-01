# RGB Inscriptions Project

This folder contains tools and protocols for inscribing RGB Genesis Contracts onto the Bitcoin blockchain and indexing them.

## 1. Inscribing RGB Assets

The **Inscription Builder** allows you to package an RGB Genesis Contract and a visual thumbnail into a single, inscribable HTML file.

### Files
*   `inscription_builder.py`: The Python script to generate the HTML.
*   `inscription.html`: A sample output file.
*   `sample_contract.rgba`: Sample RGB armored genesis data.
*   `sample_image.jpg`: Sample thumbnail image.

### Usage
```bash
python3 inscription_builder.py sample_image.jpg sample_contract.rgba output.html <CONTRACT_ID>
```

Then inscribe `output.html` using Ordinals (e.g., `ord wallet inscribe --file output.html`).

---

## 2. Inscription Indexing ("The RGB Sequence")

We have defined a protocol to index and number RGB inscriptions (RGB #0, RGB #1...) based on their order in the blockchain.

### Files
*   `PROTOCOL.md`: Detailed specification of the indexing rules.
*   `rgb_scanner_mock.py`: A prototype scanner script to detect valid RGB inscriptions.

### Usage
To scan for RGB inscriptions in a directory (simulating block data):
```bash
python3 rgb_scanner_mock.py "*.html"
```
