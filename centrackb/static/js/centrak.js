/* jshint -W014, laxcomma:true */

(function($) {
    'use strict';

    var handleThemePanelExpand = function() {
        $(document).on('click', '[data-click="filter-panel-expand"]', function () {
            var e = '.filter-panel',
            a = 'active';
            $(e).hasClass(a) ? $(e).removeClass(a) : $(e).addClass(a);
        });
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
                    'meter_status', 'meter_type', 'project_id', 'show_only', 
                    'sort_by', 'then_by'];
        
        var fname = null;
        for (var fn in fnames) {
            fname = fnames[fn];
            entry = $('[name=' + fname + ']').val();
            if (entry !== undefined && entry !== "") {
                query += (fname + "=" + entry + "&");
                
                // Note: applying keys that translate to 'Yet to be determined'
                // i.e. unknown & ytbd
                if (fname === 'acct_status' && entry === 'unknown') {
                    query += (fname + "=ytbd&");
                }
            }
        }
        
        if (query.substr(-1) === '&' || query.substr(-1) === '?')
            query = query.substring(0, query.length - 1);
        
        var pathname = window.location.pathname;
        window.location = pathname + '?' + encodeURI(query);
        return false;
    },

    handleCaptureExport = function(format) {
        var urlpath = window.location.toString()
        , pathname = window.location.pathname
        , urlpaths = urlpath.split('?');
        
        var target_url = '/export' + pathname;
        if (urlpaths.length === 1) {
            target_url += ('?' + format);
        } else {
            var tmp = urlpaths[1];
            if (tmp.substr(-1) === '#')
                tmp = tmp.substring(0, tmp.length - 1);
            target_url += ('?' + tmp + '&' + format);
        }
        window.location = target_url;
        return false;
    },

    handleUserProfileForm = function() {
        $('#form-pwd').validate();
        var form = $('#form-usr')
        , divt = $('.form-group.team')
        , txtt = divt.find('[name=team]');
        
        form.validate();
        form.find('[name=role]').bind('change', function(e){
            if ($(e.target).val() === 'team-lead') {
                txtt.attr('required', '');
                divt.removeClass('hide');
            } else {
                txtt.removeAttr('required');
                divt.addClass('hide');
                txtt.val('');
            }
        });
        
    };

    App = function () {
        return {
            init: function () {
                // init all select2
                $('.select2').select2();

                handleActivitySummaryRowToggle();
                handleThemePanelExpand();
            },

            initUserProfileForm: function() {
                handleUserProfileForm();
            },

            filterCapture: function() { 
                $('[name=filter]').bind('click', function () {
                    return handleCaptureFiltering();
                });
            },

            exportCapture: function() {
                $('[name=export_csv]').bind('click', function() {
                    return handleCaptureExport('format=csv');
                });
                $('[name=export_xls]').bind('click', function() {
                    return handleCaptureExport('format=xls');
                });
            },

            bindForUserManagement: function() {
                var self = this
                , _apiUrlPrefix = $('[name=_apiUrlPrefix]').attr('src');
                $('[name=activate_reg]').on('click', function() {
                    var code = $(this).data('registration-code')
                    , msg = 'Are you sure you want to activate this registration?'; 
                    
                    self.confirm(msg, function(result) {
                        if (result === true) {
                            $.ajax({
                                type: 'POST',
                                url: _apiUrlPrefix + 'users/activate',
                                data: {'registration-code': code},
                                success: function(data, status) {
                                    self.alert(data);
                                    var urlpath = window.location.pathname;				
                                    window.location.pathname = urlpath;
                                }
                            });
                        }
                    });
                });

                $('[name=delete_reg]').on('click', function() {
                    var code = $(this).data('registration-code')
                    , msg = 'Are you sure you want to delete this registration?';
                    
                    self.confirm(msg, function(result) {
                        if (result === true) {
                            $.ajax({
                                type: 'POST',
                                url: _apiUrlPrefix + 'registrations/' + code + '/delete',
                                success: function(data, status) {
                                    self.alert(data);
                                    var urlpath = window.location.pathname;
                                    window.location.pathname = urlpath;
                                }
                            });
                        }
                    });
                });
                
                $('[name=delete_user]').on('click', function() {
                    var username = $(this).data('username')
                      , msg = 'Are you sure you want to delete this account? This '
                            + 'operation cannot be undone.';
                    
                    self.confirm(msg, function(result) {
                        if (result === true) {
                            $.ajax({
                                type: 'POST',
                                url: _apiUrlPrefix + 'users/' + username + '/delete',
                                success: function(data, status) {
                                    self.alert(data);
                                    var urlpath = window.location.pathname;
                                    window.location.pathname = urlpath;
                                }
                            });
                        }
                    });
                });
            },
            confirm: function(question, callback) {
                var modal = $('#confirmModal')
                , result = null;
                modal.on('show.bs.modal', function(event){
                    modal.find('.modal-header h4').text('Confirm');
                    modal.find('.modal-body').text(question);
                    modal.find('.modal-footer .btn-primary').bind('click', function(){ result = true; modal.modal('hide'); });
                    modal.find('.modal-footer .btn-danger').bind('click', function() { result = false; });
                });
                modal.bind('hidden.bs.modal', function(event){
                    modal.find('.modal-footer .btn-primary').unbind('click');
                    modal.find('.modal-footer .btn-danger').unbind('click');
                    modal.unbind('hidden.bs.modal');
                    callback(result);
                });
                modal.modal({'show':true});
            },
            alert: function(message) {
                var modal = $('#alertModal');
                modal.on('show.bs.modal', function(event) {
                    modal.find('.modal-header h4').text('Alert');
                    modal.find('.modal-body').text(message);
                });
                modal.modal({'show':true});
            }
        };
    }();


    // extensions
    String.prototype.toTitleCase = function() {
        if (this && this.length > 0) {
            return this[0].toUpperCase() + this.substring(1).toLowerCase();
        }
        return this;
    };
    
    // initialize app
    App.init();
})(jQuery);
