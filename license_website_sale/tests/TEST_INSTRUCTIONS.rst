Product purchase:
- Enable the "Demo" payment provider
- Enable "additional step in checkout"
- Configure the form and set reference to required
- Open the webshop site
- Add the product "Software License" to the cart
- Go through the checkout process and finish the purchase
- Open the confirmed sale order and check if license is created and activated

Product purchase:
- Configure the form and show the field `licenses_already_exist`
- Open the webshop site and buy the "Software License"
- Go through the checkout process and finish the purchase
- Open the confirmed sale order and check if licenses are created but not activated

Subscription purchase:
- Install the license_subscription module
- Add temporal sale config to the "Software License" product for a yearly recurrence
- Open the webshop and purchase the "Software License" fro one yearly
- Open the confirmed sale order and check if end date is today in one year
