# django-flatpages-plus

## Description

A more robust FlatPages app for Django.

This app adds a few "missing" features to flatpages including tagging (via [django-taggit][] currently), page view counting, a more robust `templatetag`, created and modified datestamps and a few more niceties... 

This app is meant to replace the default `django.contrib.flatpages` app and will not work running along side it.

This app works basically the same as the default flatpages, just with a few more features.


## Usage

1. Install django-flatpages-plus by either running `setup.py`, putting it on your `PythonPath`.

1. Add `flatpages_plus` to `INSTALLED_APPS`:

        INSTALLED_APPS = [
            ...
            'flatpages_plus',
        ]

1. Add `flatpages_plus.middleware.FlatpageFallbackMiddleware` to `MIDDLEWARE_CLASSES`:

        MIDDLEWARE_CLASSES = [
            ...
            'flatpages_plus.middleware.FlatpageFallbackMiddleware',
        ]

1. Run `syncdb` to install the database tables:

        ./manage.py syncdb

## Credits

Copyright &copy; 2011 Dana Woodman <dana@danawoodman.com>


## License

Released under an MIT license. See the `LICENSE` file for more information.


[django-taggit]: https://github.com/alex/django-taggit "View django-taggit on GitHub"
