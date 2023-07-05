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
3. **Persistent Data Storage**: MongoDB

### Error Codes
The service should return appropriate HTTP status codes:
- 200's on successful requests
- 400's on client errors
- 500's on server errors

## Component Diagram
![Component Diagram](/png/component%20diagram.png)

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

### 1. POST /guid or POST /guid/{guid}
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

## Bonus Points

1. Deploying Kubernetes on AWS EC2
    ### Prerequisites

    - AWS account with appropriate permissions to create EC2 instances, security groups, and other resources.
    - AWS CLI installed and configured with your AWS credentials.
    - Access to an SSH key pair for connecting to the EC2 instances.

    ### Steps to Deploy
    Apply the async-guid-app and service:
    ```bash
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```
    Check the status of the deployed resources:
    ```bash
    kubectl -n eddie-poc get all 

    NAME                                  READY   STATUS    RESTARTS   AGE
    pod/async-guid-api-6844fdb56c-fqqtx   1/1     Running   0          7m9s
    pod/async-guid-api-6844fdb56c-w6ffz   1/1     Running   0          7m9s

    NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
    service/async-guid-api   ClusterIP   172.20.214.21   <none>        80/TCP    6m47s

    NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/async-guid-api   2/2     2            2           7m10s

    NAME                                        DESIRED   CURRENT   READY   AGE
    replicaset.apps/async-guid-api-6844fdb56c   2         2         2       7m11s
    ```

    Check the node details:
    ```bash
    kubectl get node -o wide

    NAME                           STATUS   ROLES    AGE     VERSION               INTERNAL-IP    EXTERNAL-IP   OS-IMAGE         KERNEL-VERSION                  CONTAINER-RUNTIME
    ip-10-107-8-174.ec2.internal   Ready    <none>   22h     v1.25.7-eks-a59e1f0   10.107.8.174   <none>        Amazon Linux 2   5.10.173-154.642.amzn2.x86_64   containerd://1.6.6
    ip-10-107-9-141.ec2.internal   Ready    <none>   3h18m   v1.25.7-eks-a59e1f0   10.107.9.141   <none>        Amazon Linux 2   5.10.173-154.642.amzn2.x86_64   containerd://1.6.6
    ```

2. Design API using "Producer-Consumer" Pattern (Kafka)
   
   It is ideal for work that is CPU-intensive or involves substantial I/O operations.This can be particularly useful in scenarios where I want to decouple the task creation and the task execution. For example, if the creation or update of the GUID requires heavy computation or needs to be distributed across different worker instances, this approach can be very beneficial.

   ### Bounded-Buffer Component Diagram
   ![Bounded-Buffer Component Diagram](/png/kafka%20component.png)


3. What else I can do?
   - ***Implement rate limiting***: To protect the API from being overwhelmed by too many requests, I could add rate limiting functionality. e.g. Nginx, AWS API Gateway.
   - ***Enhance security***: Implement more robust security measures, such as OAuth for API authentication. Ensure encrypted connections via HTTPS.
   - ***Automated Testing***: Increase the coverage of my unit and integration tests. Implementing Continuous Integration (CI) and Continuous Deployment (CD) pipelines can also ensure that the codebase remains robust and reliable.
   - ***Utilized Stress Testing***: Testing that checks the stability and reliability of the system under extreme conditions.