def migrate(cr, version):
    """
    Migration script to assign all existing charts to "My Dashboard"
    """
    # This script will be run after the module is upgraded
    # It will automatically assign all existing charts to "My Dashboard"
    
    # Import required modules
    from odoo import api, SUPERUSER_ID
    
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Get or create the "My Dashboard"
    my_dashboard = env['dashboard.dashboard'].get_or_create_my_dashboard(env.user)
    
    # Add all existing charts to this dashboard
    my_dashboard.action_add_all_charts_for_user()