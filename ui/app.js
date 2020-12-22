const {app, BrowserWindow, ipcMain} = require("electron")
const path = require("path")
const encoding=(buffer)=>{
    const iconv = require('iconv-lite');
    return iconv.decode(buffer,'GBK')
}

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
    ipcMain.on('debug',()=>{
        win.webContents.openDevTools()
    })
    ipcMain.on("restart", (event, args) => {
        console.log(args)
        stop()
        proc = require('./node/subprocess').proc(JSON.parse(args),(error,stdout,stderr)=>{
            // win.webContents.send('log',encoding(stdout))
            // win.webContents.send('log',encoding(stderr))
            // win.webContents.send('log',encoding(error))
        })
        proc.stdout.on("data", (data) => {
            data=encoding(data)
            win.webContents.send('log',data)
            console.log(`stdout: ${data}`);
        });
        proc.stderr.on("data", (data) => {
            data=encoding(data)
            win.webContents.send('log',data)
            console.error(`${data}`);
        });
        proc.addListener("close",()=>{console.log("close")})
        proc.addListener("error",()=>{console.log("error")})

    })
    ipcMain.on('stop',stop)
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
