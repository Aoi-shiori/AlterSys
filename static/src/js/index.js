//面向对象
//1、添加属性
//通过this关键字，绑定属性，并且制定他的值
//  function Banner() {
//     //这个里面写的代码
//      //相当于是python中的__init__
//     console.log('构造函数');
//      //this.person='zhiliao';
//  }
//  var banner = new Banner();
// //console.log(banner.person);
function Banner() {
    this.bannerGroup =$('#banner-group');
    this.listenbannerHover();
    this.index = 0;

}
Banner.prototype.listenbannerHover =function(){
        var self =this
        this.bannerGroup.hover(function () {
            //第一个函数是，把鼠标移动到banner上会执行的函数,清除计时器
            clearInterval(self.timer);
        },function () {
            //第二函数是，把鼠标从banner上一移走会执行的函数，再次运行轮播
            self.loop()
            });
};

Banner.prototype.loop =function(){
        var self=this;//需要定义，不然this代表的是当前函数
        var bannerUr =$("#banner-ur");
    //bannerUr.css({'left':-798});//直接更改样式
    this.timer=setInterval(function () {
        if(self.index>=3){
            self.index=0;
        }else {
             self.index++;
        }
          bannerUr.animate({'left':-798*self.index},
              500);//动画效果，延时500毫秒
    },2000);//计时器，2000毫秒执行一次前面的功能
};

Banner.prototype.run = function () {
    this.loop();
};
$(function () {
    var banner =new Banner();
    banner.run()
});