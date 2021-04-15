/* eslint-env node */
const webpack = require("webpack");
const path = require("path");
const VueLoaderPlugin = require("vue-loader/lib/plugin");
const OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const DuplicatePackageCheckerPlugin = require("duplicate-package-checker-webpack-plugin");

const scriptsBase = path.join(__dirname, "src");
const testsBase = path.join(__dirname, "tests");
const libsBase = path.join(scriptsBase, "libs");
const styleBase = path.join(scriptsBase, "style");

<<<<<<< HEAD
let buildconfig = {
    entry: {
        login: ["onload", "apps/login"],
        analysis: ["onload", "apps/analysis"],
        admin: ["onload", "apps/admin"],
        extended: ["onload", "apps/extended"]
    },
    output: {
        path: path.join(__dirname, "../", "static/scripts/bundled"),
        filename: "[name].bundled.js",
        chunkFilename: "[name].chunk.js"
    },
    resolve: {
        modules: [scriptsBase, "node_modules", styleBase, imageBase],
        alias: {
            jquery$: `${libsBase}/jquery.custom.js`,
            jqueryVendor$: `${libsBase}/jquery/jquery.js`,
            store$: "store/dist/store.modern.js"
        }
    },
    optimization: {
        splitChunks: {
            cacheGroups: {
                styles: {
                    name: "base",
                    chunks: "all",
                    test: m => m.constructor.name == "CssModule",
                    priority: -5
=======
module.exports = (env = {}, argv = {}) => {
    // environment name based on -d, -p, webpack flag
    const targetEnv = argv.mode || "development";

    const buildconfig = {
        entry: {
            login: ["polyfills", "bundleEntries", "entry/login"],
            analysis: ["polyfills", "bundleEntries", "entry/analysis"],
            admin: ["polyfills", "bundleEntries", "entry/admin"],
            generic: ["polyfills", "bundleEntries", "entry/generic"],
        },
        output: {
            path: path.join(__dirname, "../", "/static/dist"),
            publicPath: "/static/dist/",
            filename: "[name].bundled.js",
            chunkFilename: "[name].chunk.js",
        },
        resolve: {
            extensions: ["*", ".js", ".json", ".vue", ".scss"],
            modules: [scriptsBase, "node_modules", styleBase, testsBase],
            alias: {
                jquery$: `${libsBase}/jquery.custom.js`,
                jqueryVendor$: `${libsBase}/jquery/jquery.js`,
                storemodern$: "store/dist/store.modern.js",
                "popper.js": path.resolve(__dirname, "node_modules/popper.js/"),
                moment: path.resolve(__dirname, "node_modules/moment"),
                underscore: path.resolve(__dirname, "node_modules/underscore"),
                // client-side application config
                config$: path.join(scriptsBase, "config", targetEnv) + ".js",
            },
        },
        optimization: {
            splitChunks: {
                cacheGroups: {
                    styles: {
                        name: "base",
                        chunks: "all",
                        test: (m) => m.constructor.name == "CssModule",
                        priority: -5,
                    },
                    libs: {
                        name: "libs",
                        test: /node_modules[\\/](?!(handsontable|pikaday|moment|elkjs)[\\/])|galaxy\/scripts\/libs/,
                        chunks: "all",
                        priority: -10,
                    },
>>>>>>> refs/heads/release_21.01
                },
<<<<<<< HEAD
                libs: {
                    name: "libs",
                    test: /(node_modules|galaxy\/scripts\/(?!apps)).*\.(vue|js)$/, // .*\.(vue|js)$
                    chunks: "all",
                    priority: -10
                }
            }
        }
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: "vue-loader"
=======
>>>>>>> refs/heads/release_21.01
            },
<<<<<<< HEAD
            {
                test: /\.js$/,
                // Pretty sure we don't want anything except node_modules here
                exclude: [
                    /(node_modules\/(?!(handsontable)\/)|bower_components)/,
                    libsBase
                ],
                loader: "babel-loader",
                options: { babelrc: true }
            },
            {
                test: `${libsBase}/jquery.custom.js`,
                use: [
                    {
                        loader: "expose-loader",
                        options: "jQuery"
                    },
                    {
                        loader: "expose-loader",
                        options: "$"
                    }
                ]
            },
            {
                test: require.resolve("underscore"),
                use: [
                    {
                        loader: "expose-loader",
                        options: "_"
                    },
                    {
                        loader: "expose-loader",
                        options: "underscore"
                    }
                ]
            },
            {
                test: /\.(png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot)(\?.*$|$)/,
                use: {
                    loader: "file-loader",
=======
        },
        module: {
            rules: [
                {
                    test: /\.vue$/,
                    loader: "vue-loader",
                },
                {
                         test: /\.mjs$/,
                         include: /node_modules/,
                         type: 'javascript/auto'
                },
                {
                    test: /\.js$/,
                    /*
                     * Babel transpile excludes for:
                     * - all node_modules except for handsontable, bootstrap-vue
                     * - statically included libs (like old jquery plugins, etc.)
                     */
                    exclude: [/(node_modules\/(?!(handsontable|bootstrap-vue)\/))/, libsBase],
                    loader: "babel-loader",
>>>>>>> refs/heads/release_21.01
                    options: {
<<<<<<< HEAD
                        outputPath: "assets",
                        publicPath: "../scripts/bundled/assets/"
                    }
                }
            },
            // Alternative to setting window.bundleEntries
            // Just import "extended" in any endpoint that needs
            // access to these globals, or even-better, make
            // more endpoints and skip the global altogether
            {
                test: /apps\/extended/,
                use: [
                    {
                        loader: "expose-loader",
                        options: "bundleEntries"
                    }
                ]
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: "css-loader",
                        options: { sourceMap: true }
                    }
                ]
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: "css-loader",
                        options: { sourceMap: true }
=======
                        cacheDirectory: true,
                        cacheCompression: false,
                        presets: [["@babel/preset-env", { modules: false }]],
                        plugins: ["transform-vue-template", "@babel/plugin-syntax-dynamic-import"],
                        ignore: ["i18n.js", "utils/localization.js", "nls/*"],
>>>>>>> refs/heads/release_21.01
                    },
<<<<<<< HEAD
                    {
                        loader: "sass-loader",
                        options: { sourceMap: true }
                    }
                ]
            }
        ]
    },
    node: {
        setImmediate: false
    },
    resolveLoader: {
        alias: {
            // since we support both requirejs i18n and non-requirejs and both use a similar syntax,
            // use an alias so we can just use one file
            i18n: "amdi18n-loader"
        }
    },
    plugins: [
        // this plugin allows using the following keys/globals in scripts (w/o req'ing them first)
        // and webpack will automagically require them in the bundle for you
        new webpack.ProvidePlugin({
            $: `${libsBase}/jquery.custom.js`,
            jQuery: `${libsBase}/jquery.custom.js`,
            _: "underscore",
            Backbone: "backbone",
            Galaxy: ["app", "monitor"]
        }),
        new VueLoaderPlugin(),
        new MiniCssExtractPlugin({
            filename: "[name].css",
            sourceMap: true
        }),
        // https://github.com/webpack-contrib/mini-css-extract-plugin/issues/141
        new OptimizeCssAssetsPlugin({
            cssProcessorOptions: {
                map: {
                    inline: false,
                    annotation: true
                }
            }
        }),
        new DuplicatePackageCheckerPlugin()
    ]
=======
                },
                {
                    test: `${libsBase}/jquery.custom.js`,
                    use: [
                        {
                            loader: "expose-loader",
                            options: {
                                exposes: ["jQuery", "$"],
                            },
                        },
                    ],
                },
                {
                    test: require.resolve("underscore"),
                    use: [
                        {
                            loader: "expose-loader",
                            options: {
                                exposes: ["underscore", "_"],
                            },
                        },
                    ],
                },
                {
                    test: /\.(png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot)(\?.*$|$)/,
                    use: {
                        loader: "file-loader",
                        options: {
                            outputPath: "assets",
                            publicPath: "../dist/assets/",
                        },
                    },
                },
                // Alternative to setting window.bundleEntries
                // Just import "bundleEntries" in any endpoint that needs
                // access to these globals, or even-better, make
                // more endpoints and skip the global altogether
                {
                    test: `${scriptsBase}/bundleEntries`,
                    use: [
                        {
                            loader: "expose-loader",
                            options: {
                                exposes: "bundleEntries",
                            },
                        },
                    ],
                },
                {
                    test: `${scriptsBase}/onload/loadConfig.js`,
                    use: [
                        {
                            loader: "expose-loader",
                            options: { exposes: "config" },
                        },
                    ],
                },
                {
                    test: /\.(sa|sc|c)ss$/,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader,
                            options: {
                                hmr: process.env.NODE_ENV === "development",
                            },
                        },
                        {
                            loader: "css-loader",
                            options: { sourceMap: true },
                        },
                        {
                            loader: "postcss-loader",
                            options: {
                                plugins: function () {
                                    return [require("autoprefixer")];
                                },
                            },
                        },
                        {
                            loader: "sass-loader",
                            options: {
                                sourceMap: true,
                                sassOptions: {
                                    includePaths: [
                                        path.join(styleBase, "scss"),
                                        path.resolve(__dirname, "./node_modules"),
                                    ],
                                },
                            },
                        },
                    ],
                },
                {
                    test: /\.(txt|tmpl)$/,
                    loader: "raw-loader",
                },
                {
                    test: /\.worker\.js$/,
                    use: { loader: 'worker-loader' },
                },
            ],
        },
        node: {
            setImmediate: false,
        },
        resolveLoader: {
            alias: {
                // since we support both requirejs i18n and non-requirejs and both use a similar syntax,
                // use an alias so we can just use one file
                i18n: "amdi18n-loader",
            },
        },
        plugins: [
            // this plugin allows using the following keys/globals in scripts (w/o req'ing them first)
            // and webpack will automagically require them in the bundle for you
            new webpack.ProvidePlugin({
                $: `${libsBase}/jquery.custom.js`,
                jQuery: `${libsBase}/jquery.custom.js`,
                _: "underscore",
                Backbone: "backbone",
                Galaxy: ["app", "monitor"],
            }),
            new VueLoaderPlugin(),
            new MiniCssExtractPlugin({
                filename: "[name].css",
                sourceMap: true,
            }),
            // https://github.com/webpack-contrib/mini-css-extract-plugin/issues/141
            new OptimizeCssAssetsPlugin({
                cssProcessorOptions: {
                    map: {
                        inline: false,
                        annotation: true,
                    },
                },
            }),
            new DuplicatePackageCheckerPlugin(),
        ],
        devServer: {
            hot: true,
        },
    };

    if (process.env.GXY_BUILD_SOURCEMAPS || process.env.NODE_ENV == "development") {
        buildconfig.devtool = "source-map";
    }

    return buildconfig;
>>>>>>> refs/heads/release_21.01
};
