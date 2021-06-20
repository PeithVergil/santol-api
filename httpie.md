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
export AUTH_TOKEN=6040de24724c005e72b397fef29031990f4271c9b6b5a7120e06378457ed5818

http -v http://127.0.0.1:8000/profiles/me "Authorization: Bearer $AUTH_TOKEN"
```

Create a profile.

```bash
http -v http://127.0.0.1:8000/profiles/ "Authorization: Bearer $AUTH_TOKEN" "fname=Jane" "lname=Doe"
```