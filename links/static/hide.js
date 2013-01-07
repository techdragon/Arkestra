$(document).ready(function() {
    $('#id_links_item-0-manual_url').closest('div').addClass('manual-url').hide();
    // $('#id_links_item-1-manual_url').closest('div').addClass('method_options').hide();

    $('#id_links_item-0-destination_content_type').change(function() {
        $('div.manual-url').hide();
        if ($(this).val() == 40) {$('div.manual-url').show()} ;
    });
});
