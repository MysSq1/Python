# 导入库函数
import pandas as pd
import jieba
import matplotlib.pyplot as plt
import seaborn as sns

 # 读取 CSV 文件数据
data = pd.read_csv('双十一淘宝美妆数据.csv')
data.head()  # 展示数据的前几行
# 对重复数据进行删除处理
print(data.shape)  # 打印数据形状
data = data.drop_duplicates(inplace=False)  # 删除重复行
print(data.shape)  # 打印处理后数据形状
# 重置索引
data = data.reset_index(drop=True)  # 重置索引为新的整数索引
print('新索引：', data.index)  # 打印新的数据索引
# 查看 sale_count 列的众数
mode_01 = data['sale_count'].mode()  # 计算 sale_count 列的众数
print("sale_count列的众数：", mode_01)  # 打印 sale_count 列的众数
# 查看 comment_count 列的众数
mode_02 = data['comment_count'].mode()  # 计算 comment_count 列的众数
print("comment_count列的众数：", mode_02)  # 打印 comment_count 列的众数
# 填充缺失值为0
data = data.fillna(0)  # 将缺失值填充为0
# 对空值行数求和
null_sum = data.isnull().sum()  # 计算缺失值总数
print("缺失值总数：", null_sum.sum())  # 打印缺失值总数
# 结巴分词库
title_cut = []
for i in data.title:
    j = jieba.lcut(i)  # 对标题进行结巴分词
    title_cut.append(j)
# 对标题进行分词，新增 item_name_cut 列
data['item_name_cut'] = title_cut  # 将分词结果添加为新列
data[['title', 'item_name_cut']].head()  # 展示标题和分词后的结果
# 给商品添加分类
basic_config_data = """ 护肤品    套装    套装  
护肤品    乳液类    乳液    美白乳    润肤乳    凝乳    柔肤液'    亮肤乳    菁华乳    修护乳
护肤品    眼部护理    眼霜    眼部精华    眼膜                    
护肤品    面膜类    面膜                                                    
护肤品    清洁类    洗面    洁面    清洁    卸妆    洁颜    洗颜    去角质    磨砂                        
护肤品    化妆水    化妆水    爽肤水    柔肤水    补水露    凝露    柔肤液    精粹水    亮肤水    润肤水    保湿水    菁华水    保湿喷雾    舒缓喷雾
护肤品    面霜类    面霜    日霜    晚霜    柔肤霜    滋润霜    保湿霜    凝霜    日间霜    晚间霜    乳霜    修护霜    亮肤霜    底霜    菁华霜
护肤品    精华类    精华液    精华水    精华露    精华素                                        
护肤品    防晒类    防晒霜    防晒喷雾                                                
化妆品    口红类    唇釉    口红    唇彩                                            
化妆品    底妆类    散粉    蜜粉    粉底液    定妆粉     气垫    粉饼    BB    CC    遮瑕    粉霜    粉底膏    粉底霜        
化妆品    眼部彩妆    眉粉    染眉膏    眼线    眼影    睫毛膏                                    
化妆品    修容类    鼻影    修容粉    高光    腮红                                        
其他    其他    其他 """
# 将字符串basic_config_data 转为字典 category_config_map
category_config_map = {}
for config_line in basic_config_data.split('\n'):
    basic_cateogry_list = config_line.strip().strip('\n').strip('    ').split('    ')
    main_category = basic_cateogry_list[0]
    sub_category = basic_cateogry_list[1]
    unit_category_list = basic_cateogry_list[2:-1]
    for unit_category in unit_category_list:
        if unit_category and unit_category.strip().strip('    '):
            category_config_map[unit_category] = (main_category, sub_category)
category_config_map
def func1(row):
    sub_type = ''  # 子类别
    main_type = ''  # 主类别
    exist = False
    # 遍历item_name_cut 里每个词语
    for temp in row:
        # 如果词语包含在category_config_map里面，打上子类和主类标签
        if temp in category_config_map:
            sub_type = category_config_map.get(temp)[1]
            main_type = category_config_map.get(temp)[0]
            exist = True
            break
    if not exist:
        sub_type = '其他'
        main_type = '其他'
    return [sub_type, main_type]
data['sub_type'] = data['item_name_cut'].map(lambda r: func1(r)[0])  # 将子类别sub_type新增为一列
data['main_type'] = data['item_name_cut'].map(lambda r: func1(r)[1]) # 将主类别main-type新增为一列
data.head()
# 将“是否男士专用”新增为一列
gender = []
for i in range(len(data)):
    if '男' in data.item_name_cut[i]:
        gender.append('是')
    elif '男士' in data.item_name_cut[i]:
        gender.append('是')
    elif '男生' in data.item_name_cut[i]:
        gender.append('是')
    else:
        gender.append('否')
# 将“是否男士专用”新增为一列
gender = []
for i in range(len(data)):
    if '男' in data.item_name_cut[i]:
        gender.append('是')
    elif '男士' in data.item_name_cut[i]:
        gender.append('是')
    elif '男生' in data.item_name_cut[i]:
        gender.append('是')
    else:
        gender.append('否')
# 将“是否男士专用”新增为一列
data['是否男士专用'] = gender  # 将判断结果添加为新列
data.head()  # 展示数据的前几行

# 新增销售额、购买日期（天）为一列
data['销售额'] = data.sale_count * data.price  # 计算销售额并添加为新列
data['update_time'] = pd.to_datetime(data['update_time'])  # 转换时间格式
data[['update_time']].head()  # 展示更新时间的前几行

# 将时间设置为新的 index
data = data.set_index('update_time')  # 将更新时间设置为新的数据索引
data['day'] = data.index.day  # 新增天数为一列
del data['item_name_cut']  # 删除中文分词的一列
data.head()  # 展示数据的前几行
# 保存清理好的数据为 Excel 格式
data.to_excel('./clean_beautymakeup.xlsx', sheet_name='clean_data')  # 将数据保存为 Excel 文件
data.columns  # 打印数据的列名
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
# 创建图表，展示各个店铺的商品数量
plt.figure(figsize=(12, 7))
data['店名'].value_counts().sort_values(ascending=False).plot.bar(width=0.8, alpha=0.6, color='b')
plt.title('各品牌SKU数', fontsize=18)
plt.ylabel('商品数量', fontsize=14)
plt.show()

# 创建两个子图，展示品牌总销售量和总销售额
fig, axes = plt.subplots(1, 2, figsize=(12, 10))
ax1 = data.groupby('店名').sale_count.sum().sort_values(ascending=True).plot(kind='barh', ax=axes[0], width=0.6)
ax1.set_title('品牌总销售量', fontsize=12)
ax1.set_xlabel('总销售量')
ax2 = data.groupby('店名')['销售额'].sum().sort_values(ascending=True).plot(kind='barh', ax=axes[1], width=0.6)
ax2.set_title('品牌总销售额', fontsize=12)
ax2.set_xlabel('总销售额')
plt.subplots_adjust(wspace=0.4)
plt.show()

# 创建两个子图，展示主类别销售量占比和子类别销售量占比的饼图
fig, axes = plt.subplots(1, 2, figsize=(18, 12))
data1 = data.groupby('main_type')['sale_count'].sum()
ax1 = data1.plot(kind='pie', ax=axes[0], autopct='%.1f%%',  # 设置百分比的格式，这里保留一位小数
                 pctdistance=0.8,  # 设置百分比标签与圆心的距离
                 labels=data1.index,
                 labeldistance=1.05,  # 设置标签与圆心的距离
                 startangle=60,  # 设置饼图的初始角度
                 radius=1.2,  # 设置饼图的半径
                 counterclock=False,  # 是否逆时针，这里设置为顺时针方向
                 wedgeprops={'linewidth': 1.2, },  # 设置饼图内外边界的属性值
                 textprops={'fontsize': 16, 'color': 'k', 'rotation': 80},  # 设置文本标签的属性值
                 )
ax1.set_title('主类别销售量占比', fontsize=20)
data2 = data.groupby('sub_type')['sale_count'].sum()
ax2 = data2.plot(kind='pie', ax=axes[1], autopct='%.1f%%',
                 pctdistance=0.8,
                 labels=data2.index,
                 labeldistance=1.05,
                 startangle=230,
                 radius=1.2,
                 counterclock=False,
                 wedgeprops={'linewidth': 1.2, },
                 textprops={'fontsize': 16, 'color': 'k', 'rotation': 80},
                 )
ax2.set_title('子类别销售量占比', fontsize=20)
# 设置坐标标签
ax1.set_xlabel(..., fontsize=16, labelpad=38.5)
ax1.set_ylabel(..., fontsize=16, labelpad=38.5)
ax2.set_xlabel(..., fontsize=16, labelpad=38.5)
ax2.set_ylabel(..., fontsize=16, labelpad=38.5)
plt.subplots_adjust(wspace=0.4)
plt.show()
# 设置图表大小
plt.figure(figsize=(18, 8))
# 使用Seaborn的barplot展示不同品牌在不同总类别下的总销量，hue参数用于根据主类型（main_type）进行分组着色
sns.barplot(x='店名', y='sale_count', hue='main_type', data=data, saturation=0.75)
# 设置图表标题和坐标轴标签
plt.title('各品牌各总类的总销量', fontsize=20)
plt.ylabel('销量', fontsize=16)
plt.xlabel('店名', fontsize=16)
# 在图表中添加文字说明，提醒观察者也可使用堆叠图
plt.text(0, 78000, '注：此处也可使用堆叠图，对比效果更直观',
         verticalalignment='top', horizontalalignment='left', color='gray', fontsize=10)
# 设置刻度的字体大小和旋转角度
plt.xticks(fontsize=16, rotation=45)
plt.yticks(fontsize=16)
# 展示图表
plt.show()
# 设置图表大小
plt.figure(figsize=(18, 8))
# 使用Seaborn的barplot展示不同品牌在不同总类别下的总销售额，根据主类型（main_type）进行分组着色
sns.barplot(x='店名', y='销售额', hue='main_type', data=data, saturation=0.75)
# 设置图表标题和坐标轴标签
plt.ylabel('销售额', fontsize=16)
plt.xlabel('店名', fontsize=16)
plt.title('各品牌各总类的总销售额', fontsize=20)
# 设置刻度的字体大小和角度
plt.xticks(fontsize=16, rotation=45)
plt.yticks(fontsize=16)
plt.show()
# 设置图表大小
plt.figure(figsize=(16, 6))
# 使用Seaborn的barplot展示不同品牌在不同子类别下的总销量，根据子类型（sub_type）进行分组着色
sns.barplot(x='店名', y='sale_count', hue='sub_type', data=data, saturation=0.75)
# 设置图表标题和坐标轴标签
plt.title('各品牌各子类的总销量')
plt.ylabel('销量')
plt.show()
# 设置图表大小
plt.figure(figsize=(14, 6))
# 使用Seaborn绘制以店名和子类别为分组的销售额条形图
sns.barplot(x='店名',
            y='销售额', hue='sub_type', data=data, saturation=0.75)
plt.title('各品牌各子类的总销售额')  # 设置图表标题为各品牌各子类的总销售额
plt.ylabel('销售额')  # 设置y轴标签为销售额
plt.show()  # 展示图表
# 创建新图表
plt.figure(figsize=(12, 6))
# 绘制各品牌商品平均评论数的柱状图
data.groupby('店名').comment_count.mean().sort_values(ascending=False).plot(kind='bar', width=0.8)
plt.title('各品牌商品的平均评论数')  # 设置图表标题为各品牌商品的平均评论数
plt.ylabel('评论数')  # 设置y轴标签为评论数
plt.show()  # 展示图表
# 创建新图表
plt.figure(figsize=(18, 12))
# 分别计算各店铺的平均销售数量、平均评论数量和平均价格，并储存在变量中
x = data.groupby('店名')['sale_count'].mean()
y = data.groupby('店名')['comment_count'].mean()
s = data.groupby('店名')['price'].mean()
txt = data.groupby('店名').id.count().index  # 获取店名
# 创建箱型图
plt.figure(figsize=(18, 10))
sns.boxplot(x='店名', y='price', data=data)
plt.ylim(0, 3000)  # 限制Y轴刻度在0到3000之间，便于观察箱型图的分布情况
plt.show()  # 展示箱型图
# 按店铺分组计算商品价格总和
data.groupby('店名').price.sum()
# 计算各店铺商品平均价格
avg_price = data.groupby('店名').price.sum() / data.groupby('店名').price.count()
# 创建图表，设置大小为12英寸宽、6英寸高
fig = plt.figure(figsize=(12, 6))
# 绘制各品牌平均价格的柱状图
avg_price.sort_values(ascending=False).plot(kind='bar', width=0.8, alpha=0.6, color='b', label='各品牌平均价格')
y = data['price'].mean()  # 获取全品牌平均价格
plt.axhline(y, 0, 5, color='r', label='全品牌平均价格')  # 绘制全品牌平均价格的水平线
plt.ylabel('各品牌平均价格')  # 设置y轴标签为各品牌平均价格
plt.title('各品牌产品的平均价格', fontsize=24)  # 设置图表标题为各品牌产品的平均价格，字体大小为24
plt.legend(loc='best')  # 设置图例位置为最佳位置
plt.show()  # 展示图表
# 从数据中筛选出男士专用的产品数据
gender_data = data[data['是否男士专用'] == '是']
# 从男士专用产品数据中筛选出护肤品和化妆品的数据
gender_data_1 = gender_data[(gender_data.main_type == '护肤品') | (gender_data.main_type == '化妆品')]
# 绘制柱状图展示各店铺男士专用护肤品和化妆品的销量情况
plt.figure(figsize=(12, 6))
sns.barplot(x='店名', y='sale_count', hue='main_type', data=gender_data_1, saturation=0.75)
plt.show()
# 创建图表
f, [ax1, ax2] = plt.subplots(1, 2, figsize=(12, 6))
# 按店铺分组统计男士护肤品销量总和，并绘制水平柱状图展示排名情况
gender_data.groupby('店名').sale_count.sum().sort_values(ascending=True).plot(kind='barh', width=0.8, ax=ax1)
ax1.set_title('男士护肤品销量排名')  # 设置第一个图表标题为男士护肤品销量排名
# 按店铺分组统计男士护肤品销售额总和，并绘制水平柱状图展示排名情况
gender_data.groupby('店名').销售额.sum().sort_values(ascending=True).plot(kind='barh', width=0.8, ax=ax2)
ax2.set_title('男士护肤品销售额排名')  # 设置第二个图表标题为男士护肤品销售额排名
plt.subplots_adjust(wspace=0.4)  # 调整两个图表之间的水平间距为0.4
plt.show()  # 展示图表