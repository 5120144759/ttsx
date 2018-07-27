function add_cart(id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/ttsx/add_cart/',
        type: 'post',
        data: {'goods_id': id},
        headers: {'X-CSRFToken': csrf},
        dataType: 'json',
        success: function (json) {
            if(json.code == 200){
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