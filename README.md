# SSRF Logger

This tool generates and logs SSRF (Server-Side Request Forgery) secrets along with metadata such as timestamp and IP address it is requested from. 

## Installation

```bash
git clone https://github.com/pr0d33p/SSRF-Log.git
cd SSRF-Log
pip3 install -r requirements.txt
```

## Usage

```bash
python3 app.py
```

This will start the SSRF-Log server on `http://0.0.0.0:5000/`.

## Endpoints
This matches any endpoints sent as it catches all paths.