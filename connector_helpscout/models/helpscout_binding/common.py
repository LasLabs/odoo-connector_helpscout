# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields
from odoo.addons.queue_job.job import job


class HelpscoutBinding(models.AbstractModel):
    """Abstract model for all HelpScout binding models.

    All binding models should `_inherit` from this. They also need to declare
    the ``odoo_id`` Many2One field that relates to the Odoo record that the
    binding record represents.
    """

    _name = 'helpscout.binding'
    _inherit = 'external.binding'
    _description = 'HelpScout Binding Abstract'

    # ``odoo_id`` needs to be declared in concrete model
    backend_id = fields.Many2one(
        string='Backend',
        comodel_name='helpscout.backend',
        default=lambda s: s.env['helpscout.backend'].default_exporter,
        ondelete='restrict',
        required=True,
    )
    backend_date_created = fields.Datetime(
        help='Date that record was created on remote (created_at).',
    )
    backend_date_modified = fields.Datetime(
        help='Date that record was modified on remote (modified_at).',
    )
    sync_date = fields.Datetime(
        help='Indicates last time this record was synced.',
    )
    external_id = fields.Integer(
        string='HelpScout ID',
    )

    _sql_constraints = [
        ('backend_id_external_id_unique',
         'UNIQUE(backend_id, external_id)',
         'A binding already exists for this HelpScout record.'),
    ]

    @api.model
    @job(default_channel='root.helpscout')
    def import_batch(self, backend, filters=None):
        """Prepare the import of records modified in HelpScout."""
        if filters is None:
            filters = {}
        with backend.work_on(self._name) as work:
            importer = work.component(usage='batch.importer')
            return importer.run(filters=filters)

    @api.model
    def import_direct(self, backend, external_record):
        """Directly import a data record."""
        with backend.work_on(self._name) as work:
            importer = work.component(usage='record.importer')
            return importer.run(
                external_record.id,
                external_record=external_record,
                force=True,
            )

    @api.model
    @job(default_channel='root.helpscout')
    def import_record(self, backend, external_id, force=False):
        """Import a HelpScout record."""
        with backend.work_on(self._name) as work:
            importer = work.component(usage='record.importer')
            return importer.run(external_id, force=force)

    @api.multi
    @job(default_channel='root.helpscout')
    def export_record(self, fields=None):
        self.ensure_one()
        with self.backend_id.work_on(self._name) as work:
            exporter = work.component(usage='record.exporter')
            return exporter.run(self, fields)

    @api.model
    @job(default_channel='root.helpscout')
    def export_delete_record(self, backend, external_id):
        """Delete a record on HelpScout."""
        with backend.work_on(self._name) as work:
            deleter = work.component(usage='record.exporter.deleter')
            return deleter.run(external_id)
