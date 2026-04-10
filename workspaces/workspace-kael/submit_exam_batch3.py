import json
import urllib.request
import sys

data = {
    "examId": "exam-07b9cbc9",
    "hash": "419d7b8100908350698a665cfa7baba275ecf8f2e4a47d40fcaf7a4bf5c532f8",
    "answers": [
        {"questionId": "ret-42", "answer": "D"},
        {"questionId": "ret-32", "answer": """**Issue 1: API 405 on POST**
1. Cause: In Next.js App Router, API route handler doesn't export POST function (uses GET by default).
2. Verify: Vercel logs show handler called but method not handled; curl -X POST returns 405.
3. Fix: app/api/route/route.ts
```ts
export async function POST(request: Request) {
  const body = await request.json();
  return Response.json({ success: true });
}
```

**Issue 2: CDN images broken**
1. Cause: next.config.js lacks remotePatterns/domains for images.example.com.
2. Verify: Network tab shows CORS/403; local works (no Image component optimization).
3. Fix: next.config.js
```js
module.exports = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'images.example.com' }
    ]
  }
};
```

**Issue 3: /admin no auth**
1. Cause: middleware.ts matcher excludes /admin or middleware not rewriting.
2. Verify: No middleware execution logs; access /admin without token.
3. Fix: middleware.ts
```ts
export { default } from 'middleware';
export const config = {
  matcher: ['/admin/:path*', '/((?!api|_next/static|_next/image|favicon.ico).*)']
};
```
Ensure middleware redirects unauth.

**Issue 4: DATABASE_URL undefined**
1. Cause: Env var not set for production env in Vercel dashboard or scoped wrong.
2. Verify: Add console.log(process.env.DATABASE_URL) to API route, deploy, check logs.
3. Fix: Vercel Dashboard > Project Settings > Environment Variables > Add DATABASE_URL for Production.

**Issue 5: Hydration mismatch**
1. Cause: Client/server render diff (e.g. Date, window checks, random IDs).
2. Verify: Console error specifies mismatched element/text.
3. Fix: Use useEffect or dynamic import:
```jsx
'use client';
import { useEffect, useState } from 'react';
export default function Component() {
  const [clientOnly, setClientOnly] = useState(false);
  useEffect(() => setClientOnly(true), []);
  if (!clientOnly) return <div>Loading...</div>;
  // client render
}
```
Or dynamic: dynamic(() => import('./Component'), { ssr: false })"""}
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
