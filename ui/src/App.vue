<style scoped>
.el-container {
  height: 100%;
}

.el-main {
  display: flex;
  flex-direction: column;
}

.el-footer {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}

.lineinput {
  display: flex;
  align-items: center;
  flex-direction: row;
}

.el-input {
  width: 100px;
  margin: 10px;
}
</style>

<template>
  <el-container>
    <el-header>
      <div class="lineinput">
        状态 : &nbsp;
        <el-tag :type="status==='stop'?'danger':'success'">{{ status }}</el-tag>
      </div>

    </el-header>
    <el-main>
      <div class="lineinput">
        分辨率:
        <el-input placeholder="1920" v-model="config.width"></el-input>
        x
        <el-input placeholder="1080" v-model="config.height"></el-input>
      </div>
      <el-select v-model="config.mode" placeholder="显示模式">
        <el-option
            v-for="item in windowOtions"
            :label="item"
            :value="item"
        >
        </el-option>
      </el-select>
      <div class="lineinput">
        打开esc后 一键提高产量 :
        <el-input placeholder="f8" v-model="config.tp"></el-input>
      </div>
      <div class="lineinput">
        佩里克指纹破解 :
        <el-input placeholder="f9" v-model="config.perico"></el-input>
      </div>
      <div class="lineinput">
        挂机 :
        <el-input placeholder="null" v-model="config.afk"></el-input>
      </div>
      <div class="lineinput">
        停止所有正在运行的动作 :
        <el-input placeholder="backspace" v-model="config.stop"></el-input>
      </div>
      <div class="lineinput">
        按键延迟 <br/>
        (keydown 与keyup之间的时间<br/>
        如果丢键可以开高这个) :
        <el-input placeholder="0" v-model="config.keydelay"></el-input>
      </div>
      <div class="lineinput">
        关闭服务 :
        <el-input placeholder="delete" v-model="config.allstop"></el-input>
      </div>
      <div class="lineinput">
        <el-button style="width: 100px;margin: 10px" @click="restart()">重启服务</el-button>
        <el-button style="width: 100px;margin: 10px" @click="stop()">关闭服务</el-button>
        <el-button style="width: 100px;margin: 10px" @click="debugstart()">debug菜单</el-button>
      </div>

      <div class="lineinput">
        高级选项:
        <el-switch
            style="width: 100px"
            v-model="advanced"
            active-color="#13ce66">
        </el-switch>
      </div>

      <div v-show="advanced" class="lineinput">
        左侧指纹图像裁切比例 :
        <el-input v-for="item in [0,1,2,3]" v-model="config.cast[item]"></el-input>
      </div>
    </el-main>
    <el-footer>
      <div>@Yuandiaodiaodiao</div>
      <a href="https://github.com/Yuandiaodiaodiao/gta-helper">使用方法 & 源代码 & bug-report</a>
    </el-footer>
  </el-container>
</template>

<script>
import {reactive, watch, ref, onMounted} from 'vue'
import {ElMessage} from 'element-plus'

const loadconfig = () => {
  const configTemplate = {
    height: 1080,
    width: 1920,
    tp: 'f8',
    perico: 'f9',
    afk: '',
    stop: 'backspace',
    mode: 'fullscreen',
    cast: [0.317, 0.885, 0.226, 0.4165],
    keydelay: 0,
    allstop:'delete'
  }
  const fs = require("fs")
  try {
    if (fs.existsSync("config.json")) {
      const configfile = fs.readFileSync("config.json", {encoding: "utf-8"})
      const configjs = JSON.parse(configfile)
      return {...configTemplate, ...configjs}
    }
  } catch (e) {
    console.error(e)
  }
  return configTemplate
}
const saveconfig = (config) => {
  const fs = require("fs")
  try {
    fs.writeFileSync("config.json", JSON.stringify(config))
  } catch (e) {
    console.error(e)
  }
}
export default {
  name: 'App',
  setup() {
    const advanced = ref(false)
    const status = ref("stop")
    const config = reactive(loadconfig())
    let timeoutHandle = null
    const ipcRenderer = require("electron").ipcRenderer
    const restart = () => {
      ipcRenderer.send("restart", JSON.stringify(config))
    }
    const stop = () => {
      ipcRenderer.send("stop")
    }
    const debugstart = () => {
      ipcRenderer.send('debug')
    }
    onMounted(restart)

    watch(config, () => {
      console.log("config changed")
      //防抖半秒
      clearTimeout(timeoutHandle)
      timeoutHandle = setTimeout(() => {
        restart()
        saveconfig(config)
        ElMessage.success({message: "设置应用成功", duration: 500})
      }, 500)
    })
    ipcRenderer.on("reportState", (event, msg) => {
      if (status.value !== msg) {
        status.value = msg
      }
    })
    ipcRenderer.on('log',(event, args) => {
      console.log(args)
    })
    const windowOtions = ["fullscreen", "borderless", 'window']
    return {config, status, windowOtions, advanced, restart, stop, debugstart}
  }
}

</script>
