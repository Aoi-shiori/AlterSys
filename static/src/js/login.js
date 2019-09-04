function login() {

}

login.prototype.run=function () {
    var self =this;
    self.listenloginEvent();

};



login.prototype.listenloginEvent=function(){
    var loginbtn =$('#loginbtn');
    var mobilephones =$('#logintel');
    var passwords =$('#loginpwd');

    //var remembers=$('#rember');
    loginbtn.click(function (event) {
        event.preventDefault();//去除原按钮本身的事件
        var mobilephone=mobilephones.val();
        var password =passwords.val();
        if (rember.checked){
            var remember =1;
        }else {
            var remember =0;
        };

        // console.log('用户名:'+mobilephone,'密码:'+password,'记住我:'+remember);
        console.log('登陆用户:'+mobilephone,'记住我:'+remember);
        //console.log($.cookie("csrftoken"));
        $.ajax({
            'headers':{"X-CSRFToken":$.cookie("csrftoken")},
            'url':'/account/login/',
            'type':'POST',
            'data':{
                'MobilePhone':mobilephone,
                'password':password,
                'remember':remember
            },
            'success':function (result) {
                if(result['code'] === 200){
                    console.log(result)
                    //window.messageBox.showSuccess(result['message']);
                    location.href='/alter/index/'
                } else {
                    console.log(result)
                    if (result['message']['MobilePhone'])
                         window.messageBox.showError(result['message']['MobilePhone']);
                    else if  (result['message']['password'])
                         window.messageBox.showError(result['message']['password']);
                    else
                        window.messageBox.showError(result['message']);
                };
            }
        });

    });

};


$(function () {
    var Login =new login();
    Login.run();
});