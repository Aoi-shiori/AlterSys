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
        self.listenSigninEvent();

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
        var addBtn=$('.add-btn');
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
        addBtn.click(function () {
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


Auth.prototype.listenSigninEvent = function () {
    var self = this;
    var signinGroup = $('.signin-group');
    var AlterTypephoneInput = signinGroup.find("input[name='AlterType']");
    var AssociatedNumberInput = signinGroup.find("input[name='AssociatedNumber']");
    var DatebaseInput = signinGroup.find("input[name='Datebase']");
    var AlterContentInput = signinGroup.find("input[name='AlterContent']");
    var InformantInput = signinGroup.find("input[name='Informant']");
    var submitBtn = signinGroup.find(".submit-btn");
    submitBtn.click(function () {
        var AlterType = AlterTypephoneInput.val();
        var AssociatedNumber = AssociatedNumberInput.val();
        var Datebase = DatebaseInput.val();
        var AlterContent = AlterContentInput.val();
        var Informant = InformantInput.val();


         xfzajax.post({
            'url': '/alter/add_Alter_manager/',
            'data': {
                'AlterType': AlterType,
                'AssociatedNumber': AssociatedNumber,
                'Datebase': Datebase,
                'AlterContent': AlterContent,
                'Informant': Informant,
            },
            'success': function (result) {
                if(result['code'] == 200){
                    self.hideEvent();
                    window.location.reload();
                }else{
                    var messageObject = result['message'];
                    if(typeof messageObject == 'string' || messageObject.constructor == String){
                        window.messageBox.show(messageObject);
                    }else{
                        // {"password":['密码最大长度不能超过20为！','xxx'],"telephone":['xx','x']}
                        for(var key in messageObject){
                            var messages = messageObject[key];
                            var message = messages[0];
                            window.messageBox.show(message);
                        }
                    }
                }
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
};





$(function () {
        //让页面完成加载，然后才能找到需要的元素
        var auth = new Auth();
        auth.run();
});