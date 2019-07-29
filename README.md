# personal_relationship_in_email
李文轩 2019-07-29

##### 项目：用 PageRank 算法分析邮件里存在的人际关系

这个项目并不考虑邮件本文，只在寄件人 (MetadataFrom) 和收件人 (MetadataTo)的数据中分析人际关系。

这个项目用的是希拉里的邮件作为例子。

数据集：https://github.com/vincentlee9512/personal_relationship_in_email/tree/master/input

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
