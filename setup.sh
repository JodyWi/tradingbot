#!/usr/bin/env bash

set -Eeuo pipefail

# ============================================================
# autoluno Native Bootstrap
#
# Usage:
#   ./setup.sh
#   ./setup.sh --install
#   ./setup.sh --check
#
# Native only. NO Docker.
#
# Intended for:
#   Ubuntu / Debian / WSL Ubuntu
# ============================================================


# ============================================================
# Configuration
# ============================================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:---install}"

VENV_DIR="$ROOT_DIR/.venv"

ENV_FILE="$ROOT_DIR/.env"
ENV_EXAMPLE="$ROOT_DIR/.env.example"

LOCAL_DIR="$ROOT_DIR/.local"
RUN_DIR="$ROOT_DIR/.run"
LOG_DIR="$ROOT_DIR/.logs"

# Qdrant
QDRANT_DIR="$LOCAL_DIR/qdrant"
QDRANT_BIN="$QDRANT_DIR/qdrant"
QDRANT_STORAGE="$QDRANT_DIR/storage"
QDRANT_PID="$RUN_DIR/qdrant.pid"
QDRANT_LOG="$LOG_DIR/qdrant.log"

# MongoDB fallback paths
MONGO_DATA="$LOCAL_DIR/mongodb"
MONGO_PID="$RUN_DIR/mongodb.pid"
MONGO_LOG="$LOG_DIR/mongodb.log"

# Ollama
OLLAMA_PID="$RUN_DIR/ollama.pid"
OLLAMA_LOG="$LOG_DIR/ollama.log"

# SearXNG
SEARXNG_HOME="/usr/local/searxng"
SEARXNG_SRC="$SEARXNG_HOME/searxng-src"
SEARXNG_VENV="$SEARXNG_HOME/searx-pyenv"
SEARXNG_PYTHON="$SEARXNG_VENV/bin/python"
SEARXNG_SETTINGS="/etc/searxng/settings.yml"
SEARXNG_PID="$SEARXNG_HOME/searxng.pid"
SEARXNG_LOG="$SEARXNG_HOME/searxng.log"

# Ports
MONGO_PORT="${MONGO_PORT:-27017}"
QDRANT_PORT="${QDRANT_PORT:-6333}"
SEARXNG_PORT="${SEARXNG_PORT:-8888}"
OLLAMA_PORT="${OLLAMA_PORT:-11434}"


mkdir -p \
    "$LOCAL_DIR" \
    "$RUN_DIR" \
    "$LOG_DIR"


# ============================================================
# Output helpers
# ============================================================

ok() {
    printf '[ok] %s\n' "$*"
}

info() {
    printf '[info] %s\n' "$*"
}

warn() {
    printf '[warning] %s\n' "$*" >&2
}

fail() {
    printf '[error] %s\n' "$*" >&2
    exit 1
}

exists() {
    command -v "$1" >/dev/null 2>&1
}


# ============================================================
# Arguments
# ============================================================

case "$MODE" in

    --install)
        ;;

    --check)
        ;;

    --help|-h)
        printf 'Usage: %s [--install|--check]\n' "$0"
        exit 0
        ;;

    *)
        fail "Unknown option: $MODE"
        ;;

esac


# ============================================================
# OS detection
# ============================================================

[ -f /etc/os-release ] ||
    fail "Cannot determine Linux distribution."

# shellcheck disable=SC1091
source /etc/os-release

case "${ID:-}" in

    ubuntu|debian)
        ;;

    *)
        [[ "${ID_LIKE:-}" == *debian* ]] ||
            fail "This installer currently supports Ubuntu/Debian."
        ;;

esac

ok "Detected ${PRETTY_NAME:-Linux}"


# ============================================================
# sudo
# ============================================================

if [ "$(id -u)" -eq 0 ]; then

    SUDO=""

elif exists sudo; then

    SUDO="sudo"

else

    fail "sudo is required."

fi


# ============================================================
# apt helpers
# ============================================================

APT_UPDATED=0

apt_update_once() {

    if [ "$APT_UPDATED" -eq 0 ]; then

        info "Updating apt repositories..."

        $SUDO apt-get update

        APT_UPDATED=1

    fi
}


apt_install() {

    local package="$1"

    if dpkg -s "$package" >/dev/null 2>&1; then

        ok "$package installed"
        return 0

    fi


    if [ "$MODE" = "--check" ]; then

        warn "$package missing"
        return 0

    fi


    apt_update_once

    info "Installing $package..."

    $SUDO env \
        DEBIAN_FRONTEND=noninteractive \
        apt-get install -y "$package"

    ok "$package installed"
}


# ============================================================
# STEP 1
# Base Linux packages
# ============================================================

setup_base_packages() {

    info "STEP 1: Base system packages"

    apt_install ca-certificates
    apt_install curl
    apt_install git
    apt_install gnupg
    apt_install openssl
    apt_install tar
    apt_install unzip
    apt_install build-essential

    ok "Base packages ready"
}


# ============================================================
# STEP 2
# Python + pip + venv FIRST
# ============================================================

setup_python_runtime() {

    info "STEP 2: Python runtime"

    apt_install python3
    apt_install python3-pip
    apt_install python3-venv
    apt_install python3-dev
    apt_install python-is-python3


    exists python3 ||
        fail "python3 is still unavailable."


    ok "$(python3 --version)"


    if python3 -m pip --version >/dev/null 2>&1; then

        ok "$(python3 -m pip --version)"

    else

        fail "python3 exists but pip is unavailable."

    fi


    #
    # Test venv support before continuing.
    #
    # This catches the exact ensurepip issue from the first run.
    #

    local test_venv

    test_venv="$(mktemp -d)"

    if python3 -m venv "$test_venv/test" >/dev/null 2>&1; then

        ok "Python venv support verified"

    else

        rm -rf "$test_venv"
        fail "python3-venv is installed but venv creation failed."

    fi

    rm -rf "$test_venv"
}


# ============================================================
# STEP 3
# .env
# ============================================================

setup_env() {

    info "STEP 3: autoluno environment"

    if [ -f "$ENV_FILE" ]; then

        ok ".env exists"
        return

    fi


    if [ "$MODE" = "--check" ]; then

        warn ".env missing"
        return

    fi


    if [ -f "$ENV_EXAMPLE" ]; then

        cp "$ENV_EXAMPLE" "$ENV_FILE"

        ok "Created .env from .env.example"

    else

        info "Creating default .env..."

        cat > "$ENV_FILE" <<EOF
MONGO_URI=mongodb://127.0.0.1:${MONGO_PORT}
QDRANT_URL=http://127.0.0.1:${QDRANT_PORT}
SEARXNG_URL=http://127.0.0.1:${SEARXNG_PORT}
OLLAMA_URL=http://127.0.0.1:${OLLAMA_PORT}
EOF

        ok "Created .env"

    fi
}


# ============================================================
# STEP 4
# autoluno Python venv BEFORE SearXNG
# ============================================================

setup_project_python() {

    info "STEP 4: autoluno Python environment"


    if [ "$MODE" = "--check" ]; then

        if [ -x "$VENV_DIR/bin/python" ]; then

            ok "autoluno .venv exists"

        else

            warn "autoluno .venv missing"

        fi

        return

    fi


    if [ ! -x "$VENV_DIR/bin/python" ]; then

        info "Creating autoluno .venv..."

        rm -rf "$VENV_DIR"

        python3 -m venv "$VENV_DIR"

        ok "autoluno .venv created"

    else

        ok "autoluno .venv already exists"

    fi


    #
    # pip is explicitly prepared BEFORE anything like SearXNG
    # gets touched.
    #

    info "Preparing autoluno pip..."

    "$VENV_DIR/bin/python" \
        -m pip install \
        --upgrade \
        pip \
        setuptools \
        wheel


    ok "$("$VENV_DIR/bin/python" -m pip --version)"


    if [ -f "$ROOT_DIR/requirements.txt" ]; then

        info "Installing requirements.txt..."

        "$VENV_DIR/bin/python" \
            -m pip install \
            -r "$ROOT_DIR/requirements.txt"

        ok "autoluno Python requirements installed"


    elif [ -f "$ROOT_DIR/pyproject.toml" ]; then

        info "Installing autoluno pyproject..."

        "$VENV_DIR/bin/python" \
            -m pip install \
            -e "$ROOT_DIR"

        ok "autoluno Python project installed"


    else

        warn "No requirements.txt or pyproject.toml found"

    fi
}


# ============================================================
# STEP 5
# Node + frontend
# ============================================================

setup_frontend() {

    info "STEP 5: Node.js and frontend"


    apt_install nodejs
    apt_install npm


    if ! exists node || ! exists npm; then

        fail "Node.js/npm unavailable after installation."

    fi


    ok "Node $(node --version)"
    ok "npm $(npm --version)"


    local frontend="$ROOT_DIR/frontend"


    if [ ! -d "$frontend" ]; then

        info "No frontend directory; skipping frontend dependencies"
        return

    fi


    if [ "$MODE" = "--check" ]; then

        [ -d "$frontend/node_modules" ] \
            && ok "frontend/node_modules exists" \
            || warn "frontend/node_modules missing"

        return

    fi


    if [ -f "$frontend/package-lock.json" ]; then

        info "Installing frontend dependencies with npm ci..."

        npm --prefix "$frontend" ci


    elif [ -f "$frontend/package.json" ]; then

        info "Installing frontend dependencies with npm install..."

        npm --prefix "$frontend" install


    else

        warn "frontend/package.json missing"
        return

    fi


    ok "Frontend dependencies ready"
}


# ============================================================
# STEP 6
# MongoDB
# ============================================================

setup_mongodb() {

    info "STEP 6: MongoDB"


    if exists mongod; then

        ok "MongoDB installed"

    else

        if [ "$MODE" = "--check" ]; then

            warn "MongoDB missing"
            return

        fi


        if [ "${ID:-}" != "ubuntu" ]; then

            fail "Automatic MongoDB repository installation currently expects Ubuntu."

        fi


        local codename="${VERSION_CODENAME:-}"


        case "$codename" in

            noble|jammy|focal)
                ;;

            *)
                fail "Unsupported MongoDB Ubuntu release: $codename"
                ;;

        esac


        info "Installing MongoDB Community 8..."


        curl -fsSL \
            https://pgp.mongodb.com/server-8.0.asc |
            $SUDO gpg \
                --dearmor \
                --yes \
                -o /usr/share/keyrings/mongodb-server-8.0.gpg


        echo \
"deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu ${codename}/mongodb-org/8.0 multiverse" |
            $SUDO tee \
                /etc/apt/sources.list.d/mongodb-org-8.0.list \
                >/dev/null


        APT_UPDATED=0
        apt_update_once


        $SUDO env \
            DEBIAN_FRONTEND=noninteractive \
            apt-get install -y mongodb-org


        ok "MongoDB installed"

    fi


    start_mongodb
}


start_mongodb() {

    if pgrep -x mongod >/dev/null 2>&1; then

        ok "MongoDB running"
        return

    fi


    if [ "$MODE" = "--check" ]; then

        warn "MongoDB not running"
        return

    fi


    info "Starting MongoDB..."


    #
    # systemd
    #

    if exists systemctl; then

        $SUDO systemctl enable mongod >/dev/null 2>&1 || true
        $SUDO systemctl start mongod >/dev/null 2>&1 || true

        sleep 2

    fi


    if pgrep -x mongod >/dev/null 2>&1; then

        ok "MongoDB running via system service"
        return

    fi


    #
    # WSL/no-systemd fallback
    #

    info "Using local MongoDB fallback..."

    mkdir -p "$MONGO_DATA"


    nohup mongod \
        --dbpath "$MONGO_DATA" \
        --bind_ip 127.0.0.1 \
        --port "$MONGO_PORT" \
        >"$MONGO_LOG" \
        2>&1 &


    echo $! > "$MONGO_PID"

    sleep 3


    if pgrep -x mongod >/dev/null 2>&1; then

        ok "MongoDB running"

    else

        fail "MongoDB failed to start. See $MONGO_LOG"

    fi
}


# ============================================================
# STEP 7
# Qdrant native
# ============================================================

setup_qdrant() {

    info "STEP 7: Qdrant"


    if [ -x "$QDRANT_BIN" ]; then

        ok "Qdrant installed"

    else

        if [ "$MODE" = "--check" ]; then

            warn "Qdrant missing"
            return

        fi


        info "Installing native Qdrant..."


        mkdir -p \
            "$QDRANT_DIR" \
            "$QDRANT_STORAGE"


        local arch
        local asset
        local release_json
        local download_url


        arch="$(uname -m)"


        case "$arch" in

            x86_64)
                asset="qdrant-x86_64-unknown-linux-musl.tar.gz"
                ;;

            aarch64|arm64)
                asset="qdrant-aarch64-unknown-linux-musl.tar.gz"
                ;;

            *)
                fail "Unsupported Qdrant architecture: $arch"
                ;;

        esac


        release_json="$(
            curl -fsSL \
                https://api.github.com/repos/qdrant/qdrant/releases/latest
        )"


        download_url="$(
            printf '%s\n' "$release_json" |
                grep '"browser_download_url"' |
                grep "$asset" |
                head -1 |
                cut -d '"' -f 4
        )"


        [ -n "$download_url" ] ||
            fail "Could not resolve Qdrant release."


        info "Downloading Qdrant..."


        curl -fL \
            "$download_url" \
            -o "$QDRANT_DIR/qdrant.tar.gz"


        tar \
            -xzf "$QDRANT_DIR/qdrant.tar.gz" \
            -C "$QDRANT_DIR"


        rm -f "$QDRANT_DIR/qdrant.tar.gz"


        chmod +x "$QDRANT_BIN"


        ok "Qdrant installed"

    fi


    start_qdrant
}


start_qdrant() {

    if curl -fsS \
        --max-time 2 \
        "http://127.0.0.1:${QDRANT_PORT}/healthz" \
        >/dev/null 2>&1; then

        ok "Qdrant running"
        return

    fi


    if [ "$MODE" = "--check" ]; then

        warn "Qdrant not running"
        return

    fi


    info "Starting Qdrant..."


    #
    # Avoid spawning duplicate instances.
    #

    if [ -f "$QDRANT_PID" ]; then

        local pid
        pid="$(cat "$QDRANT_PID" 2>/dev/null || true)"

        if [ -n "$pid" ] &&
           kill -0 "$pid" >/dev/null 2>&1; then

            warn "Qdrant process exists but health endpoint is not ready"

        else

            rm -f "$QDRANT_PID"

        fi

    fi


    if [ ! -f "$QDRANT_PID" ]; then

        (
            cd "$QDRANT_DIR"

            QDRANT__STORAGE__STORAGE_PATH="$QDRANT_STORAGE" \
            QDRANT__SERVICE__HTTP_PORT="$QDRANT_PORT" \
            QDRANT__SERVICE__GRPC_PORT="$((QDRANT_PORT + 1))" \
            nohup "$QDRANT_BIN" \
                >"$QDRANT_LOG" \
                2>&1 &

            echo $! > "$QDRANT_PID"
        )

    fi


    sleep 4


    if curl -fsS \
        --max-time 3 \
        "http://127.0.0.1:${QDRANT_PORT}/healthz" \
        >/dev/null 2>&1; then

        ok "Qdrant running"

    else

        fail "Qdrant failed to start. See $QDRANT_LOG"

    fi
}


# ============================================================
# STEP 8
# SearXNG
#
# IMPORTANT:
# Python, pip and venv are ALREADY READY at this point.
# ============================================================

setup_searxng() {

    info "STEP 8: SearXNG"


    #
    # SearXNG native build dependencies
    #

    apt_install python3-dev
    apt_install python3-babel
    apt_install python3-venv
    apt_install python-is-python3

    apt_install libxslt1-dev
    apt_install zlib1g-dev
    apt_install libffi-dev
    apt_install libssl-dev

    apt_install build-essential
    apt_install git


    if [ "$MODE" = "--check" ]; then

        if [ -x "$SEARXNG_PYTHON" ] &&
           "$SEARXNG_PYTHON" \
               -c 'import searx' \
               >/dev/null 2>&1; then

            ok "SearXNG installed"

        else

            warn "SearXNG missing or incomplete"

        fi

        return

    fi


    #
    # Service user
    #

    if id searxng >/dev/null 2>&1; then

        ok "SearXNG user exists"

    else

        info "Creating SearXNG user..."


        $SUDO useradd \
            --shell /bin/bash \
            --system \
            --home-dir "$SEARXNG_HOME" \
            --comment "SearXNG service" \
            searxng


        ok "SearXNG user created"

    fi


    #
    # Home
    #

    $SUDO mkdir -p "$SEARXNG_HOME"

    $SUDO chown \
        -R searxng:searxng \
        "$SEARXNG_HOME"


    #
    # Clone sources directly AS searxng.
    #
    # No mktemp permission nonsense.
    #

    if [ ! -d "$SEARXNG_SRC/.git" ]; then

        info "Cloning SearXNG..."


        $SUDO rm -rf "$SEARXNG_SRC"


        $SUDO -H -u searxng \
            git clone \
            --depth 1 \
            https://github.com/searxng/searxng.git \
            "$SEARXNG_SRC"


        ok "SearXNG source cloned"

    else

        ok "SearXNG source exists"

    fi


    #
    # IMPORTANT:
    # Explicitly create SearXNG's own virtualenv.
    #
    # We DO NOT ask utils/searxng.sh to magically manage it.
    #

    if [ ! -x "$SEARXNG_PYTHON" ]; then

        info "Creating SearXNG Python environment..."


        $SUDO rm -rf "$SEARXNG_VENV"


        $SUDO -H -u searxng \
            python3 \
            -m venv \
            "$SEARXNG_VENV"


        ok "SearXNG venv created"

    else

        ok "SearXNG venv exists"

    fi


    #
    # Upgrade pip BEFORE installing SearXNG.
    #
    # This is the ordering change we wanted.
    #

    info "Preparing SearXNG pip..."


    $SUDO -H -u searxng \
        "$SEARXNG_PYTHON" \
        -m pip install \
        --upgrade \
        pip \
        setuptools \
        wheel


    ok "$(
        $SUDO -H -u searxng \
            "$SEARXNG_PYTHON" \
            -m pip \
            --version
    )"


    #
    # Official SearXNG additional Python build dependencies.
    #

    info "Installing SearXNG build dependencies..."


    $SUDO -H -u searxng \
        "$SEARXNG_PYTHON" \
        -m pip install \
        --upgrade \
        pyyaml \
        msgspec \
        typing-extensions \
        pybind11


    #
    # Install SearXNG itself.
    #

    if "$SEARXNG_PYTHON" \
        -c 'import searx' \
        >/dev/null 2>&1; then

        ok "SearXNG Python package already installed"

    else

        info "Installing SearXNG into its virtual environment..."


        (
            cd "$SEARXNG_SRC"

            $SUDO -H -u searxng \
                "$SEARXNG_PYTHON" \
                -m pip install \
                --use-pep517 \
                --no-build-isolation \
                -e .
        )


        ok "SearXNG Python package installed"

    fi


    #
    # Configuration
    #

    setup_searxng_settings


    #
    # Start it
    #

    start_searxng
}


setup_searxng_settings() {

    if [ -f "$SEARXNG_SETTINGS" ]; then

        ok "SearXNG settings exist"
        return

    fi


    info "Creating SearXNG settings..."


    local secret
    secret="$(openssl rand -hex 32)"


    $SUDO mkdir -p /etc/searxng


    $SUDO tee \
        "$SEARXNG_SETTINGS" \
        >/dev/null <<EOF
use_default_settings: true

server:
  bind_address: "127.0.0.1"
  port: ${SEARXNG_PORT}
  secret_key: "${secret}"
EOF


    $SUDO chmod 640 "$SEARXNG_SETTINGS"

    $SUDO chown \
        root:searxng \
        "$SEARXNG_SETTINGS"


    ok "SearXNG settings created"
}


start_searxng() {

    if curl -fsS \
        --max-time 3 \
        "http://127.0.0.1:${SEARXNG_PORT}/" \
        >/dev/null 2>&1; then

        ok "SearXNG running"
        return

    fi


    if [ "$MODE" = "--check" ]; then

        warn "SearXNG not running"
        return

    fi


    [ -x "$SEARXNG_PYTHON" ] ||
        fail "Cannot start SearXNG: Python environment missing."


    info "Starting SearXNG..."


    #
    # Remove stale PID
    #

    if $SUDO test -f "$SEARXNG_PID"; then

        local pid

        pid="$(
            $SUDO cat "$SEARXNG_PID" \
                2>/dev/null || true
        )"


        if [ -n "$pid" ] &&
           $SUDO kill -0 "$pid" \
               >/dev/null 2>&1; then

            warn "Existing SearXNG process detected"

        else

            $SUDO rm -f "$SEARXNG_PID"

        fi

    fi


    if ! $SUDO test -f "$SEARXNG_PID"; then

        $SUDO -H -u searxng \
            bash -c "
                cd '$SEARXNG_SRC'

                export SEARXNG_SETTINGS_PATH='$SEARXNG_SETTINGS'

                nohup '$SEARXNG_PYTHON' \
                    -m searx.webapp \
                    >'$SEARXNG_LOG' \
                    2>&1 &

                echo \$! > '$SEARXNG_PID'
            "

    fi


    sleep 5


    if curl -fsS \
        --max-time 4 \
        "http://127.0.0.1:${SEARXNG_PORT}/" \
        >/dev/null 2>&1; then

        ok "SearXNG running"

    else

        warn "SearXNG failed to become healthy"
        warn "Log: $SEARXNG_LOG"

    fi
}


# ============================================================
# STEP 9
# Ollama
# ============================================================

setup_ollama() {

    info "STEP 9: Ollama"


    if exists ollama; then

        ok "Ollama installed"

    else

        if [ "$MODE" = "--check" ]; then

            warn "Ollama missing"
            return

        fi


        info "Installing Ollama..."


        curl -fsSL \
            https://ollama.com/install.sh |
            sh


        exists ollama ||
            fail "Ollama installation failed."


        ok "Ollama installed"

    fi


    start_ollama
}


start_ollama() {

    if curl -fsS \
        --max-time 2 \
        "http://127.0.0.1:${OLLAMA_PORT}/api/tags" \
        >/dev/null 2>&1; then

        ok "Ollama running"
        return

    fi


    if [ "$MODE" = "--check" ]; then

        warn "Ollama not running"
        return

    fi


    info "Starting Ollama..."


    #
    # Try system service
    #

    if exists systemctl; then

        $SUDO systemctl start ollama \
            >/dev/null 2>&1 || true

        sleep 2

    fi


    if curl -fsS \
        --max-time 2 \
        "http://127.0.0.1:${OLLAMA_PORT}/api/tags" \
        >/dev/null 2>&1; then

        ok "Ollama running via system service"
        return

    fi


    #
    # WSL fallback
    #

    nohup ollama serve \
        >"$OLLAMA_LOG" \
        2>&1 &


    echo $! > "$OLLAMA_PID"


    sleep 4


    if curl -fsS \
        --max-time 3 \
        "http://127.0.0.1:${OLLAMA_PORT}/api/tags" \
        >/dev/null 2>&1; then

        ok "Ollama running"

    else

        fail "Ollama failed to start. See $OLLAMA_LOG"

    fi
}


# ============================================================
# MongoDB health
# ============================================================

probe_mongodb() {

    if [ ! -x "$VENV_DIR/bin/python" ]; then

        warn "MongoDB health check skipped: autoluno Python unavailable"
        return 1

    fi


    if "$VENV_DIR/bin/python" \
        - <<PY >/dev/null 2>&1
from pymongo import MongoClient

client = MongoClient(
    "mongodb://127.0.0.1:${MONGO_PORT}",
    serverSelectionTimeoutMS=2500,
)

client.admin.command("ping")
PY
    then

        ok "MongoDB healthy"
        return 0

    fi


    warn "MongoDB unhealthy"
    return 1
}


# ============================================================
# HTTP health
# ============================================================

probe_http() {

    local name="$1"
    local url="$2"


    if curl -fsS \
        --max-time 4 \
        "$url" \
        >/dev/null 2>&1; then

        ok "$name healthy"
        return 0

    fi


    warn "$name unavailable: $url"
    return 1
}


# ============================================================
# STEP 10
# Final verification
# ============================================================

verify() {

    printf '\n'
    printf '============================================================\n'
    printf ' autoluno Verification\n'
    printf '============================================================\n'


    printf '\nRuntimes:\n'


    exists python3 \
        && ok "$(python3 --version)" \
        || warn "Python missing"


    python3 -m pip --version \
        >/dev/null 2>&1 \
        && ok "system pip" \
        || warn "system pip missing"


    [ -x "$VENV_DIR/bin/python" ] \
        && ok "autoluno .venv" \
        || warn "autoluno .venv missing"


    exists node \
        && ok "Node $(node --version)" \
        || warn "Node missing"


    exists npm \
        && ok "npm $(npm --version)" \
        || warn "npm missing"


    printf '\nInstalled services:\n'


    exists mongod \
        && ok "MongoDB" \
        || warn "MongoDB missing"


    [ -x "$QDRANT_BIN" ] \
        && ok "Qdrant" \
        || warn "Qdrant missing"


    if [ -x "$SEARXNG_PYTHON" ] &&
       "$SEARXNG_PYTHON" \
           -c 'import searx' \
           >/dev/null 2>&1; then

        ok "SearXNG"

    else

        warn "SearXNG missing"

    fi


    exists ollama \
        && ok "Ollama" \
        || warn "Ollama missing"


    printf '\nHealth checks:\n'


    probe_mongodb || true


    probe_http \
        "Qdrant" \
        "http://127.0.0.1:${QDRANT_PORT}/healthz" \
        || true


    probe_http \
        "SearXNG" \
        "http://127.0.0.1:${SEARXNG_PORT}/" \
        || true


    probe_http \
        "Ollama" \
        "http://127.0.0.1:${OLLAMA_PORT}/api/tags" \
        || true


    printf '\nProject:\n'


    [ -f "$ENV_FILE" ] \
        && ok ".env" \
        || warn ".env missing"


    if [ -d "$ROOT_DIR/frontend" ]; then

        [ -d "$ROOT_DIR/frontend/node_modules" ] \
            && ok "Frontend dependencies" \
            || warn "Frontend dependencies missing"

    fi


    printf '\n'
    printf '============================================================\n'
}


# ============================================================
# Main
# ============================================================

printf '\n'
printf '============================================================\n'
printf ' autoluno Native Setup\n'
printf '============================================================\n'
printf '\n'


if [ "$MODE" = "--install" ]; then

    # --------------------------------------------------------
    # ORDER MATTERS
    # --------------------------------------------------------

    setup_base_packages

    # Python + pip are guaranteed FIRST.
    setup_python_runtime

    setup_env

    # autoluno Python is completely built before external
    # Python applications such as SearXNG.
    setup_project_python

    setup_frontend

    # Infrastructure
    setup_mongodb
    setup_qdrant

    # SearXNG only happens AFTER Python/pip/venv are verified.
    setup_searxng

    # Ollama last because it is independent.
    setup_ollama

else

    info "Check-only mode. Nothing will be installed."

fi


verify


printf '\n'
ok "autoluno setup complete"

printf '\n'
printf 'Activate autoluno Python:\n'
printf '  source .venv/bin/activate\n'
printf '\n'
printf 'Verify later:\n'
printf '  ./setup.sh --check\n'
printf '\n'