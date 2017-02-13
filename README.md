# WP Server

It's http server based on Python3 Tornado framework and dbsqlite3 as key-value storage. 

## Installation
You need virtualenv with pip3.4 

```sh
$ virtualenv env
$ source env/bin/activate
$ pip3.4 install -r requirements.txt
$ python3 server.py
```
## How to use
#### _Allowed methods: **PUT**, **GET**, **DELETE**_
### Create/Update object
```sh
$ curl -is 127.0.0.1:8080/api/objects/key1 -XPUT -d value1 -H 'Content-Type: application/json'
```
### Delete object
```sh
$ curl -is 127.0.0.1:8080/api/objects/key1 -XDELETE
```
### Get value of key
```sh
$ curl -is 127.0.0.1:8080/api/objects/key1
```
### List of Keys
```sh
$ curl -is 127.0.0.1:8080/api/objects
```

## Run tests

```sh
$ py.test -s -vv --cov . --cov-report=term-missing --cov-fail-under=100
```

