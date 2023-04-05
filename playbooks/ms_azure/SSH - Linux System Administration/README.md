# Common Linux Sys. Admin. Tasks over SSH

The target server for these templates is an Ubuntu 18.04 installation running within the Windows Subsystem for Linux for Windows 10.  This WSL instance is running on the same host as the Ayehu NG Server.  Adjust as needed.

Each template contains a brief description, along with a more detailed form of documentation which also contains a break-down of each command utilized for each Activity.  A note has also been attached to each Activity to explain its function.  To see more about how each Workflow operates, check the Documentation section for each.

The current templates are as follows:

## SSH – Linux - Uptime
Simple template to retrieve target machine's uptime. Note that uptime is read directly from `/proc/uptime` and parsed to output results in HH:MM:SS format.

This is achieved with the following command:

`awk '{print int($1/3600)":"int(($1%3600)/60)":"int($1%60)}' /proc/uptime`

...where `awk` takes the first column from `/proc/uptime` and divides its value accordingly in order to calculate hours, minutes, and seconds.

## SSH – Linux – Memory Info
Simple template to retrieve all available system memory information from a target machine via `/proc/meminfo`. Results are converted to a table with two columns (**Type** and **Size** [in kilobytes]). Example rows include total memory, available memory, etc.

This is achieved with the following command:

`awk '{ print $1"|",$2,$3 }' /proc/meminfo | sed 's/://g'`

...where `awk` is used to put a pipe character between the first two columns in order to be used a delimiter when converted to a table with the type **Type** and **Size** columns, respectively. The third column processed by `awk` is the unit of measurement and is appended to the **Size** column on the table. Lastly, `sed` is used to remove the colon (:) from results. These results are then converted into a table.

## SSH – Linux – Disk Usage
Simple template to retrieve the usage of all available disks and mount-points in a target machine via the `df` command. The results are then converted into a table with columns for filesystem type, disk size, disk used, available disk, percentage of disk used, and mount-point.

This is achieved with the following command:

`df -h | awk '{print $1"|",$2"|",$3"|",$4"|",$5"|",$6}'`

...where the `-h` flag for `df` prints sizes in powers of 1024 (considered human-readable) and its results are piped to `awk` in order to add pipe characters between columns to be used as as delimiter. These results are then converted into a table.

## SSH – Linux – Process
Simple template to retrieve a count of all running processes on a target machine via the `top` command. Results are converted into a table with five columns (**Total**, **Running**, **Sleeping**, **Stopped**, and **Zombie**).

This is achieved with the following command:

`top -n 1 | grep Tasks | awk '{ print "Total|"$2"\nRunning|"$4"\nSleeping|"$6"\nStopped|"$8"\nZombie|"$10 }'`

...where the `-n 1` flag for `top` allows the program to exit after one iteration, rather than be ran in its default interactive mode. The output is then piped to `grep` to filter the line containing the string *Tasks*. That output is finally piped to `awk` where custom labels are used for the first column of each row (i.e. **Total**, **Running**, etc.) and a pipe character is added before the second column on each row to act as a delimiter. These results are then converted into a table.

## SSH – Linux – List Processes
Simple template using the `ps` command to retrieve a list of all running processes. The results are converted to a table with ten columns (**USER**, **PID**, **%CPU**, **%MEM**, **VSZ**, **RSS**, **TTY**, **STAT**, **START**, **TIME**, and **COMMAND**).

This is achieved with the following command:

`ps aux | awk '{ print $1"|"$2"|"$3"|"$4"|"$5"|"$6"|"$7"|"$8"|"$9"|"$10"|"$11 }'`

...where `ps` is executed with the `aux` flags to see all process details (called *BSD style*) and pipe output to `awk` where all 11 columns are separated by a pipe character.

## SSH – Linux – CPU Info
Simple template using the `top` command to retrieve various forms of CPU usage in terms of percentage. The results are converted to a table with four columns (**User**, **System**, **Nice**, and **Idle**).

This is achieved with the following command:

`top -n 1 | grep Cpu | awk '{ $1=""; print $0 }' | awk '{ print "User|"$1"%\nSystem|"$3"%\nNice|"$5"%\nIdle|"$7"%" }'`

...where the `-n 1` flag for `top` allows the program to exit after one iteration, rather than be ran in its default interactive mode. The output is then piped to `grep` to filter the line containing the string *Cpu*. That output is finally piped to `awk` where the first column is ignored, piped to `awk` again where custom labels are used for the first column of each row (i.e. **User**, **System**, etc.) and a pipe character is added before the second column on each row that printed to act as a delimiter. These results are then converted into a table.

## SSH – Linux – Service Status
Simple template using the `service` command to query the status of all available system services.

This is achieved with the following command:

`service --status-all 2> /dev/null | sed 's/\[ - \]/Down/g' | sed 's/\[ + \]/Up/g' | awk '{ print $2"|"$1 }'`

...where the `--status-all` flag returns a list of system services and their corresponding statuses. The `2> /dev/null` redirect ignores `STDERR` output. The results are then piped to a series of `sed` commands that replace the `[ + ]` and `[ - ]` values with `Up` and `Down`, respectively.  The results are then finally piped to `awk` where the second column is printed before the first column and a pipe character is added between each to be used a delimiter. These results are then converted into a table.
