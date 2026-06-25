# Questions de réflexion

## 1. Gestion de version

### Comment organiser le travail en groupe avec des branches ?

Dans notre projet, on a décidé de travailler chacun sur une branche séparée selon la tâche qu'on avait à faire. Par exemple `bugfix/maintenance-corrective` pour les corrections de bugs, `feature/api` pour l'intégration de l'API externe. Comme ça, chacun bosse de son côté sans risquer d'écraser le travail de l'autre. Une fois qu'on estime que c'est prêt, on ouvre une Pull Request pour que le reste du groupe puisse relire avant que ça parte sur `main`.

### Quels avantages apportent les Pull Requests par rapport à un push direct sur main ?

On s'en est rendu compte assez vite dans le projet : pousser directement sur `main` c'est risqué. On peut écraser le travail de quelqu'un, introduire un bug sans que personne s'en aperçoive, ou avoir un historique git impossible à lire.

Avec les Pull Requests, le code est relu avant d'être intégré. On peut laisser des commentaires, demander des modifications, et surtout on sait exactement ce qui a été ajouté et pourquoi. C'est bien plus propre et sécurisé pour travailler à plusieurs.

---

## 2. Qualité et tests

### Qu'est-ce qu'un test unitaire et pourquoi est-il important ?

Un test unitaire, c'est un petit bout de code qui vérifie qu'une fonction précise fait bien ce qu'elle est censée faire. Par exemple, on teste que `convert(10, "EUR", "USD", rates)` retourne bien `11.0` et pas autre chose.

C'est important parce que dès qu'on modifie quelque chose dans le code, on peut relancer les tests et voir tout de suite si on a cassé quelque chose. Sans ça, on s'en rend compte souvent trop tard, en prod ou lors d'une démo.

### Pourquoi automatiser les tests dans GitHub Actions avant d'accepter une PR ?

Parce qu'on ne peut pas compter sur le fait que chaque développeur pense à lancer les tests avant de pousser. En les automatisant dans GitHub Actions, dès qu'une PR est ouverte, les tests tournent automatiquement. Si quelque chose échoue, la PR est bloquée et on ne peut pas merger du code cassé sur `main`. Ça enlève une source d'erreur humaine.

---

## 3. Refactoring

### Quelles dettes techniques observez-vous dans le code initial ?

En regardant le code de départ, plusieurs choses nous ont sauté aux yeux :

- Les taux de change sont codés en dur dans le fichier → ils seront faux dès le lendemain
- Toute la logique de conversion est directement dans l'interface Streamlit → impossible à tester proprement
- Aucune vérification des entrées → si on met 0 comme montant, l'appli affiche `0.00` sans rien dire
- Pas d'historique → on perd toutes les conversions dès qu'on rafraîchit la page

### Quelles modifications ont amélioré la maintenabilité et la lisibilité ?

Le fait d'extraire la logique dans `app_functions.py` change vraiment quelque chose. On peut tester la fonction `convert()` sans avoir à lancer toute l'interface. Pareil pour l'API : maintenant les taux sont toujours à jour, et si on veut changer de fournisseur, on ne touche qu'à un seul endroit. Les vérifications des entrées rendent aussi le code plus prévisible — on sait exactement ce qui va se passer selon ce que l'utilisateur entre.

---

## 4. Maintenance

### Classez vos modifications selon les quatre types de maintenance

| Modification | Type de maintenance |
|---|---|
| Vérification montant nul/négatif + devises identiques + messages d'erreur | Corrective |
| Bouton pour inverser les devises, ajout de GBP/CAD, historique des conversions | Évolutive |
| Remplacement des taux codés en dur par l'API exchangerate-api.com | Adaptative |
| Refactoring dans `app_functions.py`, tests unitaires, workflow GitHub Actions, flake8/black | Perfective |

### Quelle partie vous semble la plus fréquente dans un projet réel ?

D'après ce qu'on a vu, la maintenance corrective et évolutive reviennent en permanence. Il y a toujours un bug à corriger ou une nouvelle fonctionnalité demandée. La maintenance adaptative arrive plutôt lors de changements d'environnement, comme une API qui ferme ou un framework qui évolue. Quant à la perfective, elle est souvent mise de côté par manque de temps, même si c'est elle qui fait vraiment la différence sur le long terme.
