# docker
A collection of docker related scripts.

1. MySQL Client
Use this to run a docker container and connect to a remote mysql server.
- create a .my.cnf in this format:
    ``` 
    [client]
    user=''
    password=''
    host=''
    port=3306
    ```
- docker compose -f mysql.yaml up -d
- docker compose exec mysql-client mysql


