<div class="panel panel-default">
    % is_new = (True if not project._id else False)
    <div class="panel-heading">{{ "Create" if is_new else "Update"}} Project</div>
    <div class="panel-body">
        <form method="post" class="form-horizontal">
            <div class="form-group">
                <label for="id" class="col-md-2 control-label">Project Id: </label>
                <div class="col-md-6">
                    <input type="text" class="form-control" name="id" required="required"
                           value="{{ project.id or '' }}" />                    
                </div>
            </div>
            <div class="form-group">
                <label for="name" class="col-md-2 control-label">Name: </label>
                <div class="col-md-6">
                    <input type="text" class="form-control" name="name" required="required"
                           value="{{ project.name or '' }}" /> 
                </div>
            </div>
            <div class="form-group">
                <label for="xforms" class="col-md-2 control-label">XForms: </label>
                <div class="col-md-6">
                    <select class="form-control select2" name="xforms" multiple="multiple"
                            data-placeholder="Select Capture Form">
                    % for f in xforms:
                        % on = ('selected="selected"' if f.id_string in project.xforms else '')
                        <option value="{{ f.id_string }}" {{ on }}>{{ f.title }}</option>
                    % end
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label for="xforms" class="col-md-2 control-label">UForms: </label>
                <div class="col-md-6">
                    <select class="form-control select2" name="uforms" multiple="multiple"
                            data-placeholder="Select Update Form">
                    % for f in uforms:
                        % on = ('selected=""' if f.id_string in project.uforms else '')
                        <option value="{{ f.id_string }}" {{ on }}>{{ f.title }}</option>
                    % end
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label for="is_active" class="col-md-2 control-label">Active: </label>
                <div class="col-md-6">
                    <label name="is_active">
                        <input type="checkbox" name="active" class="form-control"
                               {{'checked=""' if project.active == True else '' }} />
                    </label>
                </div>
            </div>
            <div class="form-group">
                <div class="col-sm-offset-2 col-sm-6">
                    <button type="submit" class="btn btn-default">{{ "Save" if is_new else "Update" }}</button>
                    <button type="reset" class="btn btn-default">Clear</button>
                </div>
            </div>
            <input type="hidden" name="_id" value="{{ project._id or ''}}" />
        </form>
    </div>
</div>
% rebase('admin/base.tpl', title=title, year=year)