# -*- coding: utf-8 -*-

from odoo import models, fields, api

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