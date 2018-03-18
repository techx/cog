$(document).ready(function() {
    $('.update-user').api({
        action: 'update user',
        method: 'POST',
        serializeForm: true,
        onFailure: function(data) {
            var $form = $(this).closest('form');
            var $error = $form.find('.message').first();
            $error.html(data.message);
            $error.show();

            if(data.user) {
                $('input[name="name"]', $form).val(data.user.name);
                $('input[name="phone"]', $form).val(data.user.phone);
                $('input[name="location"]', $form).val(data.user.location);
            }
        },
    })
    .state({
        onActivate: function() {
          $(this).state('flash text');
        },
        text: {
          flash: 'Info updated!'
        }
    });

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

    $('.request-action').api({
        method: 'POST',
        onSuccess: function(response) {
            window.location.reload();
        },
        onFailure: function(err) {
            console.log(err);
            alert(err.message)
        }
    });
});