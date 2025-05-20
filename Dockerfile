FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Installer les dépendances système
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    unzip \
    ca-certificates \
    fontconfig \
    libfreetype6 \
    fonts-dejavu-core \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer Micromamba
RUN mkdir -p /usr/local/bin \
    && curl -Ls "https://micro.mamba.pm/api/micromamba/linux-64/latest" \
    | tar -xj -C /usr/local/bin --strip-components=1 bin/micromamba \
    && chmod +x /usr/local/bin/micromamba

# Créer un environnement Python
RUN micromamba create -y -p /opt/venv python=3.9.0 -c conda-forge

# Installer les bibliothèques Python
RUN micromamba run -p /opt/venv python -m pip install --upgrade pip \
    && micromamba run -p /opt/venv pip install \
    torch \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

# Créer le répertoire /app/src et copier les fichiers
RUN mkdir -p /app/src
COPY src/dcgan_generator.pth /app/src/dcgan_generator.pth
COPY src/app.py /app/app.py

# Définir les variables d'environnement
ENV PATH=/opt/venv/bin:$PATH
ENV HOME=/app

# Définir le point d'entrée
ENTRYPOINT ["python3", "/app/app.py"]