import tkinter
from tkinter import filedialog
import configparser

class optionPage():

    def __init__(self):

        self.console = tkinter.Toplevel()
        self.config = self.onLoadConfig()

        # UI 설정
        self.initUI(self.console)
        # 기능 설정
        self.initContents(self.console)

        self.console.mainloop()
    
    def initUI(self, console):

        console.title("환경설정")
        console.geometry("400x160+0+30")
        console.resizable(False, False)

    def initContents(self, console):
        
        label = tkinter.Label(console, text="[그룹웨어 경로]")
        label.place(x= 20, y= 10)

        gwDir=tkinter.Entry(console, width= 40)
        gwDir.place(x= 20, y= 35)

        button = tkinter.Button(console, text="찾기", overrelief="solid", width=10, command=lambda: self.askDir(gwDir))
        button.place(x= 310, y= 33)

        label = tkinter.Label(console, text="[IAM 경로]")
        label.place(x= 20, y= 63)
        
        iamDir=tkinter.Entry(console, width= 40)
        iamDir.place(x= 20, y= 88)

        button = tkinter.Button(console, text="찾기", overrelief="solid", width=10, command=lambda: self.askDir(iamDir))
        button.place(x= 310, y= 86)

        button = tkinter.Button(console, text="저장", overrelief="solid", width=10, command=lambda: self.onSaveConfig(gwDir.get(), iamDir.get(), console))
        button.pack(side="bottom", pady=10)

        if (len(self.config.sections()) != 0) :
            gwDir.insert(0, self.config["ML_DIR"]["GW_DIR"] if self.config.has_option("ML_DIR", "GW_DIR") else "")
            iamDir.insert(0, self.config["ML_DIR"]["IAM_DIR"] if self.config.has_option("ML_DIR", "IAM_DIR") else "")

    def askDir(self, target):
        target.insert(0, filedialog.askdirectory())

    def onSaveConfig(self, gwDir, iamDir, console):
        config = configparser.ConfigParser()
        
        config.remove_section("ML_DIR")
        config.add_section("ML_DIR")
        
        config.set("ML_DIR", "GW_DIR", gwDir)
        config.set("ML_DIR", "IAM_DIR", iamDir)

        with open("../config.ini", "w") as fp:
            config.write(fp)
        
        if (tkinter.messagebox.askokcancel("알림", "저장 완료되었습니다.")) :
            console.destroy()

    def onLoadConfig(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        return config