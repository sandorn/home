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
    netdbstr = f"{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}?charset={config['charset']}"

    if types == 'mysql':
        if odbc == 'OurSQL':
            driver = f'{types}+oursql'
        elif odbc == 'aiomysql':
            driver = f'{types}+aiomysql'
        elif odbc == 'connector':
            driver = f'{types}+mysqlconnector'
        elif odbc == 'mysqlclient':
            driver = f'{types}+mysqldb'
        elif odbc == 'pymysql':
            driver = f'{types}+pymysql'
        else:
            driver = 'mysql'
        return f"{driver}://{netdbstr}"

    if types == 'PostgreSQL':
        if odbc in ['pg8000', 'psycopg2']:
            driver = f'postgresql+{odbc}'
        else:
            driver = 'postgresql'
        return f"{driver}://{netdbstr}"

    if types == 'Oracle':
        driver = 'oracle+cx_oracle' if odbc == 'cx_oracle' else 'oracle'
        return f"{driver}//{netdbstr}"

    if types == 'SQLServer':
        driver = 'mssql+pyodbc' if odbc == 'pyodbc' else 'mssql+pymssql'
        return f"{driver}://{netdbstr}"

    if types == 'SQLite':
        driver = 'sqlite'
        return f"{driver}:///{config['host']}"

    if types == 'access':
        driver = 'access+pyodbc'
        return f"{driver}://{config['host']}"

    if types == 'monetdb':
        driver = 'monetdb+lite' if odbc == 'lite' else 'monetdb'
        return f"{driver}:///{config['host']}"
    
    return ''
