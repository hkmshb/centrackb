% menus = (('/admin/users/', 'Users'),
%          ('/admin/projects/', 'Projects'),
%          ('/admin/xforms/', 'XForms'),
%          ('/admin/feeders/', 'Feeders'),
%          ('/admin/stations/', 'Stations'))

<div class="panel panel-flat panel-menu panel-default">
    <ul class="list-group">
    % for m in menus:
        % path = '/%s/' % '/'.join(request.path.split('/')[1:3])
        % attr = ("active " if path == m[0] else "")
        <li class="{{ attr }}list-group-item"><a href="{{ m[0] }}"><div class="txt">{{ m[1] }}</div></a></li>
    % end
    </ul>
</div>