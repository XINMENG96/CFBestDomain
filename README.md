# CFBestDomain
CFBestDomain 是一个自动优化 Cloudflare CDN IP 的工具，旨在提高网站访问速度和稳定性。该工具通过实时获取最佳的 Cloudflare CDN IP，并使用 DNS 解析技术生成优化后的域名，帮助用户实现更快的加载速度和更低的延迟。  主要功能： 自动优化 Cloudflare CDN IP：根据网络状况自动选择最快的 Cloudflare CDN IP。 DNS 解析：利用优选 IP 自动进行 DNS 解析，生成快速响应的域名。 易于配置：通过简单的配置文件即可设置定时任务，自动更新 CDN IP。 跨平台支持：支持 Windows、Linux 和 macOS 操作系统。

该项目使用 [CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest) 项目来进行IP测速。
