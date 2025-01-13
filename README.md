# TUVbatch-python

 fzhao70
 
 Run TUV in batch with python
 
 TUV code is modified from Version 5.3.2 from NCAR website
 
 Use tuv_api.py to run the tuv
 
 root_path is the path TUV source code located
 
 ```
 from tuv_api import tuv_cli
 SA = 60
 height = 0.0 #km
 temperature = 298.0 #K
 root_path = "path you want"
 tuv_cli(SA, height, temperature, root_path)
 ```
