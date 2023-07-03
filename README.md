# Python-HTTP-Server

The code in this repository is based on the following tutorials and solutions:
* **Basics**: [https://www.youtube.com/watch?v=DeFST8tvtuI](https://www.youtube.com/watch?v=DeFST8tvtuI)

## Hosting
To host this server, execute the following command in your bash terminal, in the directory of your choice:
```sh
python -m http.server <_PORT> --bind <_HOST>
python -m http.server <_PORT> -b <_HOST>
```

## Testing
To test these, follow these commands inside your bash terminal
- Testing GET: `curl <_HOST>:<_PORT> -X GET`
- Testing POST: `curl <_HOST>:<_PORT> _X POST`

... Or get an app like Postman to test more robustly