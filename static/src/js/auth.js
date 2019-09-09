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
        self.listenEditStaffEvent();

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


//添加员工
Auth.prototype.listenAddStaffEvent= function(){
    var addstaffbtn = $('#addstaff-btn');
    addstaffbtn.click(function (event) {
            event.preventDefault();
        var mobilephone = $('#MobilePhone1').val();
        var worknumber = $('#username').val();
        var email = $('#email').val();
        var username = $('#name').val();
        var department = $('#Department').val();
        var password1 = $('#password1').val();
        var password2 = $('#password2').val();
        var groups = '';//$('#groups:checked').val();
        var gs = $("input[name='groups']");
        for (var i=0;i<gs.length;i++){
            if(gs[i].checked==true){
                groups+=(gs[i].value+",");
            }
        }
        groups = groups.substring(0, groups.length - 1);
        console.log('用户组：',groups);
        xfzajax.post({
                'url':'/account/add_staff/',
                'data':{
                    'mobilephone':mobilephone,
                    'worknumber':worknumber,
                    'email':email,
                    'username':username,
                    'department':department,
                    'password1':password1,
                    'password2':password2,
                    'groups':groups,
                },
                'success':function (result) {
                    if (result['code']===200){
                        window.messageBox.showSuccess('添加成功！');
                         setTimeout(" location.href='/account/staffs/'","300")
                    } else {
                        console.log(result);
                        console.log(result['message'][0]);
                        if  (result['message'][0]){
                             console.log('走到1了！')
                            window.messageBox.showError(result['message']);

                        }else {
                            console.log('走到2了！')
                            for(var m in result['message']){
                                window.messageBox.showError(result['message'][m][0]);
                            }
                        }
                    }

                },
                'fail':function (error) {
                    window.messageBox.showError('服务器内部错误！');
                }
        });

    });


};

//编辑员工
Auth.prototype.listenEditStaffEvent= function(){
    var EditstaffBtn = $('#Editstaff-btn');
    EditstaffBtn.click(function (event) {
        event.preventDefault();
        var btn =$(this);
        var id = btn.attr('staff-id');
        console.log('用户ID：',id);
        var mobilephone = $('#MobilePhone1').val();
        //var MobilePhone = $("input[name='MobilePhone1']").val();
        var worknumber = $('#username').val();
        var email = $('#email').val();
        var username = $('#name').val();
        var department = $('#Department').val();
        var groups = '';//$('#groups:checked').val();
        var gs = $("input[name='groups']");
        for (var i=0;i<gs.length;i++){
            if(gs[i].checked==true){
                groups+=(gs[i].value+",");
            }
        }
        groups = groups.substring(0, groups.length - 1);//减少数组长度，去除多余的逗号
        console.log('获取到的信息',mobilephone,worknumber,email,username,department)
        //alert(groups);
        xfzajax.post({
                'url':'/account/Edit_Staff/',
                'data':{
                    'id':id,
                    'mobilephone':mobilephone,
                    'worknumber':worknumber,
                    'email':email,
                    'username':username,
                    'department':department,
                    'groups':groups,
                },
                'success':function (result) {
                    if (result['code']===200){
                        window.messageBox.showSuccess('编辑成功！');
                        //window.location.reload();
                        setTimeout(" location.href='/account/staffs/'","300")
                    } else {
                        console.log('返回Json信息：',result)
                        // for (var i in result['email']){
                        //     window.messageBox.showError(result['message']['email'][i]);
                        // }
                        // for (var i in result['department']){
                        //    window.messageBox.showError(result['message']['department'][i]);
                        // }
                        // for (var i in result['username']){
                        //    window.messageBox.showError(result['message']['username'][i]);
                        // }
                        // for (var i in result['mobilephone']){
                        //    window.messageBox.showError(result['message']['mobilephone'][i]);
                        // }
                        // for (var i in result['worknumber']){
                        //    window.messageBox.showError(result['message']['worknumber'][i]);
                        // }

                        console.log(result['message'][0]);
                        if  (result['message'][0]){
                             console.log('走到1了！')
                            window.messageBox.showError(result['message']);

                        }else {
                            console.log('走到2了！')
                            for(var m in result['message']){
                                window.messageBox.showError(result['message'][m][0]);
                            }
                        }


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
                    if(Cancellation==='True'){
                                var timerInterval;
                                Swal.fire({
                                    title: '员工启用成功',
                                    html: '我在<strong></strong>秒后自动关闭.',
                                    type: 'success',
                                    timer: 1000,
                                    onBeforeOpen: function(){
                                    Swal.showLoading();
                                    timerInterval = setInterval(function () {
                                        Swal.getContent().querySelector('strong').textContent = (Swal.getTimerLeft()/1000).toFixed(0)
                                    }, 100)
                                  },
                                  onClose: function(){
                                      clearInterval(timerInterval)
                                  }
                                }).then(function () {
                                    window.location.reload();
                                })

                        ////下面是未导入sweetalter2的提示
                        //window.messageBox.show("启用成功");
                        //setTimeout("window.location.reload()","300");
                        // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
                        //     window.location.reload();
                        // });
                    }else {
                                var timerInterval;
                                Swal.fire({
                                    title: '员工注销成功',
                                    html: '我在<strong></strong>秒后自动关闭.',
                                    type: 'success',
                                    timer: 1000,
                                    onBeforeOpen: function(){
                                    Swal.showLoading();
                                    timerInterval = setInterval(function () {
                                        Swal.getContent().querySelector('strong').textContent = (Swal.getTimerLeft()/1000).toFixed(0)
                                    }, 100)
                                  },
                                  onClose: function(){
                                      clearInterval(timerInterval)
                                  }
                                }).then(function () {
                                    window.location.reload();
                                })


                    ////下面是未导入sweetalter2的提示
                    //window.messageBox.show("注销成功");
                    //setTimeout("window.location.reload()","300");
                    // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
                    //     window.location.reload();
                    // });
                        }
                }
            },
             'fail':function (error) {
                    window.messageBox.showError('服务器内部错误！');
                }
        });


    });
};




$(function () {
        //让页面完成加载，然后才能找到需要的元素
        var auth = new Auth();
        auth.run();
});