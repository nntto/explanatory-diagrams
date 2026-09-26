---
description: 出荷の処理の依存の向きを逆にするリファクタリングを、git の差分とメモから、PR 本文に載せる図にする
tags: [refactor, git-diff]
runs: 1
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, TodoWrite, Bash, Write, Edit]
expected_outcome: out/ に .drawio.svg があり、変更前は出荷の処理が 3 つの SDK を直接呼び、変更後は出荷の処理と infra/ の実装がどちらも shipping/ports.ts の interface に依存する（依存の向きが逆になる）ことと、SDK のクライアントを main.ts で作って渡すようになったことが読み取れる
---

repo/ の今のブランチのリファクタリングを、PR 本文で説明する図にして。main との差分と notes.md を見て。図はこのディレクトリの out/ に置いて。
