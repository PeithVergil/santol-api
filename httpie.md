Sample HTTPie Tequests
======================

## Authenticate

```bash
http -v http://127.0.0.1:8000/auth/authenticate "username=jane.doe@example.com" "password=abcdef123456"
```

## Profile

```bash
export AUTH_TOKEN=c8fbf2e23f01078682b69bda89e4dd2f6448450b4a7af1b804cf4b757e8f6e0f

http -v http://127.0.0.1:8000/profiles/me "Authorization: Bearer $AUTH_TOKEN"
```