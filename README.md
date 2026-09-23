# Station Météo IoT — Collecteur & API REST (SenseCAP S2120)

Système d'ingestion, de surveillance et de restitution de métriques environnementales conçu pour les stations météo LoRaWAN / MQTT de la CCI.

Le service collecte les trames de télémétrie en temps réel, assure le décodage du format hexadécimal propriétaire SenseCAP, stocke les mesures dans une base SQLite locale, déclenche des alertes e-mail automatiques en cas de dépassement de seuil critique et expose les données via une API REST sécurisée et documentée.

---

## Fonctionnalités

* **Ingestion MQTT continue** : Connexion asynchrone au broker MQTT pour écouter les topics configurés (`cci/#`).
* **Décodage de trames LoRaWAN** : Prise en charge native des payloads JSON clairs ainsi que du décodage binaire/hexadécimal (format TLV SenseCAP S2120 pour température, humidité et vitesse du vent).
* **Persistance SQLite** : Enregistrement structuré et horodaté des mesures sans dépendance de base de données externe lourde.
* **Système d'alertes SMTP** : Notification automatique par courriel lors du franchissement de seuils de température critiques (avec support SSL/TLS).
* **API REST FastAPI** : Points d'accès performants pour interroger l'historique des relevés avec documentation interactive OpenAPI intégrée.

---

## Architecture logicielle

```text
station-m-t-o-v1/
├── app/
│   ├── __init__.py
│   ├── database.py       # Initialisation SQLite et requêtes d'insertion
│   ├── main.py           # Application FastAPI et gestion du cycle de vie (lifespan)
│   ├── mqtt_client.py    # Abonnements MQTT, décodeur SenseCAP et logique métier
│   └── notifier.py       # Gestionnaire d'envois d'e-mails d'alerte (SMTP)
├── test_publish.py       # Script d'injection de trames de simulation
├── measures.db           # Fichier de base de données SQLite (généré au démarrage)
├── requirements.txt      # Dépendances Python du projet
├── .env.example          # Gabarit des variables d'environnement
└── README.md

```

---

## Prérequis

- Python version 3.10 ou supérieure.

- Un compte Google avec un mot de passe d'application généré (si utilisation d'alertes via Gmail).

- Un accès Internet pour joindre le broker MQTT (test.mosquitto.org ou broker privé).

---

## Installation

1. Cloner le projet

Bash
````
git clone [https://github.com/votre-compte/station-m-t-o-v1.git](https://github.com/votre-compte/station-m-t-o-v1.git)
cd station-m-t-o-v1

````

2. Créer et activer l'environnement virtuel

Sous Windows (PowerShell) :

PowerShell
````
python -m venv venv
.\venv\Scripts\activate

````

Bash
````
python3 -m venv venv
source venv/bin/activate
````

3. Installer les dépendances

Bash
````
pip install --upgrade pip
pip install -r requirements.txt
````

---

## Configuration (.env)

Créez un fichier nommé .env à la racine du projet en copiant le modèle ci-dessous :

Ini, TOML
````
# Configuration MQTT
MQTT_BROKER=test.mosquitto.org
MQTT_PORT=1883
MQTT_TOPIC=cci/#
MQTT_USER=
MQTT_PASSWORD=

# Seuils de surveillance
TEMP_MAX_THRESHOLD=35.0

# Configuration SMTP (Exemple Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
ALERT_RECIPIENT=destinataire-alertes@domaine.fr
````
Sécurité : Ne committez jamais votre fichier .env sur Git. Il est ignoré par défaut via le fichier .gitignore.

---

## Démarrage et utilisation

Lancer l'application complète
Démarrez le serveur FastAPI avec le rechargement automatique :

Bash
````
uvicorn app.main:app --reload
````

Au lancement, l'application :
- initialise la base de données measures.db et la table sensor_data si elles n'existent pas.

- Établit la connexion avec le broker MQTT et s'abonne au topic configuré.

- Démarre l'API REST sur le port local 8000.

---

## Points de terminaison API

Une fois le serveur démarré, vous pouvez explorer les endpoints :
| Méthode | Route | Description |
| :--- | :--- | :--- |
| `GET` | `/measures` | Liste les dernières mesures enregistrées (paramètre optionnel `limit`, défaut : 50). |
| `GET` | `/docs` | Documentation interactive Swagger UI avec test en temps réel. |
| `GET` | `/redoc` | Documentation technique ReDoc. |

---

## Exemple de réponse JSON (/measures) :

JSON
````
[
  {
    "id": 1,
    "timestamp": "2026-09-23 11:21:01",
    "sensor_id": "Station_meteo_cd41",
    "temperature": 38.2,
    "humidity": 45.0,
    "wind_speed": 14.5
  }
]

````

---

## Tests et validation

Pour vérifier la chaîne de transmission sans station physique, exécutez le script de simulation :

Bash
````
python test_publish.py
````
Le script envoie une trame de test sur le topic MQTT. Le terminal Uvicorn affiche la prise en compte de la trame, l'enregistrement en base SQLite et l'envoi de l'e-mail d'alerte si la température dépasse le seuil défini dans TEMP_MAX_THRESHOLD.



