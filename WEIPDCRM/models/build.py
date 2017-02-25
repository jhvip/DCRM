# coding=utf-8

"""
DCRM - Darwin Cydia Repository Manager
Copyright (C) 2017  WU Zheng <i.82@me.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals

import uuid

from django.db import models
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from WEIPDCRM.models.release import Release


class Build(models.Model):
    """
    DCRM Base Model: Build
    """
    
    class Meta(object):
        verbose_name = _("Build")
        verbose_name_plural = _("Builds")

    # Base Property
    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        primary_key=True,
        default=uuid.uuid4
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )
    active_release = models.ForeignKey(
        Release,
        verbose_name=_("Active Release"),
        on_delete=models.CASCADE,
        null=True
    )
    compression = models.IntegerField(
        verbose_name=_("Packages Compression"),
        choices=(
            (0, _("Plain")),
            (1, _("Gzip")),
            (2, _("Plain and Gzip")),
            (3, _("Bzip")),
            (4, _("Plain and Bzip")),
            (5, _("Gzip and Bzip")),
            (6, _("All (Recommended)")),
        ),
        default=6,
    )
    details = models.TextField(
        verbose_name=_("Details"),
        blank=True,
        null=True,
    )
    
    def __unicode__(self):
        return str(self.uuid)

    def get_admin_url(self):
        """
        :return: URL String
        :rtype: str
        """
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,)
        )
