# RGB Inscriptions Sequencer

This package provides a standalone containerized environment for running the RGB Inscriptions Sequencer, which includes:
1.  **RGB Scanner**: Value verification, checks high-compression smallblobs, decodes headers.
2.  **Explorer**: Detailed dashboard and visual analysis tools.

## Prerequisites
- Docker & Docker Compose (or Docker Desktop) installed.

## How to Run (For Everyone)
1.  Open a terminal in this folder (`RGB-Inscriptions`).
2.  Run the validation sequencer:
    ```bash
    docker-compose up --build
    ```
3.  Access the Explorer at:
    [http://localhost:8000](http://localhost:8000)

## Features
- **Auto-Indexing**: The sequencer automatically indexes valid RGB contracts.
- **Visual Description**: AI-enhanced descriptions for on-chain UDA smallblobs.
- **Inscribe UI**: Create and validate your own inscriptions.

## Troubleshooting
- If the port 8000 is occupied, edit `docker-compose.yml` and change the mapping to `"8080:8000"`.
