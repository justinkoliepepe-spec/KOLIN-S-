[app]

# (str) Title of your application
title = Mon Application

# (str) Package name
package.name = monapp

# (str) Package domain (needed for android packaging)
package.domain = org.monapp

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Ajoutez vos dépendances supplémentaires ici (ex: python3,kivy,requests)
requirements = python3,kivy

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be old enough to be supported by P4A
# Set to 33 to prevent Buildozer from trying to use unstable build-tools 37
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Automatically accept SDK licence
android.accept_sdk_license = True

[build]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1
