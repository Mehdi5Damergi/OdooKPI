{
    "name": "Auto Export to Excel by Schedule",
    "version": "19.0.0.0.1",
    "summary": "Admin-defined export of model data to Excel and email via cron",
    "author": "Synodica Solutions Pvt. Ltd.",
    "depends": ["base", "mail", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/auto_export_config_views.xml",
        "views/yandex_smtp_config_views.xml",
        "data/mail_template_auto_export.xml",
        "data/yandex_smtp_config.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "auto_export_data/static/src/js/form_view_extension.js",
            "auto_export_data/static/src/js/custom_button.js",
            "auto_export_data/static/src/js/field_picker_dialog.js",
            "auto_export_data/static/src/js/export_data_custom_dialog.js",
            "auto_export_data/static/src/xml/export_data_custom_dialog.xml",
        ],
    },
    "images": ["static/description/export_auto_data.gif"],
    "demo": [],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
