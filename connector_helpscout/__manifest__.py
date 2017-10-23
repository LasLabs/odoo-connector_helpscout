# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# pylint: disable=C8101
{
    "name": "HelpScout Connector",
    "summary": "Two way synchronization with HelpScout",
    "version": "10.0.1.0.0",
    "category": "Connector",
    "website": "https://github.com/LasLabs/odoo-connector_helpscout.git",
    "author": "LasLabs",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": ['helpscout'],
    },
    "depends": [
        "base_web_hook",
        "connector",
        "partner_firstname",
        "project",
        "queue_job",
        "sales_team",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/helpscout_security.xml",
        "views/helpscout_backend_view.xml",
        "views/helpscout_mailbox_folder_view.xml",
        "views/helpscout_web_hook_view.xml",
        "views/connector_menu.xml",
    ],
}
