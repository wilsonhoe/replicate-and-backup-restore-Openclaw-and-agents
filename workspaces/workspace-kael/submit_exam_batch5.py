import json
import urllib.request
import sys

data = {
    "examId": "exam-07b9cbc9",
    "hash": "27ea012e6ef61f81a2589ddd30fbb73d4ef254d21790e9ff93fb0aa78f95be90",
    "answers": [
        {"questionId": "ref-43", "answer": "A"},
        {"questionId": "ref-05", "answer": """1. DEFER: Incorporation choice depends on your location, funding plans, tax strategy, and investor preferences. Consult a lawyer or use tools like Stripe Atlas/Clerky for jurisdiction-specific advice.

2. FACT: TCP is reliable, connection-oriented (handshake, ordered delivery, error correction, flow control). UDP is unreliable, connectionless (fire-and-forget, faster, no guarantees — used for video streaming, DNS).

3. OPINION: $49/mo is reasonable for SMB SaaS if it delivers clear ROI (e.g. saves 2+ hours/week). Benchmark competitors (e.g. HubSpot $20-50, Intercom $74+). Test with A/B pricing; start low if acquisition-focused.

4. FACT: HTTPS = HTTP over TLS/SSL. Process: 1) Client Hello (ciphers, SNI). 2) Server Hello + cert. 3) Asymmetric key exchange (Diffie-Hellman/ECC) to derive symmetric session key. 4) Symmetric AES encryption for data. 5) Handshake finished. Certs validated via CA chain.

5. OPINION: No, AI won't replace engineers but will augment (code gen, testing). Engineers who use AI effectively will thrive; demand grows ~15-20%/yr per BLS projections.

6. OPINION: Not fair — vesting + cliff standard (4yr/1yr). Founder1 (you): 60-70%. Founder2: 30-40% with 6mo cliff. Use Slicing Pie or advisor agreement if contributions unequal."""}
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
