<form method="post">
    <div class="panel panel-default">
        <div class="panel-heading">
            Projects
            <div class="pull-right">
                <div style="margin-top: -5px;">
                    <a href="/admin/projects/create" class="btn btn-default">Add</a>
                    <button type="submit" name="del" class="btn btn-danger">Delete</button>
                </div>
            </div>
        </div>
        <div class="panel-body">
            <table class="table panel-table">
                <thead>
                    <tr><th>Project</th>
                        <th>Registered XForms</th>
                    </tr>
                </thead>
                <tbody>
                % if records:
                    % for r in records:
                    <tr><td style="white-space:nowrap;"><a href="/admin/projects/{{ r.id }}/">{{ r.name }}</a></td>
                        <td>
                        % for f in r.xforms:
                            <a href="/admin/xforms/{{ f }}" style="margin-bottom:2px; display: inline-block;">
                                <span class="label label-info">{{ get_xform_title(f) }}</span>
                            </a>
                        % end
                        % for f in r.uforms:
                            <a href="/admin/xforms/{{ f }}" style="margin-bottom:2px; display: inline-block;">
                                <span class="label label-warning">{{ get_xform_title(f) }}</span>
                            </a>
                        % end
                        </td>
                    </tr>
                    % end
                % else:
                    <tr><td colspan="2">No data available.</td></tr>
                % end
                </tbody>
            </table>
        </div>
    </div>
</form>

% rebase('admin/base.tpl', title=title, year=year)