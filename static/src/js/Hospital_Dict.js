
function HospitalDict() {

}

HospitalDict.prototype.run=function () {
      var self =this;
      self.listenAddAltTypeEvent();
      self.listenEDITAltTypeEvent();
      self.listenDELAltTypeEvent();

};

//添加医院名称分类
HospitalDict.prototype.listenAddAltTypeEvent=function () {
    var AddBtn= $('.Add_Btn');
    AddBtn.click(function () {
        event.preventDefault();//去除按钮本身的事件
            swal.fire({
              title: '请输入分类名称',
              input: 'text',
              showCancelButton: true,
              confirmButtonText: '提交',
              cancelButtonText:'取消',
              showLoaderOnConfirm: true,
              inputPlaceholder:"请输入医院名称",
              inputValidator: function(value) {
                   Swal.showLoading();
                return new Promise(function(reject,resolve) {
                  if (value)
                    setTimeout(function() {
                        //alert(value );
                        var timerInterval;
                          xfzajax.post({
                            'url': '/Dict/Add_hospital_Dict/',
                            'data': {
                                'hospital': value
                            },
                            'success': function (result) {
                                if(result['code'] === 200){
                                    console.log(result);
                                    swal.fire({
                                        type: 'success',
                                        title: 'Ajax请求完成！',
                                        html: ('提交的医院名称是：' + value+'<br><br/>')
                                            +'我在<strong></strong>秒后自动关闭.',
                                        timer:2000,
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


//编辑医院分类
HospitalDict.prototype.listenEDITAltTypeEvent=function () {
    var EdiBtn= $('.Edi_btn');
    EdiBtn.click(function (event) {
        event.preventDefault();//去除按钮本身的事件
        var current =$(this);
        var tr =current.parent().parent();
        var pk =tr.attr('id');
        var hospital=tr.attr('Hospitalname');
            swal.fire({
              title: '修改分类名称',
              input: 'text',
              showCancelButton: true,
              cancelButtonText:'取消',
              confirmButtonText: '提交',
              showLoaderOnConfirm: true,
              inputPlaceholder:"请输入分类名称",
              inputValue:hospital,
              inputValidator: function(value) {
                  Swal.showLoading();
                return new Promise(function(reject,resolve) {
                  if (value)
                    setTimeout(function() {
                        //alert(value );
                          xfzajax.post({
                            'url': '/Dict/Edit_hospital_Dict/',
                            'data': {
                                'pk':pk,
                                'Hospital': value
                            },
                            'success': function (result) {
                                if(result['code'] === 200){
                                    console.log(result);
                                    swal.fire({
                                        type: 'success',
                                        title: 'Ajax请求完成！',
                                        html: ('提交的分类名称是：' + value+'! <br/><br/>')
                                            +'我在<strong></strong>秒后自动关闭.',
                                        timer:2000,
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

                                }else{
                                    console.log(result);
                                    Swal.close();
                                }
                            }
                          });
                    }, 1000);
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

HospitalDict.prototype.listenDELAltTypeEvent=function(){
        var DelBTn = $('.Del_btn');
        DelBTn.click(function () {
            event.preventDefault();//去除按钮本身的事件
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
                        'url': '/Dict/Del_hospital_Dict/',
                        'data': {
                            'pk': pk,

                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                var timerInterval;
                                Swal.fire({
                                    title: '删除分类数据成功',
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


                            }
                        },

                    });

                } else if (result.dismiss === Swal.DismissReason.cancel) {
                    // Swal.fire(
                    //     '已取消！',
                    //     '你的数据是安全的:)',
                    //     'error'
                    // )
                    var timerInterval;
                    Swal.fire({
                      type: 'info',
                      title: '取消成功,你的数据是安全的',
                      html: '我在<strong></strong>秒后自动关闭.',
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
                    }).then( function(result) {
                      if (
                        // Read more about handling dismissals
                        result.dismiss === Swal.DismissReason.timer
                      ) {
                        console.log('倒计时结束窗口关闭')
                      }
                    });
                }
            })
        })
};



$(function () {
    var Hospital_Dict = new HospitalDict();
    Hospital_Dict.run();
});


