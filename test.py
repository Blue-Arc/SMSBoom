# encoding=utf8
# 测试程序

import sys
import time
import click
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed

# logger config
logger.remove()
logger.add(
    sink = sys.stdout,
    format = "<blue>{time:YYYY-MM-DD at HH:mm:ss}</blue> - <level>{level}</level> - <level>{message}</level>",
    colorize = True,
    backtrace = True
)

@click.group()
def cli():
    pass

def get_html(parm:int):
    '''输出函数'''
    time.sleep(1)
    logger.info("Get page {} finished".format(parm))
    return parm

@click.command()
@click.option("--thread", "-t", help = "线程数(默认为32)", type = int, default = 32)
@click.option("--num", "-n", help = "数组范围", type = int, required = True)
def run(thread:int, num:int):
    '''主函数
    多线程适用于处理多次发起耗时比较长的任务函数
    '''
    t1 = time.time()
    with ThreadPoolExecutor(max_workers = thread) as pool: # with创建线程池会阻塞到所有线程任务完成
        for n in list(range(num)):
            pool.submit(get_html, n)
    # thread_pool_exe = ThreadPoolExecutor(max_workers = thread, thread_name_prefix = "no_")
    # all_task = [thread_pool_exe.submit(get_html, n) for n in list(range(num))]
    # for future in as_completed(all_task):
    #     data = future.result()
    #     logger.info("In main: Get page {}s success".format(data))
    # # thread_pool_exe.shutdown(wait = False)
    t2 = time.time()
    logger.info(f"程序用时: {t2-t1}s")

cli.add_command(run)

if __name__ == "__main__":
    cli()