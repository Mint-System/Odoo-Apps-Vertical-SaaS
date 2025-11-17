Setup webshop:

- Install sale_subscription_disable_tokenization
- Enable the "Demo" payment provider
- Make pricelist "License Pricelist" selectable

Product purchase:

- Open the webshop site
- Add the product "Software License" to the cart
- Go through the checkout process and finish the purchase
- Open the confirmed sale order and check if license is created and activated

Product purchase:

- Configure the form and show the field `license_exists`
- Open the webshop site and buy the "Software License"
- Go through the checkout process and finish the purchase
- Open the confirmed sale order and check if licenses are created but not activated

Subscription purchase:

- Install the license_subscription module
- Add temporal sale config to the "Software License" product for a yearly recurrence
- Open the webshop and purchase the "Software License" fro one yearly
- Open the confirmed sale order and check if end date is today in one year
