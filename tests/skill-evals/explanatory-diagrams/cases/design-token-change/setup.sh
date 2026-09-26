#!/usr/bin/env bash
# 実行ごとの作業場所（カレントディレクトリ）に、このケースの入力を置く。
set -euo pipefail
case_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -R "$case_dir/input" ./input
