// https://stackoverflow.com/a/15651670
$.fn.filterByData = function(prop, val) {
    return this.filter(
        function() { return $(this).data(prop)==val; }
    );
}

$(function() {
    $('#toggle-mobile').click(() => {
        $('#primary-menu').toggleClass('visible');
    });
});