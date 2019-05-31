$(document).ready(function() {
    // enables items_list actions
    $('.item-action').api({
        method: 'POST',
        onSuccess: function (data) {
            $error = 
                $(this).closest('form').find('.message').first();
            $error.hide();

            if (data.return_id) 
                $('.return-notice').modal('show');
            else 
                setTimeout(function() {
                    window.location.reload();
                }, 250); 
        },
        onFailure: function(data) {
            $error = $('.message').filterByData('table-id', 
                $(this).data('table-id')).first();
            console.log($error);
            $error.html(data.message);
            $error.show();
        }
    });

    $('.return-notice-btn').on('click', function() {
        window.location.reload();
    });
});
