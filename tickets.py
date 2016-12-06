# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 01:45:24 2016

@author: ZengC

命令行火车票查看器

Usage:
    tickets [-gdtkzas] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达
    -a          成人
    -s          学生

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""


import requests
import re
from docopt import docopt
from stations import stations
from pprint import pprint
from prettytable import PrettyTable
from colorama import init, Fore

init()

class TrainsCollection:

    header = '车次 车站 售票时间 起止时间 历时 商务 特等 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains, options):
        """查询到的火车班次集合

        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, etc...
        """
        self.available_trains = available_trains
        self.options = options

    def _get_duration(self, raw_train,string):
        duration = raw_train.get(string).replace(':', '小时') + '分'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        if not self.available_trains:
            train = None
            return
        for raw_train in self.available_trains:
            train_no = raw_train['station_train_code']
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                time = raw_train.get('sale_time')
                if not time:
                    time = '--'
                else:
                    time = raw_train['sale_time'][0:2]+'时'+ raw_train['sale_time'][2:]+'分'
                train = [
                    train_no,        
                    '\n'.join([Fore.GREEN + raw_train['from_station_name'] + Fore.RESET,
                               Fore.RED + raw_train['to_station_name'] + Fore.RESET]),
                    time,                    
                    '\n'.join([Fore.GREEN + raw_train['start_time'] + Fore.RESET,
                               Fore.RED + raw_train['arrive_time'] + Fore.RESET]),
                    self._get_duration(raw_train,'lishi'),
                    raw_train['swz_num'],
                    raw_train['tz_num'],
                    raw_train['zy_num'],
                    raw_train['ze_num'],
                    raw_train['rw_num'],
                    raw_train['yw_num'],
                    raw_train['yz_num'],
                    raw_train['wz_num'],
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        if self.trains == None:
            return -1
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    #pprint(arguments)
    purpose_codes = 'ADULT'
    if (arguments.get('-s') == True):
        purpose_codes = '0X00'
    from_station = stations.get(arguments['<from>'])
    if not(from_station):
        print('出发城市输入有误')
        return -1
    to_station = stations.get(arguments['<to>'])
    if not(to_station):
        print('终点城市输入有误')
        return -1
    date = arguments['<date>']
    
    res = re.findall(u'^([0-9]{4})-[0-9]{2}-[0-9]{2}$',date);
    if not res:
        print('日期输入有误')
        return -1
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes={}&queryDate={}&from_station={}&to_station={}'.format(purpose_codes, date, from_station, to_station)
    r = requests.get(url, verify=False)
    available_trains = r.json()['data'].get('datas')
        
    
    options = ''.join([
        key for key, value in arguments.items() if (value is True and key != '-a' and key != '-s')
    ])
    TrainsCollection(available_trains, options).pretty_print()
    
    
if __name__ == '__main__':
        
    cli()
    
    
    