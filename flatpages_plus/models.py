from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from flatpages_plus.managers import FlatpagesManager


class FlatPage(models.Model):
    """
    A static page.
    """
    STATUS_LEVELS = (
        ('d', _('draft')),
        ('p', _('published'))
    )
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    owner = models.ForeignKey(User, verbose_name=_('owner'), default=1)
    views = models.IntegerField(_('views'), default=0, blank=True, null=True)
    status = models.CharField(_('status'), max_length=1, choices=STATUS_LEVELS, 
        default='d')
    tags = TaggableManager(blank=True)
    enable_comments = models.BooleanField(_('enable comments'))
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'flatpages/contact_page.html'. If this isn't \
        provided, the system will use 'flatpages/default.html'."))
    registration_required = models.BooleanField(_('registration required'), 
        help_text=_("If this is checked, only logged-in users will be able \
        to view the page."))
    sites = models.ManyToManyField(Site) # TODO: Make the default site, use SITE_ID (usually 1).
    created = models.DateTimeField(_('created'), auto_now_add=True, 
        blank=True, null=True)
    modified = models.DateTimeField(_('modified'), auto_now=True, 
        blank=True, null=True)
    
    objects = FlatpagesManager()
    
    class Meta:
        verbose_name = _('flat page')
        verbose_name_plural = _('flat pages')
        ordering = ('url',)
        
    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)
        
    @permalink
    def get_absolute_url(self):
        return ('flatpage', None, {
            'url': self.url
        })
