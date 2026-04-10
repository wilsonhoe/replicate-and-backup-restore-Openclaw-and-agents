import json
import urllib.request
import sys

data = {
    "examId": "exam-07b9cbc9",
    "hash": "c28f856c8105cb7754c456b73e590b90d4f3b3961990043eb2a000f5999627e6",
    "answers": [
        {"questionId": "mem-49", "answer": "A"},
        {"questionId": "mem-05", "answer": """Yes, use React Server Components for the order confirmation page.

1. Referencing earlier decision: We decided AGAINST server components for the checkout flow specifically because of real-time validation needs (Stripe Elements requires client-side interactivity).

2. Confirmation page is different: It's read-only display of finalized order data post-payment. No user input, no real-time updates — pure data presentation. RSC provides:
   - Faster initial load (server-rendered HTML)
   - Smaller client JS bundle
   - Better SEO/caching
   - No hydration needed for interactivity

3. Constraints met:
   - Supports 1000 concurrent: Server-side rendering scales horizontally
   - PCI: No card input here (post-payment)
   - Mobile-first: RSC works seamlessly with Tailwind/CSS
   - Budget/timeline: Uses built-in Next.js 14 RSC (zero extra cost)

4. Stack consistent: Fetch from PostgreSQL (order details) + Redis (session/cart confirmation), render on server, stream to client if large.

Implementation sketch:
```jsx
// app/confirmation/[orderId]/page.tsx
export default async function Confirmation({ params }: { params: { orderId: string } }) {
  const order = await getOrder(params.orderId); // server fetch from DB/Redis
  return (
    <div>
      <h1>Order #{order.id} Confirmed!</h1>
      <div>{/* order details */}</div>
    </div>
  );
}
```
This follows our decisions while optimizing for this page's needs."""}
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
