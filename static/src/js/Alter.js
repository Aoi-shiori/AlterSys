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



//构造函数Alter
function Alter() {
        //函数当中的this代表的都是函数本身，所以定义一个self避免出现冲突
        var self =this;
        //将盒子mask-wapper定义成为一个属性
        self.maskwapper=$('.mask-wapper-add');
        self.scollwapper =$('.scoll-wapper');
        //获得Renview的盒子
        self.maskwapper_Review=$('.mask-wapper-Review');

}

//Alter类的入口,运行
Alter.prototype.run=function () {
        var self=this;
        self.listenshowhideEvent();
        // self.listenSwitchEvent();
        self.listenSigninEvent();
        self.listenreviseEvent();
        self.listenDeleteEvent();
        self.listenDataPiker();
        self.listenselectnow();
        self.listenReviewEvent();
        self.listenReviewSbumitEvent();
        self.listenReviewtestEvent();

};

//用于显示事件
Alter.prototype.showEvent=function () {
        var self =this;
        self.maskwapper.show();
};

Alter.prototype.showReviewEvent=function(){
        var self=this;
        self.maskwapper_Review.show();
};

//用于隐藏事件
Alter.prototype.hideEvent=function () {
        var self =this;
        self.maskwapper.hide();
        self.maskwapper_Review.hide();
};



Alter.prototype.listenshowhideEvent=
    function(){
        var self = this;
        //将找到的元素定义
        var addBtn=$('.add-btn');
        var editorBtn =$('.editor-btn');
        var closeBtn =$('.close-btn');
        var reviseBtn =$('.revise-btn');
        var cancleBtn = $('.cancle-btn');
        var Reviewbtn=$('.Review-btn');
        //点击事件，点击就显示
        editorBtn.click(function () {
            self.showEvent();
            //不设置设置动画效果，直接将left的值设置为-400像素,用于显示编辑页面
            self.scollwapper.css({'left':'-500px'});

            var currentbtn =$(this);
            //获取到编辑按钮标签的父级元素tr标签
            tr=currentbtn.parent().parent();
            //通过找到到tr标签，通过attr获取元素
            //绑定id到tr标签，然后获取var  id =tr.attr('id');
            var  id =tr.attr('id');
            var  AlterType =tr.attr('AlterType');
            var  AssociatedNumber =tr.attr('AssociatedNumber');
            var  Database =tr.attr('Database');
            var  AlterContent =tr.attr('AlterContent');
            var  Informant =tr.attr('Informant');
            var  FillTime =tr.attr('FillTime');
            // var AlterType =tr.td($('.AlterType-td'));
            // var AssociatedNumber=tr.td($('.AssociatedNumber-td'));
            // var Datebase=tr.td($('.Datebase-td'));
            // var AlterContent=tr.td($('.AlterContent-td'));
            // var Informant=tr.td($('.Informant-td'));
            // var FillTime=tr.td($('.FillTime-td'));

            $("#ID-id").val(id);
            $("#ID-AlterType").val(AlterType);
            $("#ID-AssociatedNumber").val(AssociatedNumber);
            $("#ID-Database").val(Database);
            $("#ID-AlterContent").val(AlterContent);
            $("#ID-Informant").val(Informant);
            $("#ID-FillTime").val(FillTime);

            console.log("ID："+id);
            console.log("提交时间："+FillTime);
            console.log("提交人："+Informant);
            console.log("关联编号："+AssociatedNumber);
            console.log("变更内容："+AlterContent);





        });

        addBtn.click(function () {
             event.preventDefault();
             self.showEvent();
             self.scollwapper.css({'left':'0'});
        });
        closeBtn.click(function () {
            self.hideEvent();
        });
        reviseBtn.click(function () {

        });
        cancleBtn.click(function () {
            self.hideEvent();
        });
        // Reviewbtn.click(function () {
        //     //显示审核页面
        //     self.showReviewEvent();
        // });


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
Alter.prototype.listenreviseEvent=function(){
        var revisegroup = $('.revise-group');

        var NEWidinput = revisegroup.find("input[name='AlterID']");
        var NEWAlterTypeInput = revisegroup.find("select[name='AltType']");
        var NEWAssociatedNumberInput = revisegroup.find("input[name='AssociatedNumber']");
        var NEWDatabaseInput = revisegroup.find("select[name='Database']");
        var NEWAlterContentInput = revisegroup.find("textarea[name='AlterContent']");
        var reviseBtn = revisegroup.find(".revise-btn");
    reviseBtn.click(function () {
        var id =NEWidinput.val();
        var AltType = NEWAlterTypeInput.val();
        var AssociatedNumber = NEWAssociatedNumberInput.val();
        var Database = NEWDatabaseInput.val();
        var AlterContent = NEWAlterContentInput.val();

        Swal.fire({
            //position: 'top-end',
            type: 'question',
            title: '确认修改吗？',
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
            if(result.value){
                Swal.fire({
                    tiele:'已提交！',
                    text:'提交成功。',
                    type:'success',
                    timer: 1000
                    }).then(function () {
                    xfzajax.post({
                        'url': '/alter/edit_Alter_manager/',
                        'data': {
                            'id':id,
                            'AltType': AltType,
                            'AssociatedNumber': AssociatedNumber,
                            'Database': Database,
                            'AlterContent': AlterContent,

                        },
                        'success':function (result) {
                            if (result['code']===200){
                                Swal.fire({
                                    title:'已修改',
                                    text:'修改成功',
                                    type:'success',
                                    timer:1000
                                }).then(function () {
                                     window.location.reload();
                                })


                            }
                        },

                    });
                })
            }else if (result.dismiss === Swal.DismissReason.cancel) {
                    Swal.fire(
                        '已取消！',
                        '你的数据是安全的:)',
                        'error'
                    )
                }
            })

    });
};


//监听添加事件
Alter.prototype.listenSigninEvent = function () {
    var self = this;
    var Addgroup = $('.Add-group');
    var AlterTypepInput = Addgroup.find("select[name='AltType']");
    var AssociatedNumberInput = Addgroup.find("input[name='AssociatedNumber']");
    var DatabaseInput = Addgroup.find("select[name='Database']");
    var AlterContentInput = Addgroup.find("textarea[name='AlterContent']");
    var submitBtn = Addgroup.find(".submit-btn");
    submitBtn.click(function () {
        event.preventDefault();
        var AltType = AlterTypepInput.val();
        var AssociatedNumber = AssociatedNumberInput.val();
        var Database = DatabaseInput.val();
        var AlterContent = AlterContentInput.val();

         xfzajax.post({
            'url': '/alter/add_Alter_manager/',
            'data': {
                'AltType': AltType,
                'AssociatedNumber': AssociatedNumber,
                'Database': Database,
                'AlterContent': AlterContent,
            },
             'success': function (result) {
                if(result['code'] === 200){
                     //window.messageBox.show("添加成功");
                     swal.fire(
                         '添加成功',
                         '已经成功添加',
                         'success'
                         ).then(function () {
                          setTimeout("window.location.reload()","300")
                     })


                    //setTimeout("window.location.reload()","300");
                    // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
                    //     window.location.reload();
                    // });
                }
            }
        });
    });
};


//监听删除事件
Alter.prototype.listenDeleteEvent = function () {
    var DeleteBTN = $('.delete-btn');

    DeleteBTN.click(function () {
        var currentBtn =  $(this);
        var tr = currentBtn.parent().parent();
        var id =tr.attr('id');

        Swal.fire({
            //position: 'top-end',
            type: 'warning',
            title: '确认删除吗？',
            text: "数据删除后不能恢复哦!",
            showLoaderOnConfirm:true,
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
            if(result.value){
                Swal.fire(
                    '已删除！',
                    '删除成功。',
                    'success'
                ).then(function () {
                    xfzajax.post({
                        'url': '/alter/delete_Alter_manager/',
                        'data': {
                            'id':id,
                        },
                        'success':function (result) {
                            if (result['code']===200){
                                window.location.reload();
                                //window.messageBox.showSuccess(result['message']);
                            } else {
                                window.messageBox.showError(result['message']);
                            }
                        },

                    });
                })
            }else if (result.dismiss === Swal.DismissReason.cancel) {
                    Swal.fire(
                        '已取消！',
                        '你的数据是安全的:)',
                        'error'
                    )
                }
            })










        // xfzajax.post({
        //     'url': '/alter/delete_Alter_manager/',
        //     'data': {
        //         'id': id,
        //     },
        //      'success': function (result) {
        //         if(result['code'] === 200){
        //              window.messageBox.show("删除成功");
        //             setTimeout("window.location.reload()","300");
        //             // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
        //             //     window.location.reload();
        //             // });
        //         }
        //     }
        // });


    });
};



//监听时间控件点击
Alter.prototype.listenDataPiker=function(){
    var startPicker =$('#start-picker');
    var endPicker =$('#end-picker');
    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth()+1) + '/' + todayDate.getDate();
    var options = {
        'format': 'yyyy/mm/dd',//显示格式
        'language':  "zh-CN",//显示中文
        'formatDate':    'Y/m/d',
        'minView': "month",  //最精确的时间选择视图。
        //'defaultDate': '2017/6/1',//为空的时候默认日期
        'validateOnBlur': true,//如果输入的值为空，则默认当前日期
        'endDate': todayStr,
        'todayBtn': 'linked',//显示今日按钮
        'todayHighlight': true,//高亮当前日期
        'clearBtn': true,//清除按钮显示
        'autoclose': true //选中自动关闭
         // language: 'zh-CN',//显示中文
         //
         // format: 'yyyy-mm-dd',//显示格式
         //
         // minView: "month",//设置只显示到月份
         //
         // initialDate: new Date(),//初始化当前日期
         //
         // autoclose: true,//选中自动关闭
         //
         // todayBtn: true//显示今日按钮
    };
    //startPicker.datetimepicker.dates=['zh-CN'];
    //startPicker.datepicker(options);
    startPicker.datetimepicker(options);
    //startPicker.datepicker(options);
    endPicker.datetimepicker(options);
};


//用于获取当前选中checkbox
getchecked=function () {
    var checkArry = document.getElementsByName("se");
    for (var i = 0; i < checkArry.length; i++) {
        if(checkArry[i].checked == true) {
            return checkArry[i];
        }
    }
};

// 监控审核按钮点击事件
Alter.prototype.listenReviewEvent=function(){
    var self =this;
    var reviewBtn =$('.Review-btn');
    reviewBtn.click(function (event) {
         event.preventDefault();//去除按钮本身的事件
        var checkednow = getchecked();
        if(checkednow){
            //获取被选中元素父类的父类的
            var val = checkednow.parentElement.parentElement.getAttribute("alterid"); //$(r).parent().attr("alterid");
            //var val = r.parentElement.getAttribute("变更编号 id-td"); //$(r).parent().attr("alterid");

            //alert(val);
            self.showReviewEvent();

        }
        // if (selectnow.find("input[type='checkbox']").prop("checked")==true){
        //         self.showReviewEvent();
        //         console.log(selectnow.find("input[type='checkbox']").prop('checked')==true);
        // }
        else {
                alert("一个没有选中");
        }
    });
};


//监控点击选中事件，选中后变色，colour属性在css中定义
Alter.prototype.listenselectnow=function(){
    //var clicknow =$('.click');
    var boxfooter =$('.box-footer');
    var boxheader =$('.box-header');
    var selectnow =$('.tr-line');
    selectnow.click(function () {
        var current =$(this);
        //给当前元素的父级元素添加class属性，siblings结果如果其它同级中有colour属性，就去除其colour属性
        //current.parent().addClass('colour').siblings('tr.colour').removeClass('colour');
        current.addClass('colour').siblings('tr.colour').removeClass('colour');
        ckbox=current.children().children();
        selectnow.find("input[type='checkbox']").prop("checked", false);
        ckbox.prop('checked',true);
    });
    //点击空白区域取消变色和勾选
    // boxfooter.click(function () {
    //     selectnow.addClass('colour').siblings('tr.colour').removeClass('colour');
    //     selectnow.find("input[type='checkbox']").prop("checked", false);
    // });
    //
    // boxheader.click(function () {
    //     selectnow.addClass('colour').siblings('tr.colour').removeClass('colour');
    //     selectnow.find("input[type='checkbox']").prop("checked", false);
    // });
};


//审核提交
Alter.prototype.listenReviewSbumitEvent=function(){
    var self =this;
    var Reviewgroup = $('.Review-group');
    var ReviewsubBtn=$('.Reviewsub-btn');
    var ReviewContenInput = Reviewgroup.find("textarea[name='ReviewContent']");

    //var SbumitreviewBtn = Reviewgroup.find("input[name='Review-btn']");


    ReviewsubBtn.click(function () {
        var Reviewstatus=$("input:radio[name='Reviewstatus']:checked").val();
        var id = getchecked().parentElement.parentElement.getAttribute("id");
        var ReviewContent=ReviewContenInput.val();
        //alert(id);
        //alert(Reviewstatus);
       // alert(ReviewContent);
        //alert(Reviewer);
        xfzajax.post( {
            'url':'/alter/Review_Alter_manager/',
            'data':{
                'id':id,
                'ReviewStatus':Reviewstatus,
                'ReviewContent':ReviewContent,
            },
            'success': function (result) {
                if(result['code'] === 200){
                    //window.messageBox.show("审核成功");
                    Swal.fire(
                        '审核成功',
                        '审核提交成功啦',
                        'success'
                    ).then(function () {
                        window.location.reload()
                    })
                    //setTimeout("window.location.reload()","300")
                    // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
                    //     window.location.reload();
                    // });
                }
            }
        });

    });

};



//新审核功能测试
Alter.prototype.listenReviewtestEvent=function(){
        var reviewbtn = $('.Review-test');

        reviewbtn.click(function (event) {
            event.preventDefault();
            $.ajax({
                'url':'/execute/export_alt_datas_view/',
                //'headers':{"X-CSRFToken":$.cookie("csrftoken")},
                'type':'GET',
                'success': function (result) {
                    // console.log(result);
                    //var res = JSON.stringify(result);
                   if (result['code']===200){
                       console.log(result);

                        for(var k in result['hospital']){
                            //console.log(result[k]);
                            $("#Hospitals_select").append("<option value='"+result['hospital'][k]['pk']+"'>"+result['hospital'][k]["hospitalname"]+"</option>");
                        }

                        for(var k in result['database']){
                            //console.log(result[k]);
                            $("#database_select").append("<option value='"+result['database'][k]['pk']+"'>"+result['database'][k]["dbname"]+"</option>");
                        }
                   }else {
                       console.log('请求失败，没有获取到数据！')
                   }



                }
            });

            Swal.fire({
                    title: '变更数据审核',
                    //type: "prompt",
                    html:
                         //'<input id="swal-input1" class="swal2-input">' +
                         //'<input id="swal-input2" class="swal2-input">'+
                            '<div class="input-group" style="text-align: center;margin: auto;font-size: 14px">\
                               <label  for="ReviewType">审核通过: </label>\
                                  <input id="test111" type="radio" class="radio-btn" checked="" name="Reviewstatus" value="1">\
                               <label style="margin-left: 15px" for="ReviewType">审核不通过: </label>\
                                  <input id="test222" type="radio" class="radio-btn" name="Reviewstatus" value="2">\
                            </div>'+
                        '<textarea  style="height: 100px;" id="swal-input2" class="swal2-input"  rows="15" maxlength="1000" required="" placeholder="请输入审核内容"></textarea>'
                    ,
                    //focusConfirm: false,
                    showCancelButton: true,
                    cancelButtonText:'导出取消',
                    confirmButtonText: '确认导出',
                    }).then(function () {
                        var v = $('input[name="Reviewstatus"]:checked').val();
                          console.log('判断条件',v)

                        if (v==1){
                            console.log($('#test222').val())
                        } else {
                            console.log($('#test111').val())
                        };
            })
        })

};



$(function () {
        //让页面完成加载，然后才能找到需要的元素.
        var alter = new Alter();
        alter.run();
});


