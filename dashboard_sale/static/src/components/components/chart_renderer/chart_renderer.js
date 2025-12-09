/** @odoo-module */

import { Component, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { registry } from "@web/core/registry";

export class ChartRenderer extends Component {
    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;
        
        onMounted(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            this.renderChart();
        });
        
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }
    
    renderChart() {
        if (!this.canvasRef.el) return;
        
        const ctx = this.canvasRef.el.getContext('2d');
        const config = this.props.config || { data: { labels: [], datasets: [] } };
        
        // Destroy existing chart if it exists
        if (this.chart) {
            this.chart.destroy();
        }
        
        // Get chart type and remove quotes
        const chartType = this.props.type.replace(/'/g, '');
        
        // Create new chart based on type
        this.chart = new Chart(ctx, {
            type: chartType,
            data: config.data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: this.props.title ? this.props.title.replace(/'/g, '') : ''
                    }
                }
            }
        });
    }
}

ChartRenderer.template = "dashboard_sale.ChartRenderer";
ChartRenderer.props = {
    type: String,
    title: {type: String, optional: true},
    config: {type: Object, optional: true},
};

// Register the component
registry.category("components").add("dashboard_sale.ChartRenderer", ChartRenderer);