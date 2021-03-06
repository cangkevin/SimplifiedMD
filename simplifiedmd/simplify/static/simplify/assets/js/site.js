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

function updateResultsWithEmpty() {
    var result = $('#result-area');
    var msg = "No content to summarize";
    result.text(msg).fadeIn('slow');
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
        else {
            updateResultsWithEmpty();
        }
    });
    
    var demo1 = new autoComplete({
					selector: '#hero-demo',
					minChars: 1,
					onSelect: function(e, term, item){
						$.ajax({
								type: 'POST',
								url: 'lookup/',
								beforeSend: function(xhr, settings) {
									var csrftoken = Cookies.get('csrftoken');
									
										if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
												xhr.setRequestHeader('X-CSRFToken', csrftoken);
										}
								},
								data: {
										'title': term,
								},
								dataType: 'json',
								error: function() {
										updateResultsWithError();
								},
								success: function(data) {
									updateResults(data)
									$('html, body').animate({ scrollTop: $('#results').offset().top }, 'slow');
								}
						});
					},
					source: function(term, suggest){
								$.ajax({
								type: 'POST',
								url: 'typeahead/',
								beforeSend: function(xhr, settings) {
									var csrftoken = Cookies.get('csrftoken');
									
										if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
												xhr.setRequestHeader('X-CSRFToken', csrftoken);
										}
								},
								data: {
										'title': term,
								},
								dataType: 'json',
								error: function() {
										updateResultsWithError();
								},
								success: function(data) {
										return suggest(data.results);
								}
						});
					}
				});
});
