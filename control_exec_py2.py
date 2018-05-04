#!/usr/bin/env python2 
#coding:utf-8
#auther:sun

import os,sys,getopt,ConfigParser,threading,paramiko

def getopt_info():
    ''' 获取位置参数'''
    module,group,command = (None,None,None)
    try:
        options,args = getopt.getopt(sys.argv[1:],"hm:g:c:",["help","module=","group=","command="])
    except getopt.GetoptError:
        sys.exit(1)
    for key,value in options:
        if key in ("-h","--help"):
            help()
            sys.exit(1)
        elif key in ("-m","--module"):
            module = value
        elif key in ("-g","--group"):
            group = value
        else:
            command = value
    return module,group,command

def config_info(args):
    '''配置文件读取'''
    hosts = {}
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__),'conf/hosts'))
    if ':' in args:
        for key in config.options(args):
            for value in config.options(key):
                hosts[value] = config.get(key,value)
    else:
        for host in config.options(args):
            hosts[host] = config.get(args,host)
    return hosts

# def login(ip):
#     '''登陆远程机器'''
#     transport = paramiko.Transport((ip,22))
#     transport.connect(username='root',password='sunqiao0730')
#     print(ip)
#     return transport

def exec_cmd(lock,key,hostname,ip,cmd):
    '''执行shell操作'''
    with open(key) as f:
        key = f.readline().split()[0]
    
    private_key = paramiko.RSAKey.from_private_key_file(key)
    transport = paramiko.Transport((ip,22))
    transport.connect(username='root',pkey=private_key)
    ssh = paramiko.SSHClient()
    ssh._transport = transport
    stdin,stdout,stderr = ssh.exec_command(cmd)
    content_out = stdout.read().decode()
    content_err = stderr.read().decode()
    
    lock.acquire()
    if len(content_out) != 0:
        result = 'The result of ['+ hostname+'] is (OK):'
        print(result)
        print(content_out)
    else:
        if len(content_err) == 0:
            result = 'The result of [' + hostname + '] is (OK):'
            print(result)
            print(content_out)
        else:
            result = 'The result of ['+ hostname+'] is (ERR):'
            print(result)
            print(content_err)
    lock.release()

def exec_ftp(key,hostname,ip,cmd):
    '''ftp上传文件'''
    file = {}
    file[cmd.split()[0].split('=')[0]] = cmd.split()[0].split('=')[1]
    file[cmd.split()[1].split('=')[0]] = cmd.split()[1].split('=')[1]
    dest = os.path.join(file['dest'],os.path.basename(file['src']))

    with open(key) as f:
        key = f.readline().split()[0]

    private_key = paramiko.RSAKey.from_private_key_file(key)
    transport = paramiko.Transport((ip,22))
    transport.connect(username='root',pkey=private_key)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(file['src'],dest)
    result = 'The result of [' + hostname + '] is (OK):'
    print(result)
    transport.close()

def pool_cmd(semaphore,lock,key,hostname,ip,cmd):
    '''exec_cmd线程数控制'''
    semaphore.acquire()
    exec_cmd(lock,key,hostname,ip,cmd)
    semaphore.release()

def pool_ftp(semaphore,key,hostname,ip,cmd):
    '''exec_ftp线程数控制'''
    semaphore.acquire()
    exec_ftp(key,hostname,ip,cmd)
    semaphore.release()


def help_info():
    '''帮助提示'''
    Help = str(sys.argv[0]) + " -m [shell|copy] -g [group] -c [command]"
    print('Usage:%s' % Help)

def main():
    '''主函数:多线程操作'''
    module,group,command = getopt_info()
    #print(module,group,command)
    hosts = config_info(group)
    #print(hosts) 
    Key = os.path.join(os.path.dirname(__file__),'conf/keys')
    Lock = threading.Lock()
    semaphore  = threading.BoundedSemaphore(30)
    if module == 'shell':
        for k,v in hosts.items():
            t = threading.Thread(target=pool_cmd,args=[semaphore,Lock,Key,k,v,command])
            #t = threading.Thread(target=exec_cmd,args=[Lock,k,v,command])
            t.start()
    elif module == 'copy':
        for k,v in hosts.items():
            t = threading.Thread(target=pool_ftp,args=[semaphore,Key,k,v,command])
            #t = threading.Thread(target=exec_ftp,args=[k,v,command])
            t.start()

if __name__ == '__main__':
    try:
        main()
    except:
        help_info()