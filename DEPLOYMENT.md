# Choix de Déploiement — Justification Technique

## Environnement cible

L'application est déployée sur une machine virtuelle **Azure VM B1s**
(Ubuntu 24.04 LTS) via.

---

## Justification des choix techniques

### Pourquoi Docker et Docker Compose ?

Docker garantit que l'application fonctionne de façon identique en
développement et en production. Sans Docker, chaque serveur nécessite
une configuration manuelle (versions Python, dépendances, variables
système) — source d'erreurs et de différences d'environnement.

Docker Compose permet d'orchestrer plusieurs conteneurs (API + base de
données) avec un seul fichier de configuration et une seule commande
de démarrage : `docker compose up -d`.

### Pourquoi Flask + Gunicorn ?

Flask est un micro-framework Python léger, idéal pour construire des
API REST. Le serveur de développement Flask intégré ne gère qu'une
requête à la fois — inadapté à la production. Gunicorn est un serveur
WSGI de production qui gère plusieurs workers en parallèle, garantissant
la disponibilité sous charge.

### Pourquoi PostgreSQL ?

PostgreSQL est un système de gestion de base de données relationnelle
open-source, robuste et largement utilisé en production. La version
Alpine (postgres:16-alpine) est utilisée pour minimiser la taille de
l'image Docker.

### Pourquoi Azure VM plutôt qu'un service managé ?

Une VM offre un contrôle total sur l'environnement d'exécution et
permet de démontrer l'ensemble du processus DevOps : configuration
du serveur, installation de Docker, déploiement des conteneurs,
ouverture des ports réseau. Un service managé (ex: Azure App Service)
abstrairait ces étapes et réduirait la valeur pédagogique du projet.

### Pourquoi un build multi-stage dans le Dockerfile ?

Le build multi-stage sépare la phase de construction (avec pip et les
outils de compilation) de la phase d'exécution. L'image finale ne
contient que le strict nécessaire — réduisant la taille et la surface
d'attaque. Résultat : image de production légère sans outils inutiles.

### Pourquoi un utilisateur non-root ?

Par défaut, les processus dans un conteneur Docker s'exécutent en tant
que root. En cas de compromission de l'application, l'attaquant
obtiendrait des droits administrateur. L'utilisateur `appuser` limite
les droits au strict minimum nécessaire — principe du moindre privilège.

### Pourquoi un volume nommé pour PostgreSQL ?

Sans volume, les données de la base de données sont stockées dans le
conteneur. La suppression du conteneur entraîne la perte de toutes les
données. Un volume nommé (`postgres_data`) persiste indépendamment du
cycle de vie des conteneurs — les données survivent aux redémarrages
et aux mises à jour.

### Pourquoi les variables d'environnement via .env ?

Les secrets (mots de passe, noms de base de données) ne doivent jamais
être écrits directement dans le code ou les fichiers de configuration
versionnés. Le fichier `.env` est exclu de Git via `.gitignore`. Le
fichier `.env.example` documente les variables nécessaires sans exposer
les valeurs réelles.

---

## Architecture de déploiement
```
INTERNET
    │
    │ Port 5000 ouvert (règle Azure Network Security Group)
    ▼
Azure VM — Ubuntu 24.04 LTS (20.251.146.73)
    │
    │ Docker mappe host:5000 → conteneur:5000
    ▼
Conteneur taskmanager_api (Flask + Gunicorn)
    │
    │ Réseau bridge Docker (taskmanager_network)
    │ Hostname "db" résolu automatiquement par Docker DNS
    ▼
Conteneur taskmanager_db (PostgreSQL 16 Alpine)
    │
    │ Volume Docker monté
    ▼
Volume postgres_data (stocké sur le disque de la VM)
```

---

## Reproductibilité

Le déploiement complet depuis zéro nécessite uniquement :

1. Une VM Ubuntu 24.04 avec Docker installé
2. Le dépôt GitHub : `git clone https://github.com/perrolokoyflako/TaskManagerDevops.git`
3. Un fichier `.env` basé sur `.env.example`
4. La commande : `docker compose up -d`

Ce processus a été validé sur deux VMs Azure distinctes.
