#!usr/bin/env python
import urllib.request
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import json
import webbrowser


# Main window of the program
class MainWindow():
    def __init__(self,master):
        self.master=master
        self.loggedin = False

        self.mBar = tk.Menu(master,tearoff=0)
        
        self.fileMenu = tk.Menu(self.mBar,tearoff=0)
        self.fileMenu.add_command(label="Login",command=self.login)
        self.fileMenu.add_command(label="Close",command=quit)

        self.mBar.add_cascade(label="File",menu=self.fileMenu)

        self.runMenu = tk.Menu(self.mBar,tearoff=0)
        self.runMenu.add_command(label="Run",command=self.FindWorlds)
        self.mBar.add_cascade(label="Run",menu=self.runMenu)

        self.mainWindow=tk.Frame(master)
        self.mainWindow.pack(fill=tk.BOTH,expand=1)
        self.mainWindow.grid_columnconfigure(0, weight=2)
        self.mainWindow.grid_columnconfigure(1, weight=1)
        self.mainWindow.grid_rowconfigure(0, weight=1)
        self.mainWindow.grid_propagate(0)
        self.dataWindow = tk.Frame(self.mainWindow,borderwidth=2,relief=tk.RAISED)
        self.dataWindow.grid(row=0,column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        self.dataWindow.grid_propagate(0)
        
        self.newWindow = tk.Frame(self.mainWindow,borderwidth=2,relief=tk.SUNKEN)
        self.newWindow.grid(row=0,column=1,sticky=tk.W+tk.E+tk.N+tk.S)
        self.newWindow.grid_propagate(0)
        
        self.mainText=tk.StringVar()
        self.newWorldText=tk.StringVar()
        self.newWorldText.set("")
        self.mainText.set("Welcome to the Deepworld API v0.1!\nPlease log in using the file menu and your API key.\nYou must log in before doing anything else.")
        self.label=tk.Label(self.dataWindow,textvariable=self.mainText,justify=tk.LEFT)
        self.label.grid(row=0,column=0,rowspan=2,sticky=tk.E+tk.W)
        self.label2=tk.Label(self.newWindow,textvariable=self.newWorldText,justify=tk.LEFT)
        self.label2.grid(row=0,column=0,rowspan=2,sticky=tk.E+tk.W)
        self.worldWindowText = tk.StringVar()
        self.worldWindowText.set("")
        
        self.APILib={'My Worlds':"https://api.deepworldgame.com/v1/worlds?residency=owned",'Unexplored':'https://api.deepworldgame.com/v1/worlds?development=0'}


    
    def login(self):
        self.key = askstring("Login", "Enter your API key.")
        self.loggedin=True
        self.mainText.set("Logged in!")

        



    def callAPI(self,request=""):
        if request=="":
            request = 'My Worlds'
        self.mainText.set("Importing data from server")
        url = "".join([self.APILib[request],'&api_token=',self.key])
        data = urllib.request.urlopen(url)
        data = data.read()
        data = data.decode('UTF-8')
        self.data=json.loads(data)


    def dispNames(self):
        self.callAPI()
        cont=[]
        for i in self.data:
            cont.append(i['name'])
        
        cont=sorted(cont,key=str.lower)
        return cont

    def FindWorlds(self):
        if self.loggedin == True:
            self.callAPI("Unexplored")
            cont=["Unexplored worlds:\n"]
            for i in self.data:
                try:
                    str((i['protected']))
                except KeyError:
                    cont.append(i['name']+" - "+i['biome']+" - "+str(round(i['explored']*100,0))+"%")
                    cont.append("\n")
            cont="".join(cont)
            if cont=="":
                cont="No applicable worlds"
            self.newWorldText.set(cont)
            self.populateBtns()
        else:
            showinfo("Warning","Log in first!")

    def populateBtns(self):
        if self.loggedin == True:
            self.mainText.set("Select a World:")
            worldList = self.dispNames()
            self.btnpopulation = len(worldList)
            for i in range(self.btnpopulation):
                a = worldList[i]
                setattr(self,"WButton"+str(i),tk.Button(self.dataWindow, text=a,command=lambda a=a: self.worldWindow(a)))
                eval("self.WButton"+str(i)).grid(row=i+2,column=0,sticky=tk.E+tk.W)
        else:
            showinfo("Warning","Log in first!")
        
    def worldWindow(self,name):
        
        for i in self.data:
            if i['name']==name:
                lt1=[name," is a ", i['biome'] ," world."]
                lt2="".join(['Players online: ',str(i['players'])])
                lt3="".join(['Explored: ',str(i['explored']*100),"%"])
                lt4="".join(['Players online: ',str(i['players'])])
                if i['acidity']==0:
                    purified = "Yes"
                else:
                    purified = "No"
                lt5="".join(['Purified: ',purified])
                lt6="".join(["Size: ",str(i['size'][0]),'x',str(i['size'][1])])
                lt7="".join(['Plaques: ',str(i['content']['plaques'])])
                lt8="".join(['Landmarks: ',str(i['content']['landmarks'])])
                lt9="".join(['Teleporters: ',str(i['content']['teleporters'])])
                lt10="".join(['Spawns: ',str(i['content']['spawns'])])
                lt11="".join(['Protectors: ',str(i['content']['protectors'])])

                self.worldWindowText.set("\n".join(["".join(lt1),lt2,lt3,lt4,lt5,lt6,lt7,lt8,lt9,lt10,lt11]))

        self.worldData = tk.Label(self.dataWindow,textvariable=self.worldWindowText,justify=tk.LEFT)
        self.worldData.grid(row=0,column=2,rowspan=self.btnpopulation+1)
                


root = tk.Tk()
root.title("Deepworld API v0.1")
root.wm_state('zoomed')
display = MainWindow(root)
root.config(menu=display.mBar)

root.mainloop()
