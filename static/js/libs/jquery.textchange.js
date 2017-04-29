/*!
 * jQuery TextChange Plugin
 * http://www.zurb.com/playground/jquery-text-change-custom-event
 *
 * Copyright 2010, ZURB
 * Released under the MIT License
 */
(($ => {
	
	$.event.special.textchange = {
		
		setup(data, namespaces) {
		  $(this).data('lastValue', this.contentEditable === 'true' ? $(this).html() : $(this).val());
			$(this).bind('keyup.textchange', $.event.special.textchange.handler);
			$(this).bind('cut.textchange paste.textchange input.textchange', $.event.special.textchange.delayedHandler);
		},
		
		teardown(namespaces) {
			$(this).unbind('.textchange');
		},
		
		handler(event) {
			$.event.special.textchange.triggerIfChanged($(this));
		},
		
		delayedHandler(event) {
			var element = $(this);
			setTimeout(() => {
				$.event.special.textchange.triggerIfChanged(element);
			}, 25);
		},
		
		triggerIfChanged(element) {
		  var current = element[0].contentEditable === 'true' ? element.html() : element.val();
			if (current !== element.data('lastValue')) {
				element.trigger('textchange',  [element.data('lastValue')]);
				element.data('lastValue', current);
			}
		}
	};
	
	$.event.special.hastext = {
		
		setup(data, namespaces) {
			$(this).bind('textchange', $.event.special.hastext.handler);
		},
		
		teardown(namespaces) {
			$(this).unbind('textchange', $.event.special.hastext.handler);
		},
		
		handler(event, lastValue) {
			if ((lastValue === '') && lastValue !== $(this).val()) {
				$(this).trigger('hastext');
			}
		}
	};
	
	$.event.special.notext = {
		
		setup(data, namespaces) {
			$(this).bind('textchange', $.event.special.notext.handler);
		},
		
		teardown(namespaces) {
			$(this).unbind('textchange', $.event.special.notext.handler);
		},
		
		handler(event, lastValue) {
			if ($(this).val() === '' && $(this).val() !== lastValue) {
				$(this).trigger('notext');
			}
		}
	};	

}))(jQuery);