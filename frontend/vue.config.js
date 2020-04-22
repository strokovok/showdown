module.exports = {
    css: {
        loaderOptions: {
            sass: {
                prependData: `@import "@/assets/variables.scss";`
            }
        }
    },
    devServer: {
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:5000',
                ws: true,
                changeOrigin: true
            }
        }
    }
};
