const path = require('path');
const webpack = require('webpack');

module.exports = {
	entry: './src/js/index.js',
	devtool: 'inline-source-map',
	module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /(node_modules|bower_components)/,
        loader: "babel-loader",
        options: { presets: ["@babel/env"] }
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      }
    ]
    },
    resolve: { extensions: ["*", ".js", ".jsx"] },
	output: {
		filename: 'main.js',
		path: path.resolve(__dirname, 'static/js')
	}
};
