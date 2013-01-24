var InlineOrdering = {

    /**
     * Get list of elements that can be reordered
     *
     * At this point, only already existent records can be reordered (ie. where pk != '')
     *
     * @return Array
     * @todo Check if given record changed, and if so, make it reorderable
     * @todo Primary key might not be 'id' - better selector needed
     *
     */
    getOrderables: function () {
        var allInlineRows = InlineOrdering.jQuery('.inline-related'),
            i = 0,
            ids = [];
        
        for (i = 0; i < allInlineRows.length; i = i + 1) {
            if (InlineOrdering.jQuery('.order input, .field-order input', allInlineRows[i]).val()) {
                ids.push('#' + allInlineRows[i].id); 

            }
        }
        
        // this redundant way is required, so that proper order is maintained, 
        // otherwise orderables were returned in more or less random order
        return InlineOrdering.jQuery(ids.join(', ')); 
    },
    
    /**
     * Inits the jQuery UI D&D
     *
     */
    init: function (jQuery) {
        InlineOrdering.jQuery = $;
        // window.alert(InlineOrdering.jQuery().sortable());
        InlineOrdering.jQuery("div.inline-group").sortable({
            // axis: 'x',
            placeholder: 'ui-state-highlight',
            forcePlaceholderSize: 'true',
            items: InlineOrdering.getOrderables(),
            update: InlineOrdering.update
        });
        //jQuery("div.inline-group").disableSelection();
        
        InlineOrdering.jQuery('div.field-order').hide();
        InlineOrdering.jQuery('div.order').hide();
        InlineOrdering.jQuery('td.order input').hide();
        
        InlineOrdering.jQuery('.add-row a').click(InlineOrdering.update);
        
        InlineOrdering.getOrderables().css('cursor', 'move');

        InlineOrdering.update();
    },
    
    jQuery: null,
    
    /**
     * Updates the position field
     *
     */
    update: function () {
        InlineOrdering.getOrderables().each(function (i) {
            InlineOrdering.jQuery('input[id$=order]', this).val(i + 1);
            InlineOrdering.jQuery(this).find('h3 > span.position').remove();
            InlineOrdering.jQuery(this).find('h3').append('<span class="position">#' + (i + 1).toFixed() + '</span>');
        });
    }
    
};

jQuery(function () {
    InlineOrdering.init(jQuery);
});
