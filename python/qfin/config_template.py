
# DataBase Config
class DB_Config(object):
    crypto_crncy_str = "mysql+mysqldb://username:password@localhost/crypto_crncy?unix_socket=/tmp/mysql.sock"


# AWS Config
class AWS_Config(object):
    EMAIL_HOST          = 'email-smtp.us-east-1.amazonaws.com'
    EMAIL_HOST_USER     = 'xxx'
    EMAIL_HOST_PASSWORD = 'xxx'
    EMAIL_PORT          = 587

    Sender     = 'yzhao0527@gmail.com'
    Receipient = 'yzhao0527@gmail.com'


# GDAX
class GDAX_Config(object):
    key    = "xxx"
    seckey = "xxx"
    passwd = "xxx"
