# GUID Asynchronous RESTful API

## Description
This project provides a RESTful web API for managing a database of Globally Unique Identifiers (GUIDs) and their associated metadata.


## Business Requirements
The purpose of the project is to design and implement a web API for performing CRUD (Create, Read, Update, Delete) operations on GUIDs. The system should generate a GUID if not provided and store it with its associated metadata.

### Key Features
1. **GUID Generation**: If no GUID is provided, the system should generate a random one. 
2. **CRUD Operations**: Support for creating, reading, updating, and deleting GUIDs and their associated metadata.
3. **GUID Expiration**: GUIDs are valid for a limited period of time, defaulting to 30 days from the time of creation, if an expiration time is not provided.
4. **Data Validation**: The system should validate all input and output data to confirm it adheres to the specified formats.
5. **Caching**: The system should implement a cache layer for serving the most recently used GUIDs quickly.
6. **Asynchronous Operations**: The system operations should ideally be asynchronous.

### Technology Stack
1. **Web Framework**: Tornado
2. **Cache Layer**: Redis
3. **Persistent Data Storage**: MySQL/MongoDB

### Error Codes
The service should return appropriate HTTP status codes:
- 200's on successful requests
- 400's on client errors
- 500's on server errors

## Component Diagram
![Component Diagram](/component%20diagram.png)

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

## Extension
