from numpy import linalg,zeros,dot,sqrt,array,diag,sum,log
from scipy.stats import norm
from pandas import DataFrame
from statsmodels.api import tsa
from preprocessing import save_output,output_path
from systemic_financial_risk_monitoring.draw_img import draw_hist


'''正式分析处理'''
# PCA分析
def pca(market, index_num, order_norm_data):
    # 求相关系数矩阵,并保存
    save_output( market, order_norm_data.corr(),"corr")
    # 求特征值和特征向量
    eig_value, eig_vector = linalg.eig(order_norm_data.cov())
    # 取特征值占比和大于80%的主成分
    principal_num = 6
    for principal_num in range(index_num):
        if sum(eig_value[:principal_num])/sum(eig_value) > 0.8:
            break
    print(market+"维度主成分数：", principal_num)
    # 计算成分系数/因子载荷矩阵
    factor_loading = zeros((index_num, principal_num))
    for i in range(principal_num):
        factor_loading[:,i] = eig_vector[:,i] * sqrt(eig_value[i])
    factor_loading = DataFrame(factor_loading, index=order_norm_data.columns[-index_num:],
                                  columns=["主成分" + str(i+1) for i in range(principal_num)])
    # factor_loading.to_excel(path +"factor_loading_" + market + "维度.xlsx")
    save_output( market, factor_loading, "loading")
    # 计算因子贡献值/成分系数绝对值和
    factor_coefficient = factor_loading / eig_value.std()
    factor_contrib = factor_coefficient.abs().sum(axis=1)
    factor_contrib.to_excel(output_path(market, prefix="contrib"), header=["成分系数绝对值和"])
    # 输出PCA降维结果
    # PCA_data = np.dot(order_norm_data, eig_vector[:,:principal_num])
    # res = pd.DataFrame(PCA_data, columns=["主成分" + str(i) for i in range(1, principal_num+1)])
    # res.to_excel(path +"PCA_" + market + "维度.xlsx")


# 加权合成子市场指数，返回值包含日期索引、单个market指数
def combine(market, order_norm_data, chosen_index, stats):
    # print(order_norm_data[chosen_index].values)
    market_index = DataFrame(dot(array(order_norm_data[chosen_index].values),
                                diag(stats[chosen_index].values[1])).sum(axis=1)
                                /sum(stats[chosen_index].values[1]),
                                index=order_norm_data.index,columns=[market])
    # print(market_index)
    return market_index

def risk_possibility(label, data, regime):
    possibility = DataFrame(index=data.index, columns=[label,*regime])
    possibility[label] = log(data[label].values.astype(float))
    draw_hist(label + "（自然对数）概率密度分布直方图", label+"自然对数",possibility[label].values, {
        "line1": {"mean": -.7, "std": .167},
        "line2": {"mean": -.58, "std": .126}
    })
    possibility[regime[0]] = norm.pdf((possibility[label] + .9017) / 0.2)
    possibility[regime[1]] = norm.pdf((possibility[label] + .6418) / 0.2)
    # possibility[regime[0]] = possibility[regime[0]] / (possibility[regime[0]] + possibility[regime[1]])
    # possibility[regime[1]] = 1 - possibilit y[regime[0]]
    return possibility

def markov_analysis(data):
    model = tsa.MarkovRegression(data, k_regimes=2, order=5, switching_variance=True,trend='c')
    result = model.fit()
    print(result.summary())
    # model = tsa.MarkovAutoregression(data, k_regimes=2, order=5, switching_variance=False)
    # result = model.fit()
    # print(result.summary())