def size_convert_utf8_to_base64(utf8_len):
    fill_byte_num = 0
    if utf8_len % 3 != 0:
        fill_byte_num = 1
    return (utf8_len // 3 + fill_byte_num) * 4


def size_convert_base64_to_utf8(base64_len):
    return (base64_len // 4) * 3


# 填充字符
filler = "$"
# 进行数据传输 数据包的尺寸(单位为字节 <base64编码>) 256的倍数
data_package_size = 1024

# 计算数据包长度
data_fixed_len = size_convert_base64_to_utf8(data_package_size)
# 记录填充符个数的字符串占用的长度
record_filler_len = len(str(data_fixed_len))
# 计算数据包传输是有效数据的最大字节数
valid_data_fixed_len = data_fixed_len - record_filler_len
