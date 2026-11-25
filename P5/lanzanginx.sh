#!/bin/bash
docker run --rm -d --name nginx -p 80:80 -v $(pwd)/html:/usr/share/nginx/html nginx