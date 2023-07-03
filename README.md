# Python-HTTP-Server

The code in this repository is based on the following tutorials and solutions:
* **Basics (`basics` branch)**: [https://www.youtube.com/watch?v=DeFST8tvtuI](https://www.youtube.com/watch?v=DeFST8tvtuI)
* **POST + JSON (`main` branch)**: [https://gist.github.com/nitaku/10d0662536f37a087e1](https://gist.github.com/nitaku/10d0662536f37a087e1b)

These might be looked at later:
* [PUT request](https://gist.github.com/mildred/67d22d7289ae8f16cae7)

## Hosting
To host this server, execute the following command in your bash terminal, in the directory of your choice:
```sh
python -m http.server <_PORT> --bind <_HOST>
python -m http.server <_PORT> -b <_HOST>
```

## Testing
There are two ways to test: via Shell commands or via a 3rd-party tool like **Postman**

### Via Shell
To test these, follow these commands inside your bash terminal
- Testing GET: `curl <_HOST>:<_PORT> -X GET`
- Testing POST: `curl <_HOST>:<_PORT> _X POST`

### Via Tools
I recommend the **Postman** tool for more complicated debugging such as testing POST requests and the like: 
[Download Postman](https://learning.postman.com/docs/getting-started/installation-and-updates/#installing-postman-on-windows)