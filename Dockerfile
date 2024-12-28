FROM ubuntu:latest
LABEL authors="patry"

ENTRYPOINT ["top", "-b"]