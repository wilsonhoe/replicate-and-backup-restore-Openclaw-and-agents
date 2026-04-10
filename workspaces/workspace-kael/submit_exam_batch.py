import json
import urllib.request
import sys

try:
    with open('deployment_check.sh', 'r') as f:
        script = f.read()
except FileNotFoundError:
    print("Script file not found", file=sys.stderr)
    sys.exit(1)

data = {
    "examId": "exam-07b9cbc9",
    "hash": "12c6e57f4b68e12d5d6851cdef8054a9584329c1e3a9f3df28a2204f895237fb",
    "answers": [
        {"questionId": "exe-41", "answer": "A"},
        {"questionId": "exe-34", "answer": script}
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
