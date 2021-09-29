# Traitement d'image

Pour tester le traitement d'image : `python3 process.py`

Ce script va charger l'image `img.jpg` et faire le traitement dessus (fonction `processing`). A chaque étape, l'image correspondante est enregistrée pour pouvoir la regarder plus tard.

# Capture vidéo

Pour lancer la capture vidéo : `python3 capture.py`

Ce script récupère chaque image filmée et appelle la fonction `processing` du fichier `process.py`.

ATTENTION : ligne 4 du fichier `capture.py`, il faut mettre le bon id en paramètre de `cv.VideoCapture(id)`. Pour savoir quel est le bon id, taper la commande `ls -ltr /dev/video*` dans un terminal et mettre le chiffre correspondant à la caméra (exemple, si la caméra est sur le `/dev/video2`, alors l'id est 2).

# Travailler sur Raspberry Pi
IP = IP de la Raspberry

Pour copier un fichier sur la Raspberry : (depuis un terminal non connecté en ssh) 'scp fichier pi@IP:' (copie sur le dossier root)

Pour se connecter en ssh : 'ssh IP' (id = 'pi', password = 'raspberry').
  -> Possibilité de lancer un script python sur la carte depuis la connexion ssh.


# Ressources 

* Building a Line Following BeagleBone Robot with openCV : http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
* Exemples d'utilisation de pypot.dynamixel : https://poppy-project.github.io/pypot/dynamixel.html
