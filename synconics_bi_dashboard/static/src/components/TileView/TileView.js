/** @odoo-module **/

import { Component, onMounted, useEffect, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { TileLayoutOne } from "../TileLayouts/TileLayoutOne/TileLayoutOne";
import { TileLayoutTwo } from "../TileLayouts/TileLayoutTwo/TileLayoutTwo";
import { TileLayoutThree } from "../TileLayouts/TileLayoutThree/TileLayoutThree";
import { TileLayoutFour } from "../TileLayouts/TileLayoutFour/TileLayoutFour";

export class TileView extends Component {
  static template = "synconics_bi_dashboard.TileView";
  static components = {
    TileLayoutOne,
    TileLayoutTwo,
    TileLayoutThree,
    TileLayoutFour,
  };
  static props = {
    chartId: String,
    name: String,
    isDirty: { optional: true, type: Boolean },
    data: { optional: true, type: Object },
    update_chart: { optional: true, type: Function },
    theme: String,
    recordSets: Object,
  };

  setup() {
    this.state = useState({
      layout_type: "layout1",
      data: {},
      isError: false,
      errorMessage: false,
    });
    useEffect(
      () => {
        this.render_tile_view();
      },
      () => [
        this.props.chartId,
        this.props.recordSets,
        this.props.isDirty,
        this.props.data,
      ],
    );

    onMounted(() => {
      this.render_tile_view();
    });
  }

  render_tile_view() {
    let data = this.props.recordSets;
    
    // Handle case where data is undefined or null
    if (!data) {
      this.state.isError = true;
      this.state.errorMessage = "No data available for this chart";
      return;
    }
    
    // Handle error responses from backend
    if (typeof data == "object" && data.type && data.type === "error") {
      this.state.isError = true;
      this.state.errorMessage = data.message || "An error occurred while loading chart data";
      return;
    }
    
    // Handle case where data is an empty array
    if (Array.isArray(data) && data.length === 0) {
      this.state.isError = true;
      this.state.errorMessage = "No data available for this chart";
      return;
    }
    
    // Handle case where data is an array (unexpected)
    if (Array.isArray(data)) {
      this.state.isError = true;
      this.state.errorMessage = "Invalid data format received";
      return;
    }

    this.state.isError = false;
    this.state.layout_type = data.tile_layout_type || "layout1";
    this.state.data = data;
    this.render();
  }
}
