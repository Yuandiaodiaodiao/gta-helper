const path = require("path");
const getpath = require("./getpath.js");

let script = getpath(path.join("keyboardloop", "keyboardloop.exe"));
// script = getpath(path.join("loggingtest", "loggingtest.exe"));
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

function newprocess(args,callback){
    args=generateArgs(args)
    args.push("--modelpath")
    args.push(getpath(path.join("keyboardloop", "model")))
    console.log(args)
    console.log(script)
    let scriptstr=args.join(" ")
    let pyProc = require("child_process").execFile(script, args,{ encoding: 'gbk' },callback);
    // let cmdstr=`${script} ${scriptstr}`
    // console.log(cmdstr)
    // let pyProc = require("child_process").exec(cmdstr,{ encoding: 'gbk' });


    pyProc.on("close", (code) => {
        console.log(`child_process exit, code= ${code}`);
    });

    return pyProc
}
module.exports.proc = newprocess;
