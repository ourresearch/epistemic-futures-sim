#!/bin/zsh
cd /Users/jasonpriem/ox/epistemic-futures-sim/sim1-simple
date -u +%Y-%m-%dT%H:%M:%SZ > started-at.txt
exec claude -p "$(cat PROMPT.md)" --model claude-opus-5-5 --effort high \
  --add-dir /Users/jasonpriem/ox/epistemic-futures-corpus \
  --permission-mode acceptEdits \
  --allowedTools Read Glob Grep Write Edit Agent 'Bash(rg:*)' 'Bash(grep:*)' 'Bash(cat:*)' 'Bash(ls:*)' 'Bash(wc:*)' 'Bash(head:*)' 'Bash(tail:*)' 'Bash(sed:*)' 'Bash(find:*)' 'Bash(sort:*)' 'Bash(uniq:*)' 'Bash(cut:*)' 'Bash(awk:*)' 'Bash(jq:*)' 'Bash(python3:*)' \
  --output-format json > run.json 2> run.log
