from numpy import dot,diag,power,multiply,log
from pandas import concat,to_datetime
from algorithm import pca, combine, risk_possibility, markov_analysis
from preprocessing import clean, get_arch, unify_unity, save_output
from draw_img import single_line,double_line
from warnings import filterwarnings
filterwarnings("ignore")
# 市场集合
markets = ["股票市场","债券市场","外汇市场","货币市场","衍生品市场"]
goal = "系统性金融风险"

# 每个子市场的权重
weights = [0.3,0.3,0.1,0.2,0.1]

# 经过PCA分析后在各市场中选出的指标集合
chosen_indexes = [["市盈率Q","换手率R","融券融资比S","涨跌幅绝对波动U"],# 股票市场
                ["国债期限溢价","综合风险溢价","中证综合债指数波动率(%)"],# 债券市场
                ["人民币汇率市场扭曲程度","美元兑人民币中间价USD/CNY波动率(%)"],# 外汇市场
                ["流动性溢价","银行间质押式回购加权利率:1天（一阶差分）波动率",
                 "银行间质押式回购加权利率:7天（一阶差分）波动率","SHIBOR:3个月（一阶差分）波动率"],# 货币市场
                  ["股值期货价格偏离度","沪深300指数期货日对数收益率波动率(%)"]]# 衍生品市场

# 每个市场中待分析的指标总数量
index_nums = [7,3,2,4,2]

img_format = "svg"

regime = ["中低风险","高风险"]

market_indexes = []

for market, index_num, chosen_index in zip(markets,index_nums,chosen_indexes):
    # 数据预处理
    # clean(market)
    # 读取数据并标准化
    order_norm_data, stats = unify_unity(market, index_num)
    # PCA分析子市场中各三级指标
    pca(market, index_num, order_norm_data)
    # 加权合成子市场指数
    market_index = combine(market, order_norm_data, chosen_index, stats)
    # 绘制子市场指数
    single_line(market+"压力指数",market, market_index.index, market_index.loc[:,market])
    # 将子市场指数添加到列表中
    market_indexes.append(market_index)

# 将列表中的子市场指数合并到一个DataFrame中
data_frame = concat(market_indexes, axis=1)
# 删除空值
data_frame.dropna(axis=0, how='any', inplace=True)
# 将索引转换为时间戳
# data_frame.index = DatetimeIndex(data_frame.index).to_period('D')
# 计算相关系数矩阵
corr = data_frame.corr()
# W*St
vec = dot(data_frame.values, diag(weights))
# 合成系统性金融风险压力指数
data_frame.loc[:,goal] = power(multiply(dot(vec, corr), vec).sum(axis=1), 0.5)*2
data_frame.sort_index(inplace=True, ascending=False)
# 保存合成指数
data_frame.index = to_datetime(data_frame.index, format='%Y/%m/%d').date
data_frame.index.name = "日期"
save_output( goal, data_frame, "指数汇总")
# 绘制合成指数
single_line(goal+"压力指数",goal, data_frame.index, data_frame.loc[:,goal].values)
# 马尔科夫区制转换分析
markov_analysis(log(data_frame.loc[:,goal].values.astype(float)))
# 风险概率分析
possibility = risk_possibility(goal, data_frame, regime)
# possibility[goal] = data_frame.loc[:,goal].values
# save_output("导出数据",possibility)
double_line("风险区制概率密度情况",regime, data_frame.index, possibility)
