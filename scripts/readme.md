# Platform-specific Playbook 2 CACAO

## Requirements
```
Python >=3.10
```
## Installation
```shell
pip install -r requirements.txt
```

## Usage 
```shell
python playbook{schema|analysis}.py -v PLATFORM -p PATH -l LOG-LEVEL
```
```
-   -v | --platform: The origin of the playbooks (SOAR platform), e.g., xsoar.
-   -p |--path: Path to a file or directory of playbooks.
-   -l | --log-level: Log level (INFO|DEBUG).
```
## Example
```shell
python .\playbook{schema|analysis}.py -v xsoar -p "..\playbooks\cortex" -l DEBUG
```
