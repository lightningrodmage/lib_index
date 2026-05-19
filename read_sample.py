import pandas as pd
import json

# 读取 Excel 文件
file_path = '样本册明细.xlsx'  # 将此处替换为你的文件路径
df = pd.read_excel(file_path)

# 初始化一个空字典
result_dict = {}

# 遍历 DataFrame 的每一行，构建字典
for index, row in df.iterrows():
    project_start = row['project_start']
    sample_type = row['sample_type']
    probe_type = row['probe_type']

    # 如果 project_start 不在字典中，初始化一个新字典
    if project_start not in result_dict:
        result_dict[project_start] = {}

    # 将 sample_type 和 probe_type 添加到对应的字典中
    result_dict[project_start]['sample_type'] = sample_type
    result_dict[project_start]['probe_type'] = probe_type

# 将结果保存为 JSON 文件
output_json_path = 'output.json'  # 输出 JSON 文件的路径
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(result_dict, json_file, ensure_ascii=False, indent=4)

print("字典已成功保存为 JSON 文件。")
