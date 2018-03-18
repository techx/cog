var socket = io.connect(location.protocol + '//' + document.domain + ':' 
    + location.port + '/admin');
socket.on('connect', function() {
    console.log('Socket connected!')
    socket.emit('', {data: 'I\'m connected!'});
});

socket.on('update', function(data) {
    if (data.approved_requests) {
        $('#approved_requests').fadeOut(250, function() {
            $(this).html(data.approved_requests)
                .fadeIn(250, init_request_actions);
        });
    }
    if (data.submitted_requests) {
        $('#submitted_requests').fadeOut(250, function() {
            $(this).html(data.submitted_requests)
                .fadeIn(250, init_request_actions);
        });
    }
    if (data.lottery_quantities) {
        q = data.lottery_quantities;
        for (var i = 0; i < data.lottery_quantities.length; i++) {
            q = data.lottery_quantities[i];
            var div = $('div[data-item-id='+q['id']+']');
            div.find('.item-quantity').html(q['available']);
            div.find('.submitted-quantity').html(q['submitted']);
        }
    }
});

function init_request_actions() {   
    $('.request-action').api({
        method: 'POST',
        onSuccess: function(response) {
        },
        onFailure: function(err) {
            console.log(err);
            alert(err.message)
        }
    });
}

$(document).ready(function() {
    init_request_actions();
    $('.run-lottery.button').api({
        method: 'POST',
        onSuccess: function(response) {
            // window.location.reload();
        },
        onFailure: function(err) {
            console.log("ERROR!");
            console.log(err);
        },
        onError: function(err) {
            console.log("ERROR!");
            console.log(err);
        }
    });

    $('.run-all-lottery.button').api({
        method: 'POST',
        onSuccess: function(response) {
        },
    });
});