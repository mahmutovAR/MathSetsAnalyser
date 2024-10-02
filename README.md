# MathSetsAnalyser

This script analyzes the **math sets** in two modes: **INTERSECTION** and **AFFILIATION**.  
The main parameters are specified in the **configuration file**.  
The initial **math sets** are entered into the script via **data file**.  
The result of the script is the **output file**.
***


### Mode `INTERSECTION` (`INTS` in `config.ini`) analyzes the math sets.
Script returns the intersection of the initial **math sets**.

### Mode `AFFILIATION` (`AFFL` in `config.ini`) analyzes the math sets and predetermined point.
Script returns the predetermined **point**, if it belongs to the initial **math sets intersection**,  
or the closest endpoint(s) to the predetermined **point** otherwise.
***


## Installation
* [Python](https://www.python.org/downloads/) (3.12)  
 
The Python packages can be installed by running  
```commandline
python3 -m pip install -r requirements.txt
```
***


## Quick Start Guide
1. Run the `create_sample.py` script.  
    It will create the `config.ini` sample configuration file and the `data file.txt` file with sample data.
2. Then, run the `run_math_sets_analyser.py` script.  
    A new file `script_result.xml` will be created that contains the calculation results.
***


## Running MathSetsAnalyser
For math analysis of input data **as a script**:
* create `config.ini`   
* create data file with initial math sets  
* run `python run_math_sets_analyser.py`  


### To test MathSetsAnalyser run
```commandline
pytest
```
***


### The configuration file `config.ini` has the following structure:
`[general]`  
analysis mode: `INTS` or `AFFL`  
point (for `AFFL` mode only)  

`[input]`  
type of the data file: `JSON` `TXT` `XML`  
path to the data file

`[output]`  
type of the output file: `JSON` `TXT` `XML`  
path to the output file (including name of the file)

### Example of `config.ini` for `INTERSECTION` mode
```
[general]
mode = INTS

[input]
format = TXT
path = ../data files/input math sets

[output]
format = XML
path = ../script output files/result.xml
```

### Example of `config.ini` for `AFFILIATION` mode
```
[general]
mode = AFFL
point = 1.247

[input]
format = JSON
path = ../data files/input math sets

[output]
format = TXT
path = ../script output files/result
```
***

### The data file contains the initial math sets.

Each initial **math set** is given as `list` of ranges and points.  
The **math range** is given as `tuple` and **math point** is given as `int` or `float`  
The `-inf` is given as `float('-inf')`  
The `+inf` is given as `float('inf')`  
**Note:** For `JSON` data file initial **math set** is given as `str` object. So check the use of `' '` and `" "`

Examples of initial **math sets** for `TXT` and `XML` data file:  
`[(float("-inf"), -10.02), (10.97, float("inf"))]`  
`[(float('-inf'), -41), -18, (51, 62.01), 77.34, (103.0,  float('inf'))]`  
`[(-89, -61), (61, 72)]`  
`[14.021]`

Examples of initial **math sets** for `JSON` data file:    
`"[(float('-inf'), -10.02), (10.97, float('+inf'))]"`  
`"[float(('-inf'), -41), -18, (51, 62.01), 77.34, (103.0,  float('inf'))]"`  
`"[(-89, -61), (61, 72)]"`  
`"[14.021]"`

### Example of `JSON` data file
```
[
	"[float(('-inf'), -132), -89.61, (-24, float('inf'))]",
	"[(-43, -12), (10, 27)]"
]
```

### Example of `TXT` data file
```
[(float("-inf"), -132), -89.61, (-24, float("inf"))]
[(-43, -12), (10, 27)]
```

### Example of `XML` data file
```
<MathSets>
    <value>[(float("-inf"), -132), -89.61, (-24, float("inf"))]</value>
    <value>[(-43, -12), (10, 27)]</value>
</MathSets>
```
***

### Examples of the output file
`JSON` format (`AFFILIATION` mode)
```
"[(10, 22)]"
```
`TXT` format (`AFFILIATION` mode)
```
[-12, 10]
```
`XML` format (`INTERSECTION` mode)
```
<OutputData>
    <value>[(-77, -61), (-17, -12), (10, 22)]</value>
</OutputData>
```
***

### Files and directories:
* `errors/` exception package
* `math_analyser/` plug-in modules
* `tests/` test module
* `create_sample.py` script to generate sample source files
* `requirements.txt` required packages 
* `run_math_sets_analyser.py` math_sets_analyser launcher