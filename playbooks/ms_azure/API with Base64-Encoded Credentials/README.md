# API with Base64-Encoded Credentials

Simple template to demonstrate how to base64-encode a string containing login credentials to be used with an API, such as ZenDesk. Note that there are many APIs that require the username and password combination to be transmitted in this format. This is achieved by utilizing the following PowerShell code:

```
[string]$string_plaintext = "%login_credentials%"
$string_encoded = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($string_plaintext))
echo $string_encoded
```

...where the original username/password combination stored in the Workflow variable `login_credentials` (username:password) is stored in the PowerShell code as `string_plaintext`, and `string_encoded` stores those credentials in base64.

This template continues by showing an interaction with an API by using the `HTTPRequest` activity, in this case the one provided by ZenDesk. Here, we send the base64-encoded credentials in the header as the value of the `Authorization` parameter. This value is as follows:

`Basic %login_credentials%`

...where `Basic` is a static portion of this parameter and `login_credentials` contains the base-64 encoded credentials we created with the PowerShell code. The template continues by showing the JSON results being stored and converted into a table.

Note that this WorkFlow template will not function unless you have an active ZenDesk login, which must replace the placeholder values currently specified in the `store_credentials` activity.  Furthermore, the organization ID specified in the `http_request` activity must be replaced with a valid ID from your own account in order to see results returned from the API call.
