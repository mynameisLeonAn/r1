import re

#數字加千分位
def formatNum(num):
    if num.find("0.") == -1:
        num=str(num)
        pattern=r'(\d+)(\d{3})((,\d{3})*)'
        while True:
                num,count=re.subn(pattern,r'\1,\2\3',num)
                if count==0:
                        break

    return num

    