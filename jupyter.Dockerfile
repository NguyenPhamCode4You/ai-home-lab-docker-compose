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

# Install Python packages for Machine Learning
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    scikit-learn \
    tensorflow \
    keras \
    torch \
    torchvision \
    jupyterlab \
    nltk \
    opencv-python \
    pillow \
    h5py \
    tqdm \
    requests \
    transformers \
    sentencepiece \
    tensorflow-text \
    tfa-nightly \
    ollama \
    unsloth

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

# Install Unsloth
RUN pip install --no-cache-dir unsloth
RUN pip install --no-cache-dir tf_keras
# RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /home/jovyan

# Expose Jupyter notebook port
EXPOSE 8888

# Start JupyterLab
CMD ["start-notebook.sh"]
