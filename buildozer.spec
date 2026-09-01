[app]

# (str) Title of your application
title = KOLIN S

# (str) Package name
package.name = kolins

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0Le fichier `buildozer.spec` contient tous les paramètres requis par Buildozer pour créer l'application Android.

Voici un exemple minimaliste et directement utilisable pour une application Kivy. Vous pouvez créer le fichier sur GitHub avec ce contenu :

```ini
[app]

# Nom de votre application
title = Mon Application Kivy

# Nom du paquet (sans espaces ni caractères spéciaux)
package.name = monappkivy

# Domaine du paquet (souvent votredomaine.com en inversé)
package.domain = org.monprojet

# Dossier contenant le code source (le dossier courant .)
source.dir = .

# Extensions de fichiers à inclure
source.include_exts = py,png,jpg,kv,atlas

# Version de l'application
version = 0.1

# Dépendances Python requises par l'application
requirements = python3,kivy

# Orientation de l'écran (landscape, portrait ou all)
orientation = portrait

# Prise en charge du plein écran (0 = non, 1 = oui)
fullscreen = 0

# Architectures cibles pour Android
android.archs = arm64-v8a, armeabi-v7a

# Accepter automatiquement les licences du SDK Android
android.accept_sdk_license = True

[buildozer]

# Niveau de log pour la compilation (2 = détaillé)
log_level = 2

# Avertir en cas d'exécution sous le compte root
warn_on_root = 1
