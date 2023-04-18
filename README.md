# Discovery API client instructions

This document contains instructions on how to use the client to get outputs from the National Archives' Discovery API.
<br>
## Prerequisites

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)

Install a version of Python => 3.7.9
<br>


## How to build the code and run the client

There are to ways to build and run the client.

### 1. Build a binary
[![w](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/en-gb/windows?r=1)

Double click `build.bat` which installs the packages and creates a binary `main.exe` file in a `dist` folder and starts the client. The packages can be installed before running the batch script with `pip install -r requirements.txt`. The `pip` may require more parameters if there is a reverse proxy server in place - see [Assumptions](#Proxy)

### 2. Build a container
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

Alternatively the application can by run as a Docker container with:

```console
docker pull domlove/discovery-api-client:latest
```
```console
docker run -t -i domlove/discovery-api-client:latest
```
This can also be used for non-Windows machines like MacOS that may not run windows executables.
<br>
<br>

## How to run the outputs

The client will take record id inputs in three formats:

* GUID with dashes `{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}` `x` = hex digit `(0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F)`
* GUID as above without dashes e.g. `5d1f135756bb4af287ed351e2696a7a5`
* IAID one of three letters `(C,D,N)` then a natural number `(1..*)`

An entered id that does not comply with the above will return `Info: wrong id format`

The outputs that can be sought from the Discovery API using the cli client are as follows:
<br>
<br>



### Title

A title is displayed for any record id that has a title.

Enter `25a2b713-c78d-4535-90cd-69cdd8a6885a`

Displays `Title: 'Software '71 and Software '72 Conferences`
<br>
<br>

### Scope Content Description 

A description is displayed for any record id that has no title and has a description.

Enter `N13867509`

Displays `Description: Meal and flour account, 1834; poor house minute book, 1849`
<br>
<br>


### Citable reference

A reference is displayed for any record that has no title, no description, and has a reference. 

e.g. using a mock id with test data

Enter `D53006911`

Displays `Citable Reference: AA 10/10/TEST 1/100`
<br>
In cases where no record output is returned from the Discovery API, either of the proceeding outputs will show:
<br>
<br>

### Not sufficient information  

A not sufficient information message is displayed for any record that has no title, no description, and no reference

e.g. using a mock id with test data

Enter `40e863e1-a723-492b-bcb3-89634b55cd82`

Displays `Info: not sufficient information`
<br>
<br>
### No record found  

A no record found message is displayed for any id that is not in the Discovery records collection.

Enter `D9252750`

Displays `Info: no record found`
<br>
<br>

## How to run the tests 

### Unit test 
[![tests](https://img.shields.io/badge/tests-11%20passed%2C%200%20failed-red)](https://www.python.org/)

Automated unit tests can be run with:

```console
python unit_tests.py
```

The first two tests intentionally throw exception errors to test producing a `*.log` file of potential errors in the `logs`folder relating to API connection errors and invalid local JSON files. 

The cli will provoide a prompt to continue the tests, passing together with an `OK` message.

### Integration test

To test the integration of the client in respect of `Citable reference` and `not sufficient information` outputs, test data in the `test_data` folder have been generated as:

* `display_not_sufficient_info.json`
* `display_reference.json`

The client can take the mock ids mentioned [above](#Not-sufficient-information) when `main.exe` is placed and run in __the root directory__.



## Assumptions

### Searching discovery

It is assumed that the following type of records for a given record are either rare or do not exist to be searched using the [Discovery API](https://discovery.nationalarchives.gov.uk/API/sandbox/index):

* Records with no title, no description, and a reference 
* Records with no title, no description, and no reference 

The Discovery API does not appear have `sps.` parameters to query `title`, `scopeContent. description`, and `citableReference` key-values that are `null`

Furthermore, it is assumed that there are at least three types of ids mentioned [above](#How-to-run-the-outputs) that can be taken by the Discovery API.

### Proxy

It is assumed that some users may be using a Windows OS behind a corporate proxy server which could block the package downloads. If this happens, these steps may resolve the issue:

1. Go to `Control Panel` > `System` > `Advanced System Settings` > `Environment Variables`, and in `System variables`:
    1. Add the Python install folder to `PATH` if it's not already present e.g.`C:\Program Files\Python37`
    2. Create two variables `HTTP_PROXY` and `HTTPS_PROXY` and set both to your corporate proxy ip address `http://X.X.X.X:X`
2. Open an admin command prompt and run
    
    ```console 
    python -m pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org install pip-system-certs
    ```
    ```console 
    python -m pip install --upgrade requests
    ```
3. The packages can now be installed with this command:

    ```console
    python -m pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org install -r requirements.txt --default-timeout=120
    ```
