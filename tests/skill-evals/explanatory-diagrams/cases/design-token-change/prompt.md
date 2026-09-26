---
description: 状態の色の変更を、変更メモと変更前後の画面の画像から、PR 本文に載せる図にする
tags: [design, screenshot]
runs: 1
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, TodoWrite, Bash, Write, Edit]
expected_outcome: out/ に .drawio.png があり、変更前後の画面と、変わった部品・色の対応が読み取れる
---

input/ にあるデザイン変更のメモと画面の画像をもとに、この変更を PR 本文で説明する図を作って。図は out/ に置いて。
