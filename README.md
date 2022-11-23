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
or the nearest endpoint(s) to the predetermined **point** otherwise.
***

## Installation
**Requirements**
* `Python` 3.9+
* `bs4` (tested to work with >= 0.0.1)
* `chameleon` (tested to work with >= 3.9.1)  

**Note:** The `bs4` and `chameleon` packages can be installed by running `python3 -m pip install -r requirements.txt`
***

## Running MathSetsAnalyser
For use **as plug-ins** `import math_sets_analyser`

For math analysis of input data **as a script**:
* create `config.ini` in the script directory  
* run `python3 run_math_sets_analyser.py`

**For generating sample** configuration and data files run `.trial_run/trial_math_sets_analyser.py`,  
an output file for the input data will also be created.

**For testing** MathSetsAnalyser run `python3 -m unittest -v test_math_sets_analyser.py`
***

### The configuration file `config.ini` has the following structure:
`[general]`  
analysis mode: `INTS` or `AFFL`  
point (for `AFFL` mode only)  

`[input]`  
type of the data file: `JSON` `TXT` `XML`  
path of the data file

`[output]`  
type of the output file: `JSON` `TXT` `XML`  
path of the output file (including name of the file)

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

### The data file contains the initial math sets and their names.

Each initial **math set** is given as `list` of ranges and points.  
The **math range** is given as `tuple` and **math point** is given as `int` or `float`  
The **minus infinity** is given as `"-inf"`  
The **plus infinity** is given as `"+inf"`  
**Note:** For `JSON` data file initial **math set** is given as `str` object. So check the use of `' '` and `" "`

Examples of initial **math sets** for `TXT` and `XML` data file:  
`[("-inf", -10.02), (10.97, "+inf")]`  
`[('-inf', -41), -18, (51, 62.01), 77.34, (103.0,  '+inf')]`  
`[(-89, -61), (61, 72)]`  
`[14.021]`

Examples of initial **math sets** for `JSON` data file:    
`"[('-inf', -10.02), (10.97, '+inf')]"`  
`"[('-inf', -41), -18, (51, 62.01), 77.34, (103.0,  '+inf')]"`  
`"[(-89, -61), (61, 72)]"`  
`"[14.021]"`

### Example of `JSON` data file
```
{
	"math_set_1": "[('-inf', -132), -89.61, (-24, '+inf')]",
	"math_set_2": "[(-43, -12), (10, 27)]"
}
```

### Example of `TXT` data file
```
math_set_1
[("-inf", -132), -89.61, (-24, "+inf")]
math_set_2
[(-43, -12), (10, 27)]
```

### Example of `XML` data file
```
<InitialData>
    <MathSet math_set_name="math_set_1">
        <value>[("-inf", -132), -89.61, (-24, "+inf")]</value>
    </MathSet>
    <MathSet math_set_name="math_set_2">
        <value>[(-43, -12), (10, 27)]</value>
    </MathSet>
</InitialData>
```
***
### Examples of the output file
`JSON` format (`AFFILIATION` mode)
```
{
	"The subrange of the initial math sets intersection with the predetermined point": "[(10, 22)]"
}
```
`TXT` format (`AFFILIATION` mode)
```
The nearest endpoint(s) to the predetermined point
[-12, 10]
```
`XML` format (`INTERSECTION` mode)
```
<ScriptOutputData>
    <ScriptOutput title="The intersection of initial math sets">
        <value>[(-77, -61), (-17, -12), (10, 22)]</value>
    </ScriptOutput>
</ScriptOutputData>
```
***

### Files and directories:
* `math_sets_analyser.py` plug-in modules
- `run_math_sets_analyser.py` math_sets_analyser launcher
* `test_math_sets_analyser.py` tests
- `requirements.txt` required packages  
* `./errors` script exception package
- `./math_analyser` auxiliary modules package
* `./tests` test module package
- `.trial_run/trial_math_sets_analyser.py` script to generate sample source files
