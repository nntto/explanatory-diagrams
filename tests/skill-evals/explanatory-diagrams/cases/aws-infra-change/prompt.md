---
description: 商品画像の置き場を EFS から S3 に移すインフラの変更を、メモと Terraform の差分から、PR 本文に載せる図にする
tags: [aws, terraform]
runs: 1
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, TodoWrite, Bash, Write, Edit]
expected_outcome: out/ に .drawio.png があり、AWS の構成の中で、画像のアップロードと配信の経路のどこが足され、どこが消えたかが読み取れる
---

input/ にあるインフラの変更のメモと Terraform の差分をもとに、この変更を PR 本文で説明する図を作って。図は out/ に置いて。
