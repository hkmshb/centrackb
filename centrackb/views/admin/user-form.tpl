<div class="panel panel-default">
    <div class="panel-heading">
        <b>User</b>
    </div>
    <div class="panel-body">
        <form method="post" class="form-horizontal">
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
                    <input type="text" class="form-control" name="email" required=""
                           value="{{ user.email_addr or '' }}" readonly="" />
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
</div
%rebase('admin/base.tpl', title=title, year=year)