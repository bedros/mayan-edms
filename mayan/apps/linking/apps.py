from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from acls.permissions import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from common import (
    menu_facet, menu_object, menu_secondary, menu_setup, menu_sidebar
)
from documents.models import Document

from .classes import ResolvedSmartLink
from .links import (
    link_smart_link_acl_list, link_smart_link_create,
    link_smart_link_condition_create, link_smart_link_condition_delete,
    link_smart_link_condition_edit, link_smart_link_condition_list,
    link_smart_link_delete, link_smart_link_document_types,
    link_smart_link_edit, link_smart_link_instance_view,
    link_smart_link_instances_for_document, link_smart_link_list,
    link_smart_link_setup
)
from .models import SmartLink, SmartLinkCondition
from .permissions import (
    PERMISSION_SMART_LINK_DELETE, PERMISSION_SMART_LINK_EDIT,
    PERMISSION_SMART_LINK_VIEW
)


class LinkingApp(apps.AppConfig):
    name = 'linking'
    verbose_name = _('Linking')

    def ready(self):
        class_permissions(SmartLink, [
            ACLS_EDIT_ACL, ACLS_VIEW_ACL, PERMISSION_SMART_LINK_DELETE,
            PERMISSION_SMART_LINK_EDIT, PERMISSION_SMART_LINK_VIEW
        ])

        menu_facet.bind_links(links=[link_smart_link_instances_for_document], sources=[Document])
        menu_object.bind_links(links=[link_smart_link_condition_edit, link_smart_link_condition_delete], sources=[SmartLinkCondition])
        menu_object.bind_links(links=[link_smart_link_edit, link_smart_link_document_types, link_smart_link_condition_list, link_smart_link_acl_list, link_smart_link_delete], sources=[SmartLink])
        menu_object.bind_links(links=[link_smart_link_instance_view], sources=[ResolvedSmartLink])
        menu_secondary.bind_links(links=[link_smart_link_list, link_smart_link_create], sources=[SmartLink, 'linking:smart_link_list', 'linking:smart_link_create'])
        menu_setup.bind_links(links=[link_smart_link_setup])
        menu_sidebar.bind_links(links=[link_smart_link_condition_create], sources=['linking:smart_link_condition_list', 'linking:smart_link_condition_create', 'linking:smart_link_condition_edit', 'linking:smart_link_condition_delete'])