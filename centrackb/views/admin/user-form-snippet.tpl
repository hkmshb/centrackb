<div class="panel panel-default">
    <div class="panel-heading">
        <b>{{ title }}</b>
    </div>
    <div class="panel-body">
        <form id="form-usr" method="post" class="form-horizontal">
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
                           value="{{ user.email_addr or '' }}" {{ 'readonly=""' if readonly else ''}} />
                </div>
            </div>
            <div class="form-group">
                <label for="role" class="col-md-2 control-label">Role: </label>
                <div class="col-md-6">
                    <select id="role" name="role" class="form-control" {{'disabled=""' if readonly else ''}} >
                        <option value="">&laquo; Select One &raquo;</option>
                    % for text, value in roles:
                        <option value="{{ text }}" {{ 'selected=""' if user.role == text else ''}}>{{ text }}</option>
                    % end
                    </select>
                </div>
            </div>
            <div class="form-group team {{'hide' if user.role != 'team-lead' else ''}}">
                <label for="team" class="col-md-2 control-label">Team: </label>
                <div class="col-md-6">
                    <input type="text" class="form-control" name="team" required="" min-length="1"
                           value="{{ user.team or '' }}" {{ 'readonly=""' if readonly else ''}} />
                </div>
            </div>
            <div class="form-group {{ 'hide' if readonly else '' }}">
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
        <form id="form-pwd" method="post" action="{{ action_url }}" class="form-horizontal">
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