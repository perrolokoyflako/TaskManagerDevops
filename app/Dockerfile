#########################  STAGE 1 BUILD  #############################
#Image python pour installer dependances. AS (multistage builder) 
FROM python:3.12-slim AS builder
#Working directory
WORKDIR /app
#Copier requirements file en 1er. Optimisation cache docker. 
#Docker réutilise cette couche sans réinstaller les dépendances.
COPY requirements.txt .
# Installer les dépendances dans /install (dossier isolé pour copie finale).Pas de cache pip.  
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
######################### STAGE 2 IMAGE FINALE ########################
#Image propre sans outils de build, legere.
FROM python:3.12-slim
#metadonee de l'image
LABEL maintainer="B3SR DevOps Project"
LABEL description="Task Manager API"
#Decalration creation user non-root
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app
#Copier les dependances installes en stage 1. uniquement le necessaire.
COPY --from=builder /install /usr/local
#Copy code source
COPY app.py .
#Donner ownership à user non-root
RUN chown -R appuser:appuser /app
#Basculer vers l'utilisateur non-root pour l'exécution
USER appuser
EXPOSE 5000
#Verif santé de l'app chaque 30 sec, 3 verifs. Utilisation dependante de status healthy
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"
#Start Gunicorn server. 2 processus paralleles.  
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
