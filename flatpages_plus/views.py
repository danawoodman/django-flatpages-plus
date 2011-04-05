import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.xheaders import populate_xheaders
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect

from flatpages_plus.models import FlatPage

DEFAULT_TEMPLATE = 'flatpages_plus/default.html'

# This view is called from FlatpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching flatpage exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.
def flatpage(request, url, **kwargs):
    """
    Public interface to the flat page view.
    
    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or `flatpages_plus/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_404(FlatPage, url__exact=url, #status='p',
        sites__id__exact=settings.SITE_ID)
    return render_flatpage(request, f)

@csrf_protect
def render_flatpage(request, f):
    """
    Internal interface to the flat page view.
    """
    # If the page is a draft, only show it to users who are staff.
    if f.status == 'd' and not request.user.is_authenticated():
        raise Http404
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)
    
    # Track pageviews (but not of owner).
    if request.user != f.owner:
        f.views += 1
        f.save()
    
    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)
    
    # Create breadcrumb navigation links.
    # breadcrumb_urls = f.url.lstrip('/').rstrip('/').split('/')
    # breadcrumb_urls.insert(0, '/')
    # 
    # for i, u in enumerate(breadcrumb_urls):
    #     try: # Try and get a flatpage instance from the URL.
    #         if u != '/':
    #             u = '/%s/' % u
    #         fp = FlatPage.objects.get(url__exact=u)
    #         bt = fp.title
    #         bu = fp.url
    #     except: # Default to the URL slug, capitalized if no flatpage was found.
    #         bt = u.capitalize()
    #         bu = None
    #     breadcrumbs += [{ # Contsruct a dictionary for the breadcrumb entity.
    #         'url': bu,
    #         'title': bt,
    #     }]
    
    

    breadcrumb_urls = []
    breadcrumbs = []

    def trim_page(url):
        """Trim the last section off a URL."""
        regex = re.compile(r'(?P<url>.*/)[-\w\.]+/?$')
        try:
            trimmed_url = regex.match(url).group('url') # Return the parent page
        except:
            trimmed_url = None # Return None to indicate no parent.
        return trimmed_url

    def do_trimming(url):
        """Perform the trimming operations recursively."""
        breadcrumb_urls.append(url)
        trimmed_url = trim_page(url)
        if trimmed_url:
            do_trimming(trimmed_url)
        else:
            return True
    
    # Trim the flatpage's URL.
    do_trimming(f.url)
    
    # Reverse the list of breadcrumbs so the parent pages start first.
    breadcrumb_urls.reverse()
    
    # Loop through the list of pages and construct a list of url/title dictionaries
    # for each page to use in the templates.
    for i, u in enumerate(breadcrumb_urls):
        bn = ''
        bu = ''
        try: # Try and get a flatpage instance from the URL.
            # if u != '/':
            #     u = '/%s/' % u
            fp = FlatPage.objects.get(url__exact=u)
            bn = fp.name
            bu = fp.url
        except: # Try to handle missing pages cleanly.
            regex = re.compile(r'.*/(?P<url>[-\w\.]+)/?$')
            try:
                # Default to the URL slug of the last segment of the URL 
                # (capitalized) if no flatpage was found. This gives us an 
                # OK default for missing pages.
                bn = regex.match(u).group('url')
            except:
                # Worst case scenario we show the URL as the title if we can't 
                # grab the last bit of the URL...
                bn = u
            bn = bn.capitalize() # Capitalize it to make it look a little nicer.
            # Return None if the flatpage doesn't exist so we don't link to it, 
            # because it would cause a 404 error if we did.
            bu = None
        breadcrumbs += [{ # Contsruct a dictionary for the breadcrumb entity.
            'url': bu,
            'name': bn,
        }]
    
    
    c = RequestContext(request, {
        'flatpage': f,
        'breadcrumbs': breadcrumbs,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, FlatPage, f.id)
    return response
    # TODO: Use render_to_response here...
