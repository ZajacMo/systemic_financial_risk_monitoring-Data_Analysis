from arch import arch_model
from numpy import average
from pandas import ExcelWriter,read_excel,to_datetime,DataFrame


'''数据预处理'''

def data_path(market):
    return "..\\db\\"+ "data_" + market + "维度.xlsx"

def output_path(market, prefix="output"):
    return "..\\output\\"+ prefix +"_" + market + "维度.xlsx"

def read_data(market,sheet = "Sheet1"):
    return read_excel(data_path(market), engine='openpyxl',sheet_name=sheet,index_col=0)

def save_output(market, output, prefix="output", stats = None, path = None):
    if path is None:
        path = output_path(market, prefix)
    with ExcelWriter(path) as file:
        output.to_excel(file, sheet_name="Sheet1")
        #设置列宽
        worksheet = file.sheets["Sheet1"]
        for idx in range(output.shape[1]+1):
            worksheet.set_column(idx, idx, 20)
        if stats is not None:
            stats.to_excel(file, sheet_name="Sheet2")
            worksheet = file.sheets["Sheet2"]
            for idx in range(stats.shape[1]+1):
                worksheet.set_column(idx, idx, 20)

# 计算原始数据的波动率
def get_arch(market, cols_to_convert):
    data = read_data(market, "Sheet1")
    stats = read_data(market, "Sheet2")
    for col in cols_to_convert:
        am = arch_model(data[col]*100,x=data.index,mean='Zero', vol='GARCH', dist='normal')
        output = am.fit(disp='off').conditional_volatility
        data[col + "波动率(%)"] = output
    # data.to_excel(data_path(market), sheet_name="Sheet1")
    save_output(market, data, "data", stats, data_path(market))

# 数据清洗
def clean(market):
    data = read_data(market, "Sheet1")
    stats = read_data(market, "Sheet2")
    data.interpolate(method='linear', axis=0, inplace=True)
    data.dropna(inplace=True)
    data.index = to_datetime(data.index, format='%Y/%m/%d').date
    data.index.name = "日期"
    save_output(market, data, "data", stats, data_path(market))

# 填充空白，更改格式
def fix_data(market, index ="日期"):
    data = read_data(market, "Sheet1")
    stats = read_data(market, "Sheet2")
    # 更改索引格式为日期
    data[index] = to_datetime(data[index], format='%Y/%m/%d')
    data.set_index(index, inplace=True)
    # 线性插值
    data.interpolate(method='linear', axis=0, inplace=True)
    save_output(market, data, "data", stats, data_path(market))

# 统一量纲,实现累积分布排序
def unify_unity(market, index_num):
    # 读取数据
    data = read_data(market, "Sheet1")
    stats = read_data(market, "Sheet2")
    # 选取待分析的全部指标
    order_norm_data = DataFrame(index=data.index, columns=data.columns[-index_num:])
    # 判断指标与风险的相关性，根据相关性实现累积分布排序
    for i in order_norm_data.columns:
        if stats[i].values[0] == "同向":
            order_norm_data[i] = data[i].rank(axis=0, method='first') / data[i].count()
        elif stats[i].values[0] == "反向":
            order_norm_data[i] = 1 - data[i].rank(axis=0, method='first') / data[i].count()
        elif stats[i].values[0] == "双向":
            temp = (data[i] - average(data[i])).abs()
            order_norm_data[i] = temp.rank(axis=0, method='first') / temp.count()
        else:
            print("error")
    return order_norm_data, stats