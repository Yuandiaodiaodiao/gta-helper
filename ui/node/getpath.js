console.log(process.cwd())
console.log(process.env.NODE_ENV)
function getpath(pathname) {
    const path = require("path")

    let templateFilePath = path.join(process.cwd(), "/resources/", pathname)
    if (process.env.NODE_ENV === "development") {
        templateFilePath = path.join(process.cwd(), pathname)
    }
    return templateFilePath
}
module.exports = getpath
