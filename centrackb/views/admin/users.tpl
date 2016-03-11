<form method="post">
    <div class="panel panel-default">
        <div class="panel-heading">
            <b>Active Users</b>
        </div>
        <div class="panel-body">
            <table class="table panel-table">
                <thead>
                    <tr><th>Username</th>
                        <th>Role</th>
                        <th>Email</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                % if records:
                    % for r in records:
                    <tr><td>{{ r.username }}</td>
                        <td>{{ r.role }}</td>
                        <td>{{ r.email_addr or '-' }}</td>
                        <td style="width:60px;">
                            <a href="/admin/users/{{ r.username }}/" name="edit_user" title="Edit User">
                                <i class="glyphicon glyphicon-edit"></i>
                            </a>
                            &nbsp;
                            <a href="#" name="delete_user" class="text-danger" 
                               data-username="{{ r.username }}" title="Delete User">
                                <i class="glyphicon glyphicon-remove"></i>
                            </a>
                        </td>
                    </tr>
                    % end
                % else:
                    <tr><td colspan="4">No data available.</td></tr>
                % end
                </tbody>
            </table>
        </div>
    </div>
    
    <div class="panel panel-warning">
        <div class="panel-heading">
            <b>Users Awaiting Activation</b>
        </div>
        <div class="panel-body">
            <table class="table panel-table">
                <thead>
                    <tr><th>Username</th>
                        <th>Role</th>
                        <th>Email</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                % if pending_records:
                    % for r in pending_records:
                    <tr><td>{{ r.username }}</td>
                        <td>{{ r.role }}</td>
                        <td>{{ r.email_addr }}</td>
                        <td style="width:60px">
                            <a href="#" name="activate_reg" title="Activate"
                               data-registration-code="{{ r.pending_registration }}">
                                <i class="glyphicon glyphicon-thumbs-up"></i>
                            </a>
                            &nbsp;
                            <a href="#" name="delete_reg" class="text-danger" title="Delete Registration"
                               data-registration-code="{{ r.pending_registration }}">
                                <i class="glyphicon glyphicon-remove"></i>
                            </a>
                        </td>
                    </tr>
                    % end
                % else:
                    <tr><td colspan="4">No data available.</td></tr>
                % end
                </tbody>
            </table>
        </div>
    </div>
</form>
% def scripts():
    <script type="text/javascript">
        App.bindForUserManagement();
    </script>
% end
% rebase('admin/base.tpl', title=title, year=year, extra_scripts=scripts)