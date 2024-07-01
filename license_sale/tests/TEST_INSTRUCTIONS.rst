One license:
- Open sale order "S00021"
- Confirm the sale order
- Check if 1 license entry has been created

Increase license:
- Open confirmed sale order "S00021"
- Set quantity to 2
- Check if there are 2 licenses

New so line:
- Open confirmed sale order "S00021"
- Add new line with product "Software License"
- Check if there are 3 licenses

Duplicate order:
- Open confirmed sale order "S00021"
- Duplicate the order
- Confirm the new order
- Check if an error is thrown because due to missing customer ref
- Enter a new ref and confirm the order
- Check if there are 3 licenses

Product switch:
- Open sale order "S00022"
- Confirm the sale order
- Replace the product with "Software License (Team)"
- Open the first license and check if product is the same
