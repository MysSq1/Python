#导入库函数
import pandas as pd
from pyecharts.options import InitOpts, TitleOpts, VisualMapOpts, ItemStyleOpts
from pyecharts.charts import Map3D
from pyecharts.globals import ChartType

file_path = '用于绘制3D图的数据.xlsx'  # 设置文件路径
data_frame = pd.read_excel(file_path)  # 使用 Pandas 读取 Excel 文件中的数据
# 将读取到的数据转换为列表
data_list = data_frame.values.tolist()  # 将 Pandas DataFrame 转换为 Python 列表
# 将数据整理成与之前 data_pair 相同的格式
formatted_data = [(row[0], [row[1], row[2], row[3]]) for row in data_list]  # 格式化数据为元组列表，包含地理位置及对应数值
map3d = (
    Map3D(init_opts=InitOpts(theme='dark', width='99vw', height='97vh'))  # 初始化 Map3D 图表，设置主题、宽度和高度
    .add_schema(  # 添加地图图表的基本配置
        maptype='china',  # 地图类型为中国地图
        itemstyle_opts=ItemStyleOpts(  # 设置图形样式
            color="lightblue",  # 地图区块颜色为浅蓝色
            border_width=2,  # 描边大小为2
            border_color="white",  # 描边颜色为白色
            opacity=0.1,  # 柱子透明度为0.1
        ),
    )
    .set_global_opts(  # 设置全局配置
        title_opts=TitleOpts(title="中国每个地区的销售额"),  # 设置标题
        visualmap_opts=VisualMapOpts(is_show=True, max_=1500000000),  # 设置视觉映射组件，显示最大值为15亿
    )
    .add(  # 添加数据到图表中
        series_name='销售额',  # 设置数据系列名称
        data_pair=formatted_data,  # 设置数据对，包含地理位置及对应数值
        type_=ChartType.BAR3D,  # 设置图表类型为3D柱状图
        bar_size=1,  # 设置柱子大小
    )
)
map3d.render("3D.html")  # 将图表渲染为 HTML 文件