# django-flatpages-plus

## Description

A more robust flatpages app for Django.

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

## `templatetag`

django-flatpages-plus offers a more robust `templatetag` to use when retrieving flatpages in your templates.

The most basic usage is:

    {% get_flatpages %}

... which will return all flatpages in the system in a template variable called `flatpages`, which could be used like so:

    <ul>
        {% for f in flatpages %}
            <li><a href="{{ f.url }}" title="View the {{ f.title }} page">{{ f.title }}</a></li>
        {% endfor %}
    </ul>

Here are a few more useful examples:

    {% get_flatpages sort='views' %}

... which will sort flatpages by the most viewed first.

    {% get_flatpages sort='random' limit=5 %}

... which will return the flatpages in random order, limiting the results to 5 flatpages.

    {% get_flatpages user=1 limit=5 as user_flatpages %}

... which will return five flatpages by user whose ID is 1, as the template variable `user_flatpages`.

    {% get_flatpages tags='foo,bar,baz' %}

... which will return all flatpages that are tagged with *either* 'foo', 'bar', or 'baz'.

    {% get_flatpages remove=3 limit=5 %}

... which will return five of the most recent flatpages, excluding the flatpage with an ID of 3.

Here is a full list of the different arguments you can pass the `get_flatpages` templatetag.

    sort=                       What to sort the flatpages by. Optional.
        'modified'              Returns newest flatpages first. Default.
        '-modified'             Returns oldest flatpages first.
        'created'               Returns newest flatpages first.
        '-created'              Returns oldest flatpages first.
        'views'                 Returns the most viewed flatpages first.
        '-views'                Returns the least viewed flatpages first.
        'random'                Returns random flatpages.
    
    tags='foo,bar,baz'          Returns all flatpages tagged with _either_      
                                'foo', 'bar', or 'baz'. Optional.
    
    author=1                    Returns all flatpages by an author with ID 1. 
                                Optional.
    
    limit=10                    Limits the number of flatpages that are 
                                returned to 10 results. Optional.
                                
    remove=1                    Removes a given flatpage ID or list of IDs from
                                the results list. Can be a string of IDs 
                                (e.g. '1,5,6,8,234') or an integer 
                                (e.g. 1). Optional.


## Credits

Copyright &copy; 2011 [Dana Woodman][] <dana@danawoodman.com>


## License

Released under an MIT license. See the `LICENSE` file for more information.


[django-taggit]: https://github.com/alex/django-taggit "View django-taggit on GitHub"
[Dana Woodman]: http://www.danawoodman.com/ "View Dana's website"
