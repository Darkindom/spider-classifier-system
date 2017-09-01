$(function() {

    $('#search-btn').bind('click', function() {
        var search_word = $('#search-input').val();

        var type = $('.input-type').val();

        if (type == 'all') {
            $.ajax({
                type: 'GET',
                url: '/papers/artificial/_search',
                success: function(res) {
                    $('.info').text(res);
                },
                contentType: "application/json",
            });
        }else if (type == 'title' || type == 'abstract' || type == 'author') {
            var data = {
                "query" : {
                    "match": {}
                }
            }
            data.query.match[type] = search_word;
            $.ajax({
                type: 'POST',
                url: '/papers/artificial/_search',
                data: JSON.stringify(data),
                success: function(res) {
                    $('.info').text(res);
                },
                contentType: "application/json",
            });
        }else if (type == 'field'){

        }



    })
})
