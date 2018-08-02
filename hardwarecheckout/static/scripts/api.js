$.fn.api.settings.api = {
    'add item'          : '/inventory/add',
    'import items'      : '/inventory/autoadd',
    'update item'       : '/inventory/update/{id}',
    'return item'       : '/inventory/return/{id}', 
    'delete item'       : '/inventory/delete/{id}',
    'add subitem'       : '/inventory/subitem/add/{id}',
    'update subitem'    : '/inventory/subitem/update/{id}',
    'delete subitem'    : '/inventory/subitem/delete/{id}',
    'run all lotteries' : '/inventory/lottery/all',
    'run lottery'       : '/inventory/lottery/{id}',
    'submit request'    : '/request/submit',
    'cancel request'    : '/request/{id}/cancel',
    'approve request'   : '/request/{id}/approve',
    'fulfill request'   : '/request/{id}/fulfill/{userid}',
    'deny request'      : '/request/{id}/deny',
    'update user'       : '/user/{id}/update'
}

$.fn.api.settings.successTest = function(response) {
  if(response && response.success) {
    return response.success;
  }
  return false;
};
