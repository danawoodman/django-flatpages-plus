# from django import template
# from django.conf import settings
# from django.contrib.flatpages.models import FlatPage
# 
# 
# register = template.Library()
# 
# 
# class FlatpageNode(template.Node):
#     def __init__(self, context_name, starts_with=None, user=None):
#         self.context_name = context_name
#         if starts_with:
#             self.starts_with = template.Variable(starts_with)
#         else:
#             self.starts_with = None
#         if user:
#             self.user = template.Variable(user)
#         else:
#             self.user = None
# 
#     def render(self, context):
#         flatpages = FlatPage.objects.filter(sites__id=settings.SITE_ID)
#         # If a prefix was specified, add a filter
#         if self.starts_with:
#             flatpages = flatpages.filter(
#                 url__startswith=self.starts_with.resolve(context))
# 
#         # If the provided user is not authenticated, or no user
#         # was provided, filter the list to only public flatpages.
#         if self.user:
#             user = self.user.resolve(context)
#             if not user.is_authenticated():
#                 flatpages = flatpages.filter(registration_required=False)
#         else:
#             flatpages = flatpages.filter(registration_required=False)
# 
#         context[self.context_name] = flatpages
#         return ''
# 
# 
# def get_flatpages(parser, token):
#     """
#     Retrieves all flatpage objects available for the current site and
#     visible to the specific user (or visible to all users if no user is
#     specified). Populates the template context with them in a variable
#     whose name is defined by the ``as`` clause.
# 
#     An optional ``for`` clause can be used to control the user whose
#     permissions are to be used in determining which flatpages are visible.
# 
#     An optional argument, ``starts_with``, can be applied to limit the
#     returned flatpages to those beginning with a particular base URL.
#     This argument can be passed as a variable or a string, as it resolves
#     from the template context.
# 
#     Syntax::
# 
#         {% get_flatpages ['url_starts_with'] [for user] as context_name %}
# 
#     Example usage::
# 
#         {% get_flatpages as flatpages %}
#         {% get_flatpages for someuser as flatpages %}
#         {% get_flatpages '/about/' as about_pages %}
#         {% get_flatpages prefix as about_pages %}
#         {% get_flatpages '/about/' for someuser as about_pages %}
#     """
#     bits = token.split_contents()
#     syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
#                        "['url_starts_with'] [for user] as context_name" %
#                        dict(tag_name=bits[0]))
#    # Must have at 3-6 bits in the tag
#     if len(bits) >= 3 and len(bits) <= 6:
# 
#         # If there's an even number of bits, there's no prefix
#         if len(bits) % 2 == 0:
#             prefix = bits[1]
#         else:
#             prefix = None
# 
#         # The very last bit must be the context name
#         if bits[-2] != 'as':
#             raise template.TemplateSyntaxError(syntax_message)
#         context_name = bits[-1]
# 
#         # If there are 5 or 6 bits, there is a user defined
#         if len(bits) >= 5:
#             if bits[-4] != 'for':
#                 raise template.TemplateSyntaxError(syntax_message)
#             user = bits[-3]
#         else:
#             user = None
# 
#         return FlatpageNode(context_name, starts_with=prefix, user=user)
#     else:
#         raise template.TemplateSyntaxError(syntax_message)
# 
# register.tag('get_flatpages', get_flatpages)



# TODO: Add starts_with so we can list pages under a section (see above).

from django import template
from django.template.base import TemplateSyntaxError
from django.template.defaulttags import token_kwargs

from flatpages_plus.models import FlatPage

register = template.Library()


class FlatpagesNode(template.Node):
    
    def __init__(self, extra_context, var_name):
        self.extra_context = extra_context
        self.var_name = var_name
    
    def render(self, context):
        
        values = dict([(key, val.resolve(context)) for key, val in
                       self.extra_context.iteritems()])
        
        sort = values.get('sort', 'recent')
        tags = values.get('tags', None)
        not_tags = values.get('not_tags', None)
        starts_with = values.get('starts_with', None)
        owners = values.get('owners', None)
        limit = values.get('limit', None)
        remove = values.get('remove', None)
        
        context[self.var_name] = FlatPage.objects.get_flatpages(sort=sort, 
                                            tags=tags, 
                                            not_tags=not_tags,
                                            starts_with=starts_with,
                                            owners=owners, 
                                            limit=limit, 
                                            remove=remove)
        return ''

@register.tag
def get_flatpages(parser, token):
    """
    Returns a list of flatpages based on the given criteria.
    
    Basic usage::
    
        {% get_flatpages %}
        
    ... which returns all flatpages (not recommended on sites with many flatpages).
    
    Example usage::
    
        {% get_flatpages as flatpages %}
        {% get_flatpages sort='views' as flatpages %}
        {% get_flatpages sort='random' limit=10 as random_flatpages %}
        {% get_flatpages owners=1 limit=5 as user_flatpages %}
        {% get_flatpages tags='foo,bar,baz' as flatpages %}
        {% get_flatpages starts_with='/about/' as about_pages %}
        {% get_flatpages sort='random' remove=flatpage.id limit=5 as random_flatpages %}
    
    All fields are optional. If nothing is passed to the templatetag, it will 
    return all flatpages, sorted by most recently created
    
    Here are the available options::
    
        sort=                       What to sort the flatpages by. Optional. Default is by url.
            'created'               Returns least recently created flatpages first.
            '-created'              Returns most recently created flatpages first.
            'modified'              Returns least recently modified flatpages first.
            '-modified'             Returns most recently modified flatpages first.
            'views'                 Returns the most viewed flatpages first.
            '-views'                Returns the least viewed flatpages first.
            'random'                Returns random flatpages.
        
        tags='foo,bar,baz'          Returns all flatpages tagged with _either_      
                                    'foo', 'bar', or 'baz'. Optional.
        
        not_tags='foo,bar'          Removes any flatpages tagged with 'foo' or
                                    'bar' from the QuerySet.
    
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
    
    """
    bits = token.split_contents()
    remaining_bits = bits[1:]
    var_name = 'flatpages'
    if remaining_bits:
        if remaining_bits[-2] == 'as':
            var_name = remaining_bits[-1]
            # Remove the var_name and "as" bits from the list or it will throw an error.
            del remaining_bits[-2:-1]
    extra_context = token_kwargs(remaining_bits, parser)
    return FlatpagesNode(extra_context, var_name)

