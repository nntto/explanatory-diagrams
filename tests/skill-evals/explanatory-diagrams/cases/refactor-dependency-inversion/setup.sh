#!/usr/bin/env bash
# 実行ごとの作業場所（カレントディレクトリ）に、リファクタリングの前後を main と作業ブランチのコミットにした repo/ と、
# PR を書く人の手元のメモ notes.md を置く。
set -euo pipefail
case_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 手元の git の設定でコミットの中身が変わらないよう、グローバル・システムの設定と除外ファイルは読まず、要る設定はここで渡す。
g() {
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 \
    git -C repo -c user.name="Shop Developer" -c user.email="dev@example.com" \
    -c commit.gpgsign=false -c core.hooksPath=/dev/null -c core.excludesFile=/dev/null "$@"
}

# Finder が作る .DS_Store は写さない（入力の sha256 では無視されるので、混じっても気づけない）。
copy_into_repo() {
  cp -R "$1/." repo/
  find repo -name .DS_Store -not -path 'repo/.git/*' -delete
}

mkdir repo
g init -q -b main
copy_into_repo "$case_dir/input/before"
g add -A
GIT_AUTHOR_DATE="2026-09-01T10:00:00+09:00" GIT_COMMITTER_DATE="2026-09-01T10:00:00+09:00" \
  g commit -q -m "注文を出荷する API を足す"

g checkout -q -b refactor/shipping-ports
g rm -q -r .
copy_into_repo "$case_dir/input/after"
g add -A
GIT_AUTHOR_DATE="2026-09-03T15:00:00+09:00" GIT_COMMITTER_DATE="2026-09-03T15:00:00+09:00" \
  g commit -q -m "出荷の処理が SDK を直接呼ばないようにする"

cp "$case_dir/input/notes.md" ./notes.md
