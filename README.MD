# LITRevu - Application Web de Critiques Littéraires
![logo du projet](https://user.oc-static.com/upload/2023/06/29/168805567091_LITrevu%20banner.png)
## Description


LITRevu est une application web développée avec Django permettant à une communauté d'utilisateurs de consulter ou de solliciter des critiques de livres et d'articles. Ce projet a été réalisé dans le cadre du parcours **Développeur d'Applications Python** d'OpenClassrooms (Projet 9).

---

### Fonctionnalités principales

L'application permet aux utilisateurs de :

- **S'inscrire et se connecter** pour accéder aux fonctionnalités
- **Créer des demandes de critique (tickets)** pour des livres ou articles
- **Publier des critiques** en réponse à une demande ou de manière indépendante
- **Suivre d'autres utilisateurs** pour voir leurs publications dans son flux
- **Consulter un flux personnalisé** basé sur ses abonnements
- **Gérer ses publications** (modifier, supprimer ses tickets et critiques)
- **Rechercher des utilisateurs** et gérer ses abonnements

---

## Objectifs du projet

Ce projet a pour but de développer les compétences suivantes :
- Développement d'une application web avec Django
- Mise en place d'une architecture MVT (Modèle-Vue-Template)
- Gestion de l'authentification et des autorisations
- Création de relations entre utilisateurs (système de suivi)
- Manipulation de formulaires

---

##  Technologies utilisées

- **Python 3.13**
- **Django 5.2.7**
- **SQLite3** 
- **HTML5 / CSS3**
- **JS**

---

## Installation

### 1. Cloner le repository

```bash
git clone https://github.com/C-eorl/P9---LITRevu.git
cd P9---LITRevu
```

### 2. Créer un environnement virtuel

**Sur Windows :**
```bash
python -m venv venv
```

**Sur macOS/Linux :**
```bash
python3 -m venv venv
```

### 3. Activer l'environnement virtuel

**Sur Windows :**
```bash
venv\Scripts\activate
```

**Sur macOS/Linux :**
```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Appliquer les migrations
Avant tout, se déplacer dans le repertoire litrevu.
```bash
cd litrevu
```
Puis appliquer les migrations
```bash
python manage.py migrate
```

### 6. (Optionnel) Créer un superutilisateur

```bash
python manage.py createsuperuser
```

---

## Utilisation

### Démarrer le serveur de développement

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : **http://127.0.0.1:8000/**

### Accès à l'interface d'administration

Interface admin Django : **http://127.0.0.1:8000/admin/**

### Accèder à l'application

Vous pouvez utiliser le compte mis à votre disposition :

**- identifiant** : **test**

**- mot de passe** : **usertest**


---

## 📁 Structure du projet

```
P9---LITRevu/
├── litrevu/
│   ├── authentication/                                 # APP. Authentication
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py                                    # Formulaires Login & Signup
│   │   ├── __init__.py
│   │   ├── migrations/
│   │   ├── models.py                                   # Modèles User personnalisé
│   │   ├── static/authentication/css/                  # Style css pour template app. authenication
│   │   ├── templates/authentication/                   # Templates pour app. authentication
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │  
│   ├── litrevu/                                        # Setting du projet
│   │  
│   ├── reviews/                                        # APP. Reviews
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py                                    # Formulaires Ticket & Review
│   │   ├── __init__.py
│   │   ├── migrations/
│   │   ├── models.py                                   # Modèles Ticket, Reviews, UserFollow & UserBlocked
│   │   ├── static/reviews/
│   │   │       ├── css/                                # Style css pour template app. reviews
│   │   │       └── js/                                 # Script simple pour dynamisme 
│   │   ├── templates/reviews/                          # Templates app. reviews
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │   
│   ├── static/
│   │   ├── css                                         # Style template base.html
│   │   └── pictures                                    # Images nécessaire au style + image des posts
│   │   
│   ├── templates/                                      # Templates général au site
│   │ 
│   ├── manage.py
│   └── db.sqlite3
│
├── README.MD
└── requirements.txt

```

---

##  Fonctionnement de l'application

### Flux personnalisé
La page d'accueil affiche les tickets et critiques de l'utilisateur et de ses abonnements, triés par ordre chronologique décroissant.

### Mes posts
Cette page permet à l'utilisateur de visualiser uniquement ses propres publications et de les modifier ou supprimer.

### Créer un ticket
Formulaire permettant de demander une critique en renseignant :
- Titre du livre/article
- Description
- Image (optionnelle)

### Créer une critique
Deux possibilités :
1. En réponse à un ticket existant
2. Création libre (ticket + critique en une seule fois)

Les critiques comprennent :
- Titre
- Note (de 0 à 5 étoiles)
- Commentaire

### Abonnements
Page permettant de :
- Rechercher des utilisateurs
- S'abonner et se désabonner à d'autres utilisateurs
- Bloquer et débloquer des utilisateurs
- Voir la liste de ses abonnements
- Voir qui est abonné à son compte
- Voir la liste des utilisateurs bloqués


---

**Projet réalisé dans le cadre du parcours Développeur d'Applications Python - OpenClassrooms**