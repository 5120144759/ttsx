function detail_add_cart(id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var num = $('#num').val();
    $.ajax({
        url: '/ttsx/detail_add_cart/',
        type: 'post',
        data: {'goods_id': id, 'num': num},
        headers: {'X-CSRFToken': csrf},
        dataType: 'json',
        success: function (json) {
            if (json.code == 200) {
                $('#show_count').html(json.sum)
                alert('添加成功')
            }
        },
        error: function (json) {
            alert('出了点小问题')
        }
    })
}

function add_num() {
    var num = $('#num').val();
    num = parseInt(num) + 1;
    $('#num').val(num)
    money()
}

function sub_num() {
    var num = $('#num').val();
    if (parseInt(num) > 1) {
        num = parseInt(num) - 1;
        $('#num').val(num)
    }
    money()
}

function money() {
    var num = $('#num').val();
    var price = $('#price em').html();
    price = parseFloat(price);
    num = parseInt(num);
    $('#total em').html(price*num)
}