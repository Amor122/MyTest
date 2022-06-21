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
        url: '/test_management/get_test',   //请求后台的URL（*）
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
                title: '考试科目',
                sortable: true,
                field: 'subject',
                align: 'center',
                valign: 'middle'
            }, {
                title: '考试难度',
                sortable: true,
                searchable: true,
                field: 'difficulty',
                align: 'center',
                valign: 'middle',
            }, {
                title: '考试名称',
                searchable: true,
                field: 'test_name',
                align: 'center',
                valign: 'middle',
            }, {
                title: '开始时间',
                sortable: true,
                searchable: true,
                field: 'start_time',
                align: 'center',
                valign: 'middle',
                formatter: function (value, item, index) {
                    return value + ':00'

                }
            }, {
                title: '持续时长',
                field: 'duration',
                align: 'center',
                valign: 'middle',

            }, {
                title: '基本操作',
                field: 'edit',
                align: 'center',
                valign: 'middle',
                events: {
                    'click #edit': function (e, value, row, index) {
                        $('#test_id').val(row.id);
                        $('#test_name').val(row.test_name);
                        $('#difficulty').empty()
                        $('#subject').empty()
                        $('#start_time').val(row.start_time.replaceAll(' ', 'T'))
                        $('#duration').val(row.duration);

                        $.ajax({
                            url: "/test_management/get_test_selections",//数据请求的地址
                            method: "POST",//ajax数据访问的方法
                            dataType: "json",//s数据类型格式
                            success: function (data_receive) {
                                let difficulties = data_receive.difficulties
                                for (let index in difficulties) {
                                    if (difficulties[index] === row.difficulty) {
                                        $('#difficulty').append("<option selected value='" + difficulties[index] + "'>" + difficulties[index] + "</option>")
                                    } else {
                                        $('#difficulty').append("<option value='" + difficulties[index] + "'>" + difficulties[index] + "</option>")
                                    }
                                }
                                let subjects = data_receive.subjects
                                for (let index in subjects) {
                                    if (subjects[index] === row.subject) {
                                        $('#subject').append("<option selected value='" + subjects[index] + "'>" + subjects[index] + "</option>")
                                    } else {
                                        $('#subject').append("<option value='" + subjects[index] + "'>" + subjects[index] + "</option>")
                                    }
                                }

                            },
                            error: function () {
                                toastr.error('下拉框数据获取失败，请刷新后再试')

                            }

                        })
                        $('#table_edit').modal('show')
                    }
                },
                formatter: function (value, item, index) {
                    return "<button id='edit' class='btn btn-info btn-sm'  data-toggle='modal' data-target='#table_edit'>编辑</button>" +
                        '<button style="margin-left: 5px" class="btn btn-danger btn-sm" onclick=" if( confirm(\'确认删除该考试\') ) delete_test(\'' + item.id + '\')">删除</button>'
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

function edit_submit() {
    let form_data = {
        'test_id': $('#test_id').val(),
        'test_name': $('#test_name').val(),
        'difficulty': $('#difficulty').val(),
        'subject': $('#subject').val(),
        'start_time': $('#start_time').val(),
        'duration': $('#duration').val(),
    }
    console.log(form_data)
    $.ajax({
        url: "/test_management/edit_test_by_id",//数据请求的地址
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
                toastr.error('修改失败！')
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
    $('#difficulty_add').empty()
    $('#subject_add').empty()
    $.ajax({
        url: "/test_management/get_test_selections",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            let difficulties = data_receive.difficulties
            for (let index in difficulties) {
                $('#difficulty_add').append("<option value='" + difficulties[index] + "'>" + difficulties[index] + "</option>")
            }
            let subjects = data_receive.subjects
            for (let index in subjects) {
                $('#subject_add').append("<option value='" + subjects[index] + "'>" + subjects[index] + "</option>")
            }

        },
        error: function () {
            toastr.error('下拉框数据获取失败，请刷新后再试')
        }

    })
    $('#table_add').modal('show')
})

$('#table_add_submit').click(function () {
    let test_name_add = $('#test_name_add').val()
    let difficulty_add = $('#difficulty_add').val()
    let subject_add = $('#subject_add').val()
    let start_time_add = $('#start_time_add').val()
    let duration_add = $('#duration_add').val()
    if (!test_name_add || !difficulty_add || !subject_add || !start_time_add || !duration_add) {
        toastr.warning("参数不全")
    } else {
        let post_data = {
            'test_name_add': test_name_add,
            'difficulty_add': difficulty_add,
            'subject_add': subject_add,
            'start_time_add': start_time_add,
            'duration_add': duration_add,
        }
        $.ajax({
            url: "/test_management/add_test",//数据请求的地址
            method: "POST",//ajax数据访问的方法
            data: post_data,
            dataType: "json",//s数据类型格式
            success: function (data_receive) {
                if (data_receive.status) {
                    toastr.success('新增成功')
                    $('#table_add').modal('hide')
                    $table.bootstrapTable('refresh');

                } else {
                    if (data_receive.message) {
                        toastr.error(data_receive.message)
                    } else {
                        toastr.error('修改失败，可能是重复的！')
                    }
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


function delete_test(id) {
    let post_data = {
        'test_id': id,
    }
    $.ajax({
        url: "/test_management/delete_test_by_id",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        data: post_data,
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            if (data_receive.status) {
                toastr.success(data_receive.message)
                $table.bootstrapTable('refresh');

            } else {
                if (data_receive.message) {
                    toastr.error(data_receive.message)
                } else {
                    toastr.error('操作失败！')
                }
                $table.bootstrapTable('refresh');

            }
        },
        error: function (data_receive) {
            toastr.error('数据提交失败，请刷新后再试')
            $table.bootstrapTable('refresh');
        }

    })
}