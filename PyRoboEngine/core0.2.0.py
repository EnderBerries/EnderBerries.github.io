import os
import json
import uuid
import base64
import zipfile
from shutil import copy
import base
BuildinData = {
    "DIR_PyLib":"Robosim_Data\\StreamingAssets\\Lib",
    "version":"0.2.0",
    "ClientToken":"1ac9ccd925bc44f7928c33c18f175b89",
    "PVersion":0,
    "commands":["cls","workspace","robosim","inject","exit","help","clearcache","#"],
    "engines":["white","black"],
    "engineFiles":["Engine_White.py","Engine_Black.py"],
    "requirements":["挂起.bat","开发文档.docx","释放.bat","pssuspend.exe","rcu.py","ChangeLog.txt"],
    "targetEngineName":"Engine.py",
    "texts":{
        "program.welcome":"RyRoboEngineInstaller v0.2.0 By @EnderBerries\n版权所有:2024 EnderBerries  仅供个人学习研究 请勿二次分发\n输入\"help\"获取帮助",
        "program.input":">>>",
        "program.command.unknown":"未知的命令：%COMMAND%",
        "program.command.wrong":"命令格式错误，使用\"help\"查询相关用法",
        "program.command.help":"""
命令详解：
    关于参数:
        <aaa>:必填项
        [aaa]:可选项
        [aaa|bbb]:选填项
    命令列表:cls;workspace;robosim;engine;inject;exit;help
        """,
        "program.command.help.help":"""
help:获取帮助
    help <command>
    <command>要获取帮助的命令
        """,
        "program.command.help.cls":"""
cls:清屏
cls
        """,
        "program.command.help.exit":"""
exit:退出
exit
        """,
        "program.command.help.clearcache":"DEBUG",
        "program.command.help.workspace":"""
workspace:工作区相关
workspace list
workspace new [path] [name]
workspace init
workspace open [name]
workspace close
workspace engine [engineIncluded]
workspace rename [name] [newname]
workspace delete [name]
workspace addon list
workspace addon add [addon]
workspace addon del [addon]
    new:建立工作区
    open:打开工作区
    init:工作区初始化
    close:关闭工作区
    rename:重命名工作区
    delete:删除工作区
    engine:选择巡线引擎
    addon:关于加载项操作
    [addon]:加载项（应包含拓展名）
    path:工作区目录路径
    name,newname:工作区名称
    engineIncluded:已包含的引擎
        """,
        "program.command.help.robosim":"""
robosim:绑定robosim.exe
robosim [path|binding]
    path:robosim路径
    binding:查看是否已绑定robosim.exe
        """,
        "program.command.help.inject":"""
inject:更新robosim已导入的引擎
inject <classic>
    classic:是否使用默认引擎
        """,
        "program.command.exit.fail":"请先关闭已打开的工作区",
        "program.command.robosim.binding":"绑定成功，当前Robosim路径：%PATH%",
        "program.command.robosim.binding.fail":"当前路径无效",
        "program.command.robosim.binding.NotAPath":"指定的路径不存在",
        "program.command.robosim.check.y":"当前状态：已绑定\nRobosim路径为：%PATH%",
        "program.command.robosim.check.n":"当前状态：未绑定",
        "program.command.workspace.nospace":"当前没有工作区",
        "program.command.workspace.hasspace":"已有工作区：",
        "program.command.workspace.new.suc":"已创建工作区：%NAME%",
        "program.command.workspace.new.fail":"无效的路径或名称",
        "program.command.workspace.delete":"已删除工作区：%NAME%",
        "program.command.workspace.delete.notfound":"该工作区不存在",
        "program.command.workspace.delete.opened":"请先关闭该工作区后重试",
        "program.command.workspace.rename.fail":"要改名的工作区不存在或已有目标名称工作区",
        "program.command.workspace.rename.suc":"重命名成功",
        "program.command.workspace.open.suc":"成功打开工作区：%WORKSPACE%",
        "program.command.workspace.open.fail":"打开失败：%WORKSPACE% 已被打开",
        "program.command.workspace.open.notfound":"未找到工作区：%WORKSPACE%",
        "program.command.workspace.close.notfound":"未打开任何工作区",
        "program.command.workspace.close.suc":"成功关闭工作区",
        "program.command.workspace.engine.suc":"成功将引擎设置为：%ENGINE%",
        "program.command.workspace.engine.fail":"当前未提供此类型引擎",
        "program.command.workspace.init.fail":"请先选择引擎类型",
        "program.command.workspace.init.suc":"已成功初始化工作区 %WORKSPACE%",
        "program.command.workspace.addon.list":"以下为当前已有加载项：",
        "program.command.workspace.addon.list.notfound":"当前没有加载项",
        "program.command.workspace.addon.add":"已将 %ADDON% 加入加载项",
        "program.command.workspace.addon.add.notfound":"未找到 %ADDON%",
        "program.command.workspace.addon.add.fail":"%ADDON% 已经是当前加载项了",
        "program.command.workspace.addon.del":"已将 %ADDON% 从加载项中删去",
        "program.command.workspace.addon.del.notfound":"%ADDON% 不是当前加载项",
        "program.command.inject.notfound":"请确认加载项完整后重试",
        "program.command.inject.suc":"注入完成",
        "program.command.not_binding":"请先绑定Robosim.exe路径",

    
    }
}
injectSet = set()
activeWorkspace = {}
openedWorkspace = None
ClassicConfigValue = {
    "workspaces":{},
    "PATH_Robosim":"",
    "found_Robosim":False
}
Config = {
}
PATH_Appdata = os.path.expandvars("%APPDATA%")
PATH_Temp = os.path.join(PATH_Appdata, "PyRoboEngine\\req",str(uuid.uuid4()))
PATH_config = os.path.join(PATH_Appdata,"PyRoboEngine\\config.json")
if not os.path.exists(PATH_config):
    os.makedirs(os.path.join(PATH_Appdata,"PyRoboEngine"))
    with open(PATH_config,"w") as f:
        f.write(json.dumps(ClassicConfigValue, indent=4))
try:
    json.load(open(PATH_config))
except:
    with open(PATH_config,"w") as f:
        f.write(json.dumps(ClassicConfigValue, indent=4))

with open(PATH_config,"r") as f:
    Config = json.load(f)

def text(key:str):
    try:
        return BuildinData["texts"][key]
    except:
        return key
    
def getCommandList(inp,find = ","):
    '''
    用于拆分命令
    '''
    global CommandList
    CommandList = []
    mlist = []
    fk,hk,pos,bm,sm,lastpos, = 0,0,0,0,0,0,
    laststr = ""
    for i in inp:
        pos += 1
        if i == "{":
            hk += 1
        elif i == "}":
            hk -= 1
        elif i == "[":
            fk += 1
        elif i == "]":
             fk -= 1
        elif i == "'":
            sm += 1
            if laststr != "\\" :mlist.append("'")
        elif i == '"':
            bm += 1
            if laststr != "\\" :mlist.append('"')
        elif i == find and fk == 0 and hk == 0:
            if len(mlist) == 0:
                CommandList.append(inp[lastpos:pos-1])
                lastpos = pos 
            elif len(mlist) >= 2 and mlist[0] == mlist[-1]:
                mlist.clear()
                CommandList.append(inp[lastpos:pos-1])
                lastpos = pos 
        laststr = i
    if len(inp[lastpos:]) != 0 == 0:
        mlist.clear()
        CommandList.append(inp[lastpos:])
    return CommandList

def saveConfig():
    global Config
    with open(PATH_config,"w") as f:
        f.write(json.dumps(Config, indent=4))
        f.close()

def pullFile(workspacePath:str,engine:str) -> None:
    try:
        os.makedirs(os.path.join(PATH_Temp,"data_full"))
    except:
        pass
    b = open(os.path.join(PATH_Temp,"base.base64"),"w")
    b.write(base.baseIncluded)
    b.close()
    b = open(os.path.join(PATH_Temp,"base.base64"),"rb")
    z = open(os.path.join(PATH_Temp,"req.zip"),"wb")
    base64.decode(b,z)
    z.close()
    b.close()
    with zipfile.ZipFile(os.path.join(PATH_Temp,"req.zip"),"r") as zip:
        zip.extractall(os.path.join(PATH_Temp,"data_full"))
    fullFiles = os.listdir(os.path.join(PATH_Temp,"data_full"))
    for i in fullFiles:
        if i in BuildinData["requirements"]:
            copy(os.path.join(PATH_Temp,"data_full",i),os.path.join(workspacePath,i))
    engine_index = BuildinData["engines"].index(engine)
    copy(os.path.join(PATH_Temp,"data_full",BuildinData["engineFiles"][engine_index]),os.path.join(workspacePath,BuildinData["targetEngineName"]))


#Shell部分
def shellLoop():
    global activeWorkspace
    global openedWorkspace
    global injectSet
    tmpcmd = input(text("program.input"))
    handleCommand = getCommandList(tmpcmd,find=" ")
    longCo = len(handleCommand)
    if longCo == 0:
        pass
    elif handleCommand[0] not in BuildinData["commands"]:
       print(text("program.command.unknown").replace("%COMMAND%",handleCommand[0])) 
    else:
        if handleCommand[0] == "cls" and longCo == 1:
            os.system("cls")
            print(text("program.welcome"))

        elif handleCommand[0] == "exit" and longCo == 1:
            if openedWorkspace != None:
                print(text("program.command.exit.fail"))
            else:
                exit(0)

        elif handleCommand[0] == "help" and longCo <= 2 and longCo >= 1:
            if longCo == 1:
                print(text(f"program.command.help"))
            elif handleCommand[1] not in BuildinData["commands"]:
                print(text("program.command.unknown").replace("%COMMAND%",handleCommand[1]))
            else:
                print(text(f"program.command.help.{handleCommand[1]}"))

        elif handleCommand[0] == "robosim" and longCo == 2:
            if handleCommand[1] == "binding":
                if Config["found_Robosim"] == True:
                    print(text("program.command.robosim.check.y").replace("%PATH%",Config["PATH_Robosim"]))
                else:
                    print(text("program.command.robosim.check.n"))
            else: 
                if os.path.exists(handleCommand[1]):
                    if os.path.exists(os.path.join(os.path.dirname(handleCommand[1]),BuildinData["DIR_PyLib"],"os.py")):
                        Config["found_Robosim"] = True
                        Config["PATH_Robosim"] = handleCommand[1]
                        saveConfig()
                        print(text("program.command.robosim.binding").replace("%PATH%",handleCommand[1]))
                    else:
                        print(text("program.command.robosim.binding.fail"))
                else:
                    print(text("program.command.robosim.binding.NotAPath"))

        elif handleCommand[0] == "workspace" and longCo <= 4 and longCo >= 2:
            if Config["PATH_Robosim"] != "":
                if handleCommand[1] == "list" and longCo == 2:
                    if len(Config["workspaces"]) == 0:
                        print(text("program.command.workspace.nospace"))
                    else:
                        print(text("program.command.workspace.hasspace"))
                        for i in Config["workspaces"].keys():
                            print(i)
                elif handleCommand[1] == "new" and longCo == 4:
                    try:
                        if not os.path.exists(handleCommand[2]):
                            os.makedirs(handleCommand[2])
                        al = []
                        nl = []
                        for i in Config["workspaces"].values():
                            al.append(i["path"])
                        for i in Config["workspaces"].keys():
                            nl.append(i["path"])
                        if handleCommand[2] in al:
                            raise
                        if handleCommand[3] in nl:
                            raise
                        tmpdct={"uuid":str(uuid.uuid4()),"path":handleCommand[2],"engine":"unknown","addons":[]}
                        Config["workspaces"][handleCommand[3]] = {}
                        Config["workspaces"][handleCommand[3]].update(tmpdct)
                        saveConfig()
                        print(text("program.command.workspace.new.suc").replace("%NAME%",handleCommand[3]))
                    except:
                        print(text("program.command.workspace.new.fail"))
                elif handleCommand[1] == "delete" and longCo == 3:
                    if not handleCommand[2] == openedWorkspace:
                        if handleCommand[2] in Config["workspaces"]:
                            del(Config["workspaces"][handleCommand[2]])
                            saveConfig()
                            print(text("program.command.workspace.delete").replace("%NAME%",handleCommand[2]))
                        else:
                            print(text("program.command.workspace.delete.notfound"))
                    else:
                        print(text("program.command.workspace.delete.opened"))
                elif handleCommand[1] == "rename" and longCo == 4:
                    if handleCommand[3] in Config["workspaces"] or handleCommand[2] not in Config["workspaces"]:
                        print(text("program.command.workspace.rename.fail")) 
                    else:
                        Config["workspaces"][handleCommand[3]] = {}
                        Config["workspaces"][handleCommand[3]].update(Config["workspaces"][handleCommand[2]])
                        del(Config["workspaces"][handleCommand[2]])
                        print(text("program.command.workspace.rename.suc"))
                elif handleCommand[1] == "open" and longCo == 3:
                    if openedWorkspace == None:
                        if handleCommand[2] in Config["workspaces"]:
                            activeWorkspace = Config["workspaces"][handleCommand[2]]
                            if not "EngineVersion" in activeWorkspace or activeWorkspace["EngineVersion"] < BuildinData["PVersion"]:
                                activeWorkspace["EngineVersion"] = BuildinData["PVersion"]
                                print("YOU ARE USING A LOW PYROBOENGINE VERSION")
                            openedWorkspace = handleCommand[2]
                            spacepath = activeWorkspace['path'].replace('/','\\')
                            os.system(f"explorer /root,\"{spacepath}\"")
                            print(text("program.command.workspace.open.suc").replace("%WORKSPACE%",openedWorkspace))
                        else:
                            print(text("program.command.workspace.open.notfound").replace("%WORKSPACE%",handleCommand[2]))
                    else:
                        print(text("program.command.workspace.open.fail").replace("%WORKSPACE%",openedWorkspace))
                elif handleCommand[1] == "close" and longCo == 2:
                    if openedWorkspace == None:
                        print(text("program.command.workspace.close.notfound"))
                    else:
                        Config["workspaces"][openedWorkspace].update(activeWorkspace)
                        activeWorkspace = {}
                        openedWorkspace = None
                        saveConfig()
                        for i in injectSet:#移除注入
                            try:
                                os.remove(os.path.join(os.path.dirname(Config["PATH_Robosim"]),BuildinData["DIR_PyLib"],i))
                            except:
                                pass
                        injectSet = set()
                        print(text("program.command.workspace.close.suc"))
                elif handleCommand[1] == "engine" and longCo == 3:
                    if openedWorkspace != None:
                        if handleCommand[2] in BuildinData["engines"]:
                            activeWorkspace["engine"] = handleCommand[2]
                            if not "Engine.py" in activeWorkspace["addons"]:
                                activeWorkspace["addons"].append(BuildinData["targetEngineName"])
                            activeWorkspace["engineFile"] = BuildinData["targetEngineName"]
                            print(text("program.command.workspace.engine.suc").replace("%ENGINE%",handleCommand[2]))
                        else:
                            print(text("program.command.workspace.engine.fail"))
                    else:
                        print(text("program.command.workspace.close.notfound"))
                elif handleCommand[1] == "init":
                    if openedWorkspace != None:
                        if activeWorkspace["engine"] != "unknown":
                            pullFile(activeWorkspace["path"],activeWorkspace["engine"])
                            print(text("program.command.workspace.init.suc").replace("%WORKSPACE%",openedWorkspace))
                            pass
                        else:
                            print(text("program.command.workspace.init.fail"))
                    else:
                        print(text("program.command.workspace.close.notfound"))

                elif handleCommand[1] == "addon" and longCo >= 3 and longCo <= 4:
                    if openedWorkspace != None:
                        if activeWorkspace["engine"] != "unknown":
                            if handleCommand[2] == "list" and longCo == 3:
                                if len(activeWorkspace["addons"]):
                                    print(text("program.command.workspace.addon.list"))
                                    for i in activeWorkspace["addons"]:
                                        print(i)
                                else:
                                    print(text("program.command.workspace.addon.list.notfound"))

                            elif handleCommand[2] == "add" and longCo == 4:
                                if handleCommand[3] not in activeWorkspace["addons"]:
                                    if os.path.exists(os.path.join(activeWorkspace["path"],handleCommand[3])):
                                        activeWorkspace["addons"].append(handleCommand[3])
                                        print(text("program.command.workspace.addon.add").replace("%ADDON%",handleCommand[3]))
                                    else: print(text("program.command.workspace.addon.add.notfound").replace("%ADDON%",handleCommand[3]))
                                else: print(text("program.command.workspace.addon.add.fail").replace("%ADDON%",handleCommand[3]))

                            elif handleCommand[2] == "del" and longCo == 4:
                                if handleCommand[3] in activeWorkspace["addons"]:
                                    tempindex = activeWorkspace["addons"].index(handleCommand[3])
                                    activeWorkspace["addons"].pop(tempindex)
                                    print(text("program.command.workspace.addon.del").replace("%ADDON%",handleCommand[3]))
                                else: print(text("program.command.workspace.addon.add.notfound").replace("%ADDON%",handleCommand[3]))

                            else: print(text("program.command.wrong"))
                        else: print(text("program.command.workspace.init.fail"))
                    else: print(text("program.command.workspace.close.notfound"))
                else: print(text("program.command.wrong"))
            else: print(text("program.command.not_binding"))

        elif handleCommand[0] == "inject" and longCo == 1:
            if Config["PATH_Robosim"] != "":
                if openedWorkspace != None:
                    if activeWorkspace["engine"] != "unknown":
                        if len(activeWorkspace["addons"]):
                            #核检文件
                            passed = True
                            for i in activeWorkspace["addons"]:
                                if not os.path.exists(os.path.join(activeWorkspace["path"],i)):
                                    passed = False
                                    break
                            if passed:#复制文件
                                for i in os.listdir(activeWorkspace["path"]):
                                    if i in activeWorkspace["addons"]:
                                        copy(os.path.join(activeWorkspace["path"],i),os.path.join(os.path.dirname(Config["PATH_Robosim"]),BuildinData["DIR_PyLib"],i))
                                        injectSet.add(i)
                                print(text("program.command.inject.suc"))
                            else: print(text("program.command.inject.notfound"))
                        else: print(text("program.command.workspace.addon.list.notfound"))
                    else: print(text("program.command.workspace.init.fail"))
                else: print(text("program.command.workspace.close.notfound"))
            else: print(text("program.command.not_binding"))



        elif handleCommand[0] == "clearcache" and longCo == 1:
            with open(PATH_config,"w") as f:
                f.write("")
            print("Finished After Restart")
            exit(0)
        elif handleCommand[0] == "#":
            try:
                exec(tmpcmd[2:])
            except:
                print("Error")
        else:
            print(text("program.command.wrong"))

def main(token):
    if token == BuildinData["ClientToken"]:
        os.system("cls")
        print(text("program.welcome"))
        while True:
            shellLoop()



'''
"example":{
    "uuid":""
    "path":"C:/XXX/XXX/workspace.pyrobo",
    "engine":"white",
    "addons":[],
    "engineFile":"XXX",
    "EngineVersion":0
}
'''