# EquipIT

**EquipIT** est une application web Django et API REST conçue pour la consultation, l'emprunt et la restitution de matériel informatique d'entreprise.

Ce projet s'inscrit dans le cadre du **Projet 3 du parcours Développeur Full-Stack Back-end Avancé (Python/Django)** d'OpenClassrooms. Il met en œuvre une architecture logicielle robuste en couches découplées (Modèles, Services métier, Serializers, Vues) développée selon une approche rigoureuse de **développement dirigé par les tests (TDD)** avec une couverture de code intégrale.

---

## 📋 Prérequis

- **Python 3.14+**
- **uv** (gestionnaire de packages et d'environnements virtuels)
- **SQLite 3** (utilisé automatiquement pour le développement local)
- **PostgreSQL 18** (environnement de production cible via variable `DATABASE_URL`)

---

## 🚀 Installation et initialisation

1. **Cloner le projet et synchroniser l'environnement virtuel :**
   ```bash
   uv sync
   ```

2. **Configurer l'environnement :**
   ```bash
   cp .env.example .env
   ```

3. **Appliquer les migrations de base de données :**
   ```bash
   uv run python manage.py migrate
   ```

4. **Créer un compte administrateur :**
   ```bash
   uv run python manage.py createsuperuser
   ```

---

## ▶️ Démarrage de l'application

Lancez le serveur de développement local :
```bash
uv run python manage.py runserver
```

L'application est alors accessible sur `http://127.0.0.1:8000/`.

---

## 🖥️ Interfaces disponibles

- **Interface d'administration Django :** [`http://127.0.0.1:8000/admin/`](http://127.0.0.1:8000/admin/)  
  Permet aux administrateurs de gérer le parc matériel (ajout, édition, suppression d'équipements).
- **Documentation interactive Swagger UI :** [`http://127.0.0.1:8000/docs/`](http://127.0.0.1:8000/docs/)  
  Permet d'explorer et de tester directement tous les endpoints de l'API.
- **Schéma OpenAPI :** [`http://127.0.0.1:8000/schema/`](http://127.0.0.1:8000/schema/)  
  Spécification OpenAPI 3 brute générée dynamiquement par `drf-spectacular`.

---

## 📡 API REST

L'API fournit trois endpoints principaux sous le préfixe `/api/` :

| Méthode | Endpoint | Description | Réponses HTTP |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/equipment/` | Liste tous les équipements du parc et leur statut de disponibilité | `200 OK` |
| `PUT` | `/api/equipment/<id>/borrow/` | Emprunte un équipement disponible en renseignant l'identité de l'emprunteur | `200 OK`<br>`400 Bad Request`<br>`404 Not Found` |
| `PUT` | `/api/equipment/<id>/return/` | Restitue un équipement actuellement emprunté | `200 OK`<br>`400 Bad Request`<br>`404 Not Found` |

### Détail des requêtes d'action

#### 1. Emprunter un matériel : `PUT /api/equipment/<id>/borrow/`
- **Corps de la requête (JSON) :**
  ```json
  {
    "first_name": "Fabrice",
    "last_name": "MAILLOT"
  }
  ```
- **Comportement métier :**
  - Vérifie l'existence de l'équipement (`404` si introuvable).
  - Valide les champs obligatoires (`400` si vides ou dépassant 80 caractères).
  - Vérifie que l'équipement est disponible (`400` si déjà emprunté).
  - Met à jour le statut (`is_available = False`), enregistre l'emprunteur et horodate l'emprunt (`borrowed_at = now()`, `returned_at = null`).

#### 2. Restituer un matériel : `PUT /api/equipment/<id>/return/`
- **Corps de la requête :** Aucun body requis.
- **Comportement métier :**
  - Vérifie l'existence de l'équipement (`404` si introuvable).
  - Vérifie que l'équipement était bien emprunté (`400` si déjà disponible).
  - Met à jour le statut (`is_available = True`) et horodate le retour (`returned_at = now()`).

---

## 🏗️ Architecture du projet

Le projet adopte une séparation stricte des responsabilités (architecture en couches) :

```text
├── config/                  # Configuration du projet Django, settings et routage racine
├── equipment/               # Application principale de gestion du matériel
│   ├── models.py            # Modèle persistant Equipment (ORM Django)
│   ├── services.py          # Logique métier pure (EquipmentService, transactions atomiques, exceptions)
│   ├── serializers.py       # Validation et sérialisation DRF (EquipmentSerializer, BorrowRequestSerializer)
│   ├── views.py             # Couche API HTTP (EquipmentListView, EquipmentBorrowView, EquipmentReturnView)
│   ├── urls.py              # Routage dédié de l'application equipment
│   ├── admin.py             # Enregistrement du modèle dans l'administration Django
│   └── tests/               # Suite de tests automatisés (TDD)
│       ├── test_models.py       # Tests unitaires du modèle de données
│       ├── test_serializers.py  # Tests unitaires de validation des serializers
│       ├── test_services.py     # Tests unitaires des opérations métier
│       └── test_views.py        # Tests d'intégration des endpoints de l'API
├── templates/               # Modèles de vues HTML
├── pyproject.toml           # Gestion des dépendances uv, configuration pytest, coverage et ruff
└── journalAI.md             # Journal d'audit et historique des interactions d'assistance IA
```

---

## 🧪 Tests, qualité de code et couverture

Le développement a été conduit selon la méthodologie **TDD (Test-Driven Development)**, garantissant la conformité de chaque couche logicielle avant son intégration.

### Exécuter la suite de tests

Pour lancer les tests automatisés avec rapport de couverture complet :
```bash
uv run pytest
```

Pour générer les résultats compatibles avec les rapports **Allure** :
```bash
uv run pytest --alluredir=allure-results
```

### Couverture de code (`pytest-cov`)

La suite de tests comprend **23 tests automatisés** et assure une couverture intégrale de l'application :

```text
Name                       Stmts   Miss Branch BrPart  Cover
------------------------------------------------------------
equipment/admin.py             3      0      0      0   100%
equipment/apps.py              4      0      0      0   100%
equipment/models.py           13      0      0      0   100%
equipment/serializers.py       9      0      0      0   100%
equipment/services.py         36      0      4      0   100%
equipment/urls.py              3      0      0      0   100%
equipment/views.py            43      0      0      0   100%
------------------------------------------------------------
TOTAL                        111      0      4      0   100%
```

Un rapport HTML interactif détaillé est également disponible dans le dossier `htmlcov/index.html`.

### Vérification du style et linting (`ruff`)

Le projet respecte les standards PEP 8 et les règles de qualité du linter **Ruff** :
```bash
uv run ruff check .
```

---

## 📄 Licence

Ce projet est distribué sous la licence [MIT](LICENSE).
