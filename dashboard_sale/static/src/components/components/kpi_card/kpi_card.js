/** @odoo-module */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class KpiCard extends Component {
    setup() {
        // Setup any required functionality
    }
    
    onClick() {
        if (this.props.onClick && this.props.domain) {
            this.props.onClick(this.props.domain);
        }
    }
    
    get valueStyle() {
        const style = {};
        if (this.props.textsize) {
            style.fontSize = this.props.textsize + 'px';
        }
        return style;
    }
}

KpiCard.template = "dashboard_sale.KpiCard";
KpiCard.props = {
    name: String,
    value: {type: [Number, String], optional: true},
    percentage: {type: [Number, String], optional: true},
    previous: {type: [Number, String], optional: true},
    domain: {type: Array, optional: true},
    onClick: {type: Function, optional: true},
    textsize: {type: Number, optional: true},
};

// Register the component
registry.category("components").add("dashboard_sale.KpiCard", KpiCard);