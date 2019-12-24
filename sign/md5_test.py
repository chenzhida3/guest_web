# -*- coding: utf-8 -*-
'''
 @File    : md5_test.py
 @Time    : 2019/6/25 9:32
 @Author  : Chenzd
 @Project : MD5加密算法
 @Software: PyCharm
'''
if __name__ == '__main__':
    import hashlib
    md5 = hashlib.md5()
    sign_str = 'czd158805'
    sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
    md5.update(sign_bytes_utf8)
    sign_md5 = md5.hexdigest()
    print(sign_bytes_utf8)
    print(sign_md5)