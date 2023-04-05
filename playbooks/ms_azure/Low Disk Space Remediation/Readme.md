# Low Disk Space Remediation
### Clear Windows Update cache and delete all logs (system, application, event, etc.) if a monitored disk's available free space drops below a specified threshold.

This use-case is broken down into three (3) workflows:
* Parent Workflow: Detect Low Disk Space
* Child Workflow 1: Clear Windows Update Cache
* Child Workflow 2: Clear Windows Logs

In the parent workflow (Detect Low Disk Space), modify the activities that use a specific host to point to the host which you'll be monitoring.  Additionally, modify the following variables to match your needs:
* monitorVolume (from setMonitorDisk activity): Change from default value of *C:* to the drive letter of your choice.
* diskUsageThreshold (from setUsageThreshold activity): Change from default value of "45" to the maximum usage threshold (in percent) of your choice.

In the first child workflow (Clear Windows Update Cache), modify the activities that use a specific host to point to the host which you'll be monitoring.  Additionally, modify the following variables to match your needs:
* winUpdateCacheFolder (from setCacheFolder activity): Change from default value of "C:\Windows\SoftwareDistribution\Download\" to the path where Windows Updates stores cached files on the system you'll be monitoring.

In the second child workflow (Clear Windows Logs), modify the activities that use a specific host to point to the host which you'll be monitoring.  Additionally, modify the following variables to match your needs:
* logFolder (from setLogFolder activity): Change from default value of "C:\Windows\System32\winevt\Logs\" to the path where Windows stores logs on the system you'll be monitoring.

The parent workflow (Detect Low Disk Space) will check the specified disk to see if it's current usage exceeds the specified threshhold.  If so, it will create a new incident containing information on the percentage of the disk currently being used and then execute the two (2) child workflows (Clear Windows Update Cache, Clear Windows Logs).  Next, it will determine if the disk space usage has dropped to fall within an acceptable range below the specified threshold.  If so, it will close the incident along with details regarding how much space was saved on the disk and how much of the disk is currently being used.  If not, it will update the incident along with details regarding how much space was saved on the disk and how much of the disk is currently being used.
