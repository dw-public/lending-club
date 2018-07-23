SHELL := /bin/bash

CONTAINER_NAME := scipy-notebook
DIR := ${CURDIR}

.PHONY: start_nb
start_nb:
	docker run -it --entrypoint="/bin/bash" --name $(CONTAINER_NAME) -p 10000:8888  \
	--mount type=bind,source="$(DIR)",destination=/home/jovyan/lending_club \
	jupyter/scipy-notebook:latest
