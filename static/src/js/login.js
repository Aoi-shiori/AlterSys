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
        event.preventDefault();//去除按钮本身的事件
        var mobilephone=mobilephones.val();
        var password =passwords.val();
        if (rember.checked){
            var remember =true;
        }else {


            var remember =false;
        };

        console.log('用户名:'+mobilephone,'密码:'+password,'记住我:'+remember);
        xfzajax.post({
            'url':'/Dict/Edit_DB_Dict/',
            'data':{
                'MobilePhone':mobilephone,
                'password':password,
                'remember':remember,
            },
            'success':function (result) {
                if(result['code'] === 200){
                    window.messageBox.showSuccess('登录成功！');
                }else {
                    window.messageBox.showError(result['message']);
                }
            },
        });

    });

};


$(function () {
    var Login =new login();
    Login.run();
});