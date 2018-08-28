# Docker-Compose

`docker-compose`can be installed using the instructions provided here: https://github.com/docker/compose/releases, which are written specifically for Linux machines. This consists of two steps.

You use `curl` to retrieve the `docker-compose` binary from Github. 

Listing: Retrieve `docker-compose` binary from Github

```{#lst:curl_docker_compose}
$ sudo curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```

Use the `chmod` utility to allow `docker-compose` to be executed (`+x`).

Listing: Enable Docker Compose to be Executed

```{#lst:chmod_docker-compose}
$ sudo chmod +x /usr/local/bin/docker-compose
```

Check the version of `docker-compose` against what we expect to have installed.

```{#lst:docker_compose_version}
$ docker-compose -v
docker-compose version 1.19.0, build 9e633ef
```
