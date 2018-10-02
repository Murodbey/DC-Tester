# Welcome to DC-Tester Web Source
Please follow the steps for creating load balancer and build the DC-Tester
```
git clone https://github.com/farkhodsadykov/DC-Tester.git
cd DC-Tester
docker-compose config # To see
```

## Build  the docker environment
```
docker-compose build
```

![](https://github.com/farkhodsadykov/DC-Tester/blob/master/pictures/Screen%20Shot%202018-10-01%20at%208.19.17%20PM.png)

## Start all Services and run docker environment in deamon mode
```
docker-compose -d up
```
![](https://github.com/farkhodsadykov/DC-Tester/blob/master/pictures/Screen%20Shot%202018-10-01%20at%208.21.11%20PM.png)

## Creating 10 scale (10 dctester containers)
```
docker-compose scale dctester=10
```
![](https://github.com/farkhodsadykov/DC-Tester/blob/master/pictures/Screen%20Shot%202018-10-01%20at%208.29.46%20PM.png)

[localhost](http://localhost/)

![](https://github.com/farkhodsadykov/DC-Tester/blob/master/pictures/Screen%20Shot%202018-10-01%20at%208.32.50%20PM.png)

Everything Works :)
