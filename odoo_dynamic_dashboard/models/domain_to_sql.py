# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Bhagyadev KP (odoo@cybrosys.com)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
################################################################################
from odoo import models, fields


def get_query(self, args, operation, field, start_date=None, end_date=None,
              group_by=False, apply_ir_rules=False):
    """ Dashboard block Query Creation """
    # Convert domain to SQL WHERE clause
    # Handle case where args might be a string instead of a list
    if isinstance(args, str):
        # Try to evaluate string as a Python expression (list)
        try:
            from ast import literal_eval
            args = literal_eval(args)
        except:
            # If evaluation fails, treat as empty domain
            args = []
    
    if args:
        # Handle complex domain structures from expression.AND
        if isinstance(args, list) and len(args) > 0 and isinstance(args[0], list):
            # Flatten the domain if it's nested
            flat_args = []
            for item in args:
                if isinstance(item, list):
                    flat_args.extend(item)
                else:
                    flat_args.append(item)
            args = flat_args
        
        where_parts = []
        where_params = []
        for arg in args:
            # Skip domain operators
            if isinstance(arg, str) and arg in ['&', '|', '!']:
                continue
            # Handle standard domain tuples
            if isinstance(arg, (list, tuple)) and len(arg) == 3:
                # Qualify column names with table name to avoid ambiguous references
                column = arg[0]
                # Make sure column is a string before checking for dots
                if isinstance(column, str):
                    # If the column doesn't already contain a table prefix, add the main table prefix
                    if '.' not in column:
                        column = f'"{self._table}".{column}'
                    where_parts.append(f"{column} {arg[1]} %s")
                else:
                    # If column is not a string, use it as is
                    where_parts.append(f"{column} {arg[1]} %s")
                where_params.append(arg[2])
            # Handle leaf expressions
            elif isinstance(arg, (list, tuple)) and len(arg) > 0:
                # For now, skip complex expressions
                continue
        where_clause = " AND ".join(where_parts) if where_parts else "1=1"
    else:
        where_clause = "1=1"
        where_params = []
    if operation and field:
        data = 'COALESCE(%s("%s".%s),0) AS value' % (
            operation.upper(), self._table, field.name)
        join = ''
        group_by_str = ''
        # ✅ Handle product_id case → product_product → product_template
        if group_by and group_by.name == 'product_id':
            model_name = self._name
            field_relation = self.env[model_name]._fields.get('product_id')
            if isinstance(field_relation,
                          fields.Many2one) and field_relation.comodel_name == 'product.product':
                # Join product_product and product_template
                join += """
                           INNER JOIN product_product ON product_product.id = "%s".product_id
                           INNER JOIN product_template ON product_template.id = product_product.product_tmpl_id
                       """ % self._table
                # Use product_template.name instead of product_product.name
                data += ', product_template.name AS product_name'
                group_by_str = ' GROUP BY product_template.name'
        # ✅ Handle categ_id case → product_template → product_category
        elif group_by and group_by.name == 'categ_id':
            model_name = self._name
            field_relation = self.env[model_name]._fields.get('product_id')
            if isinstance(field_relation,
                          fields.Many2one) and field_relation.comodel_name == 'product.product':
                # Join product_product, product_template, and product_category
                join += """
                           INNER JOIN product_product ON product_product.id = "%s".product_id
                           INNER JOIN product_template ON product_template.id = product_product.product_tmpl_id
                           INNER JOIN product_category ON product_category.id = product_template.categ_id
                       """ % self._table
                # Use product_category.complete_name instead of product_product.name
                data += ', product_category.complete_name AS categ_name'
                group_by_str = ' GROUP BY product_category.complete_name'
        elif group_by:
            if group_by.ttype == 'many2one':
                relation_model = group_by.relation.replace('.', '_')
                # Special handling for res_users to join with res_partner
                if group_by.relation == 'res.users':
                    # Only add the join if it's not already present
                    if f'LEFT JOIN {relation_model} on "{relation_model}".id = "{self._table}".{group_by.name}' not in join:
                        join += ' LEFT JOIN %s on "%s".id = "%s".%s' % (
                            relation_model, relation_model, self._table, group_by.name)
                    # Only add the res_partner join if it's not already present
                    # Use a unique alias for res_partner to avoid duplicate alias errors
                    res_partner_alias = f'res_partner_{group_by.name}'
                    if f'LEFT JOIN res_partner {res_partner_alias} on {res_partner_alias}.id = {relation_model}.partner_id' not in join:
                        join += ' LEFT JOIN res_partner %s on %s.id = %s.partner_id' % (res_partner_alias, res_partner_alias, relation_model)
                    data = data + ',%s.name AS %s_name' % (res_partner_alias, group_by.name)
                    group_by_str = ' GROUP BY %s.name' % res_partner_alias
                else:
                    # Only add the join if it's not already present
                    if f'LEFT JOIN {relation_model} on "{relation_model}".id = "{self._table}".{group_by.name}' not in join:
                        join += ' LEFT JOIN %s on "%s".id = "%s".%s' % (
                            relation_model, relation_model, self._table, group_by.name)
                    rec_name = self.env[group_by.relation]._rec_name_fallback()
                    data = data + ',"%s".%s AS %s_name' % (
                        relation_model, rec_name, group_by.name)
                    group_by_str = ' GROUP BY "%s".%s' % (relation_model, rec_name)
            else:
                data = data + ',"%s".%s' % (self._table, group_by.name)
                group_by_str = ' GROUP BY "%s".%s' % (
                    self._table, str(group_by.name))
    else:
        data = '"%s".id' % (self._table)
    where_str = where_clause and (" WHERE %s" % where_clause) or ''
    if start_date and start_date != 'null':
        start_date_query = f' AND ("%s"."create_date" >= \'{start_date}\')' % self._table
    else:
        start_date_query = ''
    if end_date and end_date != 'null':
        end_date_query = f' AND ("%s"."create_date" <= \'{end_date}\')' % self._table
    else:
        end_date_query = ''
    query_str = 'SELECT %s FROM "%s" ' % (data, self._table) + join + where_str + start_date_query + end_date_query + group_by_str

    def format_param(x):
        if not isinstance(x, tuple):
            return "'" + str(x) + "'"
        elif isinstance(x, tuple) and len(x) == 1:
            return "(" + str(x[0]) + ")"
        else:
            return str(x)

    exact_query = query_str % tuple(map(format_param, where_params))
    return exact_query


models.BaseModel.get_query = get_query
