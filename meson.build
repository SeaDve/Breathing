project('breathing',
          version: '0.1.1',
    meson_version: '>= 0.50.0',
          license: 'GPL-3.0-or-later',
  default_options: [ 'warning_level=2',
                   ],
)

i18n = import('i18n')



subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')
