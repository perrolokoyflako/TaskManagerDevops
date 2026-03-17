# Task Manager API — Projet DevOps B3 SR

Une API REST de gestion de tâches, construite avec **Flask** et **PostgreSQL**, entièrement conteneurisée avec **Docker** et **Docker Compose**, déployée sur **Microsoft Azure**.

> SUP DE VINCI — 2025/2026 — B3 SR

---

## Architecture
```
┌─────────────────────────────────────────────┐
│              Docker Compose                 │
│                                             │
│  ┌──────────────┐      ┌─────────────────┐  │
│  │  Flask API   │─────▶│   PostgreSQL    │  │
│  │  (port 5000) │      │   (port 5432)   │  │
│  └──────────────┘      └────────┬────────┘  │
│                                 │           │
│                         postgres_data       │
│                         (volume nommé)      │
└─────────────────────────────────────────────┘
         │
    taskmanager_network (bridge)
```

- Le conteneur **API** traite toutes les requêtes HTTP (Flask + Gunicorn)
- Le conteneur **DB** stocke les données de façon persistante via un volume nommé
- Les deux conteneurs communiquent via un **réseau bridge personnalisé**
- Les secrets sont gérés via un fichier **`.env`** (jamais envoyé sur Git)
- L'API est déployée sur une **VM Azure** et accessible publiquement

---

## Démarrage rapide

### Prérequis
- [Docker](https://docs.docker.com/get-docker/) installé
- [Docker Compose](https://docs.docker.com/compose/install/) installé

### 1. Cloner le dépôt
```bash
git clone https://github.com/perrolokoyflako/TaskManagerDevops.git
cd TaskManagerDevops
```

### 2. Configurer les variables d'environnement
```bash
cp .env.example .env
# Modifier .env et définir votre propre mot de passe
```

### 3. Démarrer tous les services
```bash
docker compose up -d
```

### 4. Vérifier que tout tourne
```bash
docker compose ps
```

### 5. Tester l'API
```bash
curl http://localhost:5000/health
# → {"status": "ok"}
```

---

## Démo en ligne

L'API est accessible publiquement à l'adresse :
```
http://20.251.146.73:5000
```

---

## Endpoints de l'API

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/health` | Vérification de l'état |
| GET | `/tasks` | Lister toutes les tâches |
| GET | `/tasks/:id` | Récupérer une tâche |
| POST | `/tasks` | Créer une tâche |
| PATCH | `/tasks/:id` | Modifier une tâche |
| DELETE | `/tasks/:id` | Supprimer une tâche |
| GET | `/stats` | Statistiques des tâches |

### Exemples de requêtes

**Créer une tâche :**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Ma tâche", "description": "Détails ici", "priority": "high"}'
```

**Marquer une tâche comme terminée :**
```bash
curl -X PATCH http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

**Obtenir les statistiques :**
```bash
curl http://localhost:5000/stats
```

---

## Commandes utiles
```bash
# Démarrer en arrière-plan
docker compose up -d

# Voir les logs
docker compose logs -f

# Arrêter tout
docker compose down

# Réinitialisation complète (supprime la base de données)
docker compose down -v

# Reconstruire après modification du code
docker compose up -d --build
```

---

## Structure du projet
```
TaskManagerDevops/
├── app/
│   ├── app.py              # Application Flask (routes + modèles)
│   ├── requirements.txt    # Dépendances Python
│   ├── Dockerfile          # Build Docker multi-stage
│   └── .dockerignore       # Fichiers exclus de l'image
├── docker-compose.yml      # Orchestration des services
├── .env                    # Variables d'environnement (PAS sur Git)
├── .env.example            # Modèle pour le .env
├── .gitignore
└── README.md
```

---

## Sécurité

- L'application tourne en tant qu'**utilisateur non-root** dans le conteneur
- Les secrets sont dans `.env`, exclu de Git via `.gitignore`
- Le port de la base de données **n'est pas exposé** publiquement — uniquement l'API
- Un **healthcheck** est configuré sur les deux conteneurs
