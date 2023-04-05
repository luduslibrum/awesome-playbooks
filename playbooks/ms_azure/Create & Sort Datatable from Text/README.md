# Create & Sort Data Table from Text
### Crreate & Sort Data Table from Text takes data from text file, convert it into string, then it's breaking the column names by delimiter comma and rows by spaces and placing the table into excel file by applying sorting on the basis of defined column.

This use-case has following major activities used in it:
* Read text from file Write Excel Sort Data table:
In the Read text from file activity, it is reading data from text file and giving the output data in the form of string.
*** Note: - Pass the location of text file as an input into the workflow. In the second activity of workflow, we are writing the text output into the virtual data table by applying some delimiters.

* Convert Text to Table:
In this activity, it is converting the output string from previous activity into the data table by passing some certain conditions like passing delimiters for columns and rows.
*** Note: -Delimiters can be changed as per the requirement while using the code.

* Sort Data table:
In the third activity of Workflow, we are applying sorting conditions on the columns of data table.
*** Note: we can provide the order of sorting as per the requirement.

* Write Excel:
In the fourth activity of workflow, we are appending the virtual data table into the excel file. This step can be removed as per the requirement that is if we want the output into some file ,we can use it otherwise we can completely ignore this step.
*** Note: - Pass the location of Excel file as an input into the workflow.

#### INPUT AND OUTPUT VARIABLE CAN BE PASSES IN THE STARTING OF THE WORKFLOW.
