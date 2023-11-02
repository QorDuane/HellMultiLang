import tkinter
from tkinter import messagebox
import configparser
import os, shutil, re

class mainPage():

    def __init__(self):

        console = tkinter.Tk()
        self.dir = "./다국어"

        # UI 설정
        self.initUI(console)
        # 기능 설정
        self.addFeature(console)

        console.mainloop()
    
    def initUI(self, console):

        console.title("헬국어 - 나온 다국어 도우미")
        console.geometry("640x400+300+300")
        console.resizable(False, False)
        self.initMenu(console)

    def close(self, console):
        console.quit()
        console.destroy()

    def initMenu(self, console):
        
        menubar = tkinter.Menu(console);
    
        option=tkinter.Menu(menubar, tearoff=0)
        option.add_command(label="환경설정", command=self.getOptionPage)
        menubar.add_cascade(label="옵션", menu=option)
    
        console.config(menu=menubar)

    def addFeature(self, console):
        mergeResources = tkinter.Button(console, text="다국어 리소스 병합", overrelief="solid", width=15, command=self.mergeResources, repeatdelay=1000, repeatinterval=100)
        mergeResources.pack()
        
    def mergeResources(self):
        
        if not self.checkIniExists() :
            if (messagebox.askokcancel("알림", "저장된 경로가 올바르지 않습니다.\n환경설정을 진행합니다.")) :
                from pages import optionPage
                optionPage.optionPage()
                return
            
        gwDir = self.config["ML_DIR"]["GW_DIR"]
        iamDir = self.config["ML_DIR"]["IAM_DIR"]

        backUpDir = "./다국어/backUp"

        if os.path.exists(backUpDir):
            shutil.rmtree(backUpDir)

        os.makedirs(backUpDir + "/gw/js")
        os.makedirs(backUpDir + "/gw/properties")
        os.makedirs(backUpDir + "/iam/js")
        os.makedirs(backUpDir + "/iam/properties")
        os.makedirs(backUpDir + "/merged/js")
        os.makedirs(backUpDir + "/merged/properties")

        dirList = self.config.options("JS_PROPERTIES_DIR")

        for directory in dirList :
            for root, dirs, files in os.walk(self.config["JS_PROPERTIES_DIR"][directory]) :
                for file in files :
                    if file.endswith("." + directory.split('_')[1]) :
                        shutil.copy(os.path.join(root, file), os.path.join(backUpDir + "/" + directory.split('_')[0] + "/" + directory.split('_')[1], file))
                
                    if "gw" in directory :
                        if file.endswith("." + directory.split('_')[1]) :
                            shutil.copy(os.path.join(root, file), os.path.join(backUpDir + "/merged/" + directory.split('_')[1], file))

        mergeTrgtFld = [backUpDir + "/iam/js", backUpDir + "/iam/properties"]
        diffDict = {'js':{},'properties':{}}

        for folder in mergeTrgtFld :
            for root, dirs, files in os.walk(folder) :
                for file in files :
                    resDict = {}
                    
                    print(file + " 작업중...")
                    # iam 파일 읽기
                    with open(folder + "/" + file, "r", encoding="utf-8") as iamFile :
                        context = iamFile.readlines()
                        extn = file.split(".")[1]
                        for line in context:
                            if not '=' in line :
                                continue
                            if extn == "js" :
                                if not ' ' in line :
                                    continue
                                resDict[line.split("=")[0].split(" ")[1]] = re.sub(r'\n$', '', line.split("=")[1])
                            elif extn == "properties" :
                                resDict[line.split("=")[0]] = re.sub(r'\n$', '', line.split("=")[1])

                    # gw 파일 읽어서 dict에서 이미 존재하는 key 제거
                    with open(folder.replace("/iam/", "/gw/") + "/" + file, "r", encoding="utf-8") as gwFile :
                        context = gwFile.readlines()
                        extn = file.split(".")[1]
                        for line in context:
                            if not '=' in line :
                                continue
                            if extn == "js" :
                                if not ' ' in line :
                                    continue
                                if line.split("=")[0].split(" ")[1] in resDict :
                                    del resDict[line.split("=")[0].split(" ")[1]]
                            elif extn == "properties" :
                                if line.split("=")[0] in resDict :
                                    del resDict[line.split("=")[0]]

                    # 끝부분 개행 제거
                    context = [line for line in context if line.strip() != '']

                    # target 폴더 백업물 생성
                    with open(folder.replace("/iam/", "/merged/") + "/" + file, "w", encoding="utf-8") as mergedFile :
                        mergedFile.writelines(context)

                    # 남은 리소스 붙여넣기
                    with open(folder.replace("/iam/", "/merged/") + "/" + file, "a", encoding="utf-8") as mergedFile :
                        if extn == "js" :
                            for key, value in resDict.items() :
                                mergedFile.write("var " + key + "=" + value + "\n")
                                
                        elif extn == "properties" :
                            for key, value in resDict.items() :
                                mergedFile.write(key + "=" + value + "\n")

                    print(file + " 작업완료!")

        self.copyResourcesToTrgtFld(backUpDir)

    def getOptionPage(self):
        from pages import optionPage
        optionPage.optionPage()
    
    def checkIniExists(self):
        self.config = configparser.ConfigParser()
        
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        self.config.read('./다국어/config.ini', encoding='utf-8')

        if self.config.has_option("ML_DIR", "GW_DIR") and self.config.has_option("ML_DIR", "IAM_DIR") :
            return os.path.exists(self.config["ML_DIR"]["GW_DIR"]) and os.path.exists(self.config["ML_DIR"]["IAM_DIR"])
        else :
            return False
    
    def copyResourcesToTrgtFld(self, backUpDir):
        
        resDir = [
            backUpDir + "/merged/js",
            backUpDir + "/merged/properties"
        ]

        trgtDir = [
            self.config["TRGT_DIR"]["js"],
            self.config["TRGT_DIR"]["properties"]
        ]

        for directory in trgtDir :
            if os.path.exists(directory):
                shutil.rmtree(directory)
            # os.makedirs(directory)
        
        for index in range(len(resDir)) :
            shutil.copytree(resDir[index], trgtDir[index])

        messagebox.showinfo("알림", "완료")
