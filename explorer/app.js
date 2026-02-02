const DATA_URL = '../index.json';

// State
let registryData = [];

async function init() {
    try {
        const response = await fetch(DATA_URL);
        if (response.ok) {
            registryData = await response.json();
        } else {
            console.warn("Failed to load registry, valid JSON?");
        }
    } catch (e) {
        console.warn("Registry load failed, using mock data if needed.");
    }

    // Fallback Mock Data (User Requested High Fidelity Example)
    if (!registryData || registryData.length === 0) {
        registryData = [
            {
                rgb_number: 19,
                inscription_id: "rgb:csg:~wfUy0V3-k4TTfaX-2orPtgS-vjhjrdi-xuLeus_-D1PhhLA#moses-flute-karl",
                contract_id: "rgb:wW5~6EXS-qexCE6o-CVeok2m-AhpgknE-8ol9Kfb-bnFEup4",
                schema_id: "rgb:sch:~6rjymf3GTE840lb5JoXm2aFwE8eWCk3mCjOf_mUztE#spider-montana-fantasy",
                contract_type: "RGB21 (UDA)",
                asset_name: "Goddess GOAT #818",
                description: "Standard fungible token for utility access.",
                supply: 1,
                created_at: "2024-05-21T10:00:00Z",
                checksum: "c8a93474be3d21f7761c1691d82168af3858e1c5b49a6d2bce71d2989e42eb8d",
                image_details: {
                    format: "JPEG (baseline, 8-bit, 3 components)",
                    dimensions: "400×400 pixels",
                    size: "914 bytes",
                    location: "Offset 174 in decoded binary",
                    compression: "Extremely high (typical for on-chain smallblob)",
                    visual_desc: "Minimalist placeholder. The highly compressed data renders as a near-white abstract field, serving as an on-chain cryptographic artifact."
                }
            },
            {
                rgb_number: 1,
                inscription_id: "rgb_genesis.html",
                contract_type: "Genesis",
                asset_name: "RGB Genesis",
                description: "The Genesis Inscription",
                created_at: "2024-01-01T00:00:00Z"
            }
        ];
    }

    renderGrid(registryData);
    updateStats(registryData.length);

    // Modal Listeners
    const closeBtn = document.getElementById('close-btn');
    if (closeBtn) closeBtn.onclick = closeModal;

    const overlay = document.getElementById('modal-overlay');
    if (overlay) overlay.onclick = (e) => {
        if (e.target.id === 'modal-overlay') closeModal();
    };

    // Inscribe CTA
    const inscribeBtn = document.getElementById('inscribe-btn');
    if (inscribeBtn) inscribeBtn.onclick = () => {
        window.location.href = 'inscribe.html';
    };
}

function renderGrid(registry) {
    const grid = document.getElementById('grid');
    if (!grid) return;
    grid.innerHTML = '';

    const sorted = [...registry].sort((a, b) => b.rgb_number - a.rgb_number);

    sorted.forEach(item => {
        const card = document.createElement('div');
        card.className = 'rgb-card';
        card.onclick = () => openModal(item); // Click handler

        // Image Logic
        let imgUrl = 'https://placehold.co/400x400/111/444?text=RGB';
        if (item.inscription_id.includes('inscription_rust.html')) {
            imgUrl = 'https://placehold.co/400x400/050505/ff0055?text=RGB+%23' + item.rgb_number;
        } else if (item.contract_type && item.contract_type.includes("UDA")) {
            // Using placeholder with UDA specific colors per user screenshots
            imgUrl = 'https://placehold.co/400x400/050505/00ffcc?text=UDA';
        }

        // Store imgUrl on item for modal usage
        item._imgUrl = imgUrl;

        card.innerHTML = `
            <div class="card-header">
                <span class="rgb-number">RGB #${item.rgb_number}</span>
            </div>
            <div class="card-preview">
                 <img src="${imgUrl}" alt="Preview">
            </div>
            <div class="card-footer">
                <span class="contract-id">${item.contract_type || 'Unknown Type'}</span>
                <span class="label-xs">${truncatedId(item.inscription_id)}</span>
            </div>
        `;
        grid.appendChild(card);
    });
}

function truncatedId(id) {
    if (!id) return "---";
    if (id.length > 20) return id.substring(0, 8) + "..." + id.substring(id.length - 8);
    return id;
}

function openModal(item) {
    const modalBody = document.getElementById('modal-body');
    const overlay = document.getElementById('modal-overlay');
    if (!modalBody || !overlay) return;

    // Determine content based on item type
    let content = '';

    // Common Styles
    const sectionTitleStyle = "color: #00ffcc; font-size: 1.0em; margin: 0 0 15px 0; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #333; padding-bottom: 8px;";
    const gridStyle = "display: grid; grid-template-columns: 140px 1fr; gap: 8px; font-size: 0.85em; margin-bottom: 20px;";
    const labelStyle = "color: #888;";
    const valStyle = "color: #ddd; word-break: break-all; font-family: 'JetBrains Mono', monospace;";

    content = `
        <div class="modal-split">
            <div class="modal-left">
                <img src="${item._imgUrl}" class="modal-img" />
            </div>
            <div class="modal-right" style="max-height: 80vh; overflow-y: auto;">
                <h2 class="modal-title" style="margin-bottom: 5px;">RGB #${item.rgb_number}</h2>
                <div class="modal-type badge" style="margin-bottom: 25px;">${item.contract_type || 'Unknown Type'}</div>
                
                <!-- Section 1: Contract Info -->
                <h3 style="${sectionTitleStyle}">Contract Information</h3>
                <div style="${gridStyle}">
                    <div style="${labelStyle}">Contract ID</div>
                    <div style="${valStyle}">${item.contract_id || item.inscription_id}</div>

                    <div style="${labelStyle}">Schema</div>
                    <div style="${valStyle}">${formatSchema(item.schema_id || 'Unknown')}</div>

                    <div style="${labelStyle}">Asset Name</div>
                    <div style="color: #00ffcc; font-weight: 600;">${item.asset_name || ('Asset #' + item.rgb_number)}</div>

                    <div style="${labelStyle}">Asset Owner</div>
                    <div style="color: #ddd;">${item.asset_owner || 'anonymous'}</div>

                    <div style="${labelStyle}">Encoding</div>
                    <div style="color: #ddd;">Base85 (RFC1924)</div>

                    <div style="${labelStyle}">Checksum</div>
                    <div style="${valStyle}">${item.checksum || 'Pending Verification'}</div>
                </div>

                <!-- Section 2: Image Info -->
                <h3 style="${sectionTitleStyle}">Embedded Preview Image (Smallblob)</h3>
                <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 6px; font-size: 0.85em; margin-bottom: 20px;">
                    <div style="display: grid; grid-template-columns: 120px 1fr; gap: 8px;">
                        <div style="${labelStyle}">Format</div>
                        <div style="color: #fff;">${item.image_details?.format || 'JPEG (baseline)'}</div>

                        <div style="${labelStyle}">Dimensions</div>
                        <div style="color: #fff;">${item.image_details?.dimensions || '400×400 pixels'}</div>

                        <div style="${labelStyle}">File Size</div>
                        <div style="color: #fff;">${item.image_details?.size || 'Unknown'}</div>

                        <div style="${labelStyle}">Location</div>
                        <div style="color: #fff;">${item.image_details?.location || 'Embedded in binary'}</div>

                        <div style="${labelStyle}">Compression</div>
                        <div style="color: #ffaa00;">${item.image_details?.compression || 'High'}</div>

                        <div style="${labelStyle}">Visual Description</div>
                        <div style="color: #ccc; line-height: 1.4;">${item.image_details?.visual_desc || 'Standard RGB Preview'}</div>
                    </div>
                </div>

                <!-- Section 3: Educational -->
                <div style="background: rgba(0, 255, 204, 0.05); border-left: 2px solid #00ffcc; padding: 12px; font-size: 0.8em; line-height: 1.4; color: #ccc;">
                    <strong style="color: #00ffcc; display: block; margin-bottom: 5px;">About the "Smallblob"</strong>
                    The extracted image appears mostly white/blank due to extreme JPEG compression. This is intentional in RGB21 UDA contracts:
                    <ul style="margin: 5px 0; padding-left: 15px; color: #999;">
                        <li><strong>Smallblob</strong> = Tiny preview embedded on-chain</li>
                        <li><strong>Full image</strong> = Stored off-chain (IPFS, etc.)</li>
                    </ul>
                </div>
            </div>
        </div>
    `;

    modalBody.innerHTML = content;
    overlay.classList.add('active');
}

function formatSchema(schema) {
    if (schema.includes("#")) return schema.split("#")[1];
    return schema;
}

function closeModal() {
    const overlay = document.getElementById('modal-overlay');
    if (overlay) overlay.classList.remove('active');
}

function updateStats(count) {
    const el = document.getElementById('total-count');
    if (el) el.innerText = count;
}

init();
