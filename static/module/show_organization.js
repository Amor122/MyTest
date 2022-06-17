const org_ul = document.getElementById('org')
//临时存放处，不然后续的document找不到元素
const temp_ul = document.getElementById('stack')

const start_obj = document.getElementById('start')
$.ajax({
    url: "/test_management/get_organization_dict_info",//数据请求的地址
    method: "POST",//ajax数据访问的方法
    // data: post_data,
    dataType: "json",//返回数据类型格式
    success: function (data_receive) {
        let start_org = data_receive.start_org
        console.log(start_org)
        if (start_org){
            start_ul = document.createElement('ul')
            for(let i in start_org){
                start_li= document.createElement('li')
                start_li.id = start_org[i]
                start_li.innerText = start_org[i]
                start_ul.append(start_li)
            }
            start_obj.append(start_ul)
        }
        let data_list = data_receive.data_list
        console.log(data_list)
        for (let index in data_list) {
            console.log(index, data_list[index])
            li = document.getElementById(index)
            if (li) {
                console.log(li)
            } else {
                console.log('not have'+index)
                li = document.createElement('li')
                li.id = index
                li.innerText = index
                temp_ul.append(li)
            }


            if (data_list[index].length) {
                new_item = data_list[index]
                new_ul = document.createElement('ul')
                for (let item_index in new_item) {
                    child_id = new_item[item_index]
                    console.log('child_id'+child_id+item_index)
                    obj = document.getElementById(child_id)
                    if (obj) {
                        console.log('已经有了'+child_id)
                        new_ul.append(obj)
                    } else {
                        console.log('还没有'+child_id)

                        new_li = document.createElement('li')
                        new_li.id = child_id
                        new_li.innerText = child_id
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
    },
    error: function () {
    }

})


