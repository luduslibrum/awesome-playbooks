# Windows Server Patching

## Automated Server patching Using Ayehu and powershell script

### Prequisite 
* Links For Download the mentioned packages

* PswindowsUpdate : https://gallery.technet.microsoft.com/scriptcenter/2d191bcd-3308-4edd-9de2-88dff796b0bc
* ImportExcel : https://www.powershellgallery.com/packages/ImportExcel/5.4.2
* in Package folder above package is placed  you can directly move that both folder to C:\Windows\System32\WindowsPowerShell\v1.0\Modules

* 1.Wsus Server Required where all Server is enrolled for getting new patches which is released y microsoft 
* 2.PsWindowsUpdate Powershell Module Required On target Server
* 3.For Reporting :ImportExcel 5.4.2 is required on Ayehu Server
* 4.Windows Service Account with admin privillege
* 5.Create folder on c drive : ConnectionFailedLog,NoUpdateLog,PatchReport,logs  if you want to place those folder on other drives you need to change path in workflow.
* 6.put ServerList Folder in C drive : ServerList Folder Consist 3 csv file which has server entry accoriding to there group, Make sure that csv file name is same as your wsus group name .
* 7.Put WsusScript folder to C drive if you want to place in other drive please change path in workflow too.


##### Problem Statement :

To automate installation of updates and patches in multiple Windows Servers in different environments i.e (Test, Dev & Prod), along with generating a report.

Solution:

Using Powershell a couple of automation bots (Updater & Reporter) was developed, whose task is to generate the scripts for updation and reporting, Install the updates, reboot the VM after installation, post installation sending the reports, consolidating them and performing the cleanup activities. The automation bots follow RPA guidelines to get the tasks done. This is the time where traditional automation got integrated with RPA to complete the task.


#### Some Important Notes:

*  For each environment let say Dev, Test, Prod a Dev.csv,Test.csv,Prod.csv file maintained where server entry is present according to the group ,let say if a server is enrolled in wsus in dev group then we have to add that server name into our dev.csv file . so edit that file according to your requirement.
*  For getting reports 3 folder is created on ayehu server during automation workflow execution , so named accoriding to your choice or you are okay with the name then just create those folders on specified location .


### How Automated Patching Works Using Ayehu.

To Trigger this solution as of now a service now incident is use and i have integrated with ayehu but in production go with change module and simillar kind of form will be used to take input .

*  From incident Short description and description field ayehu workflow takes valuable information from that is which patch to be pushed and on which group of server it has to pushed.

example: Description: Patch Windows on Prod
         Short Description : Security Updates
		 
so once service now tickets has above information based on policy action it will get triggered and in above example it will push security updates to prod group 
simillar way if short description contains Critical Updates then critical updates were pushed and Description contains Dev or Test then that means ayehu start reading server names from correspondate csv file .

Policy Action :

Short description Contains: Patch Windows On
Assingnment Group: in my case it is different 
State:New


* once tickets is submitted then ayehu will read short description and description field and based on that patching will start on mentioned group and mention patche will pushed 

*  After mentioned patch is pushed through wsus using workflow activity ayehu will wait for few minutes to refect those patches on target server

*  then it will be get checked is there any upated on target server if update availabel then patching started and on completion rebooting is also done and  all reporting is done .

*  if no update found then that server entry goes in log file 

*  if communictaion error happen durig patching again that servere entry goes in a separte log.

*  So if all validation pass then only patching will started on target server and a report is created for that in PatchReport folder 

* After Report creation workflow will attach this report to incident.

* so overall this workflow is doing all end to end process form pushing patch to target server, Installing that patch to target server ,Rebooting the server,Report generation for target server .


##Note:

* Along with workflow please find spwecified folder for script and if needed please change according to your requirement
* In cs Servelist folder ,csv file is placed edit according to your environment.