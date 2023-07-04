# Python-HTTP-Server

The code in this repository is based on the following tutorials and solutions:
* **Basics (`basics` branch)**: [https://www.youtube.com/watch?v=DeFST8tvtuI](https://www.youtube.com/watch?v=DeFST8tvtuI)
* **POST + JSON (`main` branch)**: [https://gist.github.com/nitaku/10d0662536f37a087e1](https://gist.github.com/nitaku/10d0662536f37a087e1b)
* **Python + Flask**: [https://auth0.com/blog/developing-restful-apis-with-python-and-flask/](https://auth0.com/blog/developing-restful-apis-with-python-and-flask/)

These might be looked at later:
* [PUT request](https://gist.github.com/mildred/67d22d7289ae8f16cae7)

## Hosting
If you're starting from basics, all you need to do is execute the following command in your bash terminal, in the directory of your choice:
```sh
python -m http.server <_PORT> --bind <_HOST>
python -m http.server <_PORT> -b <_HOST>
```

If you are running the flask version, do the following:
1. Inside Command Prompt (Visual Studio Code is a little weird), `cd` to the `flask-project` folder
2. (Need to verify) Execute the following command: `set FLASK_APP=./recorder.py`
2. Execute the following command: `flask --app recorder run`

## Testing
There are two ways to test: via Shell commands or via a 3rd-party tool like **Postman**

### Via Shell
To test these, follow these commands inside your bash terminal
- Testing GET: `curl <_HOST>:<_PORT> -X GET`
- Testing POST: `curl <_HOST>:<_PORT> _X POST`

### Via Tools
I recommend the **Postman** tool for more complicated debugging such as testing POST requests and the like: 
[Download Postman](https://learning.postman.com/docs/getting-started/installation-and-updates/#installing-postman-on-windows)