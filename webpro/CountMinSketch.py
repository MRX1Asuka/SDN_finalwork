import numpy as np
from scapy.all import *
from collections import Counter

class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        self.count_matrix = np.zeros((depth, width), dtype=int)  # 初始化计数矩阵
        self.hash_params = self.generate_hash_params()  

    # 生成哈希函数参数
    def generate_hash_params(self):
        hash_params = []
        # 对于每个哈希函数，生成两个随机数作为参数
        for _ in range(self.depth):
            a = np.random.randint(1, self.width)  # 随机选择一个a
            b = np.random.randint(1, self.width)  # 随机选择一个b
            hash_params.append((a, b))
        return hash_params

    # 获取哈希值
    def get_hash_values(self, item):
        hash_values = []
        # 对于每个哈希函数，计算哈希值
        for a, b in self.hash_params:
            hash_value = (a * hash(item) + b) % self.width  # 使用哈希函数计算哈希值
            hash_values.append(hash_value)
        return hash_values

    # 添加元素
    def add(self, item):
        hash_values = self.get_hash_values(item)
        # 对于每个哈希函数，将元素添加到相应的桶中
        for i in range(self.depth):
            bucket_index = hash_values[i]  # 计算桶的索引
            self.count_matrix[i][bucket_index] += 1  # 在对应的桶中增加计数

    # 估算元素的频率
    def estimate_frequency(self, item):
        hash_values = self.get_hash_values(item)
        min_count = np.inf
        # 对于每个哈希函数，查找最小的计数值
        for i in range(self.depth):
            bucket_index = hash_values[i]  # 计算桶的索引
            count = self.count_matrix[i][bucket_index]  # 获取桶中的计数值
            min_count = min(min_count, count)  # 更新最小计数值
        return min_count

# 创建Count-Min Sketch对象
num_packets = 100000  # 数据包数量
error_tolerance = 0.0001  # 误差容忍度

width = int(np.ceil(np.exp(1) / error_tolerance))  # 计算桶的数量
depth = int(np.ceil(np.log(1 / error_tolerance)))
cms = CountMinSketch(width, depth)  # 创建 Count-Min Sketch 对象

# 定义回调函数处理每个数据包
def process_packet(packet):
    if IP in packet:
        ip = packet[IP].src
        cms.add(ip)  # 将源IP地址添加到 Count-Min Sketch 中

# 使用sniff函数读取pcap文件并处理每个数据包
sniff(offline="test_trace.pcap", prn=process_packet, store=0)

# 获取所有不重复的源IP地址
unique_ips = set()
for packet in PcapReader("test_trace.pcap"):
    if IP in packet:
        unique_ips.add(packet[IP].src)

# 估算每个源IP地址的频率
frequency_estimates = {}
exact_frequencies = Counter([packet[IP].src for packet in PcapReader("test_trace.pcap") if IP in packet])
for ip in unique_ips:
    estimate_frequency = cms.estimate_frequency(ip)  # 从 Count-Min Sketch 中估算源IP地址的频率
    exact_frequency = exact_frequencies[ip]  # 实际的源IP地址频率
    frequency_estimates[ip] = estimate_frequency

# 打印每个源IP地址的频率估算结果
for ip, estimate_frequency in frequency_estimates.items():
    exact_frequency = exact_frequencies[ip]
    difference =  estimate_frequency - exact_frequency
    print("源IP地址: {}, 估算频率: {}, 精确频率: {}, 频率差: {}".format(ip, estimate_frequency, exact_frequency, difference))


