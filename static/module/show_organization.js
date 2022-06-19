const org_ul = document.getElementById('org');
//临时存放处，不然后续的document找不到元素
const temp_ul = document.getElementById('stack');
const start_obj = document.getElementById('start');
$.ajax({
    url: "/test_management/get_organization_dict_info",//数据请求的地址
    method: "POST",//ajax数据访问的方法
    // data: post_data,
    dataType: "json",//返回数据类型格式
    success: function (data_receive) {

        function edit_organization(element_name) {
            console.log('doubleclick');
            $('#double_click_edit').modal('hide');
            let post_data = {
                'org_name': element_name
            };
            $.ajax({
                url: "/test_management/get_organization_by_name",//数据请求的地址
                method: "POST",//ajax数据访问的方法
                data: post_data,
                dataType: "json",//返回数据类型格式
                success: function (new_data) {
                    if (new_data.status) {
                        toastr.success(new_data.message)
                        data_dict = new_data.data_dict;
                        $('#organization_id').val(data_dict.organization_id)
                        $('#organization_name').val(data_dict.organization_name)
                        $('#organization_type').empty()
                        $('#up_organization').empty()
                        let organization_list = new_data.organization_list

                        if (data_dict.up_organization) {
                            $('#up_organization').append("<option  value='" + '------' + "'>" + '------' + "</option>")
                        } else {
                            $('#up_organization').append("<option selected value='" + '------' + "'>" + '------' + "</option>")
                        }
                        for (let org in organization_list) {

                            if (organization_list[org] === data_dict.up_organization) {
                                $('#up_organization').append("<option selected value='" + organization_list[org] + "'>" + organization_list[org] + "</option>")

                            } else {
                                $('#up_organization').append("<option value='" + organization_list[org] + "'>" + organization_list[org] + "</option>")
                            }
                        }
                        if (data_dict.organization_type) {
                            $('#organization_type').append("<option  value='" + '------' + "'>" + '------' + "</option>")
                        } else {
                            $('#organization_type').append("<option selected value='" + '------' + "'>" + '------' + "</option>")
                        }


                        let organization_type_list = new_data.organization_type_list;
                        for (let org in organization_type_list) {
                            if (organization_type_list[org] === data_dict.organization_type) {

                                $('#organization_type').append("<option selected value='" + organization_type_list[org] + "'>" + organization_type_list[org] + "</option>")

                            } else {
                                $('#organization_type').append("<option value='" + organization_type_list[org] + "'>" + organization_type_list[org] + "</option>")
                            }
                        }

                        $('#double_click_edit').modal('show');

                    } else {
                        toastr.error(new_data.message)
                    }

                }
            });


        }

        let start_org = data_receive.start_org;
        console.log(start_org);
        if (start_org) {
            start_ul = document.createElement('ul');
            for (let i in start_org) {
                start_li = document.createElement('li');
                start_li.id = start_org[i];
                start_li.innerText = start_org[i];
                start_ul.append(start_li)
            }
            start_obj.append(start_ul)
        }
        let data_list = data_receive.data_list;
        console.log(data_list);
        for (let index in data_list) {
            console.log(index, data_list[index]);
            li = document.getElementById(index);
            if (li) {
                console.log(li)
            } else {
                console.log('not have' + index);
                li = document.createElement('li');
                li.id = index;
                li.innerText = index;
                temp_ul.append(li)
            }


            if (data_list[index].length) {
                new_item = data_list[index];
                new_ul = document.createElement('ul');
                for (let item_index in new_item) {
                    child_id = new_item[item_index];
                    console.log('child_id' + child_id + item_index);
                    obj = document.getElementById(child_id);
                    if (obj) {
                        console.log('已经有了' + child_id);
                        new_ul.append(obj)
                    } else {
                        console.log('还没有' + child_id);
                        new_li = document.createElement('li');
                        new_li.id = child_id;
                        new_li.innerText = child_id;
                        new_ul.append(new_li)
                    }
                }
                li.append(new_ul)
            }
        }

        $("#org").jOrgChart({
            chartElement: '#chart',
            // dragAndDrop: true
        });
        prettyPrint();

        nodes = document.getElementsByClassName('node');
        nodes.forEach(function (element) {
            console.log(element.innerText);
            element.ondblclick = function () {
                edit_organization(element.innerText)
            }

        });
    },
    error: function () {
    }

});

function delete_organization() {
    let post_data = {
        'organization_id': $('#organization_id').val(),
    };
    $.ajax({
        url: "/test_management/delete_organization_by_id",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        data: post_data,
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            if (data_receive.status) {
                toastr.success(data_receive.message);
                window.location.reload()

            } else {
                if (data_receive.message) {
                    toastr.error(data_receive.message)
                } else {
                    toastr.error('操作失败！')
                }
                window.location.reload()

            }
        },
        error: function (data_receive) {
            toastr.error('数据提交失败，请刷新后再试')


        }

    })
}

function edit_organization() {
    let post_data = {
        'organization_id': $('#organization_id').val(),
        'organization_name': $('#organization_name').val(),
        'organization_type': $('#organization_type').val(),
        'up_organization': $('#up_organization').val(),
    };
    $.ajax({
        url: "/test_management/edit_organization_by_id",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        data: post_data,
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            if (data_receive.status) {
                toastr.success(data_receive.message);
                window.location.reload()

            } else {
                if (data_receive.message) {
                    toastr.error(data_receive.message)
                } else {
                    toastr.error('操作失败！')
                }
                window.location.reload()

            }
        },
        error: function (data_receive) {
            toastr.error('数据提交失败，请刷新后再试')


        }

    })
}

function add_organization() {
    let post_data = {
        'organization_name': $('#organization_name_add').val(),
        'organization_type': $('#organization_type_add').val(),
        'up_organization': $('#up_organization_add').val(),
    };
    $.ajax({
        url: "/test_management/add_organization",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        data: post_data,
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            if (data_receive.status) {
                toastr.success(data_receive.message);
                window.location.reload()

            } else {
                if (data_receive.message) {
                    toastr.error(data_receive.message)
                } else {
                    toastr.error('操作失败！')
                }
                window.location.reload()

            }
        },
        error: function (data_receive) {
            toastr.error('数据提交失败，请刷新后再试')


        }

    })
}


//新增组织按钮点击实现
$('#table_add_button').click(function () {
    $('#organization_type_add').empty()
    $('#up_organization_add').empty()
    $.ajax({
        url: "/test_management/get_organizations",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            let organization_list = data_receive.organization_list
            $('#up_organization_add').append("<option value='" + '------' + "'>" + '------' + "</option>")

            for (let org in organization_list) {
                $('#up_organization_add').append("<option value='" + organization_list[org] + "'>" + organization_list[org] + "</option>")

            }

        },
        error: function () {
            toastr.error('组织数据获取失败，请刷新后再试')

        }
    })
    $.ajax({
        url: "/test_management/get_organization_types",//数据请求的地址
        method: "POST",//ajax数据访问的方法
        dataType: "json",//s数据类型格式
        success: function (data_receive) {
            let organization_type_list = data_receive.organization_type_list
            $('#organization_type_add').append("<option value='" + '------' + "'>" + '------' + "</option>")

            for (let pos in organization_type_list) {
                $('#organization_type_add').append("<option value='" + organization_type_list[pos] + "'>" + organization_type_list[pos] + "</option>")
            }
        },
        error: function () {
            toastr.error('职位数据获取失败，请刷新后再试')

        }

    })

    $('#add_organization_button').modal('show')
})