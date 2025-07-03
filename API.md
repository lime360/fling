# API reference

## Routes
* `GET /next` - next site in the webring, must contain the `?url=[YOUR SITE URL]` parameter
* `GET /prev` - previous site in the webring, must contain the `?url=[YOUR SITE URL]` parameter
* `GET /random` - random site from the webring
* `GET /list` - a JSON list of all sites in a webring
* `POST /token` - generate a JWT token
* `POST /insert` - insert a website into the webring, requires a JWT

## cURL examples

### Generate a JWT
```sh
$ curl -X POST http://127.0.0.1:5000/token -d "{\"password\":\"[PASSWORD]\"}" -H "Content-Type: application/json"
# {"success": true, "message": "here is your JWT token! remember not to share it with anyone!", "token": "[JWT TOKEN]"}
```

### Insert a site
```sh
$ curl -X POST http://127.0.0.1:5000/insert  -d "{\"name\":\"Example\",\"url\":\"https://example.com\",\"owner\":\"John Doe\"}" -H "Content-Type: application/json" -H "Authorization: Bearer [JWT TOKEN]"
# {"success": true, "message": "site https://example.com has been added to the webring!"}
```