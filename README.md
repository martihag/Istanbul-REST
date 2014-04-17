Istanbul-REST
=============

RESTful system for persisting our tourist app.

###Required:
- Python 3+ (2.7 should work, just fix any debuggin print-statements)
- mongodb


```python
pip install -r requirements.txt
```

- run mongod
- python run.py

use of virtualenv is advised

=============

##Usage

localhost:5000/docs for api documentation.

Authentication is required.
The /accounts endpoint is open for public POST-methods such that one may register a username and password.

Create new user:
```JSON
POST Content-Type: application/json localhost:5000/accounts
{
  "username":"<user>",
  "password":"<password>"
}
```

To verify your authentication, GET the /auth endpoint. Point all login-requests here.
