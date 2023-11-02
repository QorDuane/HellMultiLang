import tkinter
from tkinter import filedialog
from tkinter import messagebox
import configparser
import os
import yaml

class optionPage():

    def __init__(self):

        self.console = tkinter.Toplevel()
        self.dir = "./다국어"
        self.config = self.onLoadConfig()
        self.naonDir = self.onLoadNaonDir(self.console)

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
        selectedDir = filedialog.askdirectory()
        if (selectedDir) :
            target.delete(0, 'end')
            target.insert(0, selectedDir)

    def onSaveConfig(self, gwDir, iamDir, console):
        config = configparser.ConfigParser()
        
        config.remove_section("ML_DIR")
        config.add_section("ML_DIR")
        
        config.set("ML_DIR", "GW_DIR", gwDir)
        config.set("ML_DIR", "IAM_DIR", iamDir)

        if not config.has_section("JS_PROPERTIES_DIR") :
            config.add_section("JS_PROPERTIES_DIR")
            config.set("JS_PROPERTIES_DIR", "GW_JS", gwDir + self.naonDir['GW']['JS'])
            config.set("JS_PROPERTIES_DIR", "GW_JS_PORTLET", gwDir + self.naonDir['GW']['JS_PORTLET'])
            config.set("JS_PROPERTIES_DIR", "IAM_JS", iamDir + self.naonDir['IAM']['JS'])
            config.set("JS_PROPERTIES_DIR", "GW_PROPERTIES", gwDir + self.naonDir['GW']['PROPERTIES'])
            config.set("JS_PROPERTIES_DIR", "IAM_PROPERTIES", iamDir + self.naonDir['IAM']['PROPERTIES'])
        
        if not config.has_section("TRGT_DIR") :
            config.add_section("TRGT_DIR")
            config.set("TRGT_DIR", "JS", gwDir + "/naon-module-web/target/naon-module-web/resources/biz/i18n/js")
            config.set("TRGT_DIR", "PROPERTIES", gwDir + "/naon-module-web/target/naon-module-web/resources/biz/i18n/properties")

        with open("./다국어/config.ini", "w") as fp:
            config.write(fp)
        
        if (messagebox.askokcancel("알림", "저장 완료되었습니다.")) :
            console.destroy()

    def onLoadConfig(self):
        config = configparser.ConfigParser()

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        
        config.read('./다국어/config.ini', encoding='utf-8')
        return config
    
    def onLoadNaonDir(self, console):
        path = 'naonDir.yml'

        try :
            with open(path, 'r') as file:
                dirData = yaml.safe_load(file)
                return dirData
            
        except FileNotFoundError :
            if (messagebox.showerror("알림", "naonDir이 없습니다.\n헬국어 프로젝트 위키페이지에서 yml을 다운로드 받아,\n실행파일과 같은 폴더에 넣어주세요.")) :
                console.destroy()