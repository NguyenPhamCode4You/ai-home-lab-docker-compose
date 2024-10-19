# syntax=docker/dockerfile:1
FROM quay.io/jupyter/base-notebook

# Switch to root user to install packages
USER root

# Install common tools and build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    python3-pip \
    g++ \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install C++ and Machine Learning dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gdb \
    clang \
    libboost-all-dev \
    libeigen3-dev \
    libopenblas-dev \
    liblapack-dev \
    libgtest-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# RUN curl -fsSL https://ollama.com/install.sh | sh

COPY ./requirements.txt /home/jovyan/requirements.txt

# Set working directory
WORKDIR /home/jovyan

# Install Python packages
RUN pip install -r requirements.txt

COPY ./unsloth /home/jovyan/unsloth
WORKDIR /home/jovyan/unsloth
RUN pip install "unsloth[colab-new]"
RUN pip install --no-deps trl peft accelerate bitsandbytes

# Set working directory
WORKDIR /home/jovyan

# Expose Jupyter notebook port
EXPOSE 8888

# Start JupyterLab
CMD ["start-notebook.sh"]
