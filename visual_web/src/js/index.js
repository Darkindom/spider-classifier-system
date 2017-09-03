$(function() {
    $('#search-btn').bind('click', function() {
        $('.main-content').show();
        var search_word = $('#search-input').val();

        var type = $('.input-type').val();

        if (type == 'all') {
            $.ajax({
                type: 'GET',
                url: '/papers/_search',
                success: function(res) {
                    $('#result-list').html('');
                    let hits = res.hits.hits;
                    for (let i = 0; i < hits.length; i++) {
                        console.log(hits[i]);

                        let toList = `<ul class='mc-list'>`;

                        toList += `<li><a href=${hits[i]['_source'].url}>${hits[i]['_source'].title}</a></li>`;
                        let authors = '<li>';
                        if ( hits[i]['_source'].authors && hits[i]['_source'].authors[0] ) {
                            for (let j = 0; j < hits[i]['_source'].authors.length; j++) {
                                authors = authors + hits[i]['_source'].authors[j] + ', ';
                            }
                        }
                        authors += '</li>';
                        toList += authors + `<li>${hits[i]['_source'].fields}</li></ul>`;

                        $('#result-list').append(toList);
                    }
                },
                contentType: "application/json",
            });
        }else if (type == 'title' || type == 'abstract' || type == 'authors') {
            var data = {
                "query" : {
                    "match": {}
                }
            }
            data.query.match[type] = search_word;
            $.ajax({
                type: 'POST',
                url: '/papers/_search',
                data: JSON.stringify(data),
                success: function(res) {
                    $('#result-list').html('');
                    let hits = res.hits.hits;
                    for (let i = 0; i < hits.length; i++) {
                        console.log(hits[i]);

                        let toList = `<ul class='mc-list'>`;

                        toList += `<li><a href=${hits[i]['_source'].url}>${hits[i]['_source'].title}</a></li>`;
                        let authors = '<li>';
                        if ( hits[i]['_source'].authors && hits[i]['_source'].authors[0] ) {
                            for (let j = 0; j < hits[i]['_source'].authors.length; j++) {
                                authors = authors + hits[i]['_source'].authors[j] + ', ';
                            }
                        }
                        authors += '</li>';
                        toList += authors + `<li>${hits[i]['_source'].fields}</li></ul>`;

                        $('#result-list').append(toList);
                    }
                },
                contentType: "application/json",
            });
        }else if(type == 'fields') {
            var data = {
                "query" : {
                    "match_all": {}
                }
            }
            // data.query.match[type] = search_word;
            $.ajax({
                type: 'POST',
                url: '/papers/'+ search_word + '/_search',
                data: JSON.stringify(data),
                success: function(res) {
                    $('#result-list').html('');
                    let hits = res.hits.hits;
                    for (let i = 0; i < hits.length; i++) {
                        console.log(hits[i]);

                        let toList = `<ul class='mc-list'>`;

                        toList += `<li><a href=${hits[i]['_source'].url}>${hits[i]['_source'].title}</a></li>`;
                        let authors = '<li>';
                        if ( hits[i]['_source'].authors && hits[i]['_source'].authors[0] ) {
                            for (let j = 0; j < hits[i]['_source'].authors.length; j++) {
                                authors = authors + hits[i]['_source'].authors[j] + ', ';
                            }
                        }
                        authors += '</li>';
                        toList += authors + `<li>${hits[i]['_source'].fields}</li></ul>`;

                        $('#result-list').append(toList);
                    }
                },
                contentType: "application/json",
            });
        }
    })
})
