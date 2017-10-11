# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    @api.model
    def get_users(self, stages, domain, order):
        _logger.info(stages)
        return [('random', 'Random'), ('fixed', 'Fixed')], {'random': True, 'fixed': True}
    
    
    class_type = fields.Selection([
        ('papus', 'Papu'),
        ('elfas', 'Elfa')
    ], string="Papu/Elfa", default="papus")
    
    
    @api.model
    def create(self, vals):
        ''' Store the initial standard price in order to be able to retrieve the cost of a product template for a given date'''
        # TDE FIXME: context brol
        _image = vals.get('image_medium')
        tools.image_resize_images(vals)
        vals['image'] = _image
        
        template = super(ProductTemplate, self).create(vals)
        if "create_product_product" not in self._context:
            template.with_context(create_from_tmpl=True).create_variant_ids()

        # This is needed to set given values to first variant after creation
        related_vals = {}
        if vals.get('barcode'):
            related_vals['barcode'] = vals['barcode']
        if vals.get('default_code'):
            related_vals['default_code'] = vals['default_code']
        if vals.get('standard_price'):
            related_vals['standard_price'] = vals['standard_price']
        if vals.get('volume'):
            related_vals['volume'] = vals['volume']
        if vals.get('weight'):
            related_vals['weight'] = vals['weight']
        if related_vals:
            template.write(related_vals)
        return template
    
    def write(self, vals):
        _image = vals.get('image_medium')
        tools.image_resize_images(vals)
        vals['image'] = _image
        res = super(ProductTemplate, self).write(vals)
        if 'attribute_line_ids' in vals or vals.get('active'):
            self.create_variant_ids()
        if 'active' in vals and not vals.get('active'):
            self.with_context(active_test=False).mapped('product_variant_ids').write({'active': vals.get('active')})
        return res


class EpicControl(models.Model):
    _name = "epic.control"
    
    fixed_products = fields.Many2many('product.template', "rel_fixed_products")
    random_products = fields.Many2many('product.template', "rel_random_products")

# class epic(models.Model):
#     _name = 'epic.epic'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100