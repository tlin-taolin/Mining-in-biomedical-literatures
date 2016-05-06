# Usage
## Manual
### Without mongo
```bash
sudo docker run --rm -it -v "$(pwd):/home/tlin/notebooks" itamtao/scrapy /bin/zsh
```

### With mongo
```bash
sudo docker run -v "$(pwd)"/db:/data --name mongodb -d mongo mongod --smallfiles
sudo docker run -it --name crawl -v "$(pwd)":/home/tlin/notebooks --link mongodb:mongodb itamtao/scrapy-mongo zsh
```

## Automatic
```bash
./.build
./.run
```
