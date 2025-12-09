from odoo.tests.common import HttpCase


class TestExportAutoDataController(HttpCase):
    def test_save_field_picker_route(self):
        # Authenticate as admin
        self.authenticate(self.env.cr.dbname, "admin", "admin")
        # Create config
        model = self.env["ir.model"].search([("model", "=", "res.partner")], limit=1)
        config = self.env["auto.export.config"].create(
            {
                "name": "Controller Export",
                "model_id": model.id,
                "domain_filter": "[]",
                "email_to": "controller@example.com",
                "interval_type": "daily",
            }
        )
        # Call the controller route
        result = self.url_open(
            "/auto_export_data/save_field_picker",
            data={"config_id": config.id, "field_paths": ["name", "email"]},
            method="POST",
            headers={"Content-Type": "application/json"},
            json=True,
        )
        self.assertIn("ok", result.text)
        config.refresh()
        self.assertEqual(len(config.field_line_ids), 2)
