Weathernow 🌤️

Application web de prévisions météo en temps réel avec affichage d’images liées à la ville.

Fonctionnalités :
- Recherche de la météo pour une ville donnée.
- Affichage des informations météo détaillées : température, vent, humidité, pression, précipitations.
- Images liées à la ville récupérées via l’API Pexels.
- Gestion des erreurs : ville inexistante ou pays entré à la place d’une ville.

Prérequis :
- Python 3.7+
- Flask
- Requests
- python-dotenv
- pycountry

Installation prérequis :
Les différentes dépendances se trouvent dans le fichier requirements.txt pour les installer il suffira de faire :
pip install -r requirements.txt


Configuration clés API
Dans le fichier .env insérer vos clés personelles obtenues sur les différents sites : https://www.weatherapi.com/ et https://www.pexels.com/login/?redirect_to=%2Fapi%2Fkey%2F

Lancer l'application
python api_weather.py

L'application sera disponible sur http://127.0.0.1:5000/search






Auteur
Loïs B. – Projet personnel Weathernow
