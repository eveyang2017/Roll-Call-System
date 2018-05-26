
//初始化
$(function () {
    //1、初始化表格
    tableInit.Init_Course();

    //2、注册增删改事件
    operate.operateInit();
});

//初始化表格
var tableInit = {

    Init_Course: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: "/app/get_course/",         //请求后台的URL（*）
            method: 'GET',                      //请求方式（*）
            toolbar: '#get_course',                //工具按钮用哪个容器
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset };
            },//传递参数（*）
            pagination: true,                   //是否显示分页（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            sortable: true,
            sortName: 'name',
            sortOrder: "asc",
            pageNumber: 1,                      //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        });
        ko.applyBindings(this.myViewModel, document.getElementById("tb_course"));
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
            name: ko.observable(),
            category: ko.observable(),
            credit: ko.observable(),
            hours: ko.observable(),
            desc: ko.observable()
        };
    },
    //新增
    operateAdd: function(){
        $('#btn_add').on("click", function () {
            $("#myModal").modal().on("shown.bs.modal", function () {
                var oEmptyModel = {
                    Name: ko.observable(),
                    Category: ko.observable(),
                    Credit: ko.observable(),
                    Hours: ko.observable(),
                    Desc: ko.observable()
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
                url: "/app/del_course/",
                type: "post",
                contentType: 'application/json',
                data: JSON.stringify(arrselectedData),
                success: function (data, status) {
                    alert(status);
                    tableInit.myViewModel.refresh();
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
            var oDataModel = ko.toJS(oViewModel);
            var funcName = oDataModel.id?"update_course/":"add_course/";
            $.ajax({
                url: "/app/"+funcName,
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

////根据窗口调整表格高度
//    $(window).resize(function() {
//        $('#tb_course').bootstrapTable('resetView', {
//            height: tableHeight()
//        })
//    })
////生成用户数据
//    $('#tb_course').bootstrapTable({
//        method: 'get',
////        contentType: "application/x-www-form-urlencoded",//必须要有！！！！
//        url:"/app/get_course/",//要请求数据的文件路径
//        height:tableHeight(),//高度调整
//        toolbar: '#toolbar',//指定工具栏
//        striped: true, //是否显示行间隔色
//        dataField: "res",//bootstrap table 可以前端分页也可以后端分页，这里
//        //我们使用的是后端分页，后端分页时需返回含有total：总记录数,这个键值好像是固定的
//        //rows： 记录集合 键值可以修改  dataField 自己定义成自己想要的就好
//        pageNumber: 1, //初始化加载第一页，默认第一页
//        pagination:true,//是否分页
//        queryParamsType:'limit',//查询参数组织方式
//        queryParams:queryParams,//请求服务器时所传的参数
//        sidePagination:'client',//指定服务器端分页
//        pageSize:10,//单页记录数
//        pageList:[5,10,20,30],//分页步进值
//        showRefresh:true,//刷新按钮
//        showColumns:true,
//        clickToSelect: true,//是否启用点击选中行
//        toolbarAlign:'right',//工具栏对齐方式
//        buttonsAlign:'right',//按钮对齐方式
//        columns:[
//            {
//                title:'全选',
//                field:'state',
//                //复选框
//                checkbox:true,
//                width:25,
//                align:'center',
//                valign:'middle'
//            },
//            {
//                title:'ID',
//                field:'id',
//                visible:false
//            },
//            {
//                title:'课程名',
//                field:'name',
//                sortable:true
//            },
//            {
//                title:'课程类别',
//                field:'desc',
//                sortable:true
//            },
//            {
//                title:'学分',
//                field:'credit',
//            },
//            {
//                title:'学时',
//                field:'hours'
//            },
//            {
//                title:'任课教师',
//                field:'teacher',
//                sortable:true
//            },
//            {
//                title:'课程说明',
//                field:'category',
//                align:'center',
//                //列数据格式化
////                formatter:operateFormatter
//            }
//        ],
//        locale:'zh-CN',//中文支持,
//        responseHandler: function(res) {   //处理 从后端 返回的数据
//            console.log(res);
////            return res
//            if (res == 0) {
//                alert('查询出问题！');
//            } else {
//                var orderListData = res['rows'];  //##### 重要！！#####
//                console.log(orderListData);
//                return orderListData;
//            }
//        },
//    })
//    //三个参数，value代表该列的值
//    function operateFormatter(value,row,index){
//        if(value==2){
//            return '<i class="fa fa-lock" style="color:red"></i>'
//        }else if(value==1){
//            return '<i class="fa fa-unlock" style="color:green"></i>'
//        }else{
//            return '数据错误'
//        }
//    }
//
//    //请求服务数据时所传参数
//    function queryParams(params){
//        return{
//            //每页多少条数据
//            pageSize: params.limit,
//            //请求第几页
//            pageIndex:params.pageNumber,
//            Name:$('#search_name').val(),
//            Tel:$('#search_tel').val()
//        }
//    }
//     //查询按钮事件
//    $('#search_btn').click(function(){
//        $('#tb_course').bootstrapTable('refresh', {url: '/app/get_course/'});
//    })
//    //tableHeight函数
//    function tableHeight(){
//        //可以根据自己页面情况进行调整
//        return $(window).height() -280;
//    }

