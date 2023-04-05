param([String]$patchType)

Try
{

if($patchType.ToUpper() -eq 'ALL UPDATES')
{
$patchList=Get-WsusUpdate -Approval  Unapproved -Status Needed
}
elseif($patchType.ToUpper() -eq 'SECURITY UPDATES')
{
$patchList=Get-WsusUpdate -Approval  Unapproved -Status Needed | Where-Object -property Classification -EQ "Security Updates"

}
elseif($patchType.ToUpper() -eq 'CRITICAL UPDATES')
{
$patchList=Get-WsusUpdate -Approval  Unapproved -Status Needed | Where-Object -property Classification -EQ "Critical Updates"
}


if($patchList -eq $null)
{
Write-Output "No Updates Found"

}
else
{
Write-Output $patchList
}

}

Catch 
{
Write-Host "Something Went Wrong:$Error"

}