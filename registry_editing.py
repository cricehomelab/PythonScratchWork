import subprocess

subprocess.run("reg delete HKEY_LOCAL_MACHINE\\System\\ControlSet001\\Services\\NetBIOS\\Linkage /v LanaMap /f")


list = ['"LanaMap"=hex:01,00,01,01,01,02,01,03,01,04,01,05']


# text_list = ['Windows Registry Editor Version 5.00 \n', '\n',
#             '[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\NetBIOS\Linkage]\n',
#             list]
line1 = "Windows Registry Editor Version 5.00 \n"
line2 = "\n"
line3 = "[HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Services\\NetBIOS\\Linkage] \n"
line4 = list
linelist = [line1, line2, line3, line4]

file = open("regupdate.reg", "w")
file.writelines(line1)
file.writelines(line2)
file.writelines(line3)
file.writelines(line4)
file.close()

subprocess.run('reg import regupdate.reg')
subprocess.check_output('reg query HKEY_LOCAL_MACHINE\\System\\ControlSet001\\Services\\NetBIOS\\Linkage /v LanaMap')
