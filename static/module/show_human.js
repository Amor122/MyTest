var $table = $('#my_table');

$(document).ready(function () {
    initTable();
});

function queryParams(params) {
    var Parameters = [];
    return {
        order: params.order,
        limit: params.limit,
        offset: params.offset,
        ParameterJson: JSON.stringify(Parameters)
    };
}

function initTable() {
    $table.bootstrapTable({
        url: 'get_human',   //请求后台的URL（*）
        method: 'post',      //请求方式（*）

        toolbar: '#toolbar',    //工具按钮用哪个容器
        striped: true,      //是否显示行间隔色
        cache: false,      //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pagination: true,     //是否显示分页（*）
        sortable: true,      //是否启用排序
        sortOrder: "asc",     //排序方式
        // queryParams: queryParams, //传递参数（*）
        sidePagination: "client",   //分页方式：client客户端分页，server服务端分页（*）
        pageSize: 50,
        pageList: [10, 25, 50, 100, 'ALL'],  //可供选择的每页的行数（*）
        search: true,      //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
        showColumns: true,     //是否显示所有的列
        minimumCountColumns: 2,    //最少允许的列数
        clickToSelect: false,    //是否启用点击选中行
        // height: 800,      //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
        uniqueId: "id",      //每一行的唯一标识，一般为主键列
        showToggle: false,     //是否显示详细视图和列表视图的切换按钮
        cardView: false,     //是否显示详细视图
        detailView: false,     //是否显示父子表
        // iconSize: 'outline',
        columns: [
            {
                title: '所属组织',
                sortable: true,
                field: 'organization',
                align: 'center',
                valign: 'middle'
            }, {
                title: '账号',
                sortable: true,
                searchable: true,
                field: 'user_id',
                align: 'center',
                valign: 'middle',
            }, {
                title: '姓名',
                field: 'user_name',
                align: 'center',
                valign: 'middle',
            }, {
                title: '职务',
                field: 'post',
                align: 'center',
                valign: 'middle',
            }, {
                title: '是否主要负责人',
                field: 'chief',
                align: 'center',
                valign: 'middle',

                formatter: function (value, item, index) {
                    if (value) {
                        return "<span style='color: green'>√</span>";
                    } else {
                        return "<span style='color: red'>×</span>";

                    }
                }

            }, {
                title: '编辑',
                field: 'edit',
                align: 'center',
                valign: 'middle',
                events: {
                    'click #edit': function (e, value, row, index) {

                        $('#id').val(row.id);
                        $('#user_name').val(row.user_name);
                        $('#user_id').val(row.user_id)
                        $('#organization').empty()
                        $.ajax({
                            url: "/test_management/get_organizations",//数据请求的地址
                            method: "POST",//ajax数据访问的方法
                            dataType: "json",//s数据类型格式
                            success: function (data_receive) {
                                let organization_list = data_receive.organization_list
                                for (let org in organization_list) {
                                    if (organization_list[org] === row.organization) {
                                        $('#organization').append("<option selected value='" + organization_list[org] + "'>" + organization_list[org] + "</option>")
                                    } else {
                                        $('#organization').append("<option value='" + organization_list[org] + "'>" + organization_list[org] + "</option>")

                                    }
                                }

                            },
                            error: function () {
                                toastr.error('组织数据获取失败，请刷新后再试')

                            }

                        })
                        $('#post').empty()
                        $.ajax({
                            url: "/test_management/get_posts",//数据请求的地址
                            method: "POST",//ajax数据访问的方法
                            dataType: "json",//s数据类型格式
                            success: function (data_receive) {
                                let post_list = data_receive.post_list
                                for (let pos in post_list) {
                                    if (post_list[pos] === row.post) {
                                        $('#post').append("<option selected value='" + post_list[pos] + "'>" + post_list[pos] + "</option>")
                                    } else {
                                        $('#post').append("<option value='" + post_list[pos] + "'>" + post_list[pos] + "</option>")

                                    }
                                }

                            },
                            error: function () {
                                toastr.error('职位数据获取失败，请刷新后再试')

                            }

                        })


                        $('#table_edit').modal('show')
                    }
                },
                formatter: function (value, item, index) {
                    return "<button id='edit' class='btn btn-info btn-sm'  data-toggle='modal' data-target='#table_edit'>编辑</button>"
                }

            }, {
                title: '密码',
                field: 'reset',
                align: 'center',
                valign: 'middle',
                formatter: function (value, item, index) {
                    return '<button class="btn btn-warning btn-sm" onclick=" if( confirm(\'确认重置该用户密码\') ) reset_password(\'' + item.id + '\')">重置</button>'
                }
            }, {
                title: '删除',
                field: 'delete',
                align: 'center',
                valign: 'middle',
                formatter: function (value, item, index) {
                    return '<button class="btn btn-danger btn-sm" onclick=" if( confirm(\'确认删除该用户\') ) delete_user(\'' + item.id + '\')">删除</button>'
                }
            },

        ]
    });
}

function getData() {
    return $table.bootstrapTable('getSelections');
}

function setSelections(data) {
    setTimeout(function () {
        $table.bootstrapTable('checkBy', {field: 'Name', values: data});
    }, 500);
}

function Refresh() {
    $table.bootstrapTable('refresh');
}

$('#sidebarToggle').click(function () {
        console.log('clicked')
        $('#table').bootstrapTable('resetView')

    }
)

function edit_human() {
    form_data = {
        'id': $('#id').val(),
        'user_name': $('#user_name').val(),
        'user_id': $('#user_id').val(),
        'organization': $('#organization').val(),
        'post': $('#post').val()
    }
    $.ajax({
        url: "/test_management/edit_human",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        // timeout: 30,
        data: form_data,
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            if (data_receive.status) {
                toastr.success('修改成功')
                $('#table_edit').modal('hide')
                $table.bootstrapTable('refresh');

            } else {
                toastr.error('修改失败，可能是重复的账号！')
                $table.bootstrapTable('refresh');

            }


        },
        error: function (data_receive) {
            toastr.error('数据提交失败，请刷新后再试')
            $('#table_edit').modal('hide')
            $table.bootstrapTable('refresh');


        }

    })


}

$('#table_add_button').click(function () {
    $('#user_id_add').empty()
    $('#user_name_add').empty()
    $.ajax({
        url: "/test_management/get_organizations",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            let organization_list = data_receive.organization_list
            for (let org in organization_list) {
                $('#organization_add').append("<option value='" + organization_list[org] + "'>" + organization_list[org] + "</option>")

            }

        },
        error: function () {
            toastr.error('组织数据获取失败，请刷新后再试')

        }
    })
    $.ajax({
        url: "/test_management/get_posts",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            let post_list = data_receive.post_list
            for (let pos in post_list) {
                $('#post_add').append("<option value='" + post_list[pos] + "'>" + post_list[pos] + "</option>")
            }
        },
        error: function () {
            toastr.error('职位数据获取失败，请刷新后再试')

        }

    })

    $('#table_add').modal('show')
})

$('#table_add_submit').click(function () {
    let user_id = $('#user_id_add').val()
    let user_name = $('#user_name_add').val()
    let organization = $('#organization_add').val()
    let post = $('#post_add').val()
    if (!user_id || !user_name) {
        toastr.warning("参数不全")
    } else {
        let post_data = {
            'user_id': user_id,
            'user_name': user_name,
            'organization': organization,
            'post': post
        }
        $.ajax({
            url: "/test_management/add_human",//数据请求的地址
            method: "POST",//ajax数据访问的方法
            data: post_data,
            dataType: "json",//s数据类型格式
            success: function (data_receive) {
                if (data_receive.status) {
                    toastr.success('新增成功')
                    $('#table_add').modal('hide')
                    $table.bootstrapTable('refresh');

                } else {
                    toastr.error('修改失败，可能是重复的账号！')
                    $table.bootstrapTable('refresh');

                }
            },
            error: function (data_receive) {
                toastr.error('数据提交失败，请刷新后再试')
                $('#table_add').modal('hide')
                $table.bootstrapTable('refresh');


            }

        })


    }


})


function reset_password(id) {
    let post_data = {
        'id': id,
    }
    $.ajax({
        url: "/test_management/reset_user_password",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        data: post_data,
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            if (data_receive.status) {
                toastr.success(data_receive.message)
                $table.bootstrapTable('refresh');

            } else {
                toastr.error('修改失败！')
                $table.bootstrapTable('refresh');

            }
        },
        error: function (data_receive) {
            toastr.error('数据提交失败，请刷新后再试')
            $table.bootstrapTable('refresh');


        }

    })
}

function delete_user(id) {
    let post_data = {
        'id': id,
    }
    $.ajax({
        url: "/test_management/delete_user_by_id",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        data: post_data,
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            if (data_receive.status) {
                toastr.success(data_receive.message)
                $table.bootstrapTable('refresh');

            } else {
                toastr.error('操作失败！')
                $table.bootstrapTable('refresh');

            }
        },
        error: function (data_receive) {
            toastr.error('数据提交失败，请刷新后再试')
            $table.bootstrapTable('refresh');


        }

    })
}