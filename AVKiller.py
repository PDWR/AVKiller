# -*- coding: UTF-8 -*-
import cv2
import pyautogui
from time import sleep
import base64
from os import popen

# --------------Imagebase64--------------
# logo base64
b64_AV_logo = {
    "hr": b'iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAMAAADzN3VRAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAACbVBMVEUAAADx8evl4tPbzLfk2c/q5eXu7ujl4NPe063nz4X21GX53YT6pU3wlT7epG/ZvKTk2dHq5eH/1Fb524H3ok77jCr/0lT4kCr/0FL/zU//yUv/xkj/xEb/wUP9vkH6ukPzkjLmum3hoWbt38vr2sv7+/fr0KLw0bT////f0sLmy6Djxqvh1Mjbyrbt4tXo3NLbyLzr5+Px7OLtvHTx8PDu7Ont7effrm3u3snt7e3n5+fr6+vs7Ozu7u7p6ent7e3013fwtFT0rWH01nbxzVr1y0n7zTz/zzf/zCn/ow//igr+ig/5ixnxkS7vm0T0rGH/z0L/yij/yB7/rST/p0b/liT/hAD/iAj7jR//yTL/xR3/xFT/27D/unD/jBH7jBr/xjD/whv/xy7/4Jj/+O//3bj/njf/wy7/vxr/wyj/23v/9t3///7/8+b/rVX/wCv/vBj/wCf/2Hf/9Nf//vz//////Pj/tGP/hAH/vSn/uRb/viX/1nb/89f/+/j/uGv/hwb/uif/thT/uh//1HL/8tb/9u3/1KX/oj3/iAf+tyX+sxL/ylj/7sv/6tP/5cn/0J3/mzH8syX+tB7/3pr//PX//fv/4L7/6M//tWb4jB70sTT+ujf/57r//vv/3Lb/sFv/yI3//v7/yIz/kBnuljz1w2r9vkz/6cD/5rn/rkv/rlb/4sL//Pn/z5v8mjPyu4T1x3b/6cL/5bn+vk7/s0n/2a7/+fP+0qTxtnr148f/+/b/7Mz+wFn+u0r/3qv/+PD++PLw1br38ej80o/+uEb/2Zz/+fD8+/r17+r3y4n/8t319fX08u709PTExC/rAAAAQHRSTlMAWZWVlTxZlZWVldXAlZWVlTxZ1cA8mGeYmJiYmJiYmGeYZ5hnP8OmKj/Dpio/w6YqP2rDpmoqP8OmKj9qamoqsrll6wAAAAFiS0dEKL2wtbIAAAAHdElNRQfkBQ0HBh1LmHlDAAABOElEQVQoz2NgoBFgZGJmYUUXZGPn4OTidnB04uHl4xcQREgICTu7uLq5e3h6efv4+vmLiMJlxAICg0AgOCQ0LCwsPEIcLiMRGQUG0TGxcUCpeISMZEIiCCQlp6SmocpIpWcAQWZWdk5uHqqMdH5BQUFhUXFJaVl5BYqMTGVVVXVNbUlpaV19A4qMbGNTc0srUKK0rb2jE1lGrqu7pxckUdLXP2Eisoz8pMlTpgIlpk2fMCN3ZvgsBbiM4uw5c4ES8+YvWJi7aPGSpUpwGeVly1cAJVauWr1mbem69RtU4DKqahs3lZZs3rJ12/bS0h071TUQQaqptWv3nr379h8oLT14SFsHORp09Q4fOXrseGnpiZP6BqgxZGhkfOp0aekZE1MzjCg1tzh75pylFbbYtraxtbOnLMEAAFuOdEy/lZaRAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIwLTA1LTEzVDA3OjA2OjI5KzAwOjAwO6igSAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMC0wNS0xM1QwNzowNjoyOSswMDowMEr1GPQAAAAASUVORK5CYII=',
    "360": b'iVBORw0KGgoAAAANSUhEUgAAAB0AAAAcCAYAAACdz7SqAAADSElEQVRIS+2WXWyTZRTHf+22rrVvuq4dpdjBaGWiTpyLMTFGY0Q0FggxJgbiTLxA/GDBG79mjJiAXpiZGCOJBpmJKGqQqTgHdF4gKJ0KEnAbsC3Qrexl3davde/efvcxJfFya7vFECPP7fM//99zTs7JczRcg6O5BkyuQ//Vqv93ytvevUtMTo3R+sQ783p00UEdPZ+IsDrMTMpPLDHClBohphjQZhZj0jlo2/Jx0V4FhW2dr4rplA8Io9flqDFVId2gJ5nNMBbOEIloiU3nUNQUGqHhi5e6CnrOKdhx4EVxMXqIquoQdYtsNN24gRWW9Zj1KxFAJpsjnopz+rIXT99+/vJ7MWYXs65xE9s2bJ/Ve9aLyUhI7D7+FnLiENYaBae1ngeWtmKX7qGyrPpqd6ezSYYjvXT2fY7n/Fdk03Gk9DLcDU/Rsv7N0qHBSEi0/7oDOXGYJfZyGu2rudu+lSq9C62mnGwuTViV8Vz4lJ8ufMtQcABjWSWmjItHb2vmhXVvlA4NT4XFnl92Mhr3sKJ2CQ86t+A0r0Ffbr6aZR4ajQf4beQHTo4cZ2C8n7AyipRejruhmefXvl46NG/8Xtcr4nLcQ73DwWrXs1gMy5B0tVSW5cFaMrkUQWWUU6PHODb4Hf1XvBiTdbhXPclz7tb5QT84sl1cUg5iNkdxLVqK1VDDLdanqZUeAsqIJgJ4fd/z81AXvVdOk0snsYpbWdu4kWceeW1+0C9P7BZnx/eR0/Wy3G7GId3MHbat2I33EVKH+cP/Dd5L3ZwLDDIRm0aXM1Av3c/ebd1zTkXBmXr38GYRUD04HQYabA9Tb3kMRAUDQQ89vk7Oj11EjiaIKVr02RrW3LSRt5s/XBi04+QecUbej9Ekc6/zcWxSHRMzffQHfmRw3I8/lGIsBCm1mjrjnXS8fLRgIgUF+Yba531fDE120uRahUEvE06cIxAL4JuYwjcpCAYNVGtvp6v196L8ihLlwV/37BLy9Am0FX2U68ZRkgmG5CQTIRPWirv4rOVI0V5FC/Pgg3/uFXKsh+DMWZREkBnVgkXXxM5NH5XkU5L4n5+9/WibiKoB9FobLe7ZR2O2TWBe0IWuFdehC63gnPH/n/L+Da0WUSzLjzJFAAAAAElFTkSuQmCC',
    "txgj": b'iVBORw0KGgoAAAANSUhEUgAAABoAAAAcCAYAAAB/E6/TAAACSklEQVRIS+2WPWhTURTHf/e+pE0sJsUOrQVR6KCbcVBoK/iFTqIWdKhQLXYRlHYoiINLVfwCRYIdFKzYQRcH8YMqxhZEcRTUWt2KFEVsa6QJbdPce+UmRGt5SV4ydMrd3nvnnt/9/8+5hydYpiWWiUMFVLbTJVkXG9OmrgZ8EqaSsH299Ly/aKAxxniRIYQomCvvx8WABQXjk4bPPwzf42BTNtbChgbB2jqRUZhb+YCuIAvRBoY+ah6+M7wc0yTm3XVV+6C5SdC+RbI/IrFmusHyguYWYOC1JjqsmE4WNm9lAI5vczixQ7KiqkTQ71kIBWBmHvpHFLdeaZJLVAX8cKxV0r3LYVUNxGehNlgi6NPEHFdjfm4cdghWwc8ZuPZCMfhWZ+RZq3r3SFaHBak0nHqgOLRZ0tokvFtnE2ltzMa+NPUhuNvl0BjOuvx12mDrt64u+zyZgM47aUa/Gb6c81Ptd+++gl13/kmK6LCgISQY7HKIrPk/3CbvuK2Y+GXobJFcOei4qrEHKtj78UTKNF/OntrWI9rucCCS7eWnHzQn76lM3cJBeHPaT30o/10qCLJt/nxUc2RAYa+tTdO7W+J3BJeeZd/ZdbPDoW2TzKumqCIbYGH9I5q+x8q1x7t3Ss7szW/Z34vsZbxY2PWY5uLQPxV2X9dWyYU2BykLjx9PinIHsbBH7zU991Wm687uczjakq1XsTlXEkgpbaQUjE+ZTAfZGae0wed4m+BFp/dSa3PD1ouKxXtLBnmpqVtMBVSuc5XfrbKd4w/6uNYdqXG3RQAAAABJRU5ErkJggg=='
}

b64_logout = b'iVBORw0KGgoAAAANSUhEUgAAACMAAAAVCAYAAADM+lfpAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAPCSURBVEhL7ZTZU1pnGIf7pzaZTKfTsZPEatMmhlgbqyUqJFNc6tagSEWJLImKiqAjokQtrlFAUAmLguBBWe6eHiObCrYXaZuLXjw3P77znme+8+P9LJ3J8KnwicqkTkmevGdrbRuXP8rRWYbk6Qmxgy1W/nBif7tyjTVvmMDJ5YFXEYIe9kMRAvHSvxdTkDk94tQ3iaK+lU69A7tfIBL04hppoOp7CXfu1fBlZYEvKr7hB5WNqd3CsGQizkniDCGZzdJp/NNdjFiXmPBcPhcTEsTP0vnsnIJMOkUqeUI0soyxS8VLpQXzthe3XkrH1A62nSNChxcEQ2E2XrcyaF4qyIjPB+ZUjNpWmfHlshIyYhawDaAen0O/Fr3IslzpzLnpMX63F487wN7Bxc08liqokbbRKM8ia6NOUsOzIXteJiXKnL/4lXWZyaIXl5LxW7rp0U8zuBK5yLLcWGAhLN6MrpGGziEUKiNqbQ4D3fKn/KJf+GdkEvEYvvUV3i6vsOwKsB8Vv/25jP5n5EOzaC1F5XUsY1I20zvmuCbTL8p2jxfOmvpaUPTrrmQyZL9PlpcJeV3opDVUVVZxv92E1hn9IJMr8K2vqrldIZIv8kN+7J9h4p2AkBJnZDvT2lx/rei3Kr7j9t3L2V3Fm/IyyWSS+FGI8PwAvaP2vEyuwIN9GnQjOgz5IruwDg+jfWVmNpydIf5LotFIvuih8CGbb9oYGJ1F5yzKRtvpEJ+7uTOpJOlVLaqJxbyMx/CMHluAhU0n8+MGlJ06ZrYW6evq5FeVAd28m3fBohnFlOqMiBDaxeMPsRc5u3T+b8us+raYNxtp+qkLTd8LJLJ+BqzrbAQTHMfFtZCOsj2/ys6+eLu5eWVk0pkQ2+tuNjbec5zP/kImLm7PDU0dMs0M2gkLBrOFXr0ZqygjV45hdHjZE4uezojbO7WPSaFh0rGFKzevrMwmphELOp0Tfz4rlhELmBKiHNrVdOutqBcDvPftMNdxn3vVD7lTq6JzYovghxcfYOlp4fnLUbRLQbHAH1smFiDhUFH7+BGfVzzgQasejX2XnZFGscDb2NwxjoUzkueLMZ1EiEVxmgyYTFNigT+yTDzgY00tF/fBHK8n9aiVXUhq5dQ++pava19c3sBZJJI6qpt+o2XaI8rsiTIymqTNPMmdyW7qyidSqhuKn22mul5FezkZ4TiCd3GG9WCcw6gf9+oCxvzGvQGTHdNa4KLA9mnGjCXOXENJ4/Nhest+pn+VPZZsTmw2D4dF+X8kU5r/ZUqT4U+2uDXyt6CRagAAAABJRU5ErkJggg=='
b64_blue_comfirm = b'iVBORw0KGgoAAAANSUhEUgAAACQAAAATCAYAAAD4f6+NAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAATnSURBVEhLzZX7U1VVFMfPX5AEYSPmo0mjZMZpanIClbJ0GmcCo5myxh8YJ8pGqWb6oaYJJ+2XRstmmhQUBC6PCyjGDe7FeBooj0AQCA3iaWKIKPI4557X3ud8W+eee+GikNNv/PC555y99lrru/dae1/hkWyOpYSwjH4eRngeR5TbQGwxxzp6X2jOQqwp4oj2GHj1DEdEzsJz7kdYlsVgEZrD8ISTIbJojqfyGQViWO/i+GoEKGvjSPLYtqcLGdaSLTSb/InH8xjWBfk+Q2J2Nxpwjpmoa2Z4vWTOFmAN+Ydb/n4NFkJIlg6LqEqOwwMmbnkxS303x/5ahtgWA1MckDVgQrZtfeMmimp1bMwnfwr+3mUD7TQ+GuR/VwW85KeS37jfz8bKYyKdYr9s+fs1WAghmRosVhTo2FTGsL+Jwy2ayGpi+OA8w0f1DD92Mrxb5aeFI6PfwF8DHK8VaojIJn8StLeV4/cx2slqhsTA3EVIusRwknbueLWOHfl2/gBCyGkVszg0bCxlcA4zvHVGx9sU/FgvR+0NA99e4Ta9Bn79x8TYbXvsSwoafY4o07GPdmxDporw4JgLsCJPQyztTtxZDVGO+bZ5glaSiLhLHO2DDJ/Wc/zUxeAZ5aiYMDE8auC3URMDkwYGJgxU3TTQNG2i908dB6o0bCrVafX/jzdLVDybe5+gR08r8JGlYCvtyIlbVHPVxAwDOnoYzv6hI3WEI6tcxbZyhrRO+m7V8LxLwztXDdR3ajjYpuMbKmOgN4K5Q33EOD3lB21XujXsKfHn9yOEZsjwUaIhmRKMThmoa1BwZMCAgxKd7dJRNA1IionbCiDqJkSNSkYJ7urAcK+GD90KVucq2OC8j2IN8VSa4Rs6dpU9aI/MkbEy05/fjxCW7kVYuoydDTqOjxhoHTZQWetFCvVKRqslSEMGlc1DIpMbGFx9OkquadhbpyFl0ERLl4oklxXDi4hcGS9eYPi8XMa2fBrLURBTrqN/SMWWInvOwxDCTokIOyUhxi3j4w6GjB5LkIQUemZQaSxB2dTALSQi9RpH403ibx0/UClzqKc6uxUSJPlirC+UkTxEfrSg+HyK65ARU0GC7jGkd+s40qbZXCYaZMTmSljlyz+HX5DNS9QnB3s4KmtEW1C7DjfV2XXHQPN1hmpqZLupOaqpr5qnqKmvkaAS8s+U8IJbhYeujDwS9EYujTm8iKnU0E+XUd1NhgqK4WNIR8VVBQlOCU8G5bcQHjs5gwDRHgVfU6nqLoo4Sk2aR03d0q+ipk/GK2RfVaDg+xbiooTVeRJ2tHNcoNsw6WcREWdkxNNNLlJvNdLY++dErKUd2OxRqWQythaIs3n+CxI0TS82lqCj9BcROGU3pg30XadVN4pYQfbweYLEIEFe7LqgomCcwUEN7hnnqO9XcKjGGyTISjiXazGE8LQpBIj2yL7j294h4bNqGd/RCXJ0Kfgin8RYcwpkHCNBv/SpONTHfCVraBVxuFFFCvWFg4RvyZzB9lLyp+/sQY6GMQMSlawxuGQBaDG7i2dm81sI4amTCBDpnMHO817sK5rE+vQpbC4VEVdKpQzMyZpBgkvEAeqRRDp1R1sVfOKaRoJb8rHbOYnlafbc54olJNbZcxalVsR2JwkJxCfmCVoKkKB79LJ0EJafmMDSYQL/AlS9+XJmGQ72AAAAAElFTkSuQmCC'
b64_white_comfirm = b'iVBORw0KGgoAAAANSUhEUgAAACQAAAAWCAYAAACosj4+AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAOaSURBVEhL7ZbXS2NREMb3j1QQVFSCvYMdG3bF3nsvWLA+CHYR8pAIir33gh3s/Vu+2ZyQuzEb2X3YXXBguPGeOXd+Z9rxG/4x+QKyJ/830PT0NMbHx7GxsWF6Y19eXl4wMDCAiYkJHB4emt7aFg3Q7e0t5ubmMDk5ibGxMVG9Xo/d3V3RoqIiREVFoayszLy+urqK6+trvL6+4urqSuzVGnVoaAgBAQGIiYlBQ0ODZo06OzuLi4sLE8FPQEdHR6iqqkJERARcXV3h7u6OhIQE9PX1ob29HcnJyQgODoa/vz88PDzg4uKC5uZm7O/v4/7+HvPz8+Lcy8tL7Owpv5+WliZQSjRA7+/vctLn52eJQltbG87PzyVNjA4dcu34+BgdHR3Izc3FwsKC7CPQ4uKiODAajWJnT1tbW8WPTSAKgZaXl9HS0iKp29rakjQFBQUhLCwM0dHR8mQU3NzcEBISgsLCQkxNTeHu7k6ixdR/Rs7OzuRwlvZWQE9PT0IeHx+PlJQUVFdXyymYpqysLFRUVCA9PR1+fn6Sxry8PGRmZqKpqQnDw8NSJ9zzWWWk2SxKNEAPDw9YX1+XAmQUQkNDERcXh9HRUflN5/X19cjJyUFgYCD6+/tRWlqK7OxsAWE3Eb6goMCs+fn5cjhfX1+Eh4dr1qj8HhtBiQaI4autrYWnp6c8GYHy8nIzENNEZUE7OTlJlHQ6naSRMEpubm5weXkpKXx7e5MIMK08gD3RAK2srMDHx0e6qbu72wqoq6sLBoNBnrGxsTJXmKbKykoN0ODgIGpqaqSu/ghIdUpJSQl6enqsgJgmtiuh2fIcD6wtwlkCMX3ct7a2ZgZKTEyUfSwHpTz4yMiIadcP+bCoOYsUEOHojCCsDxYvW5vpYvGz9VnUtGH77+3tISMjQwqf7ayA+I7KKCllJJkVS7EJVFxcLI44GNlZjMLMzAwODg4ElsV+enoqM4r2BOI1wa5JTU1FUlIS6urqJEos2t9KGUUBcb54e3vL/ImMjERjY6NcHwqIgDxdb2+vRI7OuMY0cobRnr/Zhaw5RofRpY2l8nbglaPEJlBnZ6c45HRmnXAzw88ngTgsCcUu47wiGKNJp9vb2zKJGR0extnZGQ4ODnB0dJTutFTWFf0psQJiHZCaU5Rzia3LDxOU8vj4KGuc4FRO9Z2dHbli+PfJyYnYULh/c3MTS0tLcsV8pDy05X8BVkB/W76Afi3Ad1Wn1n3XFcmHAAAAAElFTkSuQmCC'


# --------------参数定义--------------
base_temp_path = r'C:\Users\{}\Documents\\'.format(popen('echo %username%').read().strip())
av_process = {'hr': 'HipsTray.exe', 'txgj': 'QQPCTray.exe', '360': '360sd.exe'}  # 以字典的形式
logoutImage = base_temp_path + r'lougoutFromB64.png'
comfireImage = base_temp_path + r'comfireFromB64.png'
logoImage = base_temp_path + r'logoFromB64.png'
screen_before = base_temp_path + r'before.png'
screen_logout = base_temp_path + r'logout.png'
screen_comfire = base_temp_path + r'comfire.png'


# --------------检测目标计算机存在的杀毒软件--------------
def runningAVs():
    tasklist = popen('tasklist').read().split()
    for av_exe in av_process.values():
        if av_exe in tasklist:
            usingAV = [k for k, v in av_process.items() if v == av_exe][0]
            return usingAV


# --------------通过tasklist判断存在的av，获取的相应的logo--------------
def get_logo():
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
    if AV == r'hr':
        return b64_logout
    elif AV == r'360':
        return b64_blue_comfirm
    else:
        return b64_white_comfirm


# --------------定义鼠标键盘事件--------------
def press_keys(*args):
    pyautogui.hotkey(args[0], args[1])
    sleep(0.2)
    pyautogui.press(args[2])


# 截图操作
def get_screen(screenName):
    pyautogui.screenshot(screenName)


# 获取坐标操作，比对原来的截屏和待识别图标
def get_position(imgSource, imgTarget):
    source = cv2.imread(imgSource, 0)  # 0-灰度处理，防止颜色不同对定位产生影响
    target = cv2.imread(imgTarget, 0)
    wight, height = target.shape[::-1]  # 获取图片长和宽，方便确定文字的中新坐标
    res = cv2.matchTemplate(source, target, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    pos_x = int(max_loc[0] + wight / 2)
    pos_y = int(max_loc[1] + height / 2)
    print(pos_x, pos_y)
    return pos_x, pos_y


def killav():
    logout_last = get_logo()
    # 通过杀毒软件生成不同的最后一步图片
    with open(comfireImage, 'wb') as f:
        f.write(base64.b64decode(logout_last))

    sleep(1)
    press_keys('win', 'b', 'enter')
    get_screen(screen_before)
    sleep(1)
    # 右键点击logo，弹出'退出'窗口
    pyautogui.rightClick(get_position(screen_before, logoImage))

    get_screen(screen_logout)
    sleep(1)
    # 点击'退出'，出现'确认'窗口
    pyautogui.click(get_position(screen_logout, logoutImage))

    sleep(0.5)
    get_screen(screen_comfire)
    sleep(1)
    # 点击'确认'，实现对杀毒软件的完全退出
    pyautogui.click(get_position(screen_comfire, comfireImage))


 #--------------清理图片痕迹--------------
def clean():
    popen(r'del /q {} {} {} {} {} {}'.format(logoutImage, logoImage, comfireImage, screen_before, screen_logout, screen_comfire))


def main():
    killav()
    clean()


if __name__ == '__main__':
    main()


