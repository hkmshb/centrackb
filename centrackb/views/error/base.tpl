<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/bootstrap-datepicker3.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/select2.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/select2-bootstrap.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/site.css" />
    <script src="/static/js/modernizr-2.6.2.js"></script>
    <style type="text/css">
        .content h1 { font-size: 98pt; font-weight: 1000; }
        .content p { font-size: 14pt; }
        .content {
            padding-top: 50px; 
            padding-bottom: 150px;
            text-align: center; 
        }
    </style>
</head>
<body ng-app="centrakApp">
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a href="/" class="navbar-brand">CENTrak</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="/projects/">Projects</a></li>
                    <li><a href="/captures/">Captures</a></li>
                    <li><a href="/updates/">Updates</a></li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container body-content {{ "front" if defined('is_front') else "not-front" }}">
        
        {{!base}}

        <hr />
        <footer>
            <p>&copy; {{ year }} - CENTrak<p>
        </footer>
    </div>
    
    <script src="/static/js/jquery-1.10.2.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
</body>
</html>