cat db.json | jq '.[] | .text' | python process-text.py