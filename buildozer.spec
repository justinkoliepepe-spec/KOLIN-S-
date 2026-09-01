[app]

# (str) Title of your application
title = Mon Application

# (str) Package name
package.name = monapp

# (str) Package domain (needed for android packaging)
package.domain = org.monapp

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API
android.api = 31

# (int) Minimum API supported
android.minapi = 21

# (bool) Automatically accept SDK licence
android.accept_sdk_license = True

[build]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
