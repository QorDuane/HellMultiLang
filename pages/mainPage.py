import tkinter
import configparser

class mainPage():

    def __init__(self):

        console = tkinter.Tk()
        self.newWindow = None

        # UI 설정
        self.initUI(console)
        # 기능 설정
        self.initFeature(console)

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

    def initFeature(self, console):
        print('a')
        
    def getOptionPage(self):
        from pages import optionPage
        optionPage.optionPage()
    
    def checkIniExists(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        return config.has_section("ML_DIR")