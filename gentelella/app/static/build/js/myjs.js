
//初始化
$(function () {
    //1、初始化表格
    tableInit.Init();

    //2、注册增删改事件
    operate.operateInit();
});

//初始化表格
var tableInit = {
    Init: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: "{% url 'get_group' %}",         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset };
            },//传递参数（*）
            pagination: true,                   //是否显示分页（*）
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                      //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        });
        ko.applyBindings(this.myViewModel, document.getElementById("tb_dept"));
    }
};

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.operateAdd();
        this.operateUpdate();
        this.operateDelete();
        this.DepartmentModel = {
            id: ko.observable(),
            Name: ko.observable(),
            Level: ko.observable(),
            Des: ko.observable(),
            CreateTime: ko.observable()
        };
    },
    //新增
    operateAdd: function(){
        $('#btn_add').on("click", function () {
            $("#myModal").modal().on("shown.bs.modal", function () {
                var oEmptyModel = {
                    id: ko.observable(),
                    Name: ko.observable(),
                    Level: ko.observable(),
                    Des: ko.observable(),
                    CreateTime: ko.observable()
                };
                ko.utils.extend(operate.DepartmentModel, oEmptyModel);
                ko.applyBindings(operate.DepartmentModel, document.getElementById("myModal"));
                operate.operateSave();
            }).on('hidden.bs.modal', function () {
                ko.cleanNode(document.getElementById("myModal"));
            });
        });
    },
    //编辑
    operateUpdate: function () {
        $('#btn_edit').on("click", function () {
            $("#myModal").modal().on("shown.bs.modal", function () {
                var arrselectedData = tableInit.myViewModel.getSelections();
                if (!operate.operateCheck(arrselectedData)) { return; }
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                ko.applyBindings(operate.DepartmentModel, document.getElementById("myModal"));
                operate.operateSave();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("myModal"));
            });
        });
    },
    //删除
    operateDelete: function () {
        $('#btn_delete').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            $.ajax({
                url: "/Department/Delete",
                type: "post",
                contentType: 'application/json',
                data: JSON.stringify(arrselectedData),
                success: function (data, status) {
                    alert(status);
                    //tableInit.myViewModel.refresh();
                }
            });
        });
    },
    //保存数据
    operateSave: function () {
        $('#btn_submit').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/Department/"+funcName,
                type: "post",
                data: oDataModel,
                success: function (data, status) {
                    alert(status);
                    tableInit.myViewModel.refresh();
                }
            });
        });
    },
    //数据校验
    operateCheck:function(arr){
        if (arr.length <= 0) {
            alert("请至少选择一行数据");
            return false;
        }
        if (arr.length > 1) {
            alert("只能编辑一行数据");
            return false;
        }
        return true;
    }
}

function deleteGroup(id) {
    if (window.confirm("您确认删除该条记录吗？")) {
        var post_data = {
            "groupid": id
        };

        $.ajax({
            url: '/app/group_delete/',
            type: 'POST',
            data: post_data,
            dataType: 'json',
            success: function (data) {
                alert(data["status"]);
                window.location.reload(true);
            }

        });
    } else {
        alert("删除失败");
    }

}

//注册新增按钮的事件
function addinfo() {
    $("#myModalLabel").text("新增");
    $("#myModal").modal();
}


function close() {
    $("#myModal").window.close();
}


$("#selectAll").click(function () {
    alert("22121");
})

//批量选择checkbox
function seltAll() {
    var chckBoxSign = document.getElementById("selectAll");       //ckb 全选/反选的选择框id
    var chckBox = document.getElementsByName("chckBox");    //所有的选择框其那么都是chckBox
    var num = chckBox.length;
    if (chckBoxSign.checked) {
        for (var index = 0; index < num; index++) {
            chckBox[index].checked = true;
        }
    } else {
        for (var index = 0; index < num; index++) {
            chckBox[index].checked = false;
        }
    }
}

//批量删除数据
function deleteSelect() {
    var chckBox = document.getElementsByName("chckBox");
    var num = chckBox.length
    var ids = "";
    for (var index = 0; index < num; index++) {
        if (chckBox[index].checked) {
            ids += chckBox[index].value + ",";
        }
    }
    if (ids != "") {
        ids = ids.substring(0, ids.length - 1); //S 删除字符串最后一个字符的几种方法
        ids = {
            'ids': ids
        }
        if (window.confirm("确定删除所选记录？")) {
            $.ajax({
                type: "post",
                url: 'deledeSelect', //要自行删除的action
                data: ids,
                dataType: 'json',
                success: function (data) {
                    if (data["success"]) {
                        alert("删除成功");
                        window.location.reload(true);
                    }
                },
                error: function (data) {
                    alert("系统错误，删除失败");
                }
            });
        }
    } else {
        alert("请选择要删除的记录");
    }
}


//清空查询条件
function empty(){
    $("#user_name").val("");
    $("#user_email").val("");
    $("#user_address").val("");
    $("#user_cards").val("");
    $("#user_numbers").val("");
    $("#datetime_picker").val("");
    $("#datetime_end").val("");
}

function bindEdit() {
    $('#tb').on('click','.edit-row',function () {
        $('#eidtModal').modal('show');
        //1.获取当前行的所有数据
        // 将数据赋值到对应的对话框的指定位置

         $(this).parent().prevAll().each(function () {
             // cls_id
             var v = $(this).text();
             var n = $(this).attr('na');
            if(n=='cls_id'){
                var cid = $(this).attr('cid');
                $('#eidtModal select[name="cls_id"]').val(cid);
            }else if(n=='gender'){
                // v=True
                if(v=='True'){
                    $('#eidtModal :radio[value="1"]').prop('checked',true);
                }else{
                    $('#eidtModal :radio[value="0"]').prop('checked',true);
                }
            }else {
                // n=age
                // v=12
                $("#eidtModal input[name='"+ n +"']").val(v)


            }
         });


    })
}
function bindDelConfirm() {
    $('#delConfirm').click(function () {
        var rowId = $('#delNid').val();
        console.log(rowId);

        $.ajax({
            url: '/del_student/',
            type: 'GET',
            data: {'nid': rowId},
            success:function (arg) {
                var dict = JSON.parse(arg);
                if(dict.status){
                    $('tr[nid="'+ rowId+'"]').remove();
                }
                $('#delModal').modal('hide');
            }
        })

    });


}
function bindDel() {
    $('#tb').on('click','.del-row',function () {
        $('#delModal').modal('show');
        // 回去当前行的ID
        var rowId = $(this).parent().parent().attr('nid');
        $('#delNid').val(rowId);
    })
}
function bindEvent() {
    $('#addBtn').click(function () {
        $('#addModal').modal('show');
    })
}
function bindSave() {

    $('#btnSave').click(function () {
        var postData = {};
        $('#addModal').find('input,select').each(function () {
            var v = $(this).val();
            var n = $(this).attr('name');
            if(n=='gender'){
                if($(this).prop('checked')){
                    postData[n] = v;
                }
            }else{
                postData[n] = v;
            }
        });

        /*
        postData = {
             username: 'asdf',
             age:18,
             gender: 1,
             cls_id: 2
        }
         */

        $.ajax({
            url: '/add_student/',
            type: 'POST',
            data: postData,
            success:function (arg) {
                // arg是字符串
                // JSON.parse将字符串转换成字典， json.loads
                var dict = JSON.parse(arg);
                if(dict.status){
                    /*
                    postData = {
                         username: 'asdf',
                         age:18,
                         gender: 1,
                         cls_id: 2
                    }
                    自增id  = dict.data
                     */
                    createRow(postData,dict.data);
                    $('#addModal').modal('hide');
                    // window.location.reload();
                }else {
                    $('#errorMsg').text(dict.message);
                }
            }
        })

    });


}
function createRow(postData,nid) {
    var tr = document.createElement('tr');
    $(tr).attr('nid',nid);

    var tdId = document.createElement('td');
    tdId.innerHTML = nid;
    $(tr).append(tdId);

    var tdUser = document.createElement('td');
    tdUser.innerHTML = postData.username;
    $(tr).append(tdUser);

    var tdAge = document.createElement('td');
    tdAge.innerHTML = postData.age;
    $(tr).append(tdAge);


    var tdGender = document.createElement('td');
    if(postData.gender == "0"){
        tdGender.innerHTML = 'False';
    }else{
         tdGender.innerHTML = 'True';
    }
    $(tr).append(tdGender);


    var tdClass = document.createElement('td');
    var text = $('select[name="cls_id"]').find('option[value="'+ postData.cls_id +'"]').text();
    tdClass.innerHTML = text;
    $(tr).append(tdClass);

    var tdHandle = '<td> <a class="glyphicon glyphicon-remove icon del-row"></a><a class="fa fa-pencil-square-o icon edit-row"></a> </td>';
    $(tr).append(tdHandle);

    $('#tb').append(tr);
}