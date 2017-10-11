# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import WebClient, Binary, Home

import logging
import random
import json

_logger = logging.getLogger(__name__)


class EpicWeb(Home):
    @http.route('/', type='http', auth="public")
    def Home(self, **kw):
        
        products = request.env['product.template'].sudo()
        
        epic_control_obj = request.env['epic.control'].sudo()
        epic_rec = epic_control_obj.search([], limit=1)
        
        
        fix_product_ids = epic_rec.fixed_products.ids
        random_product_ids = epic_rec.random_products.ids
        
        random.shuffle(random_product_ids)
        random_product_ids = random_product_ids[:15]
        
        _logger.info(random_product_ids)
        
        product_obj = request.env['product.template'].sudo()
        
        products += product_obj.search([('id', 'in', fix_product_ids)], limit=20)
        products += product_obj.search([('id', 'in', random_product_ids)])
        
        search_product = list(products)
        random.shuffle(search_product)
        
        return request.render('epic.homepage', {
            'products': search_product
        })
        


# class Epic(http.Controller):
#     @http.route('/epic/epic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/epic/epic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('epic.listing', {
#             'root': '/epic/epic',
#             'objects': http.request.env['epic.epic'].search([]),
#         })

#     @http.route('/epic/epic/objects/<model("epic.epic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('epic.object', {
#             'object': obj
#         })