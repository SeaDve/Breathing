<h1 align="center">
  <img src="data/logo/io.github.seadve.Breathing.svg" alt="Breathing" width="192" height="192"/><br>
  Breathing
</h1>

<p align="center"><strong>Exercise your breathing</strong></p>

<br>
<p align="center">
  <a href="https://liberapay.com/SeaDve/">
    <img src="https://img.shields.io/liberapay/receives/SeaDve.svg?logo=liberapay">
  </a>
  <a href="https://hosted.weblate.org/engage/kooha/">
    <img src="https://hosted.weblate.org/widgets/kooha/-/Breathing/svg-badge.svg" alt="Translation status"  />
  </a>
  <a href="https://github.com/SeaDve/Breathing/actions/workflows/testing.yml">
    <img src="https://github.com/SeaDve/Breathing/actions/workflows/testing.yml/badge.svg" alt="CI status"/>
  </a>
</p>

<p align="center">
  <img src="screenshots/Breathing-preview.png" alt="Preview"/>
</p>

Relax, focus, and become stress-free. 

Breathing is a very simple application that guides your breathing pattern. This
pattern is recommended by experts that will help ease your anxiety. It also provides
a calming sound to make it much easier to relax.

The main features of Breathing includes the following:
* 🎵 Guide your breathing.
* 🎸 Play a relaxing tone.
* 🌐 Change to a dark-mode with ease.
* 📱 Easy-to-use user interface.
* ⌨️ User-friendly keyboard shortcuts.


## 🏗️ Building from source

### GNOME Builder
GNOME Builder is the environment used for developing this application. It can use Flatpak manifests to create a consistent building and running environment cross-distro. Thus, it is highly recommended you use it.

1. Download [GNOME Builder](https://flathub.org/apps/details/org.gnome.Builder).
2. In Builder, click the "Clone Repository" button at the bottom, using `https://github.com/SeaDve/Breathing.git` as the URL.
3. Click the build button at the top once the project is loaded.

### Meson
```
git clone https://github.com/SeaDve/Breathing.git
cd Breathing
meson builddir --prefix=/usr/local
ninja -C builddir install
```


## 🙌 Help translate Breathing
You can help Breathing translate into your native language. If you found any typos 
or think you can improve a translation, you can use the [Weblate](https://hosted.weblate.org/engage/kooha/) platform.


## ☕ Support me and the project

Breathing is free and will always be for everyone to use. If you like the project and
would like to support and fund it, you may donate through [Liberapay](https://liberapay.com/SeaDve/).


## 💝 Acknowledgment

A big thank you to all the [contributors](https://github.com/SeaDve/Kooha/graphs/contributors) 
and [translators](https://hosted.weblate.org/engage/kooha/) from Weblate.
