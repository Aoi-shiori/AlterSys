
function AltTypeDict() {

}

AltTypeDict.prototype.run=function () {
      var self =this;
      self.listenAddAltTypeEvent();

};

AltTypeDict.prototype.listenAddAltTypeEvent=function () {
    var AddBtn= $('.Add_Btn');
    AddBtn.click(function () {
            swal.fire({
              title: '请输入分类名称',
              input: 'text',
              showCancelButton: true,
              confirmButtonText: '提交',
              showLoaderOnConfirm: true,
              inputValidator: function(value) {
                return new Promise(function(resolve, reject) {
                  setTimeout(function() {
                    if (value) {
                        alert(value );
                          xfzajax.post({
                            'url': '/Dict/Add_DB_Dict/',
                            'data': {
                                'Database': value
                            },
                            'success': function (result) {
                                if(result['code'] === 200){
                                    console.log(result);
                                    window.location.reload();
                                }else{
                                    xfzalert.close();
                                }
                            }
                          });
                    } else {
                      reject('你需要输入内容')
                    }
                  }, 2000);
                });
              },
              allowOutsideClick: false
            })
    })
};





$(function () {
    var AltType_Dict = new AltTypeDict();
    AltType_Dict.run();
});