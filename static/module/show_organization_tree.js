var setting = {
    view: {
        dblClickExpand: false,//双击节点时，是否自动展开父节点的标识
        showLine: true,//是否显示节点之间的连线
        fontCss:{'color':'black','font-weight':'bold'},//字体样式函数
        selectedMulti: true //设置是否允许同时选中多个节点
    },
    // check:{
    //     chkboxType: { "Y": "", "N": "" },
    //     chkStyle: "checkbox",//复选框类型
    //     enable: true //每个节点上是否显示 CheckBox
    // },
    data: {
        simpleData: {//简单数据模式
            enable:true,
            // idKey: "id",
            // pIdKey: "pId",
            // rootPId: null
        }
    },
};
var zTreeObj;
$.ajax({
    url: "/test_management/get_organization_tree",//数据请求的地址
    method: "POST",//ajax数据访问的方法
    dataType: "json",//返回数据类型格式
    success: function (new_data) {
        let zTreeData = new_data.data_list
        console.log(zTreeData)
        zTreeObj = $.fn.zTree.init($("#myZTree"), setting, zTreeData);

    },
    error:function (){
        toastr.error('请求错误')

    }


})





