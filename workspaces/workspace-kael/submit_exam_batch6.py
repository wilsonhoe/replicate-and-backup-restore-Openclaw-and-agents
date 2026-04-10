import json
import urllib.request
import sys

data = {
    "examId": "exam-07b9cbc9",
    "hash": "5d360ed67466c2011448c217dc3c90627d232732f07d40ff0a7a53d6456a6820",
    "answers": [
        {"questionId": "rea-39", "answer": "A"},
        {"questionId": "rea-30", "answer": """**Scenario 1:**
- Coord sends PREPARE to P1,P2,P3.
- P1: YES, P2: YES, P3: NO.
- Coord receives mixed votes → decides ABORT.
- Sends ABORT to all.
- Final: All ABORT (P3 already prepared to abort).

**Scenario 2:**
- Coord sends PREPARE → All YES.
- Coord decides COMMIT, sends COMMIT to P1 → P1 COMMITs.
- Crashes before P2,P3.
- P2,P3 in PREPARED state, wait indefinitely for coord decision (timeout/abort policy may apply, but classically blocked).
- Final: P1 committed, P2/P3 blocked (uncertain).
- Blocking problem: Participants wait forever for failed coord; no way to proceed unilaterally.
- 3PC solves: Adds pre-commit phase. Coord sends PREPARE→COMMIT only if all ACK pre-commit. On recovery/failure detection, participants can decide based on votes.

**Scenario 3:**
- Coord sends PREPARE to all.
- P2 crashes (no vote).
- P1: YES, P3: YES, timeout on P2.
- Coord aborts due to timeout/no-vote.
- Sends ABORT to P1,P3 → they ABORT.
- P2 (crashed) recovers to ABORT (via log).
- Final: All ABORT."""}
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
