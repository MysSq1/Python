# 导入库函数
import pandas as pd
import random
#读取原数据集的路径
file_path = 'clean_beautymakeup.xlsx'
data_frame = pd.read_excel(file_path)
# 中国的32个地区名称示例列表
china_regions = ['北京市', '天津市', '河北省', '深圳市', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省', '上海市','江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省','广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省', '云南省', '西藏自治区', '陕西省', '甘肃省', '甘肃省','宁夏回族自治区','新疆维吾尔自治区']
# 在数据框中添加一个新列并随机插入地区名称
data_frame['地区'] = random.choices(china_regions, k=len(data_frame))
# 按地区分组并计算销售总额
sales_by_region = data_frame.groupby('地区')['销售额'].sum().reset_index()
# 导出到另一个表格
output_file = '插入地区后的数据.xlsx'  # 导出的文件名
data_frame.to_excel(output_file, index=False)  # index=False 表示不保留行索引
#用于按照地区计算销售总额
file_path = '插入地区后的数据.xlsx'
data_frame = pd.read_excel(file_path)
# 选择需要的列
selected_data = data_frame.iloc[:, [12, 10]]  # 假设索引从0开始计数，第11列对应索引10，第13列对应索引12
# 重命名列名
selected_data.columns = ['地区','销售额']
# 按地区分组并计算销售总额
sales_by_region = selected_data.groupby('地区')['销售额'].sum().reset_index()
# 导出到另一个表格
output_file = '计算出每个地区的销售额.xlsx'  # 导出的文件名
sales_by_region.to_excel(output_file, index=False)  # index=False 表示不保留行索引
sales_df = pd.read_excel('计算出每个地区的销售额.xlsx')
# 读取第二个文件 各地区省分经纬度和销售额.xlsx
coords_df = pd.read_excel('各地区省分经纬度和销售量.xlsx')
# 将两个数据框根据地区列合并，以省份为键，合并销售额
merged_df = pd.merge(coords_df, sales_df, on='地区')
# 重命名合并后的销售额列为 '销售额'
merged_df.rename(columns={'销售额_x': '经度', '销售额_y': '销售额'}, inplace=True)
# 选择需要的列
result_df = merged_df[['地区', '经度', '纬度', '销售额']]
# 用于绘制3D图的数据
result_df.to_excel('用于绘制3D图的数据.xlsx', index=False)