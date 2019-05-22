//点击弹出模态对话框
$(function () {
    //监视并找到页面中id等于btn的元素
    $('#btn').click(function () {
        //点击后展示页面中mask-wapper的盒子
        $('.mask-wapper').show();
    });
    //监视并找到页面中close-btn的元素，点击后隐藏mask-wapper
    $('.close-btn').click(function () {
        //点击后隐藏页面中mask-wapper的盒子
        $('.mask-wapper').hide();
    })
});

$(function () {
    $(".switch").click(function () {
        var scollwapper =$('.scoll-wapper');
        //获取scoll-wapper的位置属性left
        var currentLeft =scollwapper.css("left");
        //将获取到的位置XXpx属性转换成整形，用于判断大小
        currentLeft=parseInt(currentLeft);
        if (currentLeft<0){
            //
            scollwapper.animate({'left':'0'});}

        else{
            scollwapper.animate({'left':'-400px'})}

    })
})