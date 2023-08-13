const { defineConfig } = require('@vue/cli-service')

let devProxy = {
    proxy: {
        '^/data': {
            target: 'http://localhost:8081',
            changeOrigin: true,
        },
    }
}

module.exports = defineConfig({
    transpileDependencies: true,
    publicPath: process.env.dev === 'dev' ? '/' : './static',
    devServer:  process.env.dev === 'dev' ? devProxy :{}
})
