const {app, BrowserWindow, ipcMain} = require("electron")
const path = require("path")

function createWindow() {
    // 创建浏览器窗口
    win = new BrowserWindow({
        width: 1000,
        height: 1000,
        // frame: false,
        // resizable: false, //禁止改变主窗口尺寸
        webPreferences: {
            enableRemoteModule: true,
            nodeIntegration: true, // 继承 node
        },
        // titleBarStyle: "hidden", // add this line
    })

    let url
    if (process.env.NODE_ENV === "development") {
        url = "http://localhost:3000"
    } else {
        url = `file://${path.join(__dirname, "dist", "index.html")}`
    }
    // 然后加载应用的 index.html。
    win.loadURL(url)
    if (process.env.NODE_ENV === "development") {
        win.webContents.openDevTools()
    }
    let proc = null
    const stop = () => {
        if (proc) {
            proc.kill()
        }
    }
    ipcMain.on("restart", (event, args) => {
        console.log(args)
        stop()
        proc = require('./node/subprocess').proc(JSON.parse(args))
        proc.addListener("close",()=>{console.log("close")})
        proc.addListener("error",()=>{console.log("error")})

    })
    setInterval(() => {
        try{
            let status = (proc && !proc.killed && proc.exitCode==null) ? "running" : "stop"
            win.webContents.send("reportState", status)
        }catch (e) {
            console.log(e)
        }
    }, 1000)
    app.on("will-quit", stop)
}

app.on("ready", createWindow)
