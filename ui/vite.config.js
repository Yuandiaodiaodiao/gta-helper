import path from "path";
const root = path.join(__dirname, "src");
export default {
    base: "./",
    outDir: "dist",
    alias: {
        // 别名必须以 / 开头、结尾
        "/@/": root,
    },
    rollupInputOptions: {
        external: ["fs", "path", "stream", "electron"],
    },
    rollupOutputOptions: {
        format: "commonjs",
    },
};
