const path = require("path");
const getpath = require("./getpath.js");

let script = getpath(path.join("keyboardloop", "keyboardloop.exe"));
function generateArgs(arg){
    let args=[]
    Object.entries(arg).forEach(([key,value])=>{
        if (value==="")return
        args.push("--"+key)
        if(value instanceof Array){
            args=[...args,...value]
        }else{
            args.push(value)
        }
    })
    return args
}

function newprocess(args){
    args=generateArgs(args)
    args.push("--modelpath")
    args.push(getpath(path.join("keyboardloop", "model")))
    console.log(args)
    console.log(script)
    let pyProc = require("child_process").execFile(script, args);

    pyProc.stdout.on("data", (data) => {
        console.log(`stdout: ${data}`);
    });
    pyProc.stderr.on("data", (data) => {

        console.error(`${data}`);
    });
    pyProc.on("close", (code) => {
        console.log(`child_process exit, code= ${code}`);
    });

    return pyProc
}
module.exports.proc = newprocess;
