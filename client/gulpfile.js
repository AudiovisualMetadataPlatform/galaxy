<<<<<<< HEAD
var path = require("path");
var fs = require("fs");
var del = require("del");
var _ = require("underscore");
=======
const path = require("path");
const fs = require("fs");
const del = require("del");
const { src, dest, series, parallel, watch } = require("gulp");
const child_process = require("child_process");
const glob = require("glob");

/*
 * We'll want a flexible glob down the road, but for now there are no
 * un-built visualizations in the repository; for performance and
 * simplicity just add them one at a time until we upgrade older viz's.
 */
const PLUGIN_BUILD_IDS = [
    "annotate_image",
    "chiraviz",
    "editor",
    "heatmap/heatmap_default",
    "hyphyvision",
    "media_player",
    "mvpapp",
    "ngl",
    "openlayers",
    "openseadragon",
    "pv",
    "nora",
];
>>>>>>> refs/heads/release_21.01

var gulp = require("gulp");
var uglify = require("gulp-uglify");
var babel = require("gulp-babel");

var paths = {
    node_modules: "./node_modules",
<<<<<<< HEAD
    scripts: [
        "galaxy/scripts/**/*.js",
        "!galaxy/scripts/qunit/**/*",
        "!galaxy/scripts/apps/**/*",
        "!galaxy/scripts/libs/**/*"
=======
    plugin_dirs: [
        "../config/plugins/{visualizations,interactive_environments}/*/static/**/*",
        "../config/plugins/{visualizations,interactive_environments}/*/*/static/**/*",
>>>>>>> refs/heads/release_21.01
    ],
<<<<<<< HEAD
    plugin_dirs: ["../config/plugins/**/static/**/*", "!../config/plugins/**/node_modules{,/**}"],
=======
    plugin_build_modules: [`../config/plugins/visualizations/{${PLUGIN_BUILD_IDS.join(",")}}/package.json`],
>>>>>>> refs/heads/release_21.01
    lib_locs: {
        // This is a stepping stone towards having all this staged
        // automatically.  Eventually, this dictionary and staging step will
        // not be necessary.
        backbone: ["backbone.js", "backbone.js"],
        "bootstrap-tour": ["build/js/bootstrap-tour.js", "bootstrap-tour.js"],
<<<<<<< HEAD
        d3: ["d3.js", "d3.js"],
        "bibtex-parse-js": ["bibtexParse.js", "bibtexParse.js"],
=======
>>>>>>> refs/heads/release_21.01
        jquery: ["dist/jquery.js", "jquery/jquery.js"],
        "jquery.complexify": ["jquery.complexify.js", "jquery/jquery.complexify.js"],
        "jquery.cookie": ["jquery.cookie.js", "jquery/jquery.cookie.js"],
        "jquery-migrate": ["dist/jquery-migrate.js", "jquery/jquery.migrate.js"],
        "jquery-mousewheel": ["jquery.mousewheel.js", "jquery/jquery.mousewheel.js"],
        requirejs: ["require.js", "require.js"],
        underscore: ["underscore.js", "underscore.js"],
    },
    libs: ["src/libs/**/*.js"],
};

<<<<<<< HEAD
gulp.task("stage-libs", function(callback) {
    _.each(_.keys(paths.lib_locs), function(lib) {
=======
function stageLibs(callback) {
    Object.keys(paths.lib_locs).forEach((lib) => {
>>>>>>> refs/heads/release_21.01
        var p1 = path.resolve(path.join(paths.node_modules, lib, paths.lib_locs[lib][0]));
        var p2 = path.resolve(path.join("src", "libs", paths.lib_locs[lib][1]));
        if (fs.existsSync(p1)) {
            del.sync(p2);
            fs.createReadStream(p1).pipe(fs.createWriteStream(p2));
        } else {
            callback(
                p1 +
                    " does not exist, yet it is a required library.  This is an error.  Check that the package in question exists in node_modules."
            );
        }
    });
});

gulp.task("fonts", function() {
    return gulp
        .src(path.resolve(path.join(paths.node_modules, "font-awesome/fonts/**/*")))
        .pipe(gulp.dest("../static/images/fonts"));
});

// TODO: Remove script and lib tasks (for 19.05) once we are sure there are no
// external accessors (via require or explicit inclusion in templates)
gulp.task("scripts", function() {
    return gulp
        .src(paths.scripts)
        .pipe(
            babel({
                plugins: ["transform-es2015-modules-amd"]
            })
        )
        .pipe(uglify())
        .pipe(gulp.dest("../static/scripts/"));
});

<<<<<<< HEAD
gulp.task("libs", function() {
    return gulp
        .src(paths.libs)
        .pipe(uglify())
        .pipe(gulp.dest("../static/scripts/libs/"));
});
=======
function buildPlugins(callback) {
    /*
     * Walk plugin_build_modules glob and attempt to build modules.
     * */
    paths.plugin_build_modules.map((build_module) => {
        glob(build_module, {}, (er, files) => {
            files.map((file) => {
                let skip_build = false;
                const f = path.join(process.cwd(), file).slice(0, -12);
                const plugin_name = path.dirname(file).split(path.sep).pop();
                const hash_file_path = path.join(f, "static", "plugin_build_hash.txt");

                if (fs.existsSync(hash_file_path)) {
                    skip_build =
                        child_process.spawnSync("git", ["diff", "--quiet", `$(cat ${hash_file_path})`, "--", f], {
                            stdio: "inherit",
                            shell: true,
                        }).status === 0;
                } else {
                    console.log(`No build hashfile detected for ${plugin_name}, generating now.`);
                }

                if (skip_build) {
                    console.log(`No changes detected for ${plugin_name}`);
                } else {
                    console.log(`Installing Dependencies for ${plugin_name}`);
                    child_process.spawnSync(
                        "yarn",
                        ["install", "--production=false", "--network-timeout=300000", "--check-files"],
                        {
                            cwd: f,
                            stdio: "inherit",
                            shell: true,
                        }
                    );
                    console.log(`Building ${plugin_name}`);
                    child_process.spawnSync("yarn", ["build"], { cwd: f, stdio: "inherit", shell: true });
                    child_process.exec(`(git rev-parse HEAD 2>/dev/null || echo \`\`) > ${hash_file_path}`);
                }
            });
        });
    });
    return callback();
}

function cleanPlugins() {
    return del(["../static/plugins/{visualizations,interactive_environments}/*"], { force: true });
}
>>>>>>> refs/heads/release_21.01

<<<<<<< HEAD
gulp.task("plugins", function() {
    return gulp.src(paths.plugin_dirs).pipe(gulp.dest("../static/plugins/"));
});

gulp.task("clean", function() {
    //Wipe out all scripts that aren't handled by webpack
    return del(["../static/scripts/**/*.js", "!../static/scripts/bundled/**.*.js"], { force: true });
});

gulp.task("staging", ["stage-libs", "fonts"]);

gulp.task("default", ["libs", "scripts"]);
=======
const client = parallel(fonts, stageLibs);
const plugins = series(buildPlugins, cleanPlugins, stagePlugins);

function watchPlugins() {
    const BUILD_PLUGIN_WATCH_GLOB = [`../config/plugins/visualizations/{${PLUGIN_BUILD_IDS.join(",")}}/**/*`];
    watch(BUILD_PLUGIN_WATCH_GLOB, { queue: false }, plugins);
}

module.exports.client = client;
module.exports.plugins = plugins;
module.exports.watchPlugins = watchPlugins;
module.exports.default = parallel(client, plugins);
>>>>>>> refs/heads/release_21.01
