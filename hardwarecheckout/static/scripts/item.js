$(document).ready(function() {
    $('.item-form').api({
        action: 'update item',
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
          flash: 'Item updated!'
        }
    });

    $('select.dropdown').dropdown();

    $('.delete-item').api({
        action: 'delete item',
        method: 'POST',
        onSuccess: function (data) {
            window.location.replace($SCRIPT_ROOT + '/inventory');
        },
        onFailure: function(data) {
            var $error = $('#delete-error');
            $error.html(data.message);
            $error.show();
        }
    });

    $('.return-notice-btn').on('click', function() {
        window.location.reload();
    });

    $('.add-subitem').api({
        action: 'add subitem',
        method: 'POST',
        serializeForm: true,
        beforeSend: function(settings) {
            // for some reason the form is not working for me here, so I'm just gonna do it like this
            var newSubitemId = this.parentNode.getElementsByTagName('input')[0].value;

            settings.data.newSubitemId = newSubitemId;
            return settings;
        },
        onSuccess: function (data) {
            $error = 
               $(this).closest('form').find('.message').first();
            $error.hide();
            setTimeout(function() {
                window.location.reload();
            }, 250); 
        },
        onFailure: function(data) {
            $error = 
               $(this).closest('form').find('.message').first();
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

    $('.id-fulfill').api({
        action: 'fulfill request',
        method: 'POST',
        serializeForm: true,
        beforeSend: function(settings) {
            settings.data.collected_id = $(this).data('collected-id');
            return settings;
        },
        onSuccess: function(response) {
            setTimeout(function() {
                window.location.reload();
            }, 250);
        }
    });
});