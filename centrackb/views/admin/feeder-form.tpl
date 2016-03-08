<div class="panel panel-default">
    % is_new = (True if not feeder._id else False)
    <div class="panel-heading">{{ "Create" if is_new else "Update"}} Feeder</div>
    <div class="panel-body">
        <form method="post" class="form-horizontal">
            <div class="form-group">
                <label for="code" class="col-md-2 control-label">Code: </label>
                <div class="col-md-6">
                    <input type="text" class="form-control" name="code" required=""
                            maxlength="4" value="{{ feeder.code or '' }}" />
                </div>
            </div>
            <div class="form-group">
                <label for="code" class="col-md-2 control-label">Name: </label>
                <div class="col-md-6">
                    <input type="text" class="form-control" name="name" required=""
                           value="{{ feeder.name or '' }}" />
                </div>
            </div>
            <div class="form-group">
                <label for="voltage" class="col-md-2 control-label">Voltage: </label>
                <div class="col-md-6">
                % for k in ['11', '33']:
                % on = 'checked=""' if feeder.voltage == k else ''
                    <label class="radio-inline">
                        <input type="radio" name="voltage" value="{{ k }}" {{ on }}>{{k}}KV</input>
                    </label>
                % end
                </div>
            </div>
            <div class="form-group">
                <label for="code" class="col-md-2 control-label">Source: </label>
                <div class="col-md-6">
                    <select class="form-control select2" name="source_station"
                            data-placeholder="Select Source Station">
                    </select>
                </div>
            </div>

            <div class="form-group">
                <div class="col-sm-offset-2 col-sm-6">
                    <button type="submit" class="btn btn-default">{{ "Save" if is_new else "Update" }}</button>
                    <button type="reset" class="btn btn-default">Clear</button>
                </div>
            </div>
            <input type="hidden" name="_id" value="{{ feeder._id or '' }}" />
        </form>
    </div>
</div>
% rebase('admin/base.tpl', title=title, year=year)