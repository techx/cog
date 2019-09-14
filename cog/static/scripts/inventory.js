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
    $('#inventory-requests-count').text($('#my_requests tbody>tr').length);
}

$(document).ready(function() {
    init_request_actions();
    
    $('.ui.accordion').accordion({
        exclusive: false,
        onClosing: function() {
            var accordion = $(this).parent().attr("id");
            var $button = $("a[accordion='" + accordion + "']");
            $button.attr("mode", "expand");
            $button.html("<i class='plus icon'></i>&nbsp;Expand All");
        },
        onOpening: function() {
            var accordion = $(this).parent().attr("id");
            var $button = $("a[accordion='" + accordion + "']");
            $button.attr("mode", "collapse");
            $button.html("<i class='minus icon'></i>&nbsp;Collapse All");
        }
    });

    $(".expand-accordion").on("click", function(e) {
        var accordion_name = $(this).attr("accordion");
        var $accordion = $("#"+accordion_name);
        var size = $accordion.attr("size");

        if ($(this).attr("mode") == "expand") {
            for (var i=0; i<size; i++)
                $accordion.accordion("open", i);
            $(this).attr("mode", "collapse");
            $(this).html("<i class='minus icon'></i>&nbsp;Collapse All");
        }
        else {
            for (var i = 0; i < size; i++)
                $accordion.accordion("close", i);
            $(this).attr("mode", "expand");
            $(this).html("<i class='plus icon'></i>&nbsp;Expand All");
        }

        e.preventDefault();
    });

    $("#add-inventory").on("click", function() {
        $('#add-form').modal('show');
    }); 
    $("#autoadd-inventory").on("click", function() {
        $("#auto-add-form").modal("show");
    });

    $('.item-form').api({
        action: 'add item',
        method: 'POST',
        serializeForm: true,
        onSuccess: function (data) {
            setTimeout(function() {
                window.location.reload();
            }, 250);
        },
        onFailure: function (data) {
            $error = 
               $(this).closest('form').find('.message').first();
            $error.html(data.message);
            $error.show();
        }
    })
    .state({
        onActivate: function() {
          $(this).state('flash text');
        },
        text: {
          flash: 'Item Added!'
        }
    });

    $('.import-form').api({
        action: 'import items',
        method: 'POST',
        serializeForm: true,
        onSuccess: function(data) {
            setTimeout(function() {
                window.location.reload();
            });
        },
        onFailure: function (data) {
            var $error = $(this).closest('form').find('.message').first();
            $error.html(data.message);
            $error.show();
        }
    });

    $('.request-form .submit').api({
        action: 'submit request',
        method: 'POST',
        serializeForm: true,
        beforeSend: function(settings) {
            settings.data.item_id = $(this).data('item-id');
            return settings;
        },
        onError: function(error, element, xhr) {
            // handle redirects
            var json = xhr.responseJSON;
            if (xhr.status == 401 && 'redirect' in json) {
                window.location.href = location.protocol + '//' 
                    + document.domain + ':' + location.port + json['redirect'];  
            }
        },
        onFailure: function(data, element) {
            $error = 
               $(this).closest('form').find('.message').first();
            $error.html(data.message);
            $error.show();
        },
    })
    .state({
        onActivate: function() {
          $(this).state('flash text');
        },
        text: {
          flash: 'Item Requested!'
        }
    });

    $('.ui.sticky').sticky({
        context: '#inventory' 
    });

    $('select.dropdown').dropdown();

    $('#inventory-requests-toggle').click(() => {
        $('#inventory-requests-toggle, #inventory-requests').toggleClass('visible');
    });

    // var socket = io.connect(location.protocol + '//' + document.domain + ':' 
    //     + location.port + '/user');
    // socket.on('connect', function() {
    //     console.log('Socket connected!')
    //     socket.emit('', {data: 'I\'m connected!'});
    // });
    
    // socket.on('update', function(data) {
    //     if (data.requests) {
    //         $('#my_requests').fadeOut(100, function() {
    //             $(this).html(data.requests)
    //                 .fadeIn(100, init_request_actions);
    //             $('#inventory-requests-count').text($('#my_requests tbody>tr').length);
    //         });
    //     }
    // });
});