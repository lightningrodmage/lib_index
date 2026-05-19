# -*- coding: utf-8 -*-
"""
@file: index_prepare.py
@author: zy
@date: 2025/07/21
基于已有的规则排列index组成杂交pool
"""

import pandas as pd
import static_info
from datetime import datetime,timedelta
from collections import Counter
import pool_to_chip
from collections import defaultdict

sample = {
    "sample_barcode": "100260925912",  # 样本条码
    "sample_id": "X_LGC86-250715-4",
    "sample_type": "tumor",  # 样本类型
    "collection_date": "2025-07-15",  # 接收日期
    "maturity_date": "2025-07-22",  # 报告周期
    "data_volume": "13.8",  # 数据量要求
    "probe_type": "228",  # 探针类型
    "pre_pcr_library_amount": 2500,  # 预文库产量
    "pre_pcr_library_quality": "LQ",
    "max_hybrid_per_pool": 12,  # 该探针最高的杂交pool数
    "pre_library_load": 500  # 预文库投入量
}


class Sample:
    def __init__(self, sample_id, maturity_date,data_volume,index1,index2,pre_pcr_library_amount):
        self.sample_id = sample_id  # 样本id,lims获取
        self.sample_type = ""    # 样本类型,根据sample_id识别
        self.probe_type = ""
        if isinstance(maturity_date, str):
            self.maturity_date = datetime.strptime(maturity_date, "%Y-%m-%d %H:%M:%S") # 报告周期，lims获取
        else:
            self.maturity_date = maturity_date
        self.data_volume = data_volume  # 需要数据量，lims获取
        self.pre_pcr_library_amount = pre_pcr_library_amount    # 预文库得率，lims获取
        self.pre_pcr_library_quality = 'LQ'  # 预文库质量，根据data_volume和标准值评估确定
        self.index1 = index1
        self.index2 = index2
        self.pre_library_load = "500"
        self.notthy = 1

    def __repr__(self):
        return f"Sample({self.sample_id}, {self.sample_type}, {self.maturity_date}, " \
               f"{self.data_volume}, {self.probe_type}, " \
               f"{self.pre_pcr_library_amount},{self.pre_pcr_library_quality },{ self.index1},{ self.index2},{ self.pre_library_load}),{self.notthy}"

    def get_project_type(self):
        sample_start = self.sample_id.split("-")[0]
        if sample_start not in static_info.project_info_dict:
            if sample_start.endswith("PD"):
                sample_start = sample_start[:-2]
            if sample_start.endswith("PPD"):
                sample_start = sample_start[:-3]
        if sample_start in static_info.project_info_dict:
            if self.sample_id.split("-")[-1] in ["B", "G", "GB"]:
                self.sample_type = "germline"
            elif self.sample_id.split("-")[-1] in ["X"]:
                self.sample_type = "ctDNA"
            else:
                self.sample_type = static_info.project_info_dict[sample_start]["sample_type"]
            if self.sample_id.split("-")[-1] == "HRD" or self.sample_id.split("-")[-2] == "HRD":
                self.probe_type = "hrd"
            elif self.sample_id.split("-")[-1] == "R" and self.sample_id.split("-")[0] in ["THY116", "THY116T"]:
                self.probe_type = "thy116-rna"
            else:
                self.probe_type = static_info.project_info_dict[sample_start]["probe_type"]
        else:
            print(f"{self.sample_id}无法识别探针类型和样本类型，请复核")
            return
        normal_data_volume = static_info.panel_list[self.probe_type]["data_volume"][self.sample_type]
        if self.sample_id.startswith("QW15"):
            normal_data_volume = 21
        if self.data_volume <= normal_data_volume:
            self.pre_pcr_library_quality = 1
        else:
            self.pre_pcr_library_quality = 0
        if self.pre_pcr_library_quality == 1:
            self.pre_library_load = min(static_info.panel_list[self.probe_type]["input"]['one_type'][self.sample_type], self.pre_pcr_library_amount)
        else:
            self.pre_library_load = min(static_info.panel_list[self.probe_type]["input"]['one_type'][self.sample_type]*1.5,
                                        self.pre_pcr_library_amount)

    def check_thy(self):
        if "THY" in self.sample_id and self.probe_type == "pan122":
            #print("这个样本是甲状腺11")
            self.notthy = 0
        else:
            self.notthy = 1

    def change_input(self,i):
        if i > 1:
            if self.pre_pcr_library_quality == 1:
                self.pre_library_load = min(static_info.panel_list[self.probe_type]["input"]['two_type'][self.sample_type], self.pre_pcr_library_amount)
            else:
                self.pre_library_load = min(static_info.panel_list[self.probe_type]["input"]['two_type'][self.sample_type]*1.5,
                                        self.pre_pcr_library_amount)


def read_tomorrow_info(tomorrow_sample_list, pool):
    """
     :param tomorrow_sample_list: 第二天的样本清单
     :param pool: 需要填充的pool第二天的样本清单
     :return: 填充完的pool
     根据第二天的样本清单，评估哪些样本可以塞进今天的pool里
     """

def read_tomorrow_info(tomorrow_sample_list, pool):
    """
     :param tomorrow_sample_list: 第二天的样本清单
     :param pool: 需要填充的pool第二天的样本清单
     :return: 填充完的pool
     根据第二天的样本清单，评估哪些样本可以塞进今天的pool里
     """

def add_sample_to_pool(type,samples_dict,probe,result_dict,k_counter):
    #print(12345)
    #global samples_dict
    #global probe
    #global result_dict
    #global k_counter
    #print(samples_dict)

    if type in samples_dict:
        all_load = 0
        for sample in samples_dict[type]:
            all_load += sample.pre_library_load
        current_k = []  # 当前的 k 列表
        current_load = 0  # 当前 k 列表的 pre_library_load 总和
        if all_load > 6000 or len(samples_dict[type]) > static_info.panel_list[probe]['max_hybrid_per_pool']:
            for sample in samples_dict[type]:
                if current_load + sample.pre_library_load <= 6000 and len(current_k) < static_info.panel_list[probe]['max_hybrid_per_pool']:
                    current_k.append(sample)
                    current_load += sample.pre_library_load
                else:
                # 保存当前 k 列表
                    #print(f'这个时候装了{current_load}投入量')
                   # print(f'这个时候装了{len(current_k)}个样本')
                    #print(f"这个时候的pool是{current_k}")
                    result_dict[f'pool{k_counter}'] = {
                        "sample_num": len(current_k),
                        'msg': "",
                        "total_load":current_load,
                        "sample_list": current_k
                    }
                    k_counter += 1
                # 创建新的 k 列表
                    current_k = [sample]
                    current_load = sample.pre_library_load
        # 保存最后一个 k 列表
            final_k = current_k
        elif (all_load == 6000 and len(samples_dict[type]) <= static_info.panel_list[probe]['max_hybrid_per_pool']) or (all_load <= 6000 and len(samples_dict[type]) == static_info.panel_list[probe]['max_hybrid_per_pool']):
            current_k = samples_dict[type]
            result_dict[f'pool{k_counter}'] = {
                        "sample_num": len(current_k),
                        'msg': "",
                        "total_load":all_load,
                        "sample_list":current_k
                    }
            k_counter += 1
        else:
            final_k = samples_dict[type]
        #print(k_counter)
        return k_counter,final_k


def add_mix_sample_to_pool(sample_list,probe,result_dict,k_counter,i):
    sample_list = sorted(
                sample_list,
                    key=lambda x: (
                        x.maturity_date,  # 第一优先级
                        x.pre_pcr_library_quality,  # 第二优先级，假设 LQ 是一种特殊的值
                        x.pre_library_load,
                        x.index1  # 第四优先级
                    )
                )
    for sample in sample_list:
        sample.change_input(i)
        #print(sample)
    all_load = 0
    for sample in sample_list:
        all_load += sample.pre_library_load
    current_k = []  # 当前的 k 列表
    current_load = 0  # 当前 k 列表的 pre_library_load 总和
    if not static_info.panel_list[probe]:
        print(probe)
    if all_load > 6000 or len(sample_list) > static_info.panel_list[probe]['max_hybrid_per_pool']:
        for sample in sample_list:
            if current_load + sample.pre_library_load <= 6000 and len(current_k) < static_info.panel_list[probe][
                'max_hybrid_per_pool']:
                current_k.append(sample)
                current_load += sample.pre_library_load
            else:
                # 保存当前 k 列表
                #print(f'这个时候装了{current_load + sample.pre_library_load}投入量')
                #print(f'这个时候装了{len(current_k)}个样本')
                #print(f"这个时候的pool是{current_k}")
                result_dict[f'pool{k_counter}'] = {
                        "sample_num": len(current_k),
                        'msg': "",
                        "total_load":all_load,
                        "sample_list": current_k
                    }
                k_counter += 1
                # 创建新的 k 列表
                current_k = [sample]
                current_load = sample.pre_library_load
        # 保存最后一个 k 列表
        final_k = current_k
    elif (all_load == 6000 and len(sample_list) <= static_info.panel_list[probe]['max_hybrid_per_pool']) or (
            all_load <= 6000 and len(sample_list) == static_info.panel_list[probe]['max_hybrid_per_pool']):
        current_k = sample_list
        result_dict[f'pool{k_counter}'] = {
                        "sample_num": len(current_k),
                        'msg': "",
                        "total_load":all_load,
                        "sample_list": current_k
                    }
        k_counter += 1
        final_k = []
    else:
        final_k = sample_list
    #print(k_counter)
    return k_counter, final_k

def get_all_load(sample_list):
    all_load = 0
    for sample in sample_list:
        all_load += sample.pre_library_load
    return all_load

def allocate_samples(samples_dict,probe):
    """
     :param sample_list: 样本清单
     :param probe: 需要分配的探针类型
     :return: 填充完的pool_dict，没有塞满的pool
     根据样本清单，输出分好的杂交pool和没有塞满的单个pool
     """
    #print(samples_dict)
    result_dict = {}  # 存放最终的 k 列表
    k_counter = 1     # k 列表计数器，用于生成键名
    if "ctDNA" in samples_dict:
        k_counter, remain_ctDNA_sample = add_sample_to_pool("ctDNA", samples_dict,probe,result_dict,k_counter)
        if probe != "pan665":
            result_dict[f'pool{k_counter}']  = {
                        "sample_num": len(remain_ctDNA_sample),
                        'msg': f"该pool未满，还可以混入{static_info.panel_list[probe]['max_hybrid_per_pool']-len(remain_ctDNA_sample)}个下一批次样本",
                        "total_load":get_all_load(remain_ctDNA_sample),
                        "sample_list": remain_ctDNA_sample
                    }
            k_counter += 1
            remain_ctDNA_sample = []
    if "germline" in samples_dict:
        #print("germline")
        k_counter,remain_germline_sample = add_sample_to_pool("germline", samples_dict,probe,result_dict,k_counter)
    if "tumor" in samples_dict:
        #print("tumor")
        k_counter,remain_tumor_sample = add_sample_to_pool("tumor", samples_dict,probe,result_dict,k_counter)
    final_need_add_sample = []
    i = 0
    if "ctDNA" in samples_dict and probe == "pan665":
        final_need_add_sample += remain_ctDNA_sample
        i += 1
    if "germline" in samples_dict:
        final_need_add_sample += remain_germline_sample
        i += 1
    if "tumor" in samples_dict:
        final_need_add_sample += remain_tumor_sample
        i += 1
    #print(final_need_add_sample)
    k_counter, remain_final_sample = add_mix_sample_to_pool(final_need_add_sample,probe,result_dict,k_counter,i)
    if len(remain_final_sample) > 0:
        result_dict[f'pool{k_counter}'] = {
                        "sample_num": len(remain_final_sample),
                        'msg': f"该pool未满，还可以混入{static_info.panel_list[probe]['max_hybrid_per_pool']-len(remain_final_sample)}个下一批次样本,或是投入{6000-get_all_load(remain_final_sample)}的文库",
                        "total_load":get_all_load(remain_final_sample),
                        "sample_list": remain_final_sample
                    }
            # 处理 ctDNA 样本
    if result_dict == {}:
        print(probe)

    for pool in result_dict:
        is_tat = 0
        total_data_volume = 0
        for sample in result_dict[pool]['sample_list']:
            total_data_volume += sample.data_volume
            if (datetime.now() + timedelta(days=3)).date() >= sample.maturity_date.date():
                is_tat += 1
        result_dict[pool]['total_data_volume'] = total_data_volume
        result_dict[pool]['tat_sample_num'] = is_tat
        if result_dict[pool]['tat_sample_num'] > 0 and result_dict[pool]['msg'] != "":
            result_dict[pool]['msg'] = f"这个pool有{is_tat}个到期样本,但是" + result_dict[pool]['msg']
        elif result_dict[pool]['tat_sample_num'] == 0 and result_dict[pool]['msg'] != "":
            result_dict[pool]['msg'] = f"这个pool没有到期样本," + result_dict[pool]['msg'] + ",或是暂不杂交"
    #print(result_dict)
    return result_dict



def read_samples_from_excel(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(excel_file_path, skiprows=2, header=0)

    # 创建 Sample 对象列表
    samples_dict = {}
    datatime1 = datetime(9999, 1, 1, 23, 59, 0)
    for index, row in df.iterrows():
        if pd.isna(row['样本条码']):
            continue
        sample = Sample(
            sample_id=row['实验编号'],
            maturity_date=row['报告截止时间'],
            data_volume=row['DNA文库预期数据量(GB)'],
            index1=row['*index1编号'],
            index2=row['*index2编号'],
            pre_pcr_library_amount=row['*Pre-PCR文库总量(ng)']
        )
        sample.get_project_type()
        sample.check_thy()
        #print(sample)
        if isinstance(sample.maturity_date, str):
            print(type(sample.maturity_date))
        #print(sample)
        # 使用 probe_type 作为字典的键
        if sample.probe_type not in samples_dict:
            samples_dict[sample.probe_type] = {}  # 创建一个新的列表
            # 使用 sample_type 作为第二层键
        if sample.sample_type not in samples_dict[sample.probe_type]:
            samples_dict[sample.probe_type][sample.sample_type] = []  # 创建一个新的列表
            # 将样本添加到对应的列表中
        samples_dict[sample.probe_type][sample.sample_type].append(sample)
        if sample.maturity_date < datatime1:
            datatime1 = sample.maturity_date
        # 对每个 probe_type 的样本列表进行排序
    for probe_type, sample_types in samples_dict.items():
        for sample_type, sample_list in sample_types.items():
            samples_dict[probe_type][sample_type] = sorted(
                sample_list,
                    key=lambda x: (
                        x.notthy,
                        x.maturity_date,  # 第一优先级
                        x.pre_pcr_library_quality,  # 第二优先级，假设 LQ 是一种特殊的值
                        x.pre_library_load,
                        x.index1  # 第四优先级
                    )
                )
    #print(samples_dict['pan122'])
    #print(samples_dict)
    return samples_dict

def cheat_samples(samples_dict):
    all_result = {}
    for probe in samples_dict:
        probe_pool = allocate_samples(samples_dict[probe], probe)
        all_result[probe] = probe_pool
    #print(all_result)
    rows = []
    pool_list = []
    pool_msg = {}
    for probe, pools in all_result.items():
        for pool_name, pool_info in pools.items():
            name = probe + "_" + pool_name

            pool_msg[name] = {
                "到期样本数": pool_info['tat_sample_num'],
                "该pool总数据量": pool_info['total_data_volume'],
                "总index": []
            }
            check_thy = True
            for sample in pool_info['sample_list']:
                # 提取 Sample 的属性
                if sample.notthy == 1:
                    check_thy = False
                if sample.pre_pcr_library_quality == 1:
                    pre_pcr_library_quality = "normal"
                else:
                    pre_pcr_library_quality = "LQ"
                sample_data = {
                    "实验编号": sample.sample_id,
                    "样本类型": sample.sample_type,
                    "报告截止时间": sample.maturity_date,
                    "DNA文库预期数据量(GB)": sample.data_volume,
                    "探针": sample.probe_type,
                    "Pre-PCR文库投入量": sample.pre_library_load,
                    "Pre-PCR文库质量": pre_pcr_library_quality,
                    "Pre-PCR文库总量(ng) ":sample.pre_pcr_library_amount,
                    "index1编号": sample.index1,
                    "index2编号": sample.index2,
                    "该pool总数据量": pool_info['total_data_volume'],
                    "该pool到期样本数": pool_info['tat_sample_num'],
                    "该pool总文库投入量": pool_info['total_load'],
                    "pool名称": f"{probe}_{pool_name}",
                    "是否纯THY": not sample.notthy,
                    "提示信息": pool_info['msg'],
                }
                pool_msg[name]['总index'].append(sample.index1 + '_' + sample.index2)
                rows.append(sample_data)
            if check_thy:
                pool_msg[name]["是否纯THY"] = True
            else:
                pool_msg[name]["是否纯THY"] = False
            pool_list.append(pool_msg)
    #print(pool_msg)
    #print(rows)
    # 创建 DataFrame
    df = pd.DataFrame(rows)
    # 输出到 Excel 文件
    excel_file_path = './samples_output.xlsx'
    df.to_excel(excel_file_path, index=False, sheet_name='Samples')
    return pool_msg,excel_file_path


def check_index(pool_msg):
    index_map = {}

    # 遍历字典并填充 index_map
    for key, value in pool_msg.items():
        for index in value['总index']:
            if index not in index_map:
                index_map[index] = []
            index_map[index].append(key)
        # 找到重复的 index 元素及其对应的键对
    duplicates = {index: keys for index, keys in index_map.items() if len(keys) > 1}

        # 输出结果
    #for index, keys in duplicates.items():
    #    print(f"Index '{index}' 出现在以下键中: {keys}")
    #print(duplicates)
    return duplicates


class Chip:
    def __init__(self, volume, chip_type):
        """
        初始化 Chip 实例。

        :param volume: 芯片的体积（volume）
        :param chip_type: 芯片的类型（type）
        """
        self.max_volume = volume  # 芯片的体积
        self.type = chip_type  # 芯片的类型
        self.pool_list = []
        self.volume = 0
        self.index_list = []
        self.msg = []

    def __repr__(self):
        return f"Chip({self.type}, {self.volume}, {self.pool_list}, " \
               f" {self.msg}, )"


    def add_index(self,list):
        for index in list:
            self.index_list.append(index)


    def add_pool(self, pool,pool_name):
        self.add_index(pool["总index"])
        self.pool_list.append(pool_name)
        self.volume += pool['该pool总数据量']


def calculate_lane_num(pool_msg):
    lane_count = 0
    for keys in pool_msg.values():
        # 每个列表中的元素数量就是需要的 lane 数量
        lane_count = max(lane_count, len(keys))
    #print(lane_count)
    if lane_count > 4:
        return False
    else:
        return True

def can_add_to_dict(current_dict, pool_name, duplicates):
    """ 检查当前字典是否可以添加该pool """
    for key in current_dict:
        if pool_name in duplicates.get(key, []):
            return False
    return True

def add_pool_to_chip(pool_msg, index_dict_info):
    sorted_pools = sorted(pool_msg.items(), key=lambda x: x[1]['该pool总数据量'], reverse=True)
    result = []
    for pool_name, pool_info in sorted_pools:
        placed = False
        for d in result:
            # 计算当前字典的总数据量
            total_data = sum(pool_msg[name]['该pool总数据量'] for name in d)
            # 检查是否可以将 pool 添加到字典 d
            if total_data + pool_info['该pool总数据量'] <= 200 and can_add_to_dict(d, pool_name, index_dict_info):
                d.append(pool_name)
                placed = True
                break
        if not placed:
            new_dict = [pool_name]
            result.append(new_dict)

    return result

def cheat_evo(pool_msg,sorted_pool_name,chip_list):
    index_dict_info = check_index(pool_msg)
    if index_dict_info is False:
        evo = Chip(820, f"evo")
        for pool_name in sorted_pool_name:
            evo.add_pool(pool_msg[pool_name], pool_name)
            sorted_pool_name.remove(pool_name)
            del pool_msg[pool_name]
        chip_list.append(evo)
    else:
        if calculate_lane_num(index_dict_info) is False:
            print("无法分lane，需要的lane数大于4，请修改排机表。")
        else:
            print("可以分lane")
            #print(index_dict_info)
            allo = add_pool_to_chip(pool_msg, index_dict_info)
            #print(allo)
            for i, d in enumerate(allo):
                if i < 4:
                    evo = Chip(205, f"evo{i}")
                    for pool in d:
                        evo.add_pool(pool_msg[pool], pool)
                    chip_list.append(evo)
                #print(f"字典 {i + 1}: {d} (总数据量: {sum(pool_msg[name]['该pool总数据量'] for name in d)})")
                else:
                    break
            #print(chip_list)


def cheat_pool_list(pool_msg):
    move_to_end_prefixes = ('wes', 'ecs', 'hc79')
    # 输出结果
    #print(pool_list)
    chip_list = []
    pool_names = []
    total_tumor_data_volume = 0
    total_genetic_data_volume = 0
    print(pool_msg)
    sorted_pool_name = sorted(pool_msg.keys(), key=lambda k: pool_msg[k]['到期样本数'], reverse=True)
    print(sorted_pool_name)
    for name, value in pool_msg.items():
        pool_names.append(name)
        if name.split('_')[0] not in ["wes", "ecs", "hc79"]:
            total_tumor_data_volume += value['该pool总数据量']
        else:
            total_genetic_data_volume += value['该pool总数据量']
    all_data_volume = total_tumor_data_volume + total_genetic_data_volume
    print(all_data_volume)
    wes_list = []
    for name in pool_msg:
        if name.startswith('wes'):
            wes_list.append(name)
    sorted_wes_list = sorted(wes_list, key=lambda name: pool_msg[name]['到期样本数'], reverse=True)
    #print(sorted_wes_list)
    if all_data_volume <= 820:
        cheat_evo(pool_msg, sorted_pool_name, chip_list)
    elif all_data_volume > 820 and all_data_volume <= 895:
        pro = Chip(75, "pro")
        thy_list = check_thy_pool_num(sorted_pool_name,pool_msg)
        #print(thy_list)
        if len(thy_list) > 2:
            for thy_pool in thy_list[:1]:
                pro.add_pool(pool_msg[thy_pool], thy_pool)
                del pool_msg[thy_pool]
                sorted_pool_name.remove(thy_pool)
        else:
            for thy_pool in thy_list:
                pro.add_pool(pool_msg[thy_pool], thy_pool)
                del pool_msg[thy_pool]
                sorted_pool_name.remove(thy_pool)
            for name in ["abl", "hrd", "trs", "thy116_dna", "thy116_rna", "arf", "hc79"]:
                for pool_name in sorted_pool_name:
                    if pool_name.startswith(name) and pro.volume <= 80:
                        pro.add_pool(pool_msg[pool_name], pool_name)
                        del pool_msg[pool_name]
                        sorted_pool_name.remove(pool_name)
            chip_list.append(pro)
            cheat_evo(pool_msg, sorted_pool_name, chip_list)
            print(chip_list)
    elif all_data_volume > 895 and all_data_volume <= 975:
        cheat_wes_pro(pool_msg, sorted_wes_list[0], sorted_pool_name, chip_list,0)
        cheat_evo(pool_msg, sorted_pool_name, chip_list)
    elif all_data_volume > 975 and all_data_volume <= 1125:
        if len(sorted_wes_list)>=2:
            cheat_wes_pro(pool_msg, sorted_wes_list[0], sorted_pool_name, chip_list,0)
            cheat_wes_pro(pool_msg, sorted_wes_list[1], sorted_pool_name, chip_list,1)
            cheat_evo(pool_msg, sorted_pool_name, chip_list)
        else:
            print("本批次的wespool不足以杂2张150G芯片!")
    elif all_data_volume > 1125:
        cheat_wes_pro(pool_msg, sorted_wes_list[0], sorted_pool_name, chip_list, 0)
        cheat_wes_pro(pool_msg, sorted_wes_list[1], sorted_pool_name, chip_list, 1)
        cheat_evo(pool_msg, sorted_pool_name, chip_list)
        print("今天数据量太多了！！！拿掉一点再排机")
    print(chip_list)
    return chip_list


def cheat_wes_pro(pool_msg,wes_pool,sorted_pool_name,chip_list,num):
    pro = Chip(150, f"pro{num}")
    if pool_msg[wes_pool]["该pool总数据量"] > 130:
        pro.add_pool(pool_msg[wes_pool], wes_pool)
        sorted_pool_name.remove(wes_pool)
        del pool_msg[wes_pool]
        chip_list.append(pro)
    else:
        print("这批次没有满足150G芯片杂交要求的wes pool")

def check_thy_pool_num(pool_names, pool_msg):
    thy_list = []
    for name in pool_msg:
        if pool_msg[name]["是否纯THY"] is True:
            thy_list.append(name)
    sorted_thy_list = sorted(thy_list, key=lambda name: pool_msg[name]['到期样本数'], reverse=True)
    return sorted_thy_list

def check_all_index(pool_list):
    """
    :param pool_list:
    :return: 是否有index重复
    """
    combined_list = []
    for pool in pool_list:
        for name, value in pool.items():
            combined_list += value["总index"]
    # 统计元素出现的次数
    counter = Counter(combined_list)

    # 找到重复的元素
    duplicates = {item: count for item, count in counter.items() if count > 1}
    return duplicates

def read_pool_file(pool_file):
    df = pd.read_excel(pool_file,header=0)
    pool_msg = {}
    for index, row in df.iterrows():
        index_combine = row['index1编号'] + '_' + row['index2编号']
        if row['pool名称'] not in pool_msg:
            pool_msg[row['pool名称']]={
                "到期样本数":row['该pool到期样本数'],
                "该pool总数据量":row['该pool总数据量'],
                '是否纯THY': row['是否纯THY'],
                "总index": [index_combine]
            }
        else:
            pool_msg[row['pool名称']]["总index"].append(index_combine)
    #print(pool_msg)
    return pool_msg


def add_chip_result(pool_file,chip_list):
    df = pd.read_excel(pool_file, header=0)
    chip_msg = {}
    df["排机"] = ""
    df["数据量"] = 0
    for chip in chip_list:
        for pool in chip.pool_list:
            chip_msg[pool] = {}
            chip_msg[pool]["name"] = chip.type
            chip_msg[pool]["volume"] = chip.volume
    #print(chip_msg)
    for index, row in df.iterrows():
        pool_name = row['pool名称']
        if pool_name in chip_msg:  # 检查 pool_name 是否存在于 chip_msg
            df.at[index, "排机"] = chip_msg[pool_name]["name"]
            df.at[index, "数据量"] = chip_msg[pool_name]["volume"]# 使用 at 方法更新
    # 获取今天的日期
    today = datetime.now()
    # 格式化日期为 YYYY-MM-DD
    formatted_date = str(today.strftime('%Y-%m-%d'))
    # 输出结果
    excel_file_path = f"{formatted_date}排机结果.xlsx"
    df.to_excel(excel_file_path, index=False, sheet_name='Samples')


if __name__ == "__main__":
    # 指定 Excel 文件路径
    excel_file_path = '/Users/zhouyong/Desktop/DA/23.实验室index排机/测试数据3.xls'
    samples = read_samples_from_excel(excel_file_path)
    pool_msgs,pool_file = cheat_samples(samples)
    #如果直接修改分line文件，就吧pool_file改成修改后的分line文件，否则，该行注释掉
    #pool_file = '/Users/zhouyong/Desktop/DA/23.实验室index排机/samples_output_2.xlsx'
    #pool_msgs = read_pool_file(pool_file)
    chip_list = cheat_pool_list(pool_msgs)
    add_chip_result(pool_file,chip_list)
    #for probe_type, sample_list in samples.items():
    #    print(f"Probe Type: {probe_type}")
    #    for sample in sample_list:
    #        print(f"  {sample}")

