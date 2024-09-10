License db auth:
- Go to settings > sales
- Enter the auth credentials in the "License OCAD" section

Create license:
- Open the sales order "S00021" and confirm it
- Click on the license link
- Reset the license to draft and enter a license number 60XXX
- Assign and activate the license
- Check if the license has been created successfully
- Click on the download link
- The executeable "OCAD_2020_Mapping_Solution_Setup.exe" should be download

Disable/enable license:
- Open the license created in the last step
- Click on deactivate
- The license is now locked
- Click reactivate
- The license is now enabled

Update end date:
- Change the end date
- Click on "update end date"
- The license end date should be updated

Mail subscription renewal:
- Open the sale order "S00021"
- Click on "Renew" and select "send by e-mail"
- Open the "send message" dialog
- Select the mail template "Sale: Subscription Renewal"
- Check if the generated mail is correct

Mail license unlock:
- Show the licenses
- Select license "L00004"
- Open the "send message" dialog
- Select the mail template "License: License Unlock"
- Check if the generated mail is correct

Mail license information:
- Open website and by the "software license"
- Open the sale order in the backend
- Check if license information mail has been sent

Mass mailing:
- Open the mail template "Sale: License Information"
- Enable the context menu
- Open the sale order "S00021"
