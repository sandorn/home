'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-29 10:10:42
@LastEditors: Even.Sand
@LastEditTime: 2019-05-29 10:17:59
python loggingconfig.dictConfig - zs_2014的专栏 - CSDN博客
https://blog.csdn.net/zs_2014/article/details/45602243
'''

import logging
import logging.config


class SingleLevelFilter(object):
    def __init__(self, pass_level):
        self.pass_level = pass_level

    def filter(self, record):
        if self.pass_level == record.levelno:
            return True
        return False


LEVEL_COLOR = {
    logging.DEBUG: '\33[2;39m',
    logging.INFO: '\33[0;37m',
    logging.WARN: '\33[4;35m',
    logging.ERROR: '\33[5;31m',
    logging.FATAL: '\33[7;31m'
}


class ScreenHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            fs = LEVEL_COLOR[record.levelno] + "%s\n" + '\33[0m'
            try:
                if isinstance(msg, unicode) and getattr(stream, 'encoding', None):
                    ufs = fs.decode(stream.encoding)
                    try:
                        stream.write(ufs % msg)
                    except UnicodeEncodeError:
                        stream.write((ufs % msg).encode(stream.encoding))
                else:
                    stream.write(fs % msg)
            except UnicodeError:
                stream.write(fs % msg.encode("UTF-8"))

            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def init_logger():
    conf = {'version': 1,
            'disable_existing_loggers': True,
            'incremental': False,
            'formatters': {'myformat1': {'class': 'logging.Formatter',
                                         'format': '|%(asctime)s|%(name)s|%(filename)s|%(lineno)d|%(levelname)s|%(message)s',
                                         'datefmt': '%Y-%m-%d %H:%M:%S'}
                           },
            'filters': {'filter_by_name': {'class': 'logging.Filter',
                                           'name': 'logger_for_filter_name'},

                        'filter_single_level_pass': {'()': 'mylogger.SingleLevelFilter',
                                                     'pass_level': logging.WARN}
                        },
            'handlers': {'console': {'class': 'logging.StreamHandler',
                                     'level': 'INFO',
                                     'formatter': 'myformat1',
                                     'filters': ['filter_single_level_pass', ]},

                         'screen': {'()': 'mylogger.ScreenHandler',
                                    'level': logging.INFO,
                                    'formatter': 'myformat1',
                                    'filters': ['filter_by_name', ]}
                         },
            'loggers': {'logger_for_filter_name': {'handlers': ['console', 'screen'],
                                                   'filters': ['filter_by_name', ],
                                                   'level': 'INFO'},
                        'logger_for_all': {'handlers': ['console', ],
                                           'filters': ['filter_single_level_pass', ],
                                           'level': 'INFO',
                                           'propagate': False}
                        }
            }
    logging.config.dictConfig(conf)


if __name__ == '__main__':
    init_logger()
    logger_for_filter_name = logging.getLogger('logger_for_filter_name')
    logger_for_filter_name.debug('logger_for_filter_name')
    logger_for_filter_name.info('logger_for_filter_name')
    logger_for_filter_name.warn('logger_for_filter_name')
    logger_for_filter_name.error('logger_for_filter_name')
    logger_for_filter_name.critical('logger_for_filter_name')

    logger_for_all = logging.getLogger('logger_for_all')
    logger_for_all.debug('logger_for_all')
    logger_for_all.info('logger_for_all')
    logger_for_all.warn('logger_for_all')
    logger_for_all.error('logger_for_all')
    logger_for_all.critical('logger_for_all')
