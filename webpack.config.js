/**
 * Created by prism on 4/5/16.
 */
var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    entry: [
        './static/app/app.jsx'
    ],
    output : {
        path: __dirname,
        filename: './static/js/bundle.js'
    },
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
                query: {
                    plugins: ['transform-decorators-legacy' ],
                    presets: ['react', 'es2015', 'stage-0']
                }
            }
        ]
    },
    plugins: process.env.NODE_ENV === 'production' ? [
        new webpack.optimize.DedupePlugin(),
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin()
    ] : [new BundleTracker({filename: './webpack-stats.json'})],
};