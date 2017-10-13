# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import (
    mapping,
    only_create,
)


class HelpScoutMailboxFolderImportMapper(Component):
    _name = 'helpscout.import.mapper.mailbox.folder'
    _inherit = 'helpscout.import.mapper'
    _apply_on = 'helpscout.mailbox.folder'

    direct = [('name', 'name'),
              ('type', 'helpscout_type'),
              ('modified_at', 'backend_date_modified'),
              ]

    @mapping
    @only_create
    def odoo_id(self, record):
        # Searches project.task.type records for matching name
        stage = self.env['project.task.type'].search([
            ('name', '=', record.name),
        ])
        if stage:
            return {'odoo_id': stage.id}


class HelpScoutMailboxFolderImporter(Component):
    """Import one HelpScout record."""
    _name = 'helpscout.record.importer.mailbox.folder'
    _inherit = 'helpscout.importer'
    _apply_on = 'helpscout.mailbox.folder'


class HelpScoutMailboxFolderBatchImporter(Component):
    """Import a batch of HelpScout records."""
    _name = 'helpscout.batch.importer.mailbox.folder'
    _inherit = 'helpscout.direct.batch.importer'
    _apply_on = 'helpscout.mailbox.folder'