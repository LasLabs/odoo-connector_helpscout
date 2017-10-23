# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields
from odoo.addons.component.core import Component


class HelpscoutMailboxFolder(models.Model):
    _name = 'helpscout.mailbox.folder'
    _inherit = 'helpscout.binding'
    _description = 'HelpScout Mailbox Folders'

    external_id = fields.Char(
        string='HelpScout Mailbox ID, Folder ID',
    )
    helpscout_type = fields.Selection(
        selection=[
            ('assigned', 'Assigned'),
            ('closed', 'Closed'),
            ('drafts', 'Drafts'),
            ('mine', 'Mine'),
            ('needsattention', 'Needs Attention'),
            ('open', 'Open'),
            ('spam', 'Spam'),
        ],
        string="HelpScout type",
    )
    name = fields.Char(
        string='HelpScout Mailbox Folder Name',
        required=True,
    )


class HelpScoutMailboxFolderAdapter(Component):
    """Utilize the API in context."""
    _name = 'helpscout.mailbox.folder.adapter'
    _inherit = 'helpscout.adapter'
    _apply_on = 'helpscout.mailbox.folder'
    _helpscout_endpoint = 'Mailboxes'

    def search_read(self, mailbox_id):
        """Return entire folder list"""
        return self.endpoint.get_folders(mailbox_id)

    def search(self, filters=None):
        mailbox_id = filters.get('mailbox_id')
        return [
            "%d,%d" % (mailbox_id, r.id)
            for r
            in self.search_read(mailbox_id)
        ]

    def read(self, _id):
        mailbox_id, folder_id = [int(n) for n in _id.split(',')]
        return next(
            r
            for r
            in self.search_read(mailbox_id)
            if r.get('id') == folder_id
        )
