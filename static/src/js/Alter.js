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
        // self.listenSwitchEvent();
        self.listenSigninEvent();
        self.listenreviseEvent();
        self.listenDeleteEvent();

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
        var closeBtn =$('.close-btn');
        var reviseBtn =$('.revise-btn');
        var cancleBtn = $('.cancle-btn');
        //点击事件，点击就显示
        editorBtn.click(function () {
            self.showEvent();
            //不设置设置动画效果，直接将left的值设置为-400像素,用于显示编辑页面
            self.scollwapper.css({'left':'-400px'});

            var currentbtn =$(this);
            //获取到编辑按钮标签的父级元素tr标签
            tr=currentbtn.parent().parent();
            //通过找到到tr标签，通过attr获取元素
            //绑定id到tr标签，然后获取var  AlterID =tr.attr('AlterID');
            var  AlterID =tr.attr('AlterID');
            var  AlterType =tr.attr('AlterType');
            var  AssociatedNumber =tr.attr('AssociatedNumber');
            var  Datebase =tr.attr('Datebase');
            var  AlterContent =tr.attr('AlterContent');
            var  Informant =tr.attr('Informant');
            var  FillTime =tr.attr('FillTime');
            // var AlterType =tr.td($('.AlterType-td'));
            // var AssociatedNumber=tr.td($('.AssociatedNumber-td'));
            // var Datebase=tr.td($('.Datebase-td'));
            // var AlterContent=tr.td($('.AlterContent-td'));
            // var Informant=tr.td($('.Informant-td'));
            // var FillTime=tr.td($('.FillTime-td'));

            $("#ID-AlterID").val(AlterID);
            $("#ID-AlterType").val(AlterType);
            $("#ID-AssociatedNumber").val(AssociatedNumber);
            $("#ID-Datebase").val(Datebase);
            $("#ID-AlterContent").val(AlterContent);
            $("#ID-Informant").val(Informant);
            $("#ID-FillTime").val(FillTime);




        });

        addBtn.click(function () {
             self.showEvent();
             self.scollwapper.css({'left':'0'});
        });
        closeBtn.click(function () {
            self.hideEvent();
        });
        reviseBtn.click(function () {

        })
        cancleBtn.click(function () {
            self.hideEvent()
        })


};
//
// //监听事件，切换scollwapper
// Auth.prototype.listenSwitchEvent=
//     function(){
//         var self =this;
//         var swtichBtn=$(".switch");
//         swtichBtn.click(function () {
//         //获取scoll-wapper的位置属性left
//         var currentLeft =self.scollwapper.css("left");
//         //将获取到的位置XXpx属性转换成整形，用于判断大小
//         currentLeft=parseInt(currentLeft);
//         if (currentLeft<0){
//             //设置动画效果，并将left的值设置为0
//             self.scollwapper.animate({'left':'0'});
//         } else{
//             //设置动画效果，并将left的值设置为-400像素
//             self.scollwapper.animate({'left':'-400px'});
//         }
//
//     });
// };

//监听修改事件
Auth.prototype.listenreviseEvent=function(){
        var signupGroup = $('.signup-group');

        var NEWAlterIDinput = signupGroup.find("input[name='AlterID']");
        var NEWAlterTypeInput = signupGroup.find("input[name='AlterType']");
        var NEWAssociatedNumberInput = signupGroup.find("input[name='AssociatedNumber']");
        var NEWDatebaseInput = signupGroup.find("input[name='Datebase']");
        var NEWAlterContentInput = signupGroup.find("input[name='AlterContent']");
        var NEWInformantInput = signupGroup.find("input[name='Informant']");
        var reviseBtn = signupGroup.find(".revise-btn");
    reviseBtn.click(function () {
        var AlterID =NEWAlterIDinput.val();
        var AlterType = NEWAlterTypeInput.val();
        var AssociatedNumber = NEWAssociatedNumberInput.val();
        var Datebase = NEWDatebaseInput.val();
        var AlterContent = NEWAlterContentInput.val();
        var Informant = NEWInformantInput.val();

         xfzajax.post({
            'url': '/alter/edit_Alter_manager/',
            'data': {
                'AlterID':AlterID,
                'AlterType': AlterType,
                'AssociatedNumber': AssociatedNumber,
                'Datebase': Datebase,
                'AlterContent': AlterContent,
                'Informant': Informant,
            },
            'success': function (result) {
                if(result["code"] === 200){
                    window.messageBox.show("修改成功");
                    setTimeout("window.location.reload()","500");

                    // xfzalert.alertSuccess("恭喜！新闻发表成功!",function () {
                    //     window.location.reload();
                    // });
                }
            }
        });
    });
};


//监听添加事件
Auth.prototype.listenSigninEvent = function () {
    var self = this;
    var signinGroup = $('.signin-group');
    var AlterTypepInput = signinGroup.find("input[name='AlterType']");
    var AssociatedNumberInput = signinGroup.find("input[name='AssociatedNumber']");
    var DatebaseInput = signinGroup.find("input[name='Datebase']");
    var AlterContentInput = signinGroup.find("input[name='AlterContent']");
    var InformantInput = signinGroup.find("input[name='Informant']");
    var submitBtn = signinGroup.find(".submit-btn");
    submitBtn.click(function () {
        var AlterType = AlterTypepInput.val();
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
                if(result['code'] === 200){
                     window.messageBox.show("添加成功");
                    setTimeout("window.location.reload()","300");
                    // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
                    //     window.location.reload();
                    // });
                }
            }
        });
    });
};


//监听删除事件
Auth.prototype.listenDeleteEvent = function () {
    var DeleteBTN = $('.delete-btn');

    DeleteBTN.click(function () {
        var currentBtn =  $(this);
        var tr = currentBtn.parent().parent();
        var AlterID =tr.attr('AlterID');
        xfzajax.post({
            'url': '/alter/delete_Alter_manager/',
            'data': {
                'AlterID': AlterID,
            },
             'success': function (result) {
                if(result['code'] === 200){
                     window.messageBox.show("删除成功");
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