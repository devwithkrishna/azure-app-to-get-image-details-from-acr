# base image python 3.11 debian12
FROM python:3.11-slim-bookworm
# label
LABEL maintained-by="githubofkrishnadhas"
# setting workdir
WORKDIR /app
# copying files
COPY . /app/
# package updations and installations
RUN apt-update && pip install --upgrade pip && apt install poetry -y && chmod +x entrypoint.sh
# code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/app/entrypoint.sh"]