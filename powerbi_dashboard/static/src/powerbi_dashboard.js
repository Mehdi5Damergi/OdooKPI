/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";

class PowerBIDashboard extends Component {
    static template = xml`
        <div class="o_powerbi_dashboard w-100 h-100">
            <iframe 
                src="https://app.powerbi.com/reportEmbed?reportId=748f776c-397f-4d45-8ecc-f4f8479c5384&amp;autoAuth=true&amp;ctid=04a5f3b7-1e3b-4a78-aec9-f9a66ae9726b" 
                style="width: 100%; height: 100vh; border: none;"
                title="Power BI Dashboard">
            </iframe>
        </div>
    `;
}

// Register the component in the actions registry (not client_actions)
registry.category("actions").add("powerbi_dashboard_embedded", PowerBIDashboard);