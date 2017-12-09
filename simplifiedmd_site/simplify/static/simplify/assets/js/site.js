function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function updateResults(data) {
    var result = $('#result-area');
    result.text(data.simplified_text).fadeIn('slow');
}

function updateResultsWithError() {
    var result = $('#result-area');
    var error = "Couldn't simplify the provided text";
    result.text(error).fadeIn('slow');
}

$(document).ready(function() {
    var csrftoken = Cookies.get('csrftoken');
    
    $("#slider").slider({
        min: 20,
        max: 80,
        step: 10,
        value: 50
    });
    
    $("#slider").on("slide", function(slideEvt) {
	    $("#sliderVal").text(slideEvt.value);
    });

    
    var btn = $('#simplify-btn');
    btn.click(function() {
        var text = $('#text-area').val()
        var len = $('#slider').val()
        
        if (text.length > 0) {
            $.ajax({
                type: 'POST',
                url: 'ajax/simplify/',
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader('X-CSRFToken', csrftoken);
                    }
                    $('#result-area').hide().promise().done(function() {
                        $('#loader').show();
                    });
                },
                data: {
                    'text': text,
                    'length': len,
                },
                dataType: 'json',
                error: function() {
                    $('#loader').hide().promise().done(updateResultsWithError());
                },
                success: function(data) {
                    $('#loader').hide().promise().done(updateResults(data));
                }
            });
        }
    }); 
});
