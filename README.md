
# Gestionnaire de tournois d'échecs


- Projet permettant de gérer des tournois d'échecs.<br/>




## Téléchargement et installation 


- copiez le dépôt distant, dans votre terminal/interpréteur. <br/>
	Vous allez dans le dossier ou vous souhaitez placer le projet.<br/> 
Exemple : ``cd C:\Users\damie\Documents\Python_Project``
- Puis ``git clone https://github.com/DamienZeh/gestionnaire-de-tournois-d-echecs.git``
- Puis, allez dans ce projet : ``cd gestionnaire-de-tournois-d-echecs\``
- On crée l’environnement virtuel avec  ``python -m venv env``<br/>
	_(‘env’ est le nom que j’ai sur mon environnement virtuel, il est aussi noté dans le gitignore.)_
- Puis activez le : ``.\env\Scripts\activate.bat`` (pour windows)<br/>
	_(Vous avez maintenant un ‘(env)’ d’affiché, l'environnement est activé)_
- Puis, l’installation  des packages (présent dans le requirements.txt): ``pip install -r requirements.txt``

<br/>


## Description


### Démarrage

Lancez simplement le module **main.py**, avec la commande « **python fichier.py** ».<br/>
exemple : ``python main.py``<br/>
A partir de la vous arriverez dans le menu principal du projet.

### Le programme


Au lancement du programme, un fichier **database_manager.json** sera automatiquement créé,<br/>
si jamais il n'est pas déjà présent. C'est sur ce fichier que seront stockées vos informations de tournois.<br/>
Pour l'exemple, il y a un fichier .json présent avec quelques tournois et joueurs enregistrés.<br/>
Voici les différentes possibilités du programme :

- **Affichez tous les tournois/ Chargez un tournoi**<br/>
S'il y en a, vous pouvez voir tous les tournois, terminés ou non.<br/><br/>

- **Affichez la liste de tous les joueurs du classement général**<br/>
S'il y a déjà des tournois de faits, vous pouvez voir tous joueurs qui ont participé à ces tournois,<br/>
ils auront aussi un classement général dans leurs informations.<br/><br/>

- **Créez un tournoi**<br/>
Vous pouvez créer autant de tournois que vous le souhaitez.<br/>
Vous rentrez différentes informations, comme le nom, le lieu, le mode (Blitz, Bullet, Coup rapide),<br/>
 et la description. La date de création et l'affichage des rounds finis,<br/>
sont générés automatiquement au fur et à mesure.<br/>
Un tournoi est composé de 8 joueurs, et fonctionne sur le principe des rondes Suisses. <br/><br/>

- **Entrez un joueur**<br/>
Lors de la création d'un tournoi, vous pouvez entrer les informations d'un nouveau joueur participant.<br/>
Il sera aussi stocké dans la liste du classement général.<br/><br/>

- **Choisissez un joueur présent dans le classement général**<br/>
Lors de la création d'un tournoi, vous pouvez aussi choisir d'ajouter un joueur,<br/>
existant de la liste du classement général, dans votre tournoi.<br/><br/>

- **Affichez la liste de tous les joueurs du tournoi**<br/>
Après avoir chargé un tournoi, vous pouvez voir tous joueurs qui y participent,<br/>
et les informations que vous avez tapé sur eux, ainsi que leurs points totaux lors de ce tournoi.<br/><br/>

- **Modifiez le rang d'un joueur**<br/>
Vous pouvez à tout moment, changer le classement d'un joueur<br/>
(et vous le ferez aussi à la fin du tournoi, en fonction des résultats).<br/><br/>

- **Affichez les informations sur le tournoi**<br/>
Après avoir chargé un tournoi, vous pouvez accéder aux informations sur celui ci.<br/><br/>

- **Lancez un round**<br/>
Après avoir chargé un tournoi, et entrez ou importez 8 joueurs, vous pouvez lancer un round.<br/>
Un round est composé de 4 matchs.<br/>
Les matchs du premier round sont triés en fonction du classement général de chacun.<br/>
On divise les joueurs en deux moitiés, une supérieure et une inférieure.<br/>
Le meilleur joueur de la moitié supérieure est jumelé avec le meilleur joueur de la moitié inférieure, etc. <br/>
Les matchs des rounds qui suivent sont triés en fonctions des points des matchs précédents,<br/>
et si des joueurs ont les mêmes points, on les trie en fonction du classement général.<br/>
On peut réaliser autant de rounds que l'on souhaite.<br/>
A la fin de chaque round, il est demandé de rentrer manuellement les résultats.<br/><br/>

- **Affichez tous les matchs du tournoi**<br/>
Pendant un tournoi, vous pouvez afficher la liste de rounds et donc de matchs réalisés,<br/>
avec leurs dates de début et de fin.<br/><br/>

- **Terminez un tournoi**<br/>
Après avoir réalisé 4 rounds, on vous demandera si vous souhaitez poursuivre ou terminer le tournoi.<br/>
Si vous le terminez, alors une date sera automatiquement générée, et vous ne pourrez plus lancer de round.<br/><br/>

- **Quittez un tournoi/Quittez le programme**<br/>
Vous pouvez quand vous le souhaitez quitter un tournoi, et donc revenir au menu principal,<br/> 
ou même quitter le programme.<br/><br/>

**Détail sur les rounds et matchs**, Dans la mesure du possible, pour éviter les répétitions,<br/>
si le joueur 1 à déja affronté le joueur 2, alors ça sera le 3, s'il a aussi affronté le 3, ça sera le 4.<br/>
Et quand tout cela à déjà eu lieu, les matchs sont générés aléatoirement.<br/>
Et le round d'après, on recommence la procédure (jusqu'a 7 rounds de matchs inédits).<br/>

**2 possibilités pour entrer les résultats de matchs**, soit vous tapez les points proposés par le simulateur,<br/>
soit vous rentrez les points de vos vrais matchs.<br/>
Car après tout, c'est le but premier du programme, de gérer vos propre tournois.
<br/><br/>



## Auteur

* **Damien Hernandez** _alias_ [DamienZeh](https://damienhernandez.fr/)


