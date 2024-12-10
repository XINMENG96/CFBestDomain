import os

# 获取主程序所在目录
def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

# 生成默认的 app.env 文件模板
def create_default_env(env_file):
    default_env_content = """
# 定时运行（单位：分钟）
# INTERVAL_MINUTES=2880
# Cron定时运行（仅支持Linux，优先执行）
# CRON_EXPR=* * */2 * *

# Cloudflare API 配置
# Cloudflare API 邮箱
# email=your-email@example.com
# Cloudflare API 密钥
# api_key=your-cloudflare-api-key
# Cloudflare 区域 ID
# zone_id=your-cloudflare-zone-id
# DNS 记录名称
# record_name=xxx.xxx.com
# 下载速度阈值，只有下载速度大于等于此值的 IP 会被更新到 DNS
# cst_download_speed_threshold=10

# Github代理地址
# GITHUB_PROXY=https://github.proxy.com

# CloudflareSpeedTest 配置
# 延迟测速线程
# cst_n=200           
# 延迟测速次数
# cst_t=4             
# 下载测速数量
# cst_dn=10           
# 下载测速时间
# cst_dt=10           
# 测速端口
# cst_tp=443          
# 测速地址
# cst_url=https://cf.xiu2.xyz/url  
# 是否使用 HTTPing 模式
# cst_httping=True    
# HTTPing 有效状态码
# cst_httping_code=200  
# 匹配指定地区
# cst_cfcolo=         
# 平均延迟上限
# cst_tl=200          
# 平均延迟下限
# cst_tll=40          
# 丢包几率上限
# cst_tlr=0.2         
# 下载速度下限
# cst_sl=5            
# 显示结果数量
# cst_p=10            
# IP段数据文件
# cst_f=ip.txt        
# 写入结果文件
# cst_o=result.csv    
"""
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(default_env_content.strip())
    
    print(f"默认模板已生成: {env_file}")

# 主函数
def main():
    # 直接指定 config 目录为根目录中的 config 文件夹
    config_dir = os.path.join(get_script_dir(), '..', 'config')  # 获取根目录中的 config 文件夹
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)  # 如果 config 文件夹不存在，创建它

    env_file = os.path.join(config_dir, 'app.env')  # app.env 文件路径
    
    # 如果 app.env 文件不存在，生成默认模板
    if not os.path.exists(env_file):
        print("app.env 文件未找到，生成默认模板...")
        create_default_env(env_file)
    else:
        print(f"app.env 文件已存在: {env_file}")

if __name__ == "__main__":
    main()
