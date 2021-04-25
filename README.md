# myRetail-REST-API

## Description 

This is a demo retail API which exposes its services through REST API. This API can perform CRUD operations to access the datastore. RESTful service can retrieve product and price details by ID. Additionally, it also includes product description if available. 

## How to Run?

To install the dependencies, execute the following steps,

1. Make the install script executable,
    ```bash
   sudo chmod +x install_dependencies.sh 
   ```
   
2. Install the necessary dependencies,
   ```bash
    ./install_dependencies.sh
    ```
3. Once successfully installed, run
    ```bash
   python3 src/main.py 
   ```
   
4. Once you ensure the server is running, go to any desired browser and type the url ` http://127.0.0.1:5000/`

## How to Authenticate?

myRetail API service is secured with JWT token. To authenticate,follow the steps given below.

* Goto `http://127.0.0.1:5000/auth` with a valid username and password in the HTTP request and get the access token.
* Once the access token is acquired, use it with every post, update or delete request to authenticate yourself.
* If the token has expired, follow the steps [How to Authenticate](#how-to-authenticate) again to get the new token.

## How to access Services?
* To view all the products in the datastore, goto `http://127.0.0.1:5000/products`
* To view any product, goto `http://127.0.0.1:5000/products<product_id>`
* To post a new product, goto `http://127.0.0.1:5000/products<product_id>` and include form data to be uploaded. Make sure you're authenticated. To authenticate to go to section [How to Authenticate](#how-to-authenticate)
* To update an existing product, got to `http://127.0.0.1:5000/products<product_id>` and include form data to be updated.
* To delete a product, go to `http://127.0.0.1:5000/products<product_id>` and given `<product_id>` will bw deleted

## How to run Tests?
To run unit test cases,
```bash
python3 unit_test/unit_test_script.py
```

### Note
Steps written are best suited for Linux platform.
