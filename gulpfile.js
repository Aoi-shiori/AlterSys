var  gulp = require("gulp");
var cssnano = require('gulp-cssnano');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var cache = require('gulp-cache')
var concat = require("gulp-concat")
var imagemin = require('gulp-imagemin')
var bs = require('browser-sync').create();
var sass =require('gulp-sass');




var path ={
    'html':"./templates/**/**",
    'css':"./static/src/css/",
    'js':"./static/src/js/",
    'images':"./static/src/images/",
    'css_dist':'./static/dist/css',
    'js_dist':'./static/dist/js',
    'images_dist':'./static/dist/images',
};

//定义一个额处理html的任务
gulp.task('html',function () {
    return  gulp.src(path.html+'*.html')
        .pipe(bs.stream())

})

// 定义一个处理css文件改动的任务
gulp.task("css",function () {
    return gulp.src(path.css+'*.scss')
        .pipe(sass.sync().on('error',sass.logError))
        .pipe(cssnano())
        //规则 suffix: 添加一个后缀名,prefix:添加一个前缀名
        .pipe(rename({"suffix":".min"}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
});

//定义一个处理JS的任务
gulp.task('js',function () {
    return gulp.src(path.js+"*.js")
        .pipe(uglify())
        .pipe(rename({'suffix':'.min'}))
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
});


//定义一个处理图片文件的任务
gulp.task('images',function () {
    return gulp.src(path.images+'*.*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist ))
        .pipe(bs.stream())
})


//定义一个监听文件修改的任务
gulp.task('watch',function () {
    gulp.watch(path.html+'*.html',gulp.series('html'));
    gulp.watch(path.css+"*.scss",gulp.series("css"));
    gulp.watch(path.js+"*.js",gulp.series("js"));
    gulp.watch(path.images+'*.*',gulp.series('images'));

});

//初始化browser-sync的任务
gulp.task("bs",function () {
    bs.init({
        'server':{baseDir:'./'}
    });
});

//创建一个默认的任务，通过gulp.parallel('bs','watch')并行运行
gulp.task('server',gulp.series(gulp.parallel('bs','watch')));
//创建一个默认的任务，监控文件改变并进行对应任务操作
gulp.task('defult',gulp.series(gulp.parallel('watch')));