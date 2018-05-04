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
#配置文件
>hosts配置文件
```
# cat hosts
[all:]
other:
client:
    
[client]
zabbix : 192.168.136.130
client : 192.168.136.129

[other]
other : 192.168.136.128
```

1、组名不带有：时
``[]``：里面填写组名
``[]下面``：前面主机名，后面对于ip地址
2、组名带有：时
``[]``：带有：的组名
``[]下面``：前面为不带有：的组名
>keys配置文件
```
# cat keys
/root/.ssh/id_rsa
```
keys写法文件有严格，路径地址必须写在第一行，其不要加任何引号
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
> 批量执行shell命令
```
#对client组执行shell操作
python remote_exec_py2.py -m shell - g client -c 'hostname'
```
> 批量上传文件
```
#将本地/root/sun.txt上传至client组中服务器的/sun下
python remote_exe_py2c.py -m shell - g client -c src=/root/sun.txt dest=/sun"
```
# 前提条件
1、`由于该脚本基于paramiko模块开发，所以此python务必先安装paramiko模块`
2、`执行操作命令的脚本，必须实现ssh免登陆到相应服务器上`
