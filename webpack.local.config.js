/**
 * Created by prism on 1/6/17.
 */
var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    //devtool: 'source-map',
    context: __dirname,
    entry: [
        'webpack-dev-server/client?http://localhost:3000',
        'webpack/hot/only-dev-server',
        './bunny/app.jsx'
    ],

    output: {
        path: path.resolve('./static/js/bundles/'),
        filename: '[name]-[hash].js',
        publicPath: 'http://localhost:3000/assets/bundles/' // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
    },

    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoErrorsPlugin(), // don't reload if there is an error
        new BundleTracker({filename: './webpack-stats.json'}),
    ],

    module: {
        loaders: [
            // we pass the output from babel loader to react-hot loader
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loaders: ['react-hot', 'babel-loader?presets[]=es2015,presets[]=stage-0,presets[]=react,plugins[]=transform-decorators-legacy']
            }
        ]
    },

    resolve: {
        modulesDirectories: ['node_modules', 'bower_components'],
        extensions: ['', '.js', '.jsx']
    }
}