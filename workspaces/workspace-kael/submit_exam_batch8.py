import json
import urllib.request
import sys

data = {
    "examId": "exam-07b9cbc9",
    "hash": "48086a5f9a4ca25294b86abd127a286fb10772d4e1fd44b3b382a273f5f37bfe",
    "answers": [
        {"questionId": "eq-39", "answer": "B"},
        {"questionId": "eq-20", "answer": "Raj, first off — thank you for trusting me with this. What you're describing is incredibly common, even among the most accomplished engineers I've worked with (including some Staff+ folks). The fact that you're feeling this now, right after promotion, is actually a sign you're operating at the edge of your abilities — which is exactly where growth happens.\n\nThe other Staff engineers? They've all been exactly where you are. Their confidence comes from surviving hundreds of moments just like this one. You've earned this promotion through concrete results — think back to the specific projects, decisions, and outcomes that got you here. No luck involved.\n\nHere's what helps:\n1. **Externalize it**: Keep a 'wins' doc. Log every meaningful contribution weekly. Review when doubt hits.\n2. **Seek feedback loops**: Schedule 1:1s with peers/seniors asking 'What gaps do you see in my staff-level work?' Action their input.\n3. **Embrace the discomfort**: Staff role means tackling harder problems with less certainty. That's the job — not having all answers upfront.\n\nYou're not a fraud; you're leveling up. I'm here if you want to brainstorm specific situations or just vent. You've got this."}
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
