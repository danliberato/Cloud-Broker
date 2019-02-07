# Cloud Broker

This simple project is intended to apply the Cloud Broker (CB) concepts.
There are 3 main features:
* Disclosure of resources by providers;
* Resource request in the Cloud Broker by clients;
    * CB will always select the most cheap resource that matches with the client request;
* Use of resource in providers;

Definitions:
* Resources: Virtual Machines (VM);
* VM: represented by a tuple in a table (vCPUs, RAM, Storage, price, isAvaliable, provider Name, providerAP);
* Provider: A client from CB, a server for the client;
    * Controls clients requests, releases/reserves VMs, redirect client to a selected Provider;
* Client: consumes Provider resources by requesting it to the CB;

You might know:
Multithreaded server/client sockets.
### Installation
```sh
$ 	apt-get install python3
$	apt-get install python3-setuptools
$	python3 -m pip install wheel
$	python3 -m pip install awscli
$	python3 -m pip install boto3
```

### New here?
Some of the links that I have used for this little project.

| Issue? | Link |
| ------ | ------ |
| DynamoDB Create Table | [Here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html) |
| Boto3 Docs | [Here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html) |
| Run EC2, DynamoDB, IAM | [Here](https://www.youtube.com/watch?v=WE303yFWfV4) |


### Development

Want to contribute? Nice!
Feel free to to add new features or even improve my work with you knowledge.

### Configs
Verify the configs. It, by default, runs at 8888 port.

```sh
127.0.0.1:8888
```

### ToDos

 - When a VM get modified the provider must update both BC and client about (it's already done in the table);
 - Improve management by adding a better "interface";

# Workflow
![Alt text](https://i.imgur.com/WjJGPl6.png)

# License
----
MIT

# md
[Made with Dillinger](https://dillinger.io/)