from __future__ import unicode_literals

import logging

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django import apps
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common import menu_facet, menu_sidebar
from django_gpg.exceptions import GPGDecryptionError
from django_gpg.runtime import gpg
from documents.models import Document, DocumentVersion

from .links import (
    link_document_signature_delete, link_document_signature_download,
    link_document_signature_upload, link_document_verify
)
from .models import DocumentVersionSignature
from .permissions import (
    PERMISSION_DOCUMENT_VERIFY, PERMISSION_SIGNATURE_DELETE,
    PERMISSION_SIGNATURE_DOWNLOAD, PERMISSION_SIGNATURE_UPLOAD
)

logger = logging.getLogger(__name__)


def document_pre_open_hook(descriptor, instance):
    if DocumentVersionSignature.objects.has_embedded_signature(instance.document):
        # If it has an embedded signature decrypt
        try:
            result = gpg.decrypt_file(descriptor, close_descriptor=False)
            # gpg return a string, turn it into a file like object
        except GPGDecryptionError:
            # At least return the original raw content
            descriptor.seek(0)
            return descriptor
        else:
            descriptor.close()
            return StringIO(result.data)
    else:
        return descriptor


def document_post_save_hook(instance):
    if not instance.pk:
        document_signature, created = DocumentVersionSignature.objects.get_or_create(
            document_version=instance.latest_version,
        )


class DocumentSignaturesApp(apps.AppConfig):
    name = 'document_signatures'
    verbose_name = _('Document signatures')

    def ready(self):
        DocumentVersion.register_post_save_hook(1, document_post_save_hook)
        DocumentVersion.register_pre_open_hook(1, document_pre_open_hook)

        class_permissions(Document, [
            PERMISSION_DOCUMENT_VERIFY,
            PERMISSION_SIGNATURE_DELETE,
            PERMISSION_SIGNATURE_DOWNLOAD,
            PERMISSION_SIGNATURE_UPLOAD,
        ])

        menu_facet.bind_links(links=[link_document_verify], sources=[Document])
        menu_sidebar.bind_links(links=[link_document_signature_upload, link_document_signature_download, link_document_signature_delete], sources=['signatures:document_verify', 'signatures:document_signature_upload', 'signatures:document_signature_download', 'signatures:document_signature_delete'])