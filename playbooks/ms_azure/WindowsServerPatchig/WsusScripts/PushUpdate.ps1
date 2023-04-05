param([String]$patchType,[String]$ComputerGroupName)


Try
{

if($patchType.ToUpper() -eq 'ALL UPDATES')
{
$AllUpdate=Get-WsusUpdate -Approval  unapproved -Status  Needed | Approve-WsusUpdate -Action Install  -TargetGroupName $ComputerGroupName
}

else
{
$CustomUpdate=Get-WsusUpdate -Approval  Unapproved -Status Needed | Where-Object -property Classification -EQ $patchType | Select-Object -First 1 | Approve-WsusUpdate -Action Install  -TargetGroupName $ComputerGroupName
}

}

Catch
{

Write-Host "Failed To push Update on client:$Error"

}