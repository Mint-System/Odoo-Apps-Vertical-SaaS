# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-09-20

### Added

- Add product information attributes to team license demo data

### Changed

- License start and end date will not set to false on a state reset
- Status cancelled no longer visible in statusbar
- Check pricelist on renew server action
  <https://www.odoo-wiki.org/subsciption-actions.html#abonnemente-vor-abrechnung-verlangern>
- Update dependencies for license_sale
- On sale order line chancel or unlink check if parent line exists before changing the
  line
- Show field license_exists on sale form
- Update translation for license_website_sale
- Add demo data for pricelist item
- Change data order in license module
- Show runtime field on license form
- Make sure runtime is editable
- Added help to runtime field
- 

### Removed

- The button "Update Enddate" has been removed
- Remove start date in license information mail template
