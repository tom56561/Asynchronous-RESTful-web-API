# GUID Asynchronous RESTful API

## Description
This project is a RESTful API that provides a way to create, read, update, and delete GUIDs. It's written in Python, using Tornado for the web server, Redis for caching, and MongoDB for persistent storage.

## Installation and Test
```bash
docker-compose up -d
```
The application should now be running at http://localhost:8888.

```bash
python -m unittest discover -v
```
The command will find and run all the test cases in the project.

## RESTful API Documentation

### 1. POST /guid
Create a new GUID.

- Request Body:
    ```bash
    {
        "user": "<user>",
        "expire": "<expire>"
    }
    ```
- Success Response:
  - Status: `201 Created`
  - Body:
    ```bash
    {
        "guid": "<guid>",
        "user": "<user>",
        "expire": "<expire>"
    }
    ```
- Error Response:
  - Status: `400 Bad Request`, or `500 Internal Server Error`

### 2. GET /guid/{guid}
Get the metadata of a specific GUID.

- Success Response:
  - Status: `200 OK`
  - Body:
    ```bash
    {
        "guid": "<guid>",
        "user": "<user>",
        "expire": "<expire>"
    }
    ```
- Error Response:
  - Status: `404 Not Found`
  
### 3. PATCH /guid/{guid}
Update the metadata of a specific GUID.

- Request Body:
    ```bash
    {
        "user": "<user>",
        "expire": "<expire>"
    }
    ```
- Success Response:
  - Status: `200 OK`
  - Body:
    ```bash
    {
        "guid": "<guid>",
        "user": "<user>",
        "expire": "<expire>"
    }
    ```
- Error Response:
  - Status: `400 Bad Request`, `404 Not Found`, or `500 Internal Server Error`

### 4. DELETE /guid/{guid}
Delete a specific GUID.

- Success Response:
  - Status: `204 No Content`

- Error Response:
  - Status: `404 Not Found`


