from email.utils import parseaddr, formataddr
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import ssl
dict_captcha = {}


def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# async def send_email(mess, to_addr):
#     # SMTP服务器以及相关配置信息
#     smtp_server = 'smtp.163.com'  # 163邮箱用到的SMTP服务器
#     from_addr = 'victorygreens7@163.com'
#     password = 'SSQUIOCIRIQTHYRW'
#     try:
#         msg = MIMEText(mess, 'plain', 'utf-8')
#         # 1.创建邮件(写好邮件内容、发送人、收件人和标题等)
#         msg['From'] = format_addr('社区管理员 <%s>' % from_addr)  # 发件人昵称和邮箱
#         msg['To'] = format_addr('管理员 <%s>' % to_addr)  # 收件人昵称和邮箱
#         msg['Subject'] = Header('欢迎来到Victory Greens', 'utf-8').encode()  # 邮件标题
#
#         # 2.登录账号
#         server = smtplib.SMTP(smtp_server, 25)
#         server.login(from_addr, password)
#
#         # 3.发送邮件
#         server.sendmail(from_addr, [to_addr], msg.as_string())
#         server.quit()
#         print('发送邮件成功')
#         return True
#
#     except Exception as e:
#         print(e)
#         print('发送邮件失败')
#         return False




async def send_email(mess, to_addr):
    smtp_server = 'smtp.163.com'
    from_addr = 'victorygreens7@163.com'
    password = 'SSQUIOCIRIQTHYRW'

    try:
        msg = MIMEText(mess, 'plain', 'utf-8')
        msg['From'] = formataddr(('社区管理员', from_addr))
        msg['To'] = formataddr(('管理员', to_addr))
        msg['Subject'] = Header('欢迎来到Victory Greens', 'utf-8').encode()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())

        print('发送邮件成功')
        return True

    except Exception as e:
        print(e)
        print('发送邮件失败')
        return False