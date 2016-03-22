<div class="panel panel-default">
    <div class="panel-heading">
        <b>User</b>
    </div>
    <div class="panel-body">
        <form method="post" class="form-horizontal">
            <input type="hidden" name="redirect_url" value="{{ redirect_url }}" />
            <div class="form-group">
                <label for="username" class="col-md-2 control-label">Username: </label>
                <div class="col-md-6">
                    <input type="text" class="form-control" name="username" required=""
                           value="{{ user.username or '' }}" readonly="" />
                </div>
            </div>
            <div class="form-group">
                <label for="username" class="col-md-2 control-label">Email: </label>
                <div class="col-md-6">
                    <input type="email" class="form-control" name="email_addr" required=""
                           value="{{ user.email_addr or '' }}" />
                </div>
            </div>
            <div class="form-group">
                <label for="role" class="col-md-2 control-label">Role: </label>
                <div class="col-md-6">
                    <select id="role" name="role" class="form-control">
                        <option value="">&laquo; Select One &raquo;</option>
                    % for text, value in roles:
                        <option value="{{ text }}" {{ 'selected=""' if user.role == text else ''}}>{{ text }}</option>
                    % end
                    </select>
                </div>
            </div>
            <div class="form-group">
                <div class="col-sm-offset-2 col-sm-6">
                    <button type="submit" class="btn btn-default">Update</button>
                </div>
            </div>
        </form>
    </div>
</div>

<div class="panel panel-warning">
    <div class="panel-heading">
        <b>Change Password</b>
    </div>
    <div class="panel-body">
        <form id="form-pwd" method="post" action="change_password" class="form-horizontal">
            <input type="hidden" name="redirect_url" value="{{ redirect_url }}" />
            <div class="form-group">
                <label for="password" class="col-md-2 control-label">Password: </label>
                <div class="col-md-6">
                    <input type="password" name="password" class="form-control" required=""  />
                </div>
            </div>
            <div class="form-group">
                <label for="confirm_password" class="col-md-2 control-label">Confirm Password: </label>
                <div class="col-md-6">
                    <input type="password" name="confirm_password" class="form-control" required="" 
                           data-rule-equalto="[name=password]"  />
                </div>
            </div>
            <div class="form-group">
                <div class="col-sm-offset-2 col-sm-6">
                    <button type="submit" class="btn btn-warning">Change</button>
                </div>
            </div>
        </form>
    </div>
</div>
% def ex_scripts():
    <script type="text/javascript">
        (function($) {
            $(function() {
                $('#form-pwd').validate();
            });
        })(jQuery);
    </script>
% end
%rebase('admin/base.tpl', title=title, year=year, extra_scripts=ex_scripts)