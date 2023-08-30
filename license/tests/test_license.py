from odoo.tests import TransactionCase

class test_license(TransactionCase):
    def test_action_assign(self):
        rec = self.env['license.license'].create({
            'name': 'L00001',
            'key': 'GUZK-GFKD-YNAK-72OM',
            'product_id': self.env.ref('product.product_product_2').id,
            'partner_id': self.env.ref('base.res_partner_2').id,
        })
        rec.action_assign()
