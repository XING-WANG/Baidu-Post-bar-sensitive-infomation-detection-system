# Baidu-Post-bar-sensitive-infomation-detetion-system
项目功能：检测百度贴吧指定贴吧的敏感信息，锁定该信息所在帖子及位置并进行举报
采用多模式匹配算法匹配任意长度的敏感信息，锁定敏感信息所在位置
使用selenium+chrome代替scrapy爬虫框架来抵抗百度贴吧的反爬虫机制
通过selenium的鼠标动作链机制来对抗进行举报时的安全验

tips：
1.请选择和自己chrome浏览器版本适配的chromedriver
2.在db文档的所有python文件中更改数据库的username和password为自己的数据库用户名密码
3.运行UI.py启动，UI界面的网址为要爬取的贴吧URL，敏感词以;;分隔，如你;;我;;他
