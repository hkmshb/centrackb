var handleThemePanelExpand = function() {
    $(document).on('click', '[data-click="filter-panel-expand"]', function () {
        var e = '.filter-panel',
        a = 'active';
        $(e).hasClass(a) ? $(e).removeClass(a) : $(e).addClass(a)
    })
},
handleActivitySummaryRowToggle = function() {
    $('.activity-summary tr.agg-total > td > a').each(function () {
        var $this = $(this)
          , target = $this.data('target');

        $this.on('click', function () {
            $('[data-group="' + target + '"]').each(function () {
                $(this).toggle();
            });
        });
    });
},
handleCaptureFiltering = function() {
    var query = "", entry = ""
      , fnames = ['datetime_today', 'enum_id', 'rseq', 'acct_status', 'acct_no',
                  'meter_status', 'meter_type', 'project_id', 'show_duplicate', 
                  'sort_by', 'then_by'];
    
    for (fn in fnames) {
        entry = $('[name=' + fnames[fn] + ']').val();
        if (entry !== undefined && entry !== "") {
            query += (fnames[fn] + "=" + entry + "&");
        }
    }
        
    if (query.substr(-1) === '&' || query.substr(-1) === '?')
    	query = query.substring(0, query.length - 1);
    
    var pathname = window.location.pathname;
    window.location = pathname + '?' + encodeURI(query);
    return false;
};
handleCaptureExport = function() {
	var urlpath = window.location.toString()
	  , pathname = window.location.pathname
	  , urlpaths = urlpath.split('?')
	  , format = 'format=csv';
	
	var target_url = '/export' + pathname;
	if (urlpaths.length === 1)
		target_url += ('?' + format);
	else
		target_url += ('?' + urlpaths[1] + '&' + format);
	
	window.location = target_url;
	return false;
}

App = function () {
    'use strict';
    return {
        init: function () {
            // init all select2
            $('.select2').select2();

            handleActivitySummaryRowToggle(),
            handleThemePanelExpand()
        },
        filterCapture: function() { 
            $('[name=filter]').on('click', function () {
                return handleCaptureFiltering();
            });
        },
        exportCapture: function() {
            $('[name=export_csv]').on('click', function() {
                return handleCaptureExport();
            });
        }
    }
}();


// extensions
String.prototype.toTitleCase = function() {
	if (this && this.length > 0) {
		return this[0].toUpperCase() + this.substring(1).toLowerCase();
	}
	return this;
};


(function ($) {
    App.init();
})(jQuery);
