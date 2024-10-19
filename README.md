## Git Clone

```sh
git clone --recurse-submodules https://github.com/NguyenPhamCode4You/ai-home-lab-docker-compose.git
```

## Complete restart

```sh
sudo docker stop $(sudo docker ps -a -q) && sudo docker rm $(sudo docker ps -a -q) && sudo docker rmi $(sudo docker images -a -q) && sudo docker volume rm $(sudo docker volume ls -q) && sudo docker network rm $(sudo docker network ls -q)
```
