# Base Image
FROM python:3.13.5-bookworm


# Temporary
ARG GID=3333
ARG UID=$GID


# If the steps of a `Dockerfile` use files that are different from the `context` file, COPY the
# file of each step separately; and RUN the file immediately after COPY
WORKDIR /app
COPY .devcontainer/requirements.txt /app


# Environment
SHELL [ "/bin/bash", "-c" ]


RUN groupadd --system automata --gid $GID && \
    useradd --system automaton --uid $UID --gid $GID && \
    apt update && apt -q -y upgrade && apt -y install sudo && sudo apt -y install graphviz && \
    sudo apt -y install wget && sudo apt -y install curl && sudo apt -y install unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
    unzip /tmp/awscliv2.zip -d /tmp/ && cd /tmp && sudo ./aws/install && cd ~ && \
    pip install --upgrade pip && \
    pip install --requirement /app/requirements.txt --no-cache-dir && \
    mkdir /app/warehouse && \
    chown -R automaton:automata /app/warehouse


# Specific COPY
COPY src /app/src
COPY config.py /app/config.py


# Port
EXPOSE 8050


# Create mountpoint
VOLUME /app/warehouse


# automaton
USER automaton


# ENTRYPOINT
ENTRYPOINT ["python"]


# CMD
CMD ["src/main.py"]