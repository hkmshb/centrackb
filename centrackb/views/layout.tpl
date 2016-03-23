<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - CENTrack</title>
    <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/bootstrap-datepicker3.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/select2.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/select2-bootstrap.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/site.css" />
    <script src="/static/js/modernizr-2.6.2.js"></script>
    % if defined('extra_head'):
        % extra_head()
    % end
</head>
<body ng-app="centrakApp">
    % authnz = get_authnz()
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a href="/" class="navbar-brand">CENTrack</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="/projects/">Projects</a></li>
                    <li><a href="/captures/">Captures</a></li>
                    <li><a href="/updates/">Updates</a></li>
                % if not authnz.user_is_anonymous and authnz.current_user.role in ('admin', 'moderator'):
                    <li><a href="/admin/">Admin</a></li>
                % end
                </ul>
                <div class="pull-right">
                    <ul class="nav navbar-nav">
                    % if authnz.user_is_anonymous:
                        <li><a href="/login">Log In</a></li>
                        <li class="separator"><span href="#">|</span></li>
                        <li><a href="/register">Register</a></li>
                    % else:
                        <li><a href="/profile">
                                <i class="glyphicon glyphicon-user"></i>
                                {{ authnz.current_user.username }}
                            </a>
                        </li>
                        <li class="separator"><span href="#">|</span></li>
                        <li><a href="/logout">Log Out</a></li>
                    % end
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <div class="container body-content {{ "front" if defined('is_front') else "not-front" }}">
        % messages = get_session()['messages']
        % msg_pass = messages.get('pass', None)
        % msg_fail = messages.get('fail', None)
        % msg_warn = messages.get('warn', None)

        % message_list = ((msg_pass, 'success'), (msg_fail, 'danger'), (msg_warn, 'warning'))

        % messages['pass'] = []
        % messages['fail'] = []
        % messages['warn'] = []

        % for entry in message_list:
          % if entry[0]:
        <div class="alert alert-{{entry[1]}} alert-dismissible">
            <button type="button" class="close" data-dismiss="alert">&times</button>
            <ul>
            % for m in entry[0]:
              <li>{{ m }}</li>
            % end
            </ul>
        </div>
          % end
        % end
        
        {{!base}}

        <hr />
        <footer>
            <p>&copy; {{ year }} - CENTrack<p>
        </footer>
    </div>
    
    <div class="modals">
        <div class="modal fade" tabindex="-1" id="confirmModal" role="dialog">
            <div class="modal-dialog modal-sm">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4>Confirm</h4>
                    </div>
                    <div class="modal-body">
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary">Yes</button>
                        <button type="button" class="btn btn-danger" data-dismiss="modal">No</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" tabindex="-1" id="alertModal" role="dialog">
            <div class="modal-dialog modal-sm">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4>Alert</h4>
                    </div>
                    <div class="modal-body">
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-xdismiss="modal">OK</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="/static/js/jquery-1.10.2.min.js"></script>
    <script src="/static/js/jquery.validate.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/bootstrap-datepicker.min.js"></script>
    <script src="/static/js/select2.full.min.js"></script>
    <script src="/static/js/centrak.js"></script>
    <script src="/static/js/datatable.js"></script>
    % if defined('extra_scripts'):
        % extra_scripts()
    % end
</body>
</html>