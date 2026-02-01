const DATA_URL = '../index.json';

// State
let registryData = [];

async function init() {
    try {
        const response = await fetch(DATA_URL);
        if (!response.ok) throw new Error("Failed to load registry");

        registryData = await response.json();
        renderGrid(registryData);
        updateStats(registryData.length);

        // Modal Listeners
        document.getElementById('close-btn').onclick = closeModal;
        document.getElementById('modal-overlay').onclick = (e) => {
            if (e.target.id === 'modal-overlay') closeModal();
        };
    } catch (e) {
        console.error("Explorer Error:", e);
        document.getElementById('grid').innerHTML = `<div style="color:red">Failed to load RGB Sequence data. Ensure rgb-scanner has run.</div>`;
    }
}

function renderGrid(registry) {
    const grid = document.getElementById('grid');
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
                <span class="label-xs">${item.inscription_id}</span>
            </div>
        `;
        grid.appendChild(card);
    });
}

function openModal(item) {
    const modalBody = document.getElementById('modal-body');
    const overlay = document.getElementById('modal-overlay');

    // Populate
    modalBody.innerHTML = `
        <div class="modal-split">
            <div class="modal-left">
                <img src="${item._imgUrl}" class="modal-img" />
            </div>
            <div class="modal-right">
                <h2 class="modal-title">RGB #${item.rgb_number}</h2>
                <div class="modal-type badge">${item.contract_type || 'Generic Contract'}</div>
                
                <div class="modal-section">
                    <h3>Description</h3>
                    <p>${item.description || 'No description available for this asset.'}</p>
                </div>

                 <div class="modal-section">
                    <h3>Details</h3>
                    <div class="kv-row">
                        <span class="k">Inscription ID</span>
                        <span class="v code">${item.inscription_id}</span>
                    </div>
                     <div class="kv-row">
                        <span class="k">Supply</span>
                        <span class="v">${item.supply ? item.supply.toLocaleString() : '1'}</span>
                    </div>
                    <div class="kv-row">
                        <span class="k">Created</span>
                        <span class="v">${item.created_at || 'Unknown'}</span>
                    </div>
                </div>
            </div>
        </div>
    `;

    overlay.classList.add('active');
}

function closeModal() {
    document.getElementById('modal-overlay').classList.remove('active');
}

function updateStats(count) {
    document.getElementById('total-count').innerText = count;
}

init();
