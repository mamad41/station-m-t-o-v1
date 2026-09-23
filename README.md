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