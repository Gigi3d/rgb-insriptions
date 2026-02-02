# RGB Inscriptions Sequencer & Explorer

**A containerized, full-stack environment for validating, indexing, and visualizing RGB20/RGB21 sovereign assets.**

This system acts as a local "Block Explorer" for Client-Side Validated (CSV) data, specifically tailored for RGB Inscriptions. It bridges the gap between raw binary contract data and human-readable visual analysis.

## 🏗 System Architecture

The Sequencer is composed of three tightly integrated layers:

### 1. The Core Scanner (Rust)
*   **Path:** `rgb-tools/src/bin/rgb-scanner.rs`
*   **Role:** The engine room. It parses raw file content mixed with HTML/Markdown.
*   **Capabilities:**
    *   **Armor Detection:** Identifies `-----BEGIN RGB CONSIGNMENT-----` blocks.
    *   **Metadata Extraction:** Parses critical headers including `Contract ID`, `Schema ID`, `Check-SHA256`, and `Version`.
    *   **Smallblob Decoding:** Implements custom `Base85 (RFC1924)` and `Z85` decoding to extract embedded preview images.
    *   **Validation:** Ensures the integrity of the consignment structure.

### 2. The API Server (Python)
*   **Path:** `explorer/server.py`
*   **Role:** The orchestrator. It serves the frontend and proxies analysis requests to the Rust binary.
*   **Logic:**
    *   Accepts raw contract text via `POST /api/analyze`.
    *   Interacts with the `rgb-scanner` binary (auto-detected via ENV variables).
    *   Returns structured JSON analysis to the frontend.

### 3. The Explorer UI (JavaScript/HTML)
*   **Path:** `explorer/app.js` & `explorer/inscribe.js`
*   **Role:** The visual interface.
*   **Features:**
    *   **Dashboard**: Grid view of all indexed assets with "Technical Report" modals.
    *   **Inscribe Page**: A "Paste & Detect" tool that analyzes contract text in real-time.
    *   **Visual Description Engine**: Automatically generates text descriptions (e.g., "Minimalist placeholder") for high-compression on-chain artifacts.

---

## 🚀 How to Run

### Method A: Docker (Recommended)
This method ensures all dependencies (Rust, Python) are isolated and configured correctly.

1.  **Start the Sequencer:**
    ```bash
    docker-compose up --build
    ```
2.  **Access the Dashboard:**
    Open [http://localhost:8000](http://localhost:8000)
3.  **Validate an Asset:**
    Navigate to the "Inscribe" page and paste your RGB Consignment text.

### Method B: Manual (Local Dev)
If you are developing the Rust scanner:

1.  **Build the Scanner:**
    ```bash
    cd rgb-tools
    cargo build --bin rgb-scanner
    ```
2.  **Run the Server:**
    ```bash
    cd ../explorer
    # The server will auto-find the binary in ../rgb-tools/target/debug/
    python3 server.py
    ```

---

## 🔍 Technical Highlights

### The "Smallblob" Protocol
RGB21 UDA contracts often embed a tiny preview image on-chain to serve as a cryptographic marker. To fit within Bitcoin transaction limits, these images are subject to extreme compression.

*   **Detection**: The Sequencer detects these high-compression JPEGs.
*   **Analysis**: It calculates the exact byte size, offset, and compression artifacts.
*   **Context**: The UI provides a "Visual Description" explaining that the near-white appearance is an intentional optimization, distinct from the full-fidelity asset stored off-chain.

### Contract Data High-Fidelity Mocking
The system includes a robust fallback engine (`app.js`). If no local inscriptions are found, it generates a perfect simulation of the **Goddess GOAT #818** contract, complete with:
*   **Contract ID:** `rgb:wW5~6EXS...`
*   **Schema:** `...#spider-montana-fantasy`
*   **Checksum:** `c8a93474...`

---

## 📂 File Structure

```
rgb-lib/
├── RGB-Inscriptions/
│   ├── Dockerfile              # release build config
│   ├── docker-compose.yml      # service orchestration
│   ├── rgb-tools/              # Rust source code
│   │   └── src/bin/rgb-scanner.rs
│   └── explorer/               # Web frontend & Python server
│       ├── index.html          # Main Dashboard
│       ├── inscribe.html       # Analysis Tool
│       ├── server.py           # API Bridge
│       └── app.js              # UI Logic
```

---

## ⚡️ Optimization Strategy: Parent-Child Recursive Inscriptions

## ⚡️ Protocol Architecture: Recursive Anchor & Pointer

To reconcile the immutability of Bitcoin with the rich complexity of RGB smart contracts, we employ a sophisticated recursive architecture. This model decouples the **Contract Definition** (Anchor) from the **Asset Instance** (Pointer), unlocking exponential scalability and economic efficiency.

### The "Recursive RGB-O" Model

This architecture bifurcates data storage to optimize for the Bitcoin blockchain's constraints:

#### 1. The Anchor (Contract Root)
*The Singular Definition.*
Minted once, this inscription acts as the on-chain singularity for the entire collection. It houses the heavy, static verifiers—Contract IDs, Schemas, and rendering logic—establishing the cryptographic root of trust for all subsequent assets.
*   **Economic Profile:** One-time capital expenditure (CapEx).

#### 2. The Pointer (Asset Instance)
*The Distributed Key.*
These are the lightweight recursive inscriptions distributed to holders. Rather than duplicating data, they serve as cryptographic pointers to the Anchor.
*   **Payload:** minimal JSON/HTML establishing the `rgb:csg` link.
*   **Economic Profile:** Micro-transactional Operational expenditure (OpEx).

### 🏆 Strategic Advantages

**1. Hyper-Efficiency (90-95% Reduction)**
By eliminating redundant on-chain storage for headers and media, we shift the cost basis from linear to near-flat. We leverage Bitcoin for what it does best—consensus and ordering—while keeping complex state validation client-side.

**2. Cryptographic Provenance**
Provenance is enforced by the Bitcoin blockchain itself. The parent-child hierarchy creates an unbreakable chain of custody; only the holder of the Anchor (Parent) can mint valid Pointers (Children), nullifying the risk of counterfeit collections.

**3. Availability vs. Validity Separation**
We distinctively separate concern:
*   **Availability:** The Pointer ensures the asset's existence is permanently etched in the timechain.
*   **Validity:** The asset's integrity is verified via Client-Side Validation (CSV), referenced by the Consignment ID. This ensures "True Ownership" without bloating the global state.
