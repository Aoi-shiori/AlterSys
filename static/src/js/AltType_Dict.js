
function AltTypeDict() {

}

AltTypeDict.prototype.run=function () {
      var self =this;
      self.listenAddAltTypeEvent();
      self.listenEDITAltTypeEvent();
      self.listenDELAltTypeEvent();

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
              inputPlaceholder:"请输入分类名称",
              inputValidator: function(value) {
                return new Promise(function(reject,resolve) {
                  if (value)
                    setTimeout(function() {
                        //alert(value );
                          xfzajax.post({
                            'url': '/Dict/Add_DB_Dict/',
                            'data': {
                                'Database': value
                            },
                            'success': function (result) {
                                if(result['code'] === 200){
                                    console.log(result);
                                    swal.fire({
                                        type: 'success',
                                        title: 'Ajax请求完成！',
                                        html: '提交的分类名称是：' + value
                                      }).then(function () {
                                        window.location.reload();
                                    })

                                }else{
                                    console.log(result);
                                    Swal.close();
                                }
                            }
                          });
                    }, 2000);
                  else{
                     reject('你需要输入一些东西')
                  }
                });
              },
              allowOutsideClick: false
            }).then(function() {

                  swal.fire({
                    type: 'info',
                    title: 'Ajax请求取消！',
                    html: '取消成功'
                  });
            })
    })
};



AltTypeDict.prototype.listenEDITAltTypeEvent=function () {
    var EdiBtn= $('.Edi_btn');
    EdiBtn.click(function () {
        var current =$(this);
        var tr =current.parent().parent();
        var pk =tr.attr('id');
        var Database=tr.attr('DBname');
        event.preventDefault();
            swal.fire({
              title: '修改分类名称',
              input: 'text',
              showCancelButton: true,
              confirmButtonText: '提交',
              showLoaderOnConfirm: true,
              inputPlaceholder:"请输入分类名称",
              inputValue:Database,
              inputValidator: function(value) {
                return new Promise(function(reject,resolve) {
                  if (value)
                    setTimeout(function() {
                        //alert(value );
                          xfzajax.post({
                            'url': '/Dict/Edit_DB_Dict/',
                            'data': {
                                'pk':pk,
                                'Database': value
                            },
                            'success': function (result) {
                                if(result['code'] === 200){
                                    console.log(result);
                                    swal.fire({
                                        type: 'success',
                                        title: 'Ajax请求完成！',
                                        html: '提交的分类名称是：' + value
                                      }).then(function () {
                                        window.location.reload();
                                    })

                                }else{
                                    console.log(result);
                                    Swal.close();
                                }
                            }
                          });
                    }, 2000);
                  else{
                     reject('你需要输入一些东西')
                  }
                });
              },
              allowOutsideClick: false
            }).then(function() {

                  swal.fire({
                    type: 'info',
                    title: 'Ajax请求取消！',
                    html: '取消成功',
                    timer:1000,
                  });
            })
    })
};

AltTypeDict.prototype.listenDELAltTypeEvent=function(){
        var DelBTn = $('.Del_btn');
        DelBTn.click(function () {
            var current = $(this);
            var tr = current.parent().parent();
            var pk = tr.attr('id');
            swal.fire({
                type: 'question',
                title: '确认删除分类吗？！',
                showConfirmButton: true,
                //timer: 1500,
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                confirmButtonClass: 'btn btn-success',
                cancelButtonClass: 'btn btn-danger',
                buttonsStyling: false
            }).then(function (result) {
                if (result.value) {
                    xfzajax.post({
                        'url': '/Dict/Del_DB_Dict/',
                        'data': {
                            'pk': pk,

                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                Swal.fire({
                                    title: '删除分类数据',
                                    text: '删除成功',
                                    type: 'success',
                                    timer: 1000
                                }).then(function () {
                                    window.location.reload();
                                })


                            }
                        },

                    });

                } else if (result.dismiss === Swal.DismissReason.cancel) {
                    Swal.fire(
                        '已取消！',
                        '你的数据是安全的:)',
                        'error'
                    )
                }
            })
        })
};



$(function () {
    var AltType_Dict = new AltTypeDict();
    AltType_Dict.run();
});