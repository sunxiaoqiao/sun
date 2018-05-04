# 功能介绍
该脚本为自动化运维工具，基于Python开发，实现了批量系统配置、批量程序部署、批量运行命令等功能

# 目录结构
```
.
| ─ ─   
     | ─ conf
           | ─ hosts           
           | ─ keys            
     | ─ control_exec_py2.py   
     | ─ control_exec_py3.py 
```
* control_exec_py2.py ：自动化运维脚本，应用于Python2平台
* control_exec_py3.py : 自动化运维脚本，应用于Python3平台
* hosts   : 配置主机信息文件
* keys : 声明私钥的路径的文件
# 实例说明
该脚本提供主要提供了两种功能
1、实现远程批量操作命令
2、实现远程上传文件命令
>   用法：
```
Usage:./remote_exec_py2.py -m [shell|copy] -g [group] -c [command]
```
```
-m : 
    shell：定义执行shell命令
    copy：定义上传文件命令
-g : 服务器组，在hosts配置文件中定义
-c :
    ◆ 当-m为shell时，-c后面为shell的操作命令，如 -c "hostname",获取主机名
    ◆ 当-m为copy是，表示执行文件上传，如 -c “src=/root/sun.txt dest=/sun",src表示本地需要上传的文件，dest表示上传远端服务器的文件路径
```
```
#对client组执行shell命令
python remote_exec_py2.py -m shell - g client -c 'hostname'
```
```
#将本地/root/sun.txt上传至client组中服务器的/sun下
python remote_exe_py2c.py -m shell - g client -c src=/root/sun.txt dest=/sun"
```
