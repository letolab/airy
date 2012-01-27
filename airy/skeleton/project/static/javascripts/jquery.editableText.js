/**
 * editableText plugin that uses contentEditable property (FF2 is not supported)
 * Project page - http://github.com/valums/editableText
 * Copyright (c) 2009 Andris Valums, http://valums.com
 * Licensed under the MIT license (http://valums.com/mit-license/)
 */
(function(){
    /**
     * The dollar sign could be overwritten globally,
     * but jQuery should always stay accesible
     */
    var $ = jQuery;
	/**
     * Extending jQuery namespace, we
     * could add public methods here
     */
	$.editableText = {};
    $.editableText.defaults = {		 
		/**
		 * Pass true to enable line breaks.
		 * Useful with divs that contain paragraphs.
		 */
		newlinesEnabled : false,
		/**
		 * Event that is triggered when editable text is changed
		 */
		changeEvent : 'change'
	};   		
	/**
	 * Usage $('selector).editableText(optionArray);
	 * See $.editableText.defaults for valid options 
	 */		
    $.fn.editableText = function(options){
        var options = $.extend({}, $.editableText.defaults, options);
        
        return this.each(function(){
             // Add jQuery methods to the element
            var editable = $(this);
            
			/**
			 * Save value to restore if user presses cancel
			 */
			editable.data('prevValue', editable.html());
			
            editable.click(function() {
                startEditing();
                editable.focus();
            });

            editable.focusout(function() {
                stopEditing();
            });
			
			if (!options.newlinesEnabled){
				// Prevents user from adding newlines to headers, links, etc.
				editable.keypress(function(event){
					// event is cancelled if enter is pressed
					return event.which != 13;
				});
                editable.keyup(function(event) {
                    if (event.keyCode == 13) {
                        stopEditing();
                        return false;
                    }
                    if (event.keyCode == 27) {
                        stopEditing(true);
                    }
                });
			}
			
			/**
			 * Makes element editable
			 */
			function startEditing(){
                if ($('.editing-content').not(editable).length > 0) {
                    stopEditing(true);
                }
	            editable.attr('contentEditable', true);
                editable.addClass('editing-content');
                editable.data('prevValue', editable.html());
			}
			/**
			 * Makes element non-editable
			 */
			function stopEditing(cancel){
                editable.attr('contentEditable', false);
                editable.removeClass('editing-content');
                if (cancel) {
                    editable.html(editable.data('prevValue'));
                } else {
                    editable.trigger(options.changeEvent);
                }
			}
        });
    }
})();