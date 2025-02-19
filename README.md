# pethaul_api

```markdown
# Projet DevOps - Pipeline Jenkins pour PetHaul

**Responsable du cours**: Mofiala Hervé LOKOSSOU  
**Date**: 19 Février 2025  
**Durée**: 72h  

---

## Contexte
PetHaul, spécialisée dans l'élevage et le recueil d'animaux abandonnés, dispose d'une application Python pour identifier les animaux. Ce projet vise à mettre en place un pipeline Jenkins CI/CD pour déployer une stack AWS (API Gateway, Lambda, DynamoDB) avec AWS SAM.

---

## Instructions Techniques

### Structure des Répertoires
- Backend : `IABD-EVAL/votre_username/pethaul_api`
- Frontend : `IABD-EVAL/votre_username/pethaul_front`
- Langage : Python 3.12 pour les deux projets.

### Composants AWS
- Utilisation d'AWS SAM pour le déploiement.
- Création d'un bucket S3 avec convention de nommage : `pethaul-bucket-<env>-<username>`.
- Récupération de l'API_KEY Mistral AI pour le backend via les credentials Jenkins.

---

## Étapes du Pipeline Jenkins

### Jenkinsfile Requirements
1. **Stages Parallèles** :
   - Validation du template CloudFormation.
   - Exécution des tests unitaires.
   - (Bonus) Revue du code (lint).

2. **Environnement** :
   - Génération d'un fichier `.env` à partir des credentials Jenkins (AWS, Mistral AI).

3. **Intégration Frontend/Backend** :
   - Récupération de l'URL de l'API Gateway via la commande `show-results` dans le Makefile.
   - Implémentation d'une méthode GET `/chats` pour récupérer les données depuis DynamoDB.

### Commandes Makefile
```makefile
show-results:
    aws cloudformation describe-stacks \
        --stack-name "pethaul-stack-${env}" \
        --region ${AWS_REGION} \
        --query 'Stacks[0].Outputs[?OutputKey==`DynamoDBTableName`].OutputValue' --output text
    aws cloudformation describe-stacks \
        --stack-name "pethaul-stack-${env}" \
        --region ${AWS_REGION} \
        --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text
```

---

## Soumission du Projet

### Éléments à Fournir
- **Fichiers** : `Jenkinsfile` (backend/frontend).
- **Liens Git** : 
  - Repos privés avec accès en lecture pour `hervlokossou@gmail.com` (HTagPersistence).
  - Documentation des commandes du Bot Telegram sur la GitHub Page.
- **Captures d'écran Jenkins** :
  - Interface des jobs.
  - Liste des exécutions (succès/échec).
- **Identifiant Telegram Bot** : À inclure dans l'e-mail.

⏰ **Date Limite** : 1er Mars 2025 à 23h59.  
📧 **Envoi** : hervlokossou@gmail.com avec sujet `[IABD-EVAL] DevOps - <Votre Username>`.

---

## Critères d'Évaluation
- Qualité de la chaîne CI/CD (tests, gestion des credentials, types de jobs).
- Respect des conventions de nommage (pénalités en cas de non-respect).
- Gestion des erreurs et logs explicites.
- Intégration frontend/backend fonctionnelle.

⚠️ **Alerte Plagiat** : Un outil de détection sera utilisé. En cas de reprise de code, note maximale de **9/20** avec rattrapage obligatoire.

---



**Bon Courage !** 🚀  
*« Le succès est un mauvais professeur. Il pousse les gens intelligents à croire qu’ils ne peuvent pas perdre. » – Bill Gates*
```