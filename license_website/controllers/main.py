from odoo import _, http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class LicensePortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'license_count' in counters:
            model = request.env['license.license']
            values['license_count'] = (
                model.search_count([])
                if model.check_access_rights('read', raise_exception=False)
                else 0
            )
        return values

    def _license_get_page_view_values(self, license, access_token, **kwargs):
        values = {
            'page_name': 'Licenses',
            'license': license,
        }
        return self._get_page_view_values(
            license, access_token, values, 'my_licenses_history', False, **kwargs
        )

    def _get_filter_domain(self, kw):
        return []

    @http.route(
        ['/my/licenses', '/my/licenses/page/<int:page>'],
        type='http',
        auth='user',
        website=True,
    )
    def portal_my_licenses(
        self, page=1, date_start=None, sortby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        license_obj = request.env['license.license']
        
        # Avoid error if the user does not have access.
        if not license_obj.check_access_rights('read', raise_exception=False):
            return request.redirect('/my')

        domain = self._get_filter_domain(kw)

        searchbar_sortings = {
            'date_start': {'label': _('Date Start'), 'order': 'date_start desc'},
            'name': {'label': _('Name'), 'order': 'name desc'},
        }

        # Default sort by order
        if not sortby:
            sortby = 'date_start'
        order = searchbar_sortings[sortby]['order']
        
        # Count for pager
        license_count = license_obj.search_count(domain)
        
        # Pager
        pager = portal_pager(
            url='/my/licenses',
            url_args={
                'date_start': date_start,
                'sortby': sortby,
            },
            total=license_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        licenses = license_obj.search(
            domain, order=order, limit=self._items_per_page, offset=pager['offset']
        )

        request.session['my_licenses_history'] = licenses.ids[:100]
        values.update(
            {
                'date_start': date_start,
                'licenses': licenses,
                'page_name': 'Licenses',
                'pager': pager,
                'default_url': '/my/licenses',
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
            }
        )
        return request.render('license_website.portal_my_licenses', values)

    @http.route(
        ['/my/license/<int:license_id>'],
        type='http',
        auth='public',
        website=True,
    )
    def portal_my_license_detail(self, license_id, access_token=None, **kw):
        try:
            license_sudo = self._document_check_access(
                'license.license', license_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._license_get_page_view_values(license_sudo, access_token, **kw)
        return request.render('license_website.portal_license_page', values)
