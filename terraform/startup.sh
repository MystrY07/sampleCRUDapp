#!/bin/bash
set -euxo pipefail

apt-get update -y
apt-get install -y python3-venv python3-pip git

git clone https://github.com/MystrY07/sampleCRUDapp.git /opt/sampleCRUDapp
cd /opt/sampleCRUDapp/backend

python3 -m venv /opt/crud-venv
/opt/crud-venv/bin/pip install -r requirements.txt

cat > /etc/systemd/system/crudapp.service <<'EOF'
[Unit]
Description=CRUD FastAPI backend
Wants=network-online.target
After=network-online.target

[Service]
WorkingDirectory=/opt/sampleCRUDapp/backend
ExecStart=/opt/crud-venv/bin/uvicorn main:app --host 0.0.0.0 --port 80
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now crudapp