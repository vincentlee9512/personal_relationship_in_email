"""
Author: 李文轩

邮件中的人际关系 - 用 PageRank 算法进行分析

这个项目并不考虑邮件本文，只在寄件人 (MetadataFrom) 和收件人 (MetadataTo)的数据中分析人际关系。

这个项目用的是希拉里的邮件作为例子。

数据集：https://github.com/vincentlee9512/personal_relationship_in_email/tree/master/input

项目步骤：

    1. 数据加载

    2. 数据准备阶段：
        - 数据探索：查看数据源中异常情况（空值，异常数据等）
        - 数据清洗：选择性填补空值和异常数据或直接删除无效行；
        - 特征选择：
            - 因为是按照寄件人和收件人分析人际关系，不考虑邮件本文内容，所以选择 MetadataFrom 和 MetadataTo 这两个字段作为特征
            - 计算个人间的寄件次数决定权重，次数越多权重越大

    3. 数据挖掘阶段：
        - PR 值计算
        - PR 值筛选
        - 可视化：绘制时，根据权重大小，决定绘制的节点大小。
"""

import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# 数据加载
# 读取人名，persons是人名集
persons_file = pd.read_csv('./input/Persons.csv')
persons = {}
for index, row in persons_file.iterrows():
    persons[row['Id']] = row['Name']

# 读取别名，用作同一人物的名称，aliases是别名集
aliases_file = pd.read_csv('./input/Aliases.csv')
aliases = {}
for index, row in aliases_file.iterrows():
    aliases[row['Alias']] = row['PersonId']


def format_name(name):
    """
    将名字和别名做统一格式化处理
    :param name: 未经格式化的名字
    :return: 格式化后的名字
    """
    res = name

    # 所有字母改成小写
    res = str(res).lower()

    # 去除逗号和 "@" 后面的内容
    res = res.replace(',', '').split('@')[0]

    # 别名转换
    if res in aliases.keys():
        res = persons[aliases[res]]

    return res


def show_graph(graph, layout='spring_layout'):
    """
    绘制网络图（可视化）
    :param graph: 输入图
    :param layout: 默认值为'spring_layout'，中心放射状
    """
    if layout == 'circular_layout':
        nx_layout = nx.circular_layout(graph)
    else:
        nx_layout = nx.spring_layout(graph)

    # 设置节点大小（与pagerank值有关）；因为pr值很小，所以*20000
    nodesize = [x['pagerank']*20000 for v, x in graph.node(data=True)]

    # 设置边长
    edgesize = [np.sqrt(e[2]['weight']) for e in graph.edges(data=True)]

    # 绘制节点
    nx.draw_networkx(graph, nx_layout, node_size=nodesize, alpha=0.4)

    # 绘制边
    nx.draw_networkx(graph, nx_layout, edge_size=edgesize, alpha=0.2)

    # 绘制节点的label
    nx.draw_networkx(graph, nx_layout, font_size=10)

    # 输出
    plt.show()



def main():

    """
    整个项目的 main 函数

    执行后，将会生成项目数据分析中的人际关系图
    """

    # 数据加载

    # 邮件本文、MetadataFrom、MetadataTo
    emails = pd.read_csv('./input/Emails.csv')

    # 删除空行
    emails.dropna(how='all', inplace=True)

    # 统一格式化 emails 的 MetadataFrom 和 MetadataTo
    emails.MetadataFrom = emails.MetadataFrom.apply(format_name)
    emails.MetadataTo = emails.MetadataTo.apply(format_name)

    # 将图中的边的权重设置为收发邮件的次数
    edges_weights = defaultdict(list)
    for row in zip(emails.MetadataFrom, emails.MetadataTo):
        edge = (row[0], row[1])
        if(edge not in edges_weights):
            edges_weights[edge] = 1
        else:
            edges_weights[edge] += 1

    # 将 ((from, to), weight) 转化为 （from, to, weight) 方便操作
    edges_weights = [(key[0], key[1], val) for (key, val) in edges_weights.items()]

    # 创建一个有向图
    graph = nx.DiGraph()

    # 设置有向图中的路径和权重
    graph.add_weighted_edges_from(edges_weights)

    # 计算每个人的pr值
    pagerank = nx.pagerank(graph)

    # 将 pr 值作为节点的属性
    nx.set_node_attributes(graph, name='pagerank', values=pagerank)

    # 绘制网络图
    # 全图信息量太多，下面给这个图做了精简，忽略pr值过小的节点
    # show_graph(graph)

    # 对全图进行精简
    # 设置pr值阀值，超过这个阀值才会被显示在图上
    pagerank_threshold = 0.005

    # 复制一份全图，删除pr值少于阀值的节点
    small_graph = graph.copy()
    for n, p_rank in graph.nodes(data=True):
        if p_rank['pagerank'] < pagerank_threshold:
            small_graph.remove_node(n)

    # 这里用 circular_layout 代替默认的 spring_layout；让节点分布成一个圆环，增加阅读性
    show_graph(small_graph, 'circular_layout')
    pass


if __name__ == "__main__":
    main()

