const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
module.exports = {
optimization: {
  minimizer: [
    new UglifyJsPlugin({
      cache: true,
      parallel: true,
      sourceMap: true // set to true if you want JS source maps
    }),
    new OptimizeCSSAssetsPlugin({})
  ]
},
plugins: [
    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      filename: "[name].css",
      chunkFilename: "[id].css"
    })
  ],
  module: {
    rules: [
      { test: /\.css$/,
        use: [
        MiniCssExtractPlugin.loader,
        "css-loader" }
        ]
      },
      {
    test: /\.html$/,
    use: [ {
      loader: 'html-loader',
      options: {
        minimize: true
        ]
      }
      { test: /\.js$/,
        exclude: /node_modules/,
        use: [
        loader: 'babel-loader'
        ]
      },
      babel-loader
      uglify
      less
      html-loader
    ]
  }
};
