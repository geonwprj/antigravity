#!/bin/bash
# Antigravity LXC Bootstrap Script
# Usage: curl -sSL https://raw.githubusercontent.com/geonwprj/antigravity/main/bootstrap.sh | bash

set -e

echo "🌌 Initializing Antigravity 4-Tier Node..."

# 1. Define base directories
BASE_DIR="$HOME/.gemini"
AGENT_DIR="$HOME/.agent"

echo "📂 Creating directory structure..."
mkdir -p "$BASE_DIR/antigravity/knowledge"
mkdir -p "$BASE_DIR/antigravity/skills"
mkdir -p "$AGENT_DIR/workflows"

# 2. Set environment defaults
if [ ! -f "$HOME/.env" ]; then
    echo "🌍 Setting timezone to Asia/Hong_Kong..."
    echo "TZ=Asia/Hong_Kong" > "$HOME/.env"
fi

# 3. Download Core Rules & Logic
# These will point to the public repo once initialized
REPO_URL="https://raw.githubusercontent.com/geonwprj/antigravity/main"

echo "📜 Pulling Tier 1: Rules..."
curl -sSL "$REPO_URL/GEMINI.md" -o "$BASE_DIR/GEMINI.md"

echo "🧠 Pulling Tier 2: Knowledge Artifacts..."
# Pulling core knowledge (example)
curl -sSL "$REPO_URL/knowledge/homelab_standards.md" -o "$BASE_DIR/antigravity/knowledge/homelab_standards.md"

echo "⚡ Pulling Tier 3: Skills..."
# Note: Skills usually have multiple files, we'll pull the main SKILL.md for core ones
mkdir -p "$BASE_DIR/antigravity/skills/project-delivery"
curl -sSL "$REPO_URL/skills/project-delivery/SKILL.md" -o "$BASE_DIR/antigravity/skills/project-delivery/SKILL.md"

echo "🛠️ Pulling Tier 4: Workflows..."
curl -sSL "$REPO_URL/workflows/sync-manifest.md" -o "$AGENT_DIR/workflows/sync-manifest.md"

echo "💠 Pulled System Manifest..."
curl -sSL "$REPO_URL/system_manifest.md" -o "$BASE_DIR/system_manifest.md"

echo "✅ Antigravity Node Initialized!"
echo "Next step: Paste the 'First Contact Protocol' prompt into your agent."
