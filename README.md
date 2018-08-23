# cet46query
暴力查询四六级成绩:可以设定座位区间和初始考场号，自动识别验证码，查询准考证号是否正确。

使用步骤：
1.需要安装requests,pillow和tesseract
在命令行中运行：
pip install requests
pip install pillow
pip install pytesseract
tesseract软件请从以下网页下载：
https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#400-alpha-for-windows
具体过程可参考百度教程（该软件无需安装中文语言包）：
https://jingyan.baidu.com/article/219f4bf788addfde442d38fe.html

2.修改文件中如下部分：
lower=1
upper=30
#这一部分修改成个人信息即可
roomId=33
seatId=5
username='XXX'
areaId='1100911812'
其中lower是座位下限，upper是座位上限，roomId是初始考场号，seatId是初始座位号，username是姓名，areaId是前十位考区号。

3.运行python程序即可开始试各种准考证号，逐次加一，试成功保存至record.txt文件中。
