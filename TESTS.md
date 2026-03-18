# Tests, Validation et Reproductibilité — Task Manager API

Ce document recense tous les tests effectués sur l'API ainsi que
la procédure complète pour reproduire le déploiement depuis zéro.

---

## Environnements testés

| Environnement | URL de base | Statut |
|---------------|-------------|--------|
| Local (VM Azure) | http://localhost:5000 | [ ] |
| Production (Azure public) | http://YOUR_VM_IP:5000 | [ ] |

---

## PARTIE 1 — Tests de l'API

### 1. Test de santé (Health Check)

Vérifie que l'API est démarrée et répond correctement.
```bash
curl http://localhost:5000/health
```

Réponse attendue :
```json
{"status": "ok"}
```

Résultat : [ ]

---

### 2. Créer une tâche (POST /tasks)

Vérifie la création d'une nouvelle tâche avec tous les champs.
```bash
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title": "Ma tâche", "description": "Description ici", "priority": "high"}'
```

Réponse attendue (HTTP 201) :
```json
{
  "id": 1,
  "title": "Ma tâche",
  "description": "Description ici",
  "done": false,
  "priority": "high"
}
```

Résultat : [ ]

---

### 3. Lister toutes les tâches (GET /tasks)

Vérifie que les tâches créées sont bien stockées et récupérables.
```bash
curl http://localhost:5000/tasks
```

Réponse attendue (HTTP 200) :
```json
[
  {
    "id": 1,
    "title": "Ma tâche",
    "description": "Description ici",
    "done": false,
    "priority": "high"
  }
]
```

Résultat : [ ]

---

### 4. Récupérer une tâche par ID (GET /tasks/:id)

Vérifie qu'on peut récupérer une tâche spécifique.
```bash
curl http://localhost:5000/tasks/1
```

Réponse attendue (HTTP 200) :
```json
{
  "id": 1,
  "title": "Ma tâche",
  "description": "Description ici",
  "done": false,
  "priority": "high"
}
```

Résultat : [ ]

---

### 5. Modifier une tâche (PATCH /tasks/:id)

Vérifie qu'on peut marquer une tâche comme terminée.
```bash
curl -X PATCH http://localhost:5000/tasks/1 -H "Content-Type: application/json" -d '{"done": true}'
```

Réponse attendue (HTTP 200) :
```json
{
  "id": 1,
  "title": "Ma tâche",
  "description": "Description ici",
  "done": true,
  "priority": "high"
}
```

Résultat : [ ]

---

### 6. Filtrer les tâches par statut (GET /tasks?done=false)

Vérifie que le filtre par statut fonctionne correctement.
```bash
curl http://localhost:5000/tasks?done=false
```

Réponse attendue : liste des tâches non terminées uniquement.

Résultat : [ ]

---

### 7. Filtrer les tâches par priorité (GET /tasks?priority=high)

Vérifie que le filtre par priorité fonctionne correctement.
```bash
curl http://localhost:5000/tasks?priority=high
```

Réponse attendue : liste des tâches avec priorité "high" uniquement.

Résultat : [ ]

---

### 8. Obtenir les statistiques (GET /stats)

Vérifie que l'endpoint de statistiques calcule correctement.
```bash
curl http://localhost:5000/stats
```

Réponse attendue (HTTP 200) :
```json
{
  "done": 0,
  "high_priority_pending": 1,
  "pending": 1,
  "total": 1
}
```

Résultat : [ ]

---

### 9. Supprimer une tâche (DELETE /tasks/:id)

Vérifie qu'une tâche peut être supprimée.
```bash
curl -X DELETE http://localhost:5000/tasks/1
```

Réponse attendue (HTTP 200) :
```json
{"message": "Task 1 deleted"}
```

Résultat : [ ]

---

### 10. Validation des erreurs

Vérifie que l'API retourne des erreurs appropriées pour les requêtes invalides.

**Créer une tâche sans titre :**
```bash
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"description": "sans titre"}'
```

Réponse attendue (HTTP 400) :
```json
{"error": "title is required"}
```

Résultat : [ ]

**Priorité invalide :**
```bash
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title": "Test", "priority": "urgent"}'
```

Réponse attendue (HTTP 400) :
```json
{"error": "priority must be low, medium or high"}
```

Résultat : [ ]

---

### 11. Test de persistance des données

Vérifie que les données survivent à un redémarrage complet des conteneurs.
```bash
# Étape 1 — Créer une tâche
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title": "Test persistance", "priority": "high"}'

# Étape 2 — Redémarrer les conteneurs (sans -v pour garder le volume)
docker compose down
docker compose up -d

# Étape 3 — Vérifier que la tâche est toujours présente
curl http://localhost:5000/tasks
```

Réponse attendue : la tâche créée avant le redémarrage est toujours présente.

Résultat : [ ]

---

### 12. Test d'accessibilité publique

Vérifie que l'API est accessible depuis l'extérieur du serveur.
```bash
curl http://YOUR_VM_IP:5000/health
```

Réponse attendue :
```json
{"status": "ok"}
```

Résultat : [ ]

---

## Récapitulatif des tests

| Test | Endpoint | Résultat |
|------|----------|----------|
| Health check | GET /health | [ ] |
| Créer une tâche | POST /tasks | [ ] |
| Lister les tâches | GET /tasks | [ ] |
| Récupérer par ID | GET /tasks/:id | [ ] |
| Modifier une tâche | PATCH /tasks/:id | [ ] |
| Filtrer par statut | GET /tasks?done=false | [ ] |
| Filtrer par priorité | GET /tasks?priority=high | [ ] |
| Statistiques | GET /stats | [ ] |
| Supprimer une tâche | DELETE /tasks/:id | [ ] |
| Validation erreurs | POST /tasks (sans titre) | [ ] |
| Validation erreurs | POST /tasks (priorité invalide) | [ ] |
| Persistance données | redémarrage conteneurs | [ ] |
| Accessibilité publique | GET /health (IP publique) | [ ] |

---

## PARTIE 2 — Reproductibilité du déploiement

Cette section documente la procédure complète pour déployer
le projet depuis zéro sur n'importe quelle VM Ubuntu 24.04.

Cette procédure a été validée sur deux VMs Azure distinctes.

---

### Prérequis

- Une VM Ubuntu 24.04 LTS (Azure VM B1s recommandé)
- Port 22 (SSH) et port 5000 ouverts dans les règles réseau Azure
- Accès SSH à la VM

---

### Étape 1 — Installer Docker
```bash
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker
```

Vérification :
```bash
docker --version
docker compose version
```

---

### Étape 2 — Installer Git
```bash
sudo apt install git -y
```

---

### Étape 3 — Cloner le dépôt
```bash
git clone https://github.com/perrolokoyflako/TaskManagerDevops.git
cd TaskManagerDevops
```

---

### Étape 4 — Créer le fichier .env
```bash
cat > .env << 'EOF'
POSTGRES_DB=taskmanager
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=VOTRE_MOT_DE_PASSE
API_PORT=5000
EOF
```

Les variables disponibles sont documentées dans `.env.example`.

---

### Étape 5 — Lancer les conteneurs
```bash
docker compose up -d
```

Docker va automatiquement :
- Télécharger l'image PostgreSQL 16 Alpine
- Construire l'image Flask depuis le Dockerfile
- Créer le réseau bridge `taskmanager_network`
- Créer le volume `postgres_data`
- Démarrer la base de données et attendre qu'elle soit prête
- Démarrer l'API une fois la base de données saine

---

### Étape 6 — Vérifier le déploiement
```bash
# Vérifier que les conteneurs tournent
docker compose ps

# Tester l'API en local
curl http://localhost:5000/health
```

Résultat attendu :
```json
{"status": "ok"}
```

---

### Étape 7 — Ouvrir le port 5000 sur Azure

Dans le portail Azure :
1. Aller sur la VM → Réseau → Paramètres réseau
2. Ajouter une règle de port entrant
3. Port : 5000 — Protocole : TCP — Action : Autoriser
4. Tester depuis l'extérieur :
```bash
curl http://YOUR_VM_IP:5000/health
```

---

### Résumé de la reproductibilité

| Étape | Commande principale | Durée estimée |
|-------|---------------------|---------------|
| Installer Docker | curl -fsSL https://get.docker.com | sudo sh | ~2 min |
| Cloner le projet | git clone ... | ~10 sec |
| Configurer .env | cat > .env | ~1 min |
| Lancer l'app | docker compose up -d | ~2 min |
| Vérifier | curl http://localhost:5000/health | ~5 sec |

Durée totale estimée : **moins de 10 minutes** depuis une VM vierge.
