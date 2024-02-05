# Carrying Tools

become contributers by carrying something...
本人的Bilibili主页：
https://space.bilibili.com/391744592/

![搬运工图片](https://afuwz.com/wp-content/uploads/2021/04/%E6%90%AC%E8%BF%90%E5%B7%A5.jpg)


## Normal Workflow

1. 使用脚本  从红色电视机软件上往下搬
2. 用腾讯jianying，导入视频，识别字幕
3. 导出字幕，并在jianying中删除原字幕
4. 使用脚本  翻译
5. 再次导入字幕

## Install Depdencies

1. [腾讯jianying](https://www.capcut.cn/)(点击下载)
2. python3(我用的python3.11 您看着办)
3. Please install python depdencies using:
   
```
pip install -r requirements.txt
```

4.小小的链接工作
```
sudo ln -s `which yt-dlp` /usr/local/bin/youtube-dl
```

## Usage of Scripts of Steps in Workflow

### step1 script usage:

跑之前先把红色电视机视频的地址写在文件里，可以命名成<input文件路径>，一个一行,参见`exampleinput.txt``

然后
```
python3 download.py --input <input文件路径>
```

#####例如：
```
python3 download.py --input exampleinput.txt
```
并行下载 挺快的。

### step4 script usage:

直接用
```
python3 download.py --input <导出的srt文件路径> --output <存储的新srt路径>
```

#####例如：
```
python3 translate_srt.py --input exampleinput.srt --output out.srt
```

## 想要添砖加瓦请联系我，或者您直接fork也行
> liuyoudehama@gmail.com