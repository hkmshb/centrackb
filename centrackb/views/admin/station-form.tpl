<div class="panel panel-default">
    % is_new = (True if not station._id else False)
    <div class="panel-heading">
        <b>{{ "Create" if is_new else "Update" }} Station</b>
    </div>
    <div class="panel-body">
        <form method="post" class="form-horizontal">
            <div class="form-group">
                <label for="code" class="col-md-2 control-label">Source Feeder: </label>
                <div class="col-md-6">
                    <input type="hidden" name="source_feeder" value="{{ feeder.code or '' }}" />
                    <input class="form-control" name="source_feeder_text" required=""
                           disabled="" value="{{ feeder.voltage or '' }}KV {{ feeder.name or '' }}" />
                </div>
            </div>
            <div class="form-group">
                <label for="code" class="col-md-2 control-label">Code: </label>
                <div class="col-md-3">
                    <input type="text" class="form-control" name="code" required=""
                           maxlength="6" value="{{ station.code or '' }}" />
                </div>
            </div>
            <div class="form-group">
                <label for="code" class="col-md-2 control-label">Name: </label>
                <div class="col-md-6">
                    <input type="text" class="form-control" name="name" required=""
                           value="{{ station.name or '' }}" />
                </div>
            </div>
            <div class="form-group">
                <label for="code" class="col-md-2 control-label">Rating: </label>
                <div class="col-md-2">
                    <input type="integer" class="form-control" name="capacity" required=""
                           value="{{ station.capacity or '' }}" />
                </div>
                <div class="col-md-4">
                    <select class="form-control select2" name="vratio" required=""
                            data-placeholder="Select Voltage Ratio">
                        <option value=""></option>
                        % for i in vratio_choices:
                        <option value="{{ i[0] }}" {{'selected=""' if station.vratio == str(i[0]) else ''}}>{{ i[1] }}</option>
                        % end
                    </select>
                </div>
            </div>
            <div class="form-group">
                <div class="col-md-offset-2 col-md-6">
                    <label for="id_public" class="item-title">
                        % on = 'checked' if station.public else ''
                        <input type="checkbox" id="id_public" name="public" {{ on }} /> Is Public
                    </label>
                </div>
            </div>
            <div class="form-group">
                <div class="col-sm-offset-2 col-sm-6">
                    <button type="submit" class="btn btn-default">{{ "Save" if is_new else "Update" }}</button>
                    <button type="reset" class="btn btn-default">Clear</button>
                </div>
            </div>
            <input type="hidden" name="_id" value="{{ station._id or '' }}" />
        </form>
    </div>
</div>
%rebase('admin/base.tpl', title=title, year=year)