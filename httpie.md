Sample HTTPie Requests
======================

## User

Authenticate a user.

```bash
http -v http://127.0.0.1:8000/auth/authenticate "username=jane.doe@example.com" "password=abcdef123456"
```

Create a new user.

```bash
http -v http://127.0.0.1:8000/auth/users "username=jane.doe@example.com" "password=abcdef123456"
```

## Profile

Fetch profile detail.

```bash
export AUTH_TOKEN=4953e0d18bc45d8cbf087b06aed5bd22412749fc002ba621a2db5949f6ef937c

http -v http://127.0.0.1:8000/profiles/me "Authorization: Bearer $AUTH_TOKEN"
```

Create a profile.

```bash
http -v http://127.0.0.1:8000/profiles/ "Authorization: Bearer $AUTH_TOKEN" "fname=Jane" "lname=Doe"
```