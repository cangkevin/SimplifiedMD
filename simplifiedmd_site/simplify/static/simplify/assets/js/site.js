function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function updateResults(data) {
    var result = $('#result-area');
    result.text(data.simplified_text);
}

function updateResultsWithError() {
    var result = $('#result-area');
    var error = "Couldn't simplify the provided text";
    result.text(error);
}

$(document).ready(function() {
    var csrftoken = Cookies.get('csrftoken');
    var btn = $('#simplify-btn');
    btn.click(function() {
    
        var text = $('#text-area').val()
        if (text.length != 0) {
            $.ajax({
                type: "POST",
                url: 'ajax/simplify/',
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                data: {
                    'text': text
                },
                dataType: 'json',
                error: function() {
                    updateResultsWithError()
                },
                success: function(data) {
                    updateResults(data)
                }
            }); 
        }
    });
    
});
