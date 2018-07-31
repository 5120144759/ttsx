function add_cart(id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/ttsx/add_cart/',
        type: 'post',
        data: {'goods_id': id},
        headers: {'X-CSRFToken': csrf},
        dataType: 'json',
        success: function (json) {
            if (json.code == 200) {
                $('#show_count').html(json.sum)
            }
        },
        error: function (json) {
            alert('出了点小问题')
        }
    })
}

$(function () {
    $.get('/ttsx/cart_num/', function (json) {
        $('#show_count').html(json.sum)
    })
});

function add_cart_goods(id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/ttsx/add_goods/',
        type: 'post',
        dataType: 'json',
        data: {'cart_id': id},
        headers: {'X-CSRFToken': csrf},
        success: function (json) {
            if (json.code == 200) {
                $('#num_' + id).val(json.c_num);
                getprice(json.c_num, json.price, id);
                get_count_price();
            }
        },
        error: function (json) {
            alert('出了点小问题')
        }
    })
}

function sub_cart_goods(id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/ttsx/sub_goods/',
        type: 'post',
        dataType: 'json',
        data: {'cart_id': id},
        headers: {'X-CSRFToken': csrf},
        success: function (json) {
            if (json.code == 200){
                $('#num_' + id).val(json.c_num);
                getprice(json.c_num, json.price, id);
                get_count_price();
            }
            if (json.code == 201){
                $('#ul_' + id).remove();
                get_count_price();
            }
        },
        error: function (json) {
            alert('出了点小问题')
        }
    })
}

function getprice(num, price, id) {
    p = num * price;
    p = p.toFixed(2);
    $('#subtotal_' + id).text(p);
}

function del_cart(id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/ttsx/del_cart/',
        type: 'post',
        dataType: 'json',
        data: {'cart_id': id},
        headers: {'X-CSRFToken': csrf},
        success: function (json) {
            if (json.code == 200){
                alert('删除成功');
                $('#ul_' + id).remove();
                get_count_price();
            }
        }
    })
}

function change(id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/ttsx/change/',
        type: 'post',
        dataType: 'json',
        data: {'cart_id': id},
        headers: {'X-CSRFToken': csrf},
        success: function (json) {
            if (json.code == 200){
                if (json.is_select){
                    $('#check_' + id).attr('checked', true)
                }else{
                    $('#check_' + id).attr('checked', false)
                }
                get_count_price();
            }
        },
        error: function (json) {
            alret('请求失败')
        }
    })
}

function get_count_price() {
    $.get('/ttsx/get_price/', function (json) {
        if(json.code == 200){
            $('#get_price').html(json.count_price)
        }
    })
}
get_count_price();