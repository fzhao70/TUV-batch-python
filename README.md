# TUVbatch-python

 Fanghe Zhao
 
 ## Description
 
 Run TUV in batch with python
 
 TUV code is modified from Version 5.3.2 from NCAR website
 
 Use tuv_api.py to run the tuv
 
 root_path is the path TUV source code located
 
 Use gfortran to compile, you can use other compiler by modify the Makefile in program

 ## Example

 ```
 from tuv_api import tuv_cli
 SA = 60
 height = 0.0 #km
 temperature = 298.0 #K
 root_path = "path you want"
 tuv_cli(SA, height, temperature, root_path)
 ```

 ## Install

 Just git clone this directory or put it in your project, and use it as example.