

//构造函数Alter
function Execute() {
        //函数当中的this代表的都是函数本身，所以定义一个self避免出现冲突
        var self =this;
        //将盒子mask-wapper定义成为一个属性
        self.maskwapper=$('.mask-wapper-add');
        self.scollwapper =$('.scoll-wapper');
        //获得Renview的盒子
        self.maskwapper_Review=$('.mask-wapper-Review');

}

//Alter类的入口,运行
Execute.prototype.run=function () {
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
        self.listenExportSbumitEvent();
        self.listenExportNewSbumitEvent();
        self.listenExportbumitEvent();

};

//用于显示事件
Execute.prototype.showEvent=function () {
        var self =this;
        self.maskwapper.show();
};

Execute.prototype.showReviewEvent=function(){
        var self=this;
        self.maskwapper_Review.show();
};

//用于隐藏事件
Execute.prototype.hideEvent=function () {
        var self =this;
        self.maskwapper.hide();
        self.maskwapper_Review.hide();
};



Execute.prototype.listenshowhideEvent=
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
            var  AlterID =tr.attr('AlterID');
            var  Hospital =tr.attr('Hospital');
            var  ExecutionResult =tr.attr('ExecutionResult');
            var  Executor =tr.attr('Executor');
            var  ExecutionTime =tr.attr('ExecutionTime');
            // var AlterType =tr.td($('.AlterType-td'));
            // var AssociatedNumber=tr.td($('.AssociatedNumber-td'));
            // var Datebase=tr.td($('.Datebase-td'));
            // var AlterContent=tr.td($('.AlterContent-td'));
            // var Informant=tr.td($('.Informant-td'));
            // var FillTime=tr.td($('.FillTime-td'));
            $("#ID-executeID").val(id);
            $("#ID-id").val(AlterID);
            $("#ID-Hospital").val(Hospital);
            $("#ID-ExecutionResult").val(ExecutionResult);
            $("#ID-Executor").val(Executor);
            $("#ID-ExecutionTime").val(ExecutionTime);




        });

        addBtn.click(function () {
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
Execute.prototype.listenreviseEvent=function(){
        var revisegroup = $('.revise-group');
        var executeID_Input = revisegroup.find("input[name='executeID']");
        var AlterID_Input = revisegroup.find("input[name='id']");
        var Hospital_Input = revisegroup.find("input[name='Hospital']");
        var ExecutionResult_Input = revisegroup.find("textarea[name='ExecutionResult']");
        var reviseBtn = revisegroup.find(".revise-btn");
    reviseBtn.click(function () {
        var id =executeID_Input.val();
        var AlterID = AlterID_Input.val();
        var Hospital = Hospital_Input.val();
        var ExecutionResult = ExecutionResult_Input.val();

         xfzajax.post({
            'url': '/execute/execute_Alter_Execute/',
            'data': {
                'id':id,
                'AlterID':AlterID,
                'Hospital': Hospital,
                'ExecutionResult': ExecutionResult,
            },
            'success': function (result) {
                if(result["code"] === 200){
                    window.messageBox.show("执行成功");
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
Execute.prototype.listenSigninEvent = function () {
    var self = this;
    var Addgroup = $('.Add-group');
    var AlterIDInput = Addgroup.find("input[name='AlterID']");
    var HospitalInput = Addgroup.find("input[name='Hospital']");
    var ExecutionResultInput = Addgroup.find("textarea[name='ExecutionResult']");
    var submitBtn = Addgroup.find(".submit-btn");
    submitBtn.click(function () {
        var AlterID = AlterIDInput.val();
        var Hospital = HospitalInput.val();
        var ExecutionResult = ExecutionResultInput.val();

         xfzajax.post({
            'url': '/execute/add_Alter_Execute/',
            'data': {
                'AlterID': AlterID,
                'Hospital': Hospital,
                'ExecutionResult': ExecutionResult,
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
Execute.prototype.listenDeleteEvent = function () {
    var DeleteBTN = $('.delete-btn');
    DeleteBTN.click(function () {
        var currentBtn =  $(this);
        var tr = currentBtn.parent().parent();
        var id =tr.attr('id');
        console.log(executeID);
        xfzajax.post({
            'url': '/execute/delete_Alter_Execute/',
            'data': {
                'id': id,
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



//监听时间控件
Execute.prototype.listenDataPiker=function(){
    var startPicker =$('#startpicker');
    var endPicker =$('#endpicker');
    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth()+1) + '/' + todayDate.getDate();
    var options = {
        // 'showButtonPanel': true,
        // 'format': 'yyyy/mm/dd',
        // 'startDate': '2017/6/1',
        // 'endDate': todayStr,
        // 'language': 'zh-CN',
        // 'todayBtn': 'linked',
        // 'todayHighlight': true,
        // 'clearBtn': true,
        // 'autoclose': true



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
    };
    startPicker.datetimepicker(options);
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
Execute.prototype.listenReviewEvent=function(){
    var self =this;
    var reviewBtn =$('.Review-btn');
    reviewBtn.click(function () {
        var checkednow = getchecked();
        if(checkednow){
            //获取被选中元素父类的父类的
            var val = checkednow.parentElement.parentElement.getAttribute("alterid"); //$(r).parent().attr("alterid");
            //var val = r.parentElement.getAttribute("变更编号 id-td"); //$(r).parent().attr("alterid");

            alert(val);
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
Execute.prototype.listenselectnow=function(){
    //var clicknow =$('.click');
    var boxfooter =$('.box-footer');
    var boxheader =$('.box-header');
    var selectnow =$('.tr-line');
    var count =0;
    selectnow.click(function () {
        count++;
        // var current =$(this);
        // //给当前元素的父级元素添加class属性，siblings结果如果其它同级中有colour属性，就去除其colour属性
        // //current.parent().addClass('colour').siblings('tr.colour').removeClass('colour');
        // current.addClass('colour').siblings('tr.colour').removeClass('colour');
        // ckbox=current.children().children();
        // selectnow.find("input[type='checkbox']").prop("checked", false);
        // ckbox.prop('checked',true);
        //


        //如果是偶数就取消颜色和弹框 奇数就加上背景色并选中
        if (count % 2 ===0) {

            selectnow.removeClass('colour');
            selectnow.find("input[type='checkbox']").prop("checked", false);
        }
        else {
            var current =$(this);
            //给当前元素的父级元素添加class属性，siblings结果如果其它同级中有colour属性，就去除其colour属性
            //current.parent().addClass('colour').siblings('tr.colour').removeClass('colour');
            current.addClass('colour').siblings('tr.colour').removeClass('colour');
            ckbox=current.children().children();
            selectnow.find("input[type='checkbox']").prop("checked", false);
            ckbox.prop('checked',true);
        }


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



Execute.prototype.listenReviewSbumitEvent=function(){
    var self =this;
    var Reviewgroup = $('.Review-group');
    var ReviewsubBtn=$('.Reviewsub-btn');
    var ReviewContenInput = Reviewgroup.find("textarea[name='ReviewContent']");
    var ReviewerInput = Reviewgroup.find("input[name='Reviewer']");
    //var SbumitreviewBtn = Reviewgroup.find("input[name='Review-btn']");


    ReviewsubBtn.click(function () {
        var Reviewstatus=$("input:radio[name='Reviewstatus']:checked").val();
        var AlterID = getchecked().parentElement.parentElement.getAttribute("alterid");
        var ReviewContent=ReviewContenInput.val();
        var Reviewer =ReviewerInput.val();
        alert(AlterID);
        alert(Reviewstatus);
        alert(ReviewContent);
        alert(Reviewer);
        xfzajax.post( {
            'url':'/alter/Review_Alter_manager/',
            'data':{
                'AlterID':AlterID,
                'ReviewStatus':Reviewstatus,
                'ReviewContent':ReviewContent,
                'Reviewer':Reviewer,
            },
            'success': function (result) {
                if(result['code'] === 200){
                    window.messageBox.show("审核成功");
                    setTimeout("window.location.reload()","300");
                    // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
                    //     window.location.reload();
                    // });
                }
            }
        });

    });

};


//监听导出全部按钮
Execute.prototype.listenExportSbumitEvent=function(){
    var self =this;
    var exportBTN = $('.export-BTN');
    var formgroup= $('.form-group');
    var DatabaseType= formgroup.find("select[name='DatabaseType']");
    var hospital = formgroup.find("select[name='Hospital']");

    exportBTN.click(function () {
        // var Reviewstatus=$("input:radio[name='Reviewstatus']:checked").val();
        // var AlterID = getchecked().parentElement.parentElement.getAttribute("alterid");
        // var ReviewContent=ReviewContenInput.val();
        // var Reviewer =ReviewerInput.val();
        var Database= DatabaseType.val();
        var Hospital= hospital.val();
        alert('选择的医院是:',Hospital);
        //alert('选择的数据库是',Database);
        // alert(AlterID);
        // alert(Reviewstatus);
        // alert(ReviewContent);
        // alert(Reviewer);

        $.ajax({
            'url':'/execute/export/',
            //'headers':{"X-CSRFToken":$.cookie("csrftoken")},
            'type':'POST',
            //'dataType':'json',
            'data': {
                'DatabaseType': Database,
                'Hospital':Hospital,
            },
            'success': function (result) {
                if(result['code'] === 200){

                    var form = $('<form action="download/" method="post"></form>');
                    $('body').append(form);
                    form.submit(); //自动提交
                    window.messageBox.show("提交导出成功!");
                    //setTimeout("window.location.reload()","300");
                    // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
                    //     window.location.reload();
                    // });
                }else {
                    //alert(JSON.stringify(result));
                    window.messageBox.show(result['message']);
                }
            }
        });
        // xfzajax.post( {
        //     'url':'/execute/export/',
        //     'data':{
        //         'DatabaseType':Database,
        //     },
        //     'dataType':'json',
        //     'success': function (result) {
        //         alert(result);
        //         window.location.href=result;
        //         if(result['code'] === 200){
        //             window.messageBox.show("提交导出成功");
        //             setTimeout("window.location.reload()","300");
        //             // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
        //             //     window.location.reload();
        //             // });
        //         }else {
        //             //alert(JSON.stringify(result));
        //             window.messageBox.show(result['message']);
        //         }
        //     }
        // });

    });

};



//监听导出最新按钮
Execute.prototype.listenExportNewSbumitEvent=function(){
    var self =this;
    var exportNew = $('#testOut');
    var formgroup= $('.form-group');
    var DatabaseType= formgroup.find("select[name='DatabaseType']");

    exportNew.click(function () {
        // var Reviewstatus=$("input:radio[name='Reviewstatus']:checked").val();
        // var AlterID = getchecked().parentElement.parentElement.getAttribute("alterid");
        // var ReviewContent=ReviewContenInput.val();
        // var Reviewer =ReviewerInput.val();
        var Database= DatabaseType.val();
        console.log(Database);
        // alert(AlterID);
        // alert(Reviewstatus);
        // alert(ReviewContent);
        // alert(Reviewer);

        xfzajax.post({
            'url':'/execute/exportAltData/',
            //'headers':{"X-CSRFToken":$.cookie("csrftoken")},
            // 'type':'POST',
            //'dataType':'json',
            'data': {
                'DatabaseType': Database,
            },
            'success': function (result) {
                if(result['code'] === 200){
                    var form = $('<form action="download/" method="post">' +
                        '<input type=\'hidden\' id=\'infos\' name=\'csrfmiddlewaretoken\' value=\'\' />' +
                        '</form>');
                    $('body').append(form);
                    // $("#downForm").append('{% csrf_token %}');
                    // $("#downForm").append("<input type='hidden' id='infos' name='csrfmiddlewaretoken' value='' />");
                    console.log($.cookie("csrftoken"));
                    $("#infos").val($.cookie("csrftoken"));

                    // return;
                    // $("#downForm").submit();

                    form.submit(); //自动提交
                    window.messageBox.show("提交导出成功!");
                    //setTimeout("window.location.reload()","300");
                    // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
                    //     window.location.reload();
                    // });
                }else {
                    //alert(JSON.stringify(result));
                    window.messageBox.show(result['message']);
                }
            }
        });
        // xfzajax.post( {
        //     'url':'/execute/export/',
        //     'data':{
        //         'DatabaseType':Database,
        //     },
        //     'dataType':'json',
        //     'success': function (result) {
        //         alert(result);
        //         window.location.href=result;
        //         if(result['code'] === 200){
        //             window.messageBox.show("提交导出成功");
        //             setTimeout("window.location.reload()","300");
        //             // xfzalert.alertSuccess('恭喜！新闻发表成功!',function () {
        //             //     window.location.reload();
        //             // });
        //         }else {
        //             //alert(JSON.stringify(result));
        //             window.messageBox.show(result['message']);
        //         }
        //     }
        // });

    });

};

// //新數據導出功能
// Execute.prototype.listenExportbumitEvent=function(){
//         var exportbtn = $('.export-btn');
//         exportbtn.click(function () {
//                 $.ajax({
//                 //'url':'/execute/test_select/',
//                 'url':'/execute/export_alt_datas_view/',
//                 //'headers':{"X-CSRFToken":$.cookie("csrftoken")},
//                 'type':'GET',
//                 //'dataType':'json',
//                 'success': function (result) {
//                     // console.log(result);
//                     //var res = JSON.stringify(result);
//                    if (result['code']===200){
//                        console.log(result);
//
//                         for(var k in result['hospital']){
//                             //console.log(result[k]);
//                             //$("#Hospitals_select").append("<option value='"+result['hospital'][k]['pk']+"'>"+result['hospital'][k]["hospitalname"]+"</option>");
//                             $("#Hospitals_select").append("<option value='"+result['hospital'][k]['dept_id']+"'>"+result['hospital'][k]["dept_name"]+"</option>");
//
//                         }
//
//                         for(var k in result['database']){
//                             //console.log(result[k]);
//                             $("#database_select").append("<option value='"+result['database'][k]['pk']+"'>"+result['database'][k]["dbname"]+"</option>");
//
//                         }
//                    }else {
//                        console.log('请求失败，没有获取到数据！')
//                    }
//
//
//
//                 }
//             });
//
//             //     xfzajax.get({
//             //     'url':'/execute/test_select/',
//             //     //'headers':{"X-CSRFToken":$.cookie("csrftoken")},
//             //     //'dataType':'json',
//             //     'success': function (result) {
//             //         // console.log(result);
//             //         //var res = JSON.stringify(result);
//             //         console.log(result.data);
//             //         var datas = result.data;
//             //         for(var k in datas){
//             //             console.log(datas[k]);
//             //             $("#Hospitals_select").append("<option value='"+datas[k]["pk"]+"'>"+datas[k]["Hospital"]+"</option>");
//             //
//             //         }
//             //     }
//             // });
//
//
//
//
//
//                 Swal.fire({
//                     title: '请选择执行医院和导出数据库',
//                     //type: "prompt",
//                     html:
//                         // Hospitals+
//                         // '<input id="swal-input1" class="swal2-input">' +
//                         // '<input id="swal-input2" class="swal2-input">'+
//                          '<lable style ="float: left;display: inline-block;width:30%;color: grey; border:0;text-align: right;" class="form-control"><b>执行医院:</b></lable>\
//                          <select style ="float: left;display: inline-block;width:70%" name="Hospitals" id="Hospitals_select" class="form-control">\
//                                <option value="0">全部</option>\
//                           </select><br/>'+ '\
//                           \<lable style ="float: left;display: inline-block;width:30%;color: grey; border:0;text-align: right;" class="form-control"><b>导出数据库:</b></lable>\
//                           <select  style ="float: left;display: inline-block;width:70%" name="database" id="database_select" class="form-control">\
//                                <option value="0">全部</option>\
//                           </select>',
//                     //focusConfirm: false,
//                     showCancelButton: true,
//                     cancelButtonText:'导出取消',
//                     confirmButtonText: '确认导出',
//                     }).then(function(result){
//                         if (result.dismiss === Swal.DismissReason.cancel ||result.dismiss === Swal.DismissReason.backdrop ){
//                             console.log('用户取消！')
//                             return;
//                         }
//                         var hospital = $("#Hospitals_select option:selected").val();
//                         var hospitaltext = $("#Hospitals_select option:selected").text();
//                         //console.log($("#swal-input1").val());
//                         console.log(hospital);
//                         console.log(hospitaltext);
//
//                         var database = $("#database_select option:selected").val();
//                         var databasetext = $("#database_select option:selected").text();
//                         //console.log($("#swal-input1").val());
//                         console.log(database);
//                         console.log(databasetext);
//                          // alert(document.getElementById('swal-input1').value); // value of my-input1
//                          // alert(document.getElementById('swal-input2').value); // value of my-select
//                         $.ajax( {
//                                 //'url':'/execute/exportAltData/',
//                                 'url':'/execute/export_alt_datas_view/',
//                                 'headers':{"X-CSRFToken":$.cookie("csrftoken")},
//                                 'type':'POST',
//                                 'data':{
//                                     'database':database,
//                                     'hospital':hospital
//                                 },
//                                 //'dataType':'json',
//                                 'success': function (result) {
//                                     if(result['code'] === 200 ) {
//
//                                         var form = $('<form action="download/?dbname='+databasetext+'&hospitalid='+hospital+'" method="post">' +
//                                             '<input type=\'hidden\' id=\'infos\' name=\'csrfmiddlewaretoken\' value=\'\' />' +
//                                             '</form>');
//                                         $('body').append(form);
//                                         // $("#downForm").append('{% csrf_token %}');
//                                         // $("#downForm").append("<input type='hidden' id='infos' name='csrfmiddlewaretoken' value='' />");
//                                         console.log($.cookie("csrftoken"));
//                                         $("#infos").val($.cookie("csrftoken"));
//
//                                         // return;
//                                         // $("#downForm").submit();
//
//                                         form.submit(); //自动提交
//                                         console.log('导出请求提交成功')
//                                         window.messageBox.show("提交导出成功");
//
//                                     }else if(result['code'] !== 200 ){
//                                         //alert(JSON.stringify(result));
//                                         //window.messageBox.show(result['message']);
//                                          console.log(result['message'])
//                                         swal.fire(
//                                             result['message'],
//                                             '如无医院可选，请先维护字典！',
//                                             'warning'
//                                         )
//                                     }
//                                 }
//                         });
//                     })
//         })
// };





//測試新數據導出功能
Execute.prototype.listenExportbumitEvent=function(){
        var exportbtn = $('.export-btn');
        exportbtn.click(function () {
                $.ajax({
                //'url':'/execute/test_select/',
                'url':'/execute/export_alt_datas_view/',
                //'headers':{"X-CSRFToken":$.cookie("csrftoken")},
                'type':'GET',
                //'dataType':'json',
                'success': function (result) {
                    // console.log(result);
                    //var res = JSON.stringify(result);
                   if (result['code']===200){
                       console.log(result);

                        for(var k in result['hospital']){
                            //console.log(result[k]);
                            //$("#Hospitals_select").append("<option value='"+result['hospital'][k]['pk']+"'>"+result['hospital'][k]["hospitalname"]+"</option>");
                            $("#Hospitals_select").append("<option value='"+result['hospital'][k]['dept_id']+"'>"+result['hospital'][k]["dept_name"]+"</option>");

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
                    title: '请选择执行医院和导出数据库',
                    //type: "prompt",
                    html:
                        // Hospitals+
                        // '<input id="swal-input1" class="swal2-input">' +
                        // '<input id="swal-input2" class="swal2-input">'+
                         '<lable style ="float: left;display: inline-block;width:30%;color: grey; border:0;text-align: right;" class="form-control"><b>执行医院:</b></lable>\
                         <select style ="float: left;display: inline-block;width:70%" name="Hospitals" id="Hospitals_select" class="form-control">\
                               <option value="0">全部</option>\
                          </select><br/>'+ '\
                          \<lable style ="float: left;display: inline-block;width:30%;color: grey; border:0;text-align: right;" class="form-control"><b>导出数据库:</b></lable>\
                          <select  style ="float: left;display: inline-block;width:70%" name="database" id="database_select" class="form-control">\
                               <option value="0">全部</option>\
                          </select>',
                    //focusConfirm: false,
                    showCancelButton: true,
                    cancelButtonText:'导出取消',
                    confirmButtonText: '确认导出',
                    }).then(function(result){
                        if (result.dismiss === Swal.DismissReason.cancel ||result.dismiss === Swal.DismissReason.backdrop ){
                            console.log('用户取消！')
                            return;
                        }
                        var hospital = $("#Hospitals_select option:selected").val();
                        var hospitaltext = $("#Hospitals_select option:selected").text();
                        //console.log($("#swal-input1").val());
                        console.log(hospital);
                        console.log(hospitaltext);

                        var database = $("#database_select option:selected").val();
                        var databasetext = $("#database_select option:selected").text();
                        //console.log($("#swal-input1").val());
                        console.log(database);
                        console.log(databasetext);
                         // alert(document.getElementById('swal-input1').value); // value of my-input1
                         // alert(document.getElementById('swal-input2').value); // value of my-select
                            $.ajax( {
                                    //'url':'/execute/exportAltData/',
                                    'url':'/execute/export_alt_datas_view/',
                                    'headers':{"X-CSRFToken":$.cookie("csrftoken")},
                                    'type':'POST',
                                    'data':{
                                        'database':database,
                                        'hospital':hospital
                                    },
                                    //'dataType':'json',
                                    'success': function (result) {
                                        if(result['code'] === 200 ) {
                                             console.log('返回的数据库列表是：',result)
                                            for(var i in result['data']){
                                                 console.log('返回的数据库：',result['data'][i])
                                            }

                                            //判断数据库是否选中全部
                                            if(database !='0'){
                                                var form = $('<form action="download/?dbname='+databasetext+'&hospitalid='+hospital+'&databaseid='+database+'" method="post">' +
                                                '<input type=\'hidden\' id=\'infos\' name=\'csrfmiddlewaretoken\' value=\'\' />' +
                                                '</form>');
                                            }else {
                                                console.log('医院ID是：',hospital)
                                                var form = $('<form action="new_file_down/?dblist='+result['data']+'&hospitalid='+hospital+'" method="post">' +
                                                '<input type=\'hidden\' id=\'infos\' name=\'csrfmiddlewaretoken\' value=\'\' />' +
                                                '</form>');
                                            }
                                            $('body').append(form);
                                            // $("#downForm").append('{% csrf_token %}');
                                            // $("#downForm").append("<input type='hidden' id='infos' name='csrfmiddlewaretoken' value='' />");
                                            console.log($.cookie("csrftoken"));
                                            $("#infos").val($.cookie("csrftoken"));

                                            // return;
                                            // $("#downForm").submit();

                                            form.submit(); //自动提交
                                            console.log('导出请求提交成功')
                                            window.messageBox.show("提交导出成功");

                                        }
                                        else if(result['code'] !== 200 ){
                                            //alert(JSON.stringify(result));
                                            //window.messageBox.show(result['message']);
                                             console.log(result['message'])
                                            swal.fire(
                                                result['message'],
                                                '如无医院可选，请先维护字典！',
                                                'warning'
                                            )
                                        }
                                    }
                            });

                    })
        })
};






$(function () {
        //让页面完成加载，然后才能找到需要的元素.
        var execute = new Execute();
        execute.run();
});