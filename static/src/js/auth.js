// //点击弹出模态对话框
// $(function () {
//     //监视并找到页面中id等于btn的元素
//     $('#btn').click(function () {
//         //点击后展示页面中mask-wapper的盒子
//         $('.mask-wapper').show();
//     });
//     //监视并找到页面中close-btn的元素，点击后隐藏mask-wapper
//     $('.close-btn').click(function () {
//         //点击后隐藏页面中mask-wapper的盒子
//         $('.mask-wapper').hide();
//     })
// });

// $(function () {
//     $(".switch").click(function () {
//         var scollwapper =$('.scoll-wapper');
//         //获取scoll-wapper的位置属性left
//         var currentLeft =scollwapper.css("left");
//         //将获取到的位置XXpx属性转换成整形，用于判断大小
//         currentLeft=parseInt(currentLeft);
//         if (currentLeft<0){
//             //设置动画效果，并将left的值设置为0
//             scollwapper.animate({'left':'0'});
//         } else{
//             //设置动画效果，并将left的值设置为-400像素
//             scollwapper.animate({'left':'-400px'});
//         }
//
//     });
// });





//构造函数Auth
function Auth() {
        //函数当中的this代表的都是函数本身，所以定义一个self避免出现冲突
        var self =this;
        //将盒子mask-wapper定义成为一个属性
        self.maskwapper=$('.mask-wapper');
        self.scollwapper =$('.scoll-wapper');
}

//auth类的入口,运行
Auth.prototype.run=function () {
        var self=this;
        self.listenshowhideEvent();
        self.listenSwitchEvent();
        self.listenAddStaffEvent();
        self.listenCancellationEvent();

};

//用于显示事件
Auth.prototype.showEvent=function () {
        var self =this;
        self.maskwapper.show();
};

//用于隐藏事件
Auth.prototype.hideEvent=function () {
        var self =this;
        self.maskwapper.hide();
};

Auth.prototype.listenshowhideEvent=
    function(){
        var self = this;
        //将找到的元素定义
        var editorBtn =$('.editor-btn');
        var deleteBtn =$('.delete-btn');
        var closeBtn =$('.close-btn');
        //点击事件，点击就显示
        editorBtn.click(function () {
            self.showEvent();
    });
        deleteBtn.click(function () {
            self.showEvent();
        });
        closeBtn.click(function () {
            self.hideEvent();
        });

};

//监听事件，切换scollwapper
Auth.prototype.listenSwitchEvent=
    function(){
        var self =this;
        var swtichBtn=$(".switch");
        swtichBtn.click(function () {
        //获取scoll-wapper的位置属性left
        var currentLeft =self.scollwapper.css("left");
        //将获取到的位置XXpx属性转换成整形，用于判断大小
        currentLeft=parseInt(currentLeft);
        if (currentLeft<0){
            //设置动画效果，并将left的值设置为0
            self.scollwapper.animate({'left':'0'});
        } else{
            //设置动画效果，并将left的值设置为-400像素
            self.scollwapper.animate({'left':'-400px'});
        }

    });
};



Auth.prototype.listenAddStaffEvent= function(){
    var addstaffbtn = $('#addstaff-btn');
    addstaffbtn.click(function () {
        event.preventDefault();
        var MobilePhone = $('#MobilePhone1').val();
        var username = $('#username').val();
        var email = $('#email').val();
        var name = $('#name').val();
        var Department = $('#Department').val();
        var password1 = $('#password1').val();
        var password2 = $('#password2').val();
        var Permissions = $('#Permissions').find("option:selected").val();
alert(Permissions);
        var groups = $('#groups:checked').val();
        xfzajax.post({
                'url':'/account/add_staff/',
                'data':{
                    'MobilePhone':MobilePhone,
                    'username':username,
                    'email':email,
                    'name':name,
                    'Department':Department,
                    'password1':password1,
                    'password2':password2,
                    'Permissions':Permissions,
                    'groups':groups,
                },
                'success':function (result) {
                    if (result['code']===200){
                        window.messageBox.showSuccess('添加成功！');
                    } else {
                        window.messageBox.showError('服务有问题！');
                    }
                },
                'fail':function (error) {
                    window.messageBox.showError('服务器内部错误！');
                }
        });

    });


};


//监听注销事件
Auth.prototype.listenCancellationEvent = function () {
    var CancellationBtn = $('.Cancellation_btn');

    CancellationBtn.click(function () {
        var currentBtn =  $(this);
        var tr = currentBtn.parent().parent();
        var id =tr.attr('id');
        var Cancellation=tr.attr('Cancellation');
        xfzajax.post({
            'url': '/account/Cancellation/',
            'data': {
                'id': id,
                'Cancellation':Cancellation,
            },
             'success': function (result) {
                if(result['code'] === 200){
                     window.messageBox.show("操作成功");
                    setTimeout("window.location.reload()","300");
                    // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
                    //     window.location.reload();
                    // });
                }
            }
        });


    });
};




$(function () {
        //让页面完成加载，然后才能找到需要的元素
        var auth = new Auth();
        auth.run();
});