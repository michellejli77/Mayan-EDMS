from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import Document

from metadata.conf.settings import AVAILABLE_MODELS
from metadata.conf.settings import AVAILABLE_FUNCTIONS

available_models_string = (_(u' Available models: %s') % u','.join([name for name, model in AVAILABLE_MODELS.items()])) if AVAILABLE_MODELS else u''
available_functions_string = (_(u' Available functions: %s') % u','.join([u'%s()' % name for name, function in AVAILABLE_FUNCTIONS.items()])) if AVAILABLE_FUNCTIONS else u''


class MetadataType(models.Model):
    name = models.CharField(unique=True, max_length=48, verbose_name=_(u'name'), help_text=_(u'Do not use python reserved words, or spaces.'))
    title = models.CharField(max_length=48, verbose_name=_(u'title'), blank=True, null=True)
    default = models.CharField(max_length=128, blank=True, null=True,
        verbose_name=_(u'default'),
        help_text=_(u'Enter a string to be evaluated.%s') % available_functions_string)
    lookup = models.CharField(max_length=128, blank=True, null=True,
        verbose_name=_(u'lookup'),
        help_text=_(u'Enter a string to be evaluated.  Example: [user.get_full_name() for user in User.objects.all()].%s') % available_models_string)
    #TODO: datatype?

    def __unicode__(self):
        return self.title if self.title else self.name

    class Meta:
        verbose_name = _(u'metadata type')
        verbose_name_plural = _(u'metadata types')


class MetadataSet(models.Model):
    title = models.CharField(max_length=48, verbose_name=_(u'title'))

    def __unicode__(self):
        return self.title if self.title else self.name

    class Meta:
        verbose_name = _(u'metadata set')
        verbose_name_plural = _(u'metadata set')


class MetadataSetItem(models.Model):
    """
    Define the set of metadata that relates to a set or group of
    metadata fields
    """
    metadata_set = models.ForeignKey(MetadataSet, verbose_name=_(u'metadata set'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
    #required = models.BooleanField(default=True, verbose_name=_(u'required'))

    def __unicode__(self):
        return unicode(self.metadata_type)

    class Meta:
        verbose_name = _(u'metadata set item')
        verbose_name_plural = _(u'metadata set items')


class DocumentMetadata(models.Model):
    """
    Link a document to a specific instance of a metadata type with it's
    current value
    """
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'type'))
    value = models.TextField(blank=True, null=True, verbose_name=_(u'value'), db_index=True)

    def __unicode__(self):
        return unicode(self.metadata_type)

    class Meta:
        verbose_name = _(u'document metadata')
        verbose_name_plural = _(u'document metadata')
