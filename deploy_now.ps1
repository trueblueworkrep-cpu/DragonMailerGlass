param(
  [string]$Server = "62.72.3.154",
  [string]$User = "root",
  [string]$Domain = "dragon-mailer.com",

  # PuTTY-format host key fingerprint to avoid interactive prompts (see: plink -batch ...)
  [string]$HostKey = "ssh-ed25519 255 SHA256:0f0/xQme/T4xYBIAJfw7tu9AQEFWWmv0whNeiwEMfFY",

  # Where to upload the bundle on the server.
  [string]$RemoteZip = "/tmp/dragonmailer_bundle.zip",

  # Where the app files live on the server (used as Docker build context).
  [string]$RemoteAppDir = "/var/www/dragonmailer",

  # Where the docker-compose stack lives on the server.
  [string]$RemoteStackDir = "/docker/dragonmailer",

  # The docker network Traefik uses to reach containers.
  [string]$TraefikNetwork = "wg-easy_default",

  # Optional: provide a file containing the SSH password (no newline preferred).
  # If omitted, the script prompts and creates a temp pw file under .deploy/.
  [string]$PasswordFile = ""
)

$ErrorActionPreference = 'Stop'

function Resolve-ExePath {
  param([Parameter(Mandatory = $true)][string]$ExeName)
  $cmd = Get-Command $ExeName -ErrorAction SilentlyContinue
  if ($cmd -and $cmd.Source) { return $cmd.Source }

  $common = @(
    "C:\\Program Files\\PuTTY\\$ExeName",
    "C:\\Program Files (x86)\\PuTTY\\$ExeName"
  )
  foreach ($p in $common) {
    if (Test-Path $p) { return $p }
  }

  throw "Could not find $ExeName. Install PuTTY (plink/pscp) or add it to PATH."
}

$plink = Resolve-ExePath -ExeName "plink.exe"
$pscp = Resolve-ExePath -ExeName "pscp.exe"

$deployDir = Join-Path $PSScriptRoot ".deploy"
New-Item -ItemType Directory -Force $deployDir | Out-Null

$stageDir = Join-Path $deployDir "stage"
if (Test-Path $stageDir) { Remove-Item -Recurse -Force $stageDir }
New-Item -ItemType Directory -Force $stageDir | Out-Null

$bundleZip = Join-Path $deployDir "dragonmailer_bundle.zip"
if (Test-Path $bundleZip) { Remove-Item -Force $bundleZip }

$remoteScript = Join-Path $deployDir "remote_deploy_docker.sh"

$pwFileToUse = $PasswordFile
$createdPwFile = $false

try {
  # Build bundle staging directory.
  $include = @(
    "app.py",
    "requirements.txt",
    "dragonmailer.service",
    "dashboard_jelly.py",
    "enhanced_animations.py",
    "jelly_components.py",
    "skeuomorphic_components.py",
    "config",
    "images"
  )

  foreach ($rel in $include) {
    $src = Join-Path $PSScriptRoot $rel
    if (-not (Test-Path $src)) { throw "Missing required path: $rel" }

    $dst = Join-Path $stageDir $rel
    $dstParent = Split-Path -Parent $dst
    if (-not (Test-Path $dstParent)) { New-Item -ItemType Directory -Force $dstParent | Out-Null }

    Copy-Item -Path $src -Destination $dst -Recurse -Force
  }

  # Create zip without relying on Compress-Archive quirks.
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  [System.IO.Compression.ZipFile]::CreateFromDirectory($stageDir, $bundleZip)

  # Password handling (PuTTY expects a file via -pwfile).
  if (-not $pwFileToUse) {
    $secure = Read-Host "SSH password for $User@$Server (won't echo)" -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
      $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    } finally {
      [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }

    $pwFileToUse = Join-Path $deployDir "pw.txt"
    Set-Content -Path $pwFileToUse -Value $plain -NoNewline -Encoding ascii
    $createdPwFile = $true
  }

  # Remote deploy script (executed via plink -m).
  @"
#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$RemoteAppDir"
STACK_DIR="$RemoteStackDir"
ZIP="$RemoteZip"
DOMAIN="$Domain"
NETWORK="$TraefikNetwork"

echo "== Unpack app bundle =="
mkdir -p "\$APP_DIR"
rm -rf "\$APP_DIR"/*
unzip -o "\$ZIP" -d "\$APP_DIR"
rm -f "\$ZIP" || true

echo "== Ensure docker network exists =="
if ! docker network inspect "\$NETWORK" >/dev/null 2>&1; then
  echo "ERROR: Docker network '\$NETWORK' not found. Traefik must be configured to use a reachable network." >&2
  exit 2
fi

echo "== Stop old systemd service (if any) =="
systemctl stop dragonmailer >/dev/null 2>&1 || true
systemctl disable dragonmailer >/dev/null 2>&1 || true

echo "== Remove host venv (container build uses its own) =="
rm -rf "\$APP_DIR/venv" || true

echo "== Dockerfile + .dockerignore =="
cat > "\$APP_DIR/.dockerignore" <<'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
venv/
.env
.git/
.deploy/
EOF

cat > "\$APP_DIR/Dockerfile" <<'EOF'
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit","run","app.py","--server.port=8501","--server.address=0.0.0.0","--server.headless=true","--server.enableCORS=false","--server.enableXsrfProtection=false"]
EOF

echo "== docker-compose stack =="
mkdir -p "\$STACK_DIR"
cat > "\$STACK_DIR/docker-compose.yml" <<EOF
services:
  dragonmailer:
    build:
      context: \$APP_DIR
    restart: unless-stopped
    networks:
      - \$NETWORK
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=\$NETWORK"
      - "traefik.http.routers.dragonmailer.rule=Host(\`$DOMAIN\`) || Host(\`www.$DOMAIN\`)"
      - "traefik.http.routers.dragonmailer.entrypoints=websecure"
      - "traefik.http.routers.dragonmailer.tls=true"
      - "traefik.http.routers.dragonmailer.tls.certresolver=letsencrypt"
      - "traefik.http.services.dragonmailer.loadbalancer.server.port=8501"

networks:
  \${NETWORK}:
    external: true
EOF

echo "== Build & start =="
docker compose -f "\$STACK_DIR/docker-compose.yml" up -d --build

echo "== Status =="
docker compose -f "\$STACK_DIR/docker-compose.yml" ps
"@ | Set-Content -Path $remoteScript -NoNewline -Encoding ascii

  # Ensure LF endings so bash doesn't choke.
  (Get-Content $remoteScript -Raw) -replace "`r`n", "`n" | Set-Content -Path $remoteScript -NoNewline -Encoding ascii

  # Upload bundle.
  & $pscp -batch -hostkey $HostKey -pwfile $pwFileToUse $bundleZip "$User@$Server`:$RemoteZip"

  # Run remote deploy.
  & $plink -batch -ssh -hostkey $HostKey -pwfile $pwFileToUse "$User@$Server" -m $remoteScript
}
finally {
  # Clean up local staging directory (contains secrets).
  if (Test-Path $stageDir) { Remove-Item -Recurse -Force $stageDir }

  # Remove temp password file if we created it.
  if ($createdPwFile -and $pwFileToUse -and (Test-Path $pwFileToUse)) {
    Remove-Item -Force $pwFileToUse
  }
}
