const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
    devServer: {
        port: 8888
    },
    configureWebpack: config => {
        config.plugins.forEach((val) => {
            if (val instanceof HtmlWebpackPlugin) {
                val.options.title = 'similar-star'
            }
        })
    },
    "transpileDependencies": [
        "vuetify"
    ]
}