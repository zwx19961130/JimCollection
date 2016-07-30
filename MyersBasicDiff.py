def diff_len(a: str, b: str):
    # 一对字符串之间的差异, 表现在图中, 就是竖线与横线
    # 考虑最差的情况, 即A与B完全不相等, 将会有a+b最大总长度的竖线与横线
    # 可以将这个值理解为弹药数量, 每一个差异都是要消灭的敌人
    # 通过逐步提升弹药供给来找到战果最好的消灭方案(斜线最多)
    # 10颗子弹消灭的敌人必然可以由用9颗子弹消灭敌人的最佳方案+第10颗子弹的最佳方案解决
    # 到目前为止与普通的DP方法没有显著差别, 仅是从一个更几何的角度去看待问题
    max_supply = len(a) + len(b)

    # 默认把A当作置于上方的x轴, B当作置于下方的y轴
    # k线的下标由x-y决定
    # 从左上角(0, 0)开始画对角线, 原点不可能和任何点画对角线, 所以k_1和k_-1线必然分别用横线与竖线连接至原点
    # 初始时, k_0线必然会得到k_1线的x, 不多用if, 将k_1线的x设为0
    max_x_nth_k_line = {1: 0}

    # 0有意义, 所以从1开始计数, range参数+1
    for supply in range(max_supply + 1):
        # Myers的论文证明了弹药数量的奇偶性与最终所停留的k线的是一致的
        # 所以迭代的步进为2
        for nth_k in range(-supply, supply + 1, 2):

            # 第一个判断的作用: 当处于k_-d线时, 唯一能消耗弹药的方式就是横移到k_-d+1线的x处
            # 两个角度:
            # -d已经是底部了, 不能从更低的k线增量计算
            # 弹药增量是从下往上, 同样的弹药供给, 那么k_-d+1线必然会多消耗一个横移弹药
            # 第二组判断的作用: 一般情况
            # 正确性: k_n+1或k_n-1线最优解可以漂移出增加1个弹药的k_n线最优解
            if nth_k == -supply or (nth_k != supply and max_x_nth_k_line[nth_k - 1] < max_x_nth_k_line[nth_k + 1]):
                # 从k_n+1漂移到k_n, x的位置不变, y往下一个单位
                x = max_x_nth_k_line[nth_k + 1]
            else:
                # 从k_n-1漂移到k_n, y的位置不变, x向前一个单位
                x = max_x_nth_k_line[nth_k - 1] + 1
            # 从k和x可以直接得出y的位置
            y = x - nth_k

            # 本轮弹药补给使用完毕, 开始尝试能否走对角线, 获取战果
            # String下标是从0开始的, 所以实际上a[x] == b[y]等同于自然下标a[x+1] == b[y+1]
            while x < len(a) and y < len(b) and a[x] == b[y]:
                x += 1
                y += 1
            # 最优写回
            max_x_nth_k_line[nth_k] = x

            # 所有子弹已经打完, 无法获取更多战果
            if x >= len(a) and y >= len(b):
                return print('diff_len is', supply)


# 从相反方向出发的函数
# 将输入reverse一遍即可, k线下标不变
# 结果应当相同
def diff_len_reverse(a: str, b: str):
    a = a[::-1]
    b = b[::-1]

    max_supply = len(a) + len(b)
    max_x_nth_k_line = {1: 0}
    for supply in range(max_supply + 1):
        for nth_k in range(-supply, supply + 1, 2):

            if nth_k == -supply or (nth_k != supply and max_x_nth_k_line[nth_k - 1] < max_x_nth_k_line[nth_k + 1]):
                x = max_x_nth_k_line[nth_k + 1]
            else:
                x = max_x_nth_k_line[nth_k - 1] + 1
            y = x - nth_k

            while x < len(a) and y < len(b) and a[x] == b[y]:
                x += 1
                y += 1
            max_x_nth_k_line[nth_k] = x

            if x >= len(a) and y >= len(b):
                return print('diff_len_reverse is', supply)


if __name__ == '__main__':
    A = 'ABCABBA'
    B = 'CBABAC'
    diff_len(A, B)
    diff_len_reverse(A, B)
