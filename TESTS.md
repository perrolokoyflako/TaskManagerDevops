# Tests et Validation — Task Manager API

Ce document recense tous les tests effectués sur l'API,
en local et en production sur Azure.

---

## Environnements testés

| Environnement | URL de base | Statut |
|---------------|-------------|--------|
| Local (VM Azure) | http://localhost:5000 | Validé |
| Production (Azure public) | http://20.251.146.73:5000 | Validé |

---

## 1. Test de santé (Health Check)

Vérifie que l'API est démarrée et répond correctement.
```bash
curl http://localhost:5000/health
```

Réponse attendue :
```json
{"status": "ok"}
```

Résultat : ####

---

## 2. Créer une tâche (POST /tasks)

Vérifie la création d'une nouvelle tâche avec tous les champs.
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "NFL Fantasy Draft", "description": "Preparer les top 25", "priority": "medium"}'
```

Réponse attendue (HTTP 201) :
```json
{
  "id": 1,
  "title": "NFL Fantasy Draft",
  "description": "Preparer les top 25",
  "done": false,
  "priority": "medium"
}
```

Résultat : ####

---

## 3. Lister toutes les tâches (GET /tasks)

Vérifie que les tâches créées sont bien stockées et récupérables.
```bash
curl http://localhost:5000/tasks
```

Réponse attendue (HTTP 200) :
```json
[
  {
    "id": 1,
    "title": "NFL Fantasy Draft",
    "description": "Preparer les top 25",
    "done": false,
    "priority": "medium"
  }
]
```

Résultat : ####
---

## 4. Récupérer une tâche par ID (GET /tasks/:id)

Vérifie qu'on peut récupérer une tâche spécifique.
```bash
curl http://localhost:5000/tasks/1
```

Réponse attendue (HTTP 200) :
```json
{
  "id": 1,
  "title": "NFL Fantasy Draft",
  "description": "Preparer les top 25",
  "done": false,
  "priority": "medium"
}
```

Résultat : ####
---

## 5. Modifier une tâche (PATCH /tasks/:id)

Vérifie qu'on peut marquer une tâche comme terminée.
```bash
curl -X PATCH http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

Réponse attendue (HTTP 200) :
```json
{
  "id": 1,
  "title": "NFL Fantasy Draft",
  "description": "Preparer les top 25",
  "done": true,
  "priority": "medium"
}
```

Résultat : ####

---

## 6. Filtrer les tâches (GET /tasks?done=false)

Vérifie que le filtre par statut fonctionne.
```bash
curl http://localhost:5000/tasks?done=false
```

Réponse attendue : liste des tâches non terminées uniquement.

Résultat : ####

---

## 7. Obtenir les statistiques (GET /stats)

Vérifie que l'endpoint de statistiques calcule correctement.
```bash
curl http://localhost:5000/stats
```

Réponse attendue (HTTP 200) :
```json
{
  "done": 1,
  "high_priority_pending": 0,
  "pending": 0,
  "total": 1
}
```

Résultat : ####

---

## 8. Supprimer une tâche (DELETE /tasks/:id)

Vérifie qu'une tâche peut être supprimée.
```bash
curl -X DELETE http://localhost:5000/tasks/1
```

Réponse attendue (HTTP 200) :
```json
{"message": "Task 1 deleted"}
```

Résultat : ####

---

## 9. Validation des erreurs

Vérifie que l'API retourne des erreurs appropriées.

**Créer une tâche sans titre :**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"description": "sans titre"}'
```

Réponse attendue (HTTP 400) :
```json
{"error": "title is required"}
```

Résultat : ####

**Priorité invalide :**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "priority": "urgent"}'
```

Réponse attendue (HTTP 400) :
```json
{"error": "priority must be low, medium or high"}
```

Résultat : ####

---

## 10. Test de persistance des données

Vérifie que les données survivent à un redémarrage des conteneurs.
```bash
# Créer une tâche
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test persistance", "priority": "high"}'

# Redémarrer les conteneurs
docker compose down
docker compose up -d

# Vérifier que la tâche est toujours là
curl http://localhost:5000/tasks
```

Réponse attendue : la tâche créée avant le redémarrage est toujours présente.

Résultat : ####

---

## 11. Test d'accessibilité publique

Vérifie que l'API est accessible depuis l'extérieur du serveur.
```bash
curl http://20.251.146.73:5000/health
```

Réponse attendue :
```json
{"status": "ok"}
```

Résultat : ####
---

## Récapitulatif

| Test | Endpoint | Résultat |
|------|----------|----------|
| Health check | GET /health | PASS |
| Créer une tâche | POST /tasks | PASS |
| Lister les tâches | GET /tasks | PASS |
| Récupérer par ID | GET /tasks/:id | PASS |
| Modifier une tâche | PATCH /tasks/:id | PASS |
| Filtrer les tâches | GET /tasks?done=false | PASS |
| Statistiques | GET /stats | PASS |
| Supprimer une tâche | DELETE /tasks/:id | PASS |
| Validation erreurs | POST /tasks | PASS |
| Persistance données | redémarrage conteneurs | PASS |
| Accessibilité publique | GET /health (IP publique) | PASS |
