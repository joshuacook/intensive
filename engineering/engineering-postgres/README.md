# Postgres with GIS

This system makes use of Docker Compose to build a system linking Jupyter to a PostgreSQL database with the PostGIS tools installed. 

## Bio and Contact

Developed by Joshua Cook:

- http://joshuacook.me
- [Twitter](https://twitter.com/joshuacook)
- [Github](https://github.com/joshuacook)
- [LinkedIn](https://www.linkedin.com/in/joshuapaulcook/)
- [Apress](https://www.apress.com/us/book/9781484230114)
- [UCLA Extension Data Science Certificate](https://www.uclaextension.edu/specialtyprogram/landingPage.do?method=load&specialtyProgramId=196400770)

## Install Docker Compose

### Install Compose on macOS
Docker for Mac and Docker Toolbox already include Compose along with other Docker apps, so Mac users do not need to install Compose separately. Docker install instructions for these are here:

- [Get Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
- [Get Docker Toolbox (for older systems)](https://docs.docker.com/toolbox/overview/)

### Install Compose on Windows systems

Docker for Windows and Docker Toolbox already include Compose along with other Docker apps, so most Windows users do not need to install Compose separately. Docker install instructions for these are here:

- [Get Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
- [Get Docker Toolbox (for older systems)](https://docs.docker.com/toolbox/overview/)

### Install Compose on Linux

On Linux, you can download the Docker Compose binary from the [Compose repository release page on GitHub](https://github.com/docker/compose/releases). Follow the instructions from the link, which involve running the curl command in your terminal to download the binaries. These step by step instructions are also included below.

Run this command to download the latest version of Docker Compose:

```
sudo curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```

Use the latest Compose release number in the download command.

The above command is an example, and it may become out-of-date. To ensure you have the latest version, check the Compose repository release page on GitHub.

Apply executable permissions to the binary:

```
sudo chmod +x /usr/local/bin/docker-compose
```

Test the installation.

```
$ docker-compose --version
docker-compose version 1.19.0, build 1719ceb
```

## Using the PostGIS System

To launch the system, run

```bash
$ docker-compose up -d
```

The `docker-compose.yml` file defines a Docker Volume. The first time that this command is run, the volume will be created. The volume is attached to the Postgres container and is used to persist database data.

To check the system's status, run

```bash
$ docker-compose ps
```

To bring the system down, run 

```bash
$ docker-compose down
```

### Authentication

This system has a default password of `geojupyter`. To specify an alternative password, first generate a hashed version of your desired password

```python
>>> from IPython.lib import passwd
>>> passwd(#YOURPASSWORD#)
sha1:93e8ffee1b39:6cce61498112b850ebcb1027df57fc1a5f4bd99e
```

then add this to the `docker-compose.yml` file as the argument passed to the Jupyter service

```
    jupyter:
        build: docker/jupyter
        ports:
            - 80:8888
        volumes:
            - .:/home/jovyan
        command: ["start-notebook.sh", "--NotebookApp.password='sha1:93e8ffee1b39:6cce61498112b850ebcb1027df57fc1a5f4bd99e'"]
```


## The Project Root Design Pattern

The `docker-compose.yml` file mounts the root of this project to `/home/jovyan` within the Docker conatainer. For purposes of organization we will keep all of our notebooks in the `ipynb` directory and all of our Python modules in the `lib` directory. In order to reference the code library, however, we must be able to refer to it. This must be done from the project root. 

In order to do this, we will use the *Project Root Design Pattern*.

In each Jupyter Notebook, from which we wish to refer to the library, we will use the following code:

```python
cd /home/jovyan
```

Running that code in a notebook will make `/home/jovyan` our working directory. From there, we can refer to modules in the library as

```python
from lib.sample_module import sample_func
import lib.other_module as om
```
