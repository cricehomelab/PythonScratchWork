"""
This was the result of playing around in a VM trying to see how i can update the LanaMap registry value I have commented
lines of code that could change a registry unconsciously and am marking them as dangerous.

"""

import subprocess

# THIS WILL DELETE A REGISTRY KEY MAKE SURE IT WORKS BEFORE RUNNING
# ***************************************************************************************************************
#subprocess.run("reg delete HKEY_LOCAL_MACHINE\\System\\ControlSet001\\Services\\NetBIOS\\Linkage /v LanaMap /f")
# ***************************************************************************************************************
line1 = "Windows Registry Editor Version 5.00 \n"
line2 = "\n"
line3 = "[HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Services\\NetBIOS\\Linkage] \n"
line4 = '"LanaMap"=hex:01,00,01,01,01,02,01,03,01,04,01,05'
linelist = [line1, line2, line3, line4]

# creates and opens a file named regupdate.reg in the working directory
file = open("regupdate.reg", "w")
# adds the desired content to the .reg file.
file.writelines(line1)
file.writelines(line2)
file.writelines(line3)
file.writelines(line4)
file.close()
# THIS WILL IMPORT A REGISTRY KEY MAKE SURE IT WORKS BEFORE RUNNING
# ********************************************************************************************************************
#subprocess.run('reg import regupdate.reg')
#subprocess.check_output('reg query HKEY_LOCAL_MACHINE\\System\\ControlSet001\\Services\\NetBIOS\\Linkage /v LanaMap')
# ********************************************************************************************************************