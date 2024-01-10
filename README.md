<div align="center">
<img src="assets/image/logo.JPG" width="300"></img>
</div>

第一代程序（tk框架）由[Q-M-D](https://github.com/Q-M-D)制作。

第二代程序考虑到行政老师电脑孱弱的性能，于是利用strealit框架将计算部分上云，同时重写了后端逻辑，由[Arnoliu](https://github.com/arnoliudaxia)制作。

# 有关资产价值求和与数据格式化问题的解决方案
## 0. 依赖安装
```pip install -r requirements.txt```
## 1. 资产价值求和程序

```
python v2/server.py
```

## 2. 打印标签

由于需要本地交互打印机，所以保留原tk程序

最终的程序是`python qrcodePrint/genQRcode_print.py`，运行方式为：

可用pyinstaller将其打包为exe文件，运行方式为：

```pyinstaller -F calc_sum.py```，打包后的exe文件在dist目录下。

**注意在win10及以上系统编译的程序无法再win7系统上运行，需要在win7系统上编译。**


# 关于python生成可执行文件

在当前目录下运行
```pyinstaller -F -W -i logo.JPG QRcustom.py```
其中`QRcustom.py`为需要打包的python文件，`logo.JPG`为打包后的exe文件的图标，`-F`表示打包为单个exe文件，`-i`表示指定exe文件的图标,'-w'表示不显示命令行窗口（默认不写）。

# 弃用程序

- `format.py` 数据格式化是为了处理数据中不能被政府系统识别的字符，以及一些过长的数据，使其能够被政府系统识别。使用方法见`master`分支


# contributors

| [<img src="https://github.com/arnoliudaxia.png" width="100px;"/><br /><sub>arnoliudaxia</sub>](https://github.com/arnoliudaxia) | [<img src="https://github.com/Q-M-D.png" width="100px;"/><br /><sub>Q-M-D</sub>](https://github.com/Q-M-D) |
|:-------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------:|
