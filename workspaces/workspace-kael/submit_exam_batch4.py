import json
import urllib.request
import sys

data = {
    "examId": "exam-07b9cbc9",
    "hash": "75b9802561d4417a51b04cd9c2850136a8ffd5e082a39d8070c0606fad5e2a96",
    "answers": [
        {"questionId": "und-43", "answer": "B"},
        {"questionId": "und-05", "answer": """1. Actual problem: Spike in 500 timeout errors on /api/checkout starting ~2 hours ago after deploying new payment provider SDK v3 (which has 5s default timeout vs old 30s).

2. Constraints mentioned:
   - Load test ended at 3pm (not the cause).
   - Staging down for maintenance, so only local unit tests run.
   - Users bounce after ~10s.
   - Provider recommends 10s for v3 to avoid duplicate charges on longer timeouts.

3. Decision made: Hotfix timeout to 10s (provider recommendation), @carol pushing the change.

4. Left unresolved: Adding timeout config to config service for deploy-free changes (good idea, but postponed to fix bleeding first)."""}
    ]
}

url = "https://clawvard.school/api/exam/batch-answer"

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

with urllib.request.urlopen(req) as response:
    result = response.read().decode('utf-8')
    print(result)
