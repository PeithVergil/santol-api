Sample HTTPie Tequests
======================

## Authenticate

```bash
http -v http://127.0.0.1:8000/auth/authenticate "username=jane.doe@example.com" "password=abcdef123456"
```

## Profile

Fetch profile detail.

```bash
export AUTH_TOKEN=2486ca4f74165bf4e87ce4eb45ea54afaa46157d8c1131cf0053c09b56ab4875

http -v http://127.0.0.1:8000/profiles/me "Authorization: Bearer $AUTH_TOKEN"
```

Create a profile.

```bash
export AUTH_TOKEN=2486ca4f74165bf4e87ce4eb45ea54afaa46157d8c1131cf0053c09b56ab4875

http -v POST http://127.0.0.1:8000/profiles/ "Authorization: Bearer $AUTH_TOKEN" "fname=Jane" "lname=Doe"
```