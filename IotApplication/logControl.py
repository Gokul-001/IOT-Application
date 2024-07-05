import os,logging

def logger(from_info):
    logging.basicConfig(filename=os.getenv('logs_path'),
                            filemode='a',
                            level=logging.INFO,
                            format="%(asctime)s - %(name)s -- %(message)s ",
                            datefmt='%Y-%m-%d | %H:%M:%S'
                            )
    log=logging.getLogger(from_info)
    return log

