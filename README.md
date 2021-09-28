# Traitement d'image

Pour tester le traitement d'image : `python3 process.py`

Ce script va charger l'image `img.jpg` et faire le traitement dessus (fonction `processing`). A chaque étape, l'image correspondante est enregistrée pour pouvoir la regarder plus tard.

# Capture vidéo

Pour lancer la capture vidéo : `python3 capture.py`

Ce script récupère chaque image filmée et appelle la fonction `processing` du fichier `process.py`.

ATTENTION : ligne 4 du fichier `capture.py`, il faut mettre le bon id en paramètre de `cv.VideoCapture(id)`. Pour savoir quel est le bon id, taper la commande `ls -ltr /dev/video*` dans un terminal et mettre le chiffre correspondant à la caméra (exemple, si la caméra est sur le `/dev/video2`, alors l'id est 2).

# Ressources 
Building a Line Following BeagleBone  Robot with openCV : http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
