FROM python:latest
LABEL authors="ilya"

COPY ./ ~/project

ENTRYPOINT ["python3", "~/project/main.py"]