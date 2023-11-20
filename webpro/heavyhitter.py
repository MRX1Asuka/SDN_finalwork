import pyshark
from collections import Counter



# 创建Count-Min Sketch数据结构
class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width  # Count-Min Sketch的宽度
        self.depth = depth  # Count-Min Sketch的深度
        self.sketch = [[0] * width for _ in range(depth)]  # 初始化Count-Min Sketch矩阵

    def update(self, item):
        # 更新Count-Min Sketch
        for i in range(self.depth):
            hash_value = hash((i, item)) % self.width  # 使用哈希函数生成哈希值
            self.sketch[i][hash_value] += 1  # 对应位置计数加1

    def query(self, item):
        # 查询项的最小计数
        min_count = float('inf')
        for i in range(self.depth):
            hash_value = hash((i, item)) % self.width  # 使用哈希函数生成哈希值
            min_count = min(min_count, self.sketch[i][hash_value])  # 更新最小计数
        return min_count

# 打开捕获文件(这里我把数据集保存到了桌面，复制它的链接即可)
cap = pyshark.FileCapture('/home/xyl/102101422/final_work/webpro/trace2.pcap')

# 创建Count-Min Sketch实例
cms = CountMinSketch(width=1000, depth=5)

# 遍历每个数据包
for pkt in cap:
    # 检查数据包是否具有IP层
    if 'IP' in pkt:
        # 获取源IP地址
        src_ip = pkt['IP'].src
        # 更新Count-Min Sketch
        cms.update(src_ip)
        #print("check OK")

# 关闭捕获文件
cap.close()

# 检测重要元素
top_k = 10  # 获取前10个重要元素
count_threshold = 1000  # 设置计数阈值!

counter = Counter()
for pkt in cap:
    if 'IP' in pkt:
        src_ip = pkt['IP'].src
        # 查询Count-Min Sketch的计数
        count = cms.query(src_ip)
        if count >= count_threshold:
            counter[src_ip] = count

# 打印最高频率流
print("最高频率流 (Top 10):")
for ip, count in counter.most_common(top_k):
    print(f"IP地址: {ip}, 计数: {count}")
