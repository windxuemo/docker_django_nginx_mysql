# DJANGO + Nginx + Rabbitmq + MongoDB + MySQL

## Env
* ubuntu18.04

## Install
``` shell
 sudo apt-get update
 sudo apt-get install ca-certificates curl gnupg

 sudo install -m 0755 -d /etc/apt/keyrings
 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
 sudo chmod a+r /etc/apt/keyrings/docker.gpg


echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```


## Dependence

* Docker version 24.0.2, build cb74dfc
* Docker Compose version v2.18.1

## Get Started

```
$ docker-compose up --build
```

### Development

- Main site
    - http://localhost

- Admin page
    - http://localhost/admin

### Commands
create a django app
```
$ docker exec python ./manage.py startapp {app_label}
```

create models from existing database
```
$ docker exec python ./manage.py inspectdb > {path/to/models.py}
```

execute migration
```
$ docker exec python ./manage.py migrate
```

create a migration file
```
$ docker exec python ./manage.py makemigrations
```

create dump fixture files
```
$ docker exec python ./manage.py dumpdata {app_label.model} --indent 2 > {path/to/fuxture.json}
```

load data from fixture files
```
$ docker exec python ./manage.py loaddata --verbosity 2 > {path/to/fuxture.json}
```

create an admin account
```
$ docker exec -it python ./manage.py createsuperuser
```
