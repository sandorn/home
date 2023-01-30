'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:50
LastEditTime : 2022-12-20 20:23:27
FilePath     : /xjLib/xt_DAO/cfg.PY
Github       : https://github.com/sandorn/home
==============================================================
'''
from copy import deepcopy

DB_CONFIG = {
    'TXbook': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'password': '123456',
        'db': 'biqukan',
        'charset': 'utf8mb4'
    },
    'TXbx': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'password': '123456',
        'db': 'bxflb',
        'charset': 'utf8mb4'
    },
    'TX_Root': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'root',
        'password': 'Sand2808',
        'db': 'bxflb',
        'charset': 'utf8mb4'
    },
    'db4': {
        'type': 'mysql',
        'host': 'db4free.net',
        'port': 3306,
        'user': 'sandorn',
        'password': 'eeM3sh4KPkp4sJ8A',
        'db': 'baoxianjihuashu',
        'charset': 'utf8mb4'
    },
    'redis': {
        'type': 'redis',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 4
    },
    'Jkdoc': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'password': '123456',
        'db': 'Jkdoc',
        'charset': 'utf8mb4'
    }
}

# # 有优化空间

DB_CONFIG['default'] = DB_CONFIG['TXbook']


def connect_str(key, odbc=None):
    if key not in DB_CONFIG: raise ValueError(f'错误提示：检查数据库配置：{key}')
    config = deepcopy(DB_CONFIG[key])
    types = config['type']

    if types == 'mysql':
        if odbc == 'OurSQL':
            drver = f'{types}+oursql'
        elif odbc == 'aiomysql':
            drver = f'{types}+aiomysql'
        elif odbc == 'connector':
            drver = f'{types}+mysqlconnector'
        elif odbc == 'mysqlclient':
            drver = f'{types}+mysqldb'
        elif odbc == 'pymysql':
            drver = f'{types}+pymysql'
        else:
            drver = 'mysql'
        return f"{drver}://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}?charset={config['charset']}"

    if types == 'PostgreSQL':
        if odbc == 'pg8000':
            drver = 'postgresql+pg8000'
        elif odbc == 'psycopg2':
            drver = 'postgresql+psycopg2'
        else:
            drver = 'postgresql'
        return f"{drver}://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}?charset={config['charset']}"

    if types == 'Oracle':
        drver = 'oracle+cx_oracle' if odbc == 'cx_oracle' else 'oracle'
        return f"{drver}//{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}?charset={config['charset']}"
        # cx_oracle:'oracle+cx_oracle://scott:tiger@tnsname'

    if types == 'SQLServer':
        drver = 'mssql+pyodbc' if odbc == 'pyodbc' else 'mssql+pymssql'
        return f"{drver}://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}?charset={config['charset']}"
        # pyodbc:'mssql+pyodbc://scott:tiger@mydsn'

    if types == 'SQLite':
        drver = 'sqlite'
        return f"{drver}:///{config['host']}"

    if types == 'access':
        drver = 'access+pyodbc'
        return f"{drver}://{config['host']}"

    if types == 'monetdb':
        drver = 'monetdb+lite' if odbc == 'lite' else 'monetdb'
        return f"{drver}:///{config['host']}"
