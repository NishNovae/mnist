# mnist

- [x] GET method file upload
- [x] SQL INSERT queries
- [ ] MNIST based on database

### Development settings
- Run uvicorn fastAPI server
```bash
$ uvicorn src.mnist.main:app --reload
```

- Use `run.sh` bash file from `/src/mnist/` to run docker process

### Docker 
```bash
sudo docker run -d --name mnist10 \
-e LINE_NOTI_TOKEN=<MY_LINE_TOKEN> \
-e DB_IP=172.17.0.1 -e DB_PORT=53306 \
-v /home/ubuntu/images:/home/ubuntu/images \
-e UPLOAD_DIR=/home/ubuntu/images/n10 \
-p 8010:8080 say7777/mnist
```
