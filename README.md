# TP Docker – Application Items

## Description
Application conteneurisée composée de trois services :  
- **API** (Flask) avec routes `/status` et `/items` pour gérer des items.  
- **Base de données** PostgreSQL avec persistance via volume.  
- **Front-end** statique (HTML/JS) pour afficher, ajouter et supprimer des items.

## Lancement
1. Cloner le dépôt :  
```bash
git clone <URL_DU_DEPOT>
cd TP_DOCKER_API
