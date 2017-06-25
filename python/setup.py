from distutils.core import setup

setup(name='qfin',
      version='0.01',
      description='Quantitative Finance Toolbox',
      author='Yue Zhao',
      author_email='yzhao0527@gmail.com',
      packages=[
            'qfin',
            'qfin.CryptoCrncy',
            'qfin.CryptoCrncy.data',
            'qfin.CryptoCrncy.proc',
            'qfin.utils', 
        ],
     )
