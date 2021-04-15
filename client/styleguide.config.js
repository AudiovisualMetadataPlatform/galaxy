<<<<<<< HEAD
let path = require("path");
let glob = require("glob");
=======
const path = require("path");
const glob = require("glob");
const fs = require("fs");
const merge = require("webpack-merge");
const baseConfig = require("./webpack.config.js");
>>>>>>> refs/heads/release_21.01

const webpackConfig = baseConfig();

<<<<<<< HEAD
// We don't use webpack for our sass files in the main app, but use it here
// so we get rebuilds
webpackConfig.module.rules.push({
    test: /\.scss$/,
    use: [
        {
            loader: "style-loader"
        },
        {
            loader: "css-loader",
            options: {
                alias: {
                    "../images": path.resolve(__dirname, "../static/images"),
                    ".": path.resolve(__dirname, "../static/style/blue")
                }
            }
        },
        {
            loader: "sass-loader",
            options: {
                sourceMap: true
            }
        }
    ]
});

webpackConfig.module.rules.push({ test: /\.(png|jpg|gif|eot|ttf|woff|woff2|svg)$/, use: ["file-loader"] });
=======
const fileLoaderTest = /\.(png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot)(\?.*$|$)/;

const fileLoaderConfigRule = { rules: [{ test: fileLoaderTest, use: ["file-loader"] }] };
>>>>>>> refs/heads/release_21.01

<<<<<<< HEAD
sections = []
=======
webpackConfig.module = merge.smart(webpackConfig.module, fileLoaderConfigRule);
webpackConfig.output.publicPath = "";

webpackConfig.resolve.modules.push(path.join(__dirname, "src/style/scss"));
>>>>>>> refs/heads/release_21.01

<<<<<<< HEAD
glob("./galaxy/docs/galaxy-*.md", (err, files) => {
    files.forEach( file => {
        name = file.match( /galaxy-(\w+).md/ )[1]
        sections.push({ name: "Galaxy " + name, content: file })
    });
}),

sections.push( ...[
    {
        name: "Basic Bootstrap Styles",
        content: "./galaxy/docs/bootstrap.md"
    },
    // This will require additional configuration
    // {
    //     name: 'Components',
    //     components: './galaxy/scripts/components/*.vue'
    // }
])
=======
const galaxyStyleDocs = [];
glob.sync("./docs/galaxy-*.md").forEach((file) => {
    const name = file.match(/galaxy-(\w+).md/)[1];
    galaxyStyleDocs.push({ name: name, content: file });
});

const sections = [
    {
        name: "Galaxy styles",
        sections: galaxyStyleDocs,
    },
    {
        name: "Basic Bootstrap Styles",
        content: "./docs/bootstrap.md",
    },
    {
        name: "Components",
        // Components that are directories will get their own section
        sections: glob
            .sync("./src/components/*")
            .map((file) => {
                if (fs.lstatSync(file).isDirectory()) {
                    return {
                        name: path.basename(file),
                        components: file + "/**/*.vue",
                    };
                }
            })
            .filter((v) => v),
        // ...while top level components are handled here.
        components: "./src/components/*.vue",
    },
];
>>>>>>> refs/heads/release_21.01

module.exports = {
    webpackConfig,
    pagePerSection: true,
    sections,
    require: ["./src/style/scss/base.scss", "./src/polyfills.js", "./src/bundleEntries.js"],
    vuex: "./src/store/index.js",
};
