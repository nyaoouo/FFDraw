# FFDraw: 一个针对FFxiv的悬浮窗图形显示框架

> 安装路径请不要有中文日文，必须纯英文

### 小白懒人包版本

- [下载](https://github.com/gogofishman/FFDraw/releases)
- 适用人群：python环境我不会装啊，exe怎么报错啊，py文件怎么启动啊，怎么更新啊我去
- 双击`run.bat`，会自动在当前文件夹安装FFD，同时搭建python环境，并启动FFD
- 什么？你不会填网络代理端口？兄弟还是当绿玩吧，与科技无缘



### python 版本

* 需求 `python3.10` 或以上的`x64版本`作为运行环境
* 下载专案后在专案目录运行 `python -m pip install -r requirements.txt` 安装依赖
* 如果遇到安装依赖问题请自行搜索 `pip换源` 相关
* 执行 `main.py`

### exe 版本

* 去 [release](https://github.com/nyaoouo/FFDraw/releases/latest) 下载带exe的发布
* 双击 `FFDraw.exe` 运行
* 注：exe版本未必属于最新版本，也未必适应你的运行环境，请尽量使用python版本或从其他人获取最新版本的build (安装 `pyinstaller` 并运行 `pack.py`)
* 注2：cn版本与正常版本差异为默认值适配国内网络、国服默认路径编码，无需手动设置，两个版本均能适用与国服与国际服
* 注3：如果报毒，可以使用`python版本`或者`关掉防毒`或者`添加c盘信任`或者`不用`

### 注

* 如果在非独显直连的机器上遇到图层黑色无法穿透之类，请尝试游戏以及本程序均使用核显并重启程序
* 如果遇到报错 `failed to set hardware filter to promiscuous mode` 之类，请修改 `config.json` 中的 `sniffer/sniff_promisc` 为 `false` 并重启程序
* 如果遇到报错 `Npcap/Winpcap is not installed` 之类，请下载 [npcap](https://npcap.com/dist/npcap-1.72.exe) 安装后重启
* 如果遇到编码问题 `utf8 cant decode` 之类，请修改 `config.json` 中的 `path_encoding` 为 `gbk` 并重启程序
* 关于跨域：设置 `web_server/enable_cors`，另外如果你不打算给链接设置ssl， chrome 请在 [chrome://flags/](chrome://flags/) 中设置 `Block insecure private network requests`
  为 `disable` [(ref)](https://developer.chrome.com/articles/cors-rfc1918-feedback/#chrome%27s-plans-to-enable-cors-rfc1918)



## 插件库

[插件库](doc/插件库.md)

- ffd可以自由添加插件功能，同时也有许多作者制作了功能多样的自定义插件。
- 通常在插件没有特殊说明的情况下，可以在`"自定义插件路径"`中添加第三方插件的本地路径（更推荐），或者将插件文件夹放进 `plugins` 文件夹中
- 插件作者提交自己的插件请在插件库的md文件中提交仓库链接



## 第三方插件绘制

[端口绘制参数](doc/Development/第三方科技绘制.md)

- 对于想采用第三方科技通过端口使用ffd绘制的朋友可以点击这里查看文档
- 适用场景：使用ACT的trn或cactbot来绘制ffd图形



## 插件开发

* 编写python模块置于plugins文件夹中，会自动导入
* `update(main:FFDraw)->any` 每帧调用，一般用于直接调用gui进行绘制
* `process_command(command:dict)->bool` httpapi在找不到指令cmd时调用，返回true为已处理

