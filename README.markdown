# django-flatpages-plus

## Description

**Note: This project is no longer actively maintained, use at your own risk. Feel free to submit pull requests if you find a bug.**

A more robust flatpages app for Django.

This app adds a few "missing" features to flatpages including: 

- Tagging (via [django-taggit][] currently)
- Automatic and intelligent breadcrumb creation.
- Page view tracking
- A more robust manager.
- A more robust `templatetag` (see "get_flatpages Templatetag" below)
- "Page title" (used for `<title>` tag) and "Link name" (used to give links to pages a sane name).
- Published status (published or draft) to control page visibility on the front end.
- Automatically associate a FlatPage with the current site (from settings.SITE_ID).
- A provided template for FlatPages so you can be up and running quickly.
- A page owner (a User) who is responsible for the page.
- Created and modified datestamps.

This app is meant to replace the default `django.contrib.flatpages` app and will not work running along side it.

This app works basically the same as the default flatpages, just with a few more features.


## Usage

1. Install django-flatpages-plus by either running `setup.py`, or somehow putting it on your `PythonPath`. I recommend installing with [PIP](http://pip.openplans.org/) in a [virtualenv](http://pypi.python.org/pypi/virtualenv) (and using [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/) to make things easier for you).

        pip install django-flatpages-plus

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


## Dependencies

This application currently requires [django-taggit](https://github.com/alex/django-taggit).

*I have plans to make it optional, but currently it is hard coded in.*

The application uses [Django South](http://south.aeracode.org/) for database schema migrations. You shouldn't need it except if you need to upgrade the application after a database change.


## get_flatpages Templatetag

django-flatpages-plus offers a more robust `templatetag` to use when retrieving flatpages in your templates.

The `get_flatpages` templatetag uses the `FlatpagesManager` in `managers.py` to handle sorting, filtering and excluding flatpages from the result set.

Here are a few things you can do with the templatetag:

- Sort flatpages by when they were modified (most recent/least recent), created (also most recent/least recent), their view count (most viewed/least viewed) or randomize the results.
- Filter flatpages by the user or users that "own" the page.
- Filter results by what the URL starts with.
- Get all pages that are tagged with a particular tag or set of tags.
- Limit the results set to a specific number of results.
- Remove a particular flatpage from a set of results. Useful if you want to show related flatpages without showing the current page in the list.

### Basic Usage

The most basic usage is:

    {% load flatpages_plus_tags %}
    {% get_flatpages %}

... which will return all flatpages in the system in a template variable called `flatpages`, which could be used like so:

    <ul>
        {% for f in flatpages.all %}
            <li><a href="{{ f.url }}" title="View the {{ f.name }} page">{{ f.name }}</a></li>
        {% endfor %}
    </ul>

### More Examples

Here are a few more useful examples:

    {% get_flatpages sort='views' %}

... which will sort flatpages by the most viewed first.

    {% get_flatpages sort='random' limit=5 %}

... which will return the flatpages in random order, limiting the results to five flatpages.

    {% get_flatpages users=1 limit=5 as user_flatpages %}

... which will return five flatpages by the user whose ID is 1, as the template variable `user_flatpages`.

    {% get_flatpages tags='foo,bar,baz' %}

... which will return all flatpages that are tagged with *either* 'foo', 'bar', 'baz', or a combination of the three.

    {% get_flatpages remove=3 limit=5 %}

... which will return five of the most recent flatpages, excluding the flatpage with an ID of 3.

    {% get_flatpages starts_with='/about/' %}

... which will return all pages whose URLs start with `/about/` (e.g. `/about/`, `/about/contact/`, `/about/team/`, etc...).

Here is a full list of the different arguments you can pass the `get_flatpages` templatetag.

    sort=                       What to sort the flatpages by. Optional. Default is by url.
        'created'               Returns least recently created flatpages first.
        '-created'              Returns most recently created flatpages first.
        'modified'              Returns least recently modified flatpages first.
        '-modified'             Returns most recently modified flatpages first.
        'views'                 Returns the least viewed flatpages first.
        '-views'                Returns the most viewed flatpages first.
        'random'                Returns random flatpages.
        
    tags='foo,bar,baz'          Returns all flatpages tagged with _either_      
                                'foo', 'bar', or 'baz'. Optional.
    
    starts_with='/about/'       Return all flatpages that have a URL that 
                                starts with '/about/'.
    
    owners=1                    Returns all flatpages by the User with ID 1. 
                                Optional. Can be a string of IDs 
                                (e.g. '1,5,6,8,234') or an integer 
                                (e.g. 1). Optional.
                                
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
