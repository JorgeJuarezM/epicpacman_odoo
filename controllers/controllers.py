# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import WebClient, Binary, Home

import logging
import random
import json
import base64
import io
import imghdr

_logger = logging.getLogger(__name__)


class EpicWeb(Home):
    
    @http.route('/images/<int:product_id>', type='http', auth="public")
    def images(self, product_id):
        
        product = request.env['product.template'].browse([product_id])
        imgname = 'logo'
        imgext = '.png'
                   
        image_base64 = base64.b64decode(product.image)
        image_data = io.BytesIO(image_base64)
        imgext = '.' + (imghdr.what(None, h=image_base64) or 'png')
        response = http.send_file(image_data, filename=imgname + imgext)
        return response
    
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
        
        products = []
        
        for p in search_product:
            products.append({
                'id': p.id,
                'price': p.list_price,
                'description': p.description_picking,
                'description_sale': p.description_sale,
                'name': p.name,
                'class_type': p.class_type
            })
        
        return request.render('epic.homepage', {
            'products': products
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