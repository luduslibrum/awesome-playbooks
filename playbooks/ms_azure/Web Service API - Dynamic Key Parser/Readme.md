<h1>Web Service API - Dynamic Key Parser</h1>
<br>
This workflow is designed to be triggered when any incoming Web Service API event is received by Ayehu NG.  Although each key-value pair from the incoming event can be referenced directly in the workflow (e.g. %nameFirst% for the "nameFirst" key), each of the keys and their respective values can also be dynamically parsed from the payload received.
<br><br>
In this example, there’s a MemorySet activity storing a sample from the “Raw” field from an incoming Web Service API event.  If you configure your trigger to execute this workflow, it will automatically read that “Raw” field on-the-fly.  However, the MemorySet activity at the top of this sample workflow will need to be disabled so it does not overwrite the value of "Raw".
<br><br>
As seen in the workflow, the next step is to convert the key-value pairs in the XML to a table.  Then, loop through each column and extract the column name for the “key name”, and the column’s value for the “key value”.
<br><br>
The ReplaceString and DeleteMemoryTableColumns activities are used to remove unwanted keys from the XML before being converted to a table.
