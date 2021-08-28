# Installing Redis on EC2 Instance

## Cretae a new EC2 instance

## SSH into the instance

```
sudo apt-get upgrade
sudo apt-get install redis-server

```

## Enable redis on System Boot

```
sudo systemctl enable redis-server
```

## Start redis

```
sudo systemctl start redis-server
redis-cli
```

## Check if Redis is working

```
redis-cli ping
```

[Refer this link](https://www.youtube.com/watch?v=acW0B_DyMGQ)
