% get = lambda x: x['$regex'][2:-2] or '' if x else ''
% selected = lambda x, y: 'selected=""' if x and (x['$regex'][2:-2] or '') == y else ''
% selected2 = lambda x, y: 'selected=""' if x == y else ''

<form class="form-stacked" method="get">
    <div class="filter-panel">
        <a href="javascript:;" data-click="filter-panel-expand" class="filter-collapse-btn">
            <i class="glyphicon glyphicon-filter"></i>
        </a>
        <div class="filter-panel-content">
            <h5 class="m-t-0">Filter Parameters</h5>
            <div class="divider"></div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Capture Date</div>
                <div class="col-md-7">
                    <div class="input-group date">
                        <input type="text" class="form-control" name="datetime_today" placeholder="yyyy-mm-dd" 
                               value="{{ get(q.datetime_today) }}" required="" disabled="">
                            <span class="input-group-addon btn" style="border-radius: 0 4px 4px 0;">
                                <i class="glyphicon glyphicon-th"></i>
                            </span>
                        </input>
                    </div>
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Feeder/Project</div>
                <div class="col-md-7">
                    <select name="project_id" class="form-control input-sm">
                        <option value="">&laquo; Select One &raquo;</option>
                    % for (value, text) in project_choices:
                        <option value="{{ value }}" {{! selected(q.project_id, value) }}>{{ text }}</option>
                    % end
                    </select>
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Enumerator ID</div>
                <div class="col-md-7">
                    <input type="text" class="form-control" name="enum_id" value="{{ get(q.enum_id)}}"/>
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Route Sequence</div>
                <div class="col-md-7">
                    <input type="text" class="form-control input-sm" name="rseq" value="{{ get(q.rseq) }}" />
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Account Status</div>
                <div class="col-md-7">
                    <select name="acct_status" class="form-control input-sm">
                        <option value="">&laquo; Select One &raquo;</option>
                    % for item in acct_status_choices:
                        <option value="{{ item[0] }}" {{! selected(q.acct_status, item[0]) }}>{{ item[1] }}</option>
                    % end
                    </select>
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Book Code</div>
                <div class="col-md-7">
                    <input type="text" class="form-control input-sm" name="book_code" 
                           value="{{ get(q.acct_no) }}" />
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Meter Status</div>
                <div class="col-md-7">
                    <select name="meter_status" class="form-control input-sm" placeholder="Select Meter Status">
                        <option value="">&laquo; Select One &raquo;</option>
                    % for item in meter_status_choices:
                        <option value="{{ item[0] }}" {{! selected(q.meter_status, item[0]) }}>{{ item[1] }}</option>
                    % end
                    </select>
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Meter Type</div>
                <div class="col-md-7">
                    <select name="meter_type" class="form-control input-sm">
                        <option value="">&laquo; Select One &raquo;</option>
                    % for item in meter_type_choices:
                        <option value="{{ item[0] }}" {{! selected(q.meter_type, item[0]) }}>{{ item[1] }}</option>
                    % end
                    </select>
                </div>
            </div>
            
            <div class="divider"></div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Show Only</div>
                <div class="col-md-7">
                    <select name="show_only" class="form-control input-sm">
                        <option value="">&laquo; Select One &raquo;</option>
                    % for (key, value) in capture_category_choices:
                        <option value="{{ key }}" {{! selected2(q.show_only, key) }}>{{ value }}</option>
                    % end
                    </select>
                </div>
            </div>
            
            % sort_choices = (('rseq', 'Route Sequence'), ('group', 'Enum. Group'), ('datetime_today', 'Capture Date'))
            <div class="divider"></div>
            <h5 class="m-t-0">Sort Parameters</h5>
            <div class="divider"></div>
            
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Sort By</div>
                <div class="col-md-7">
                    <select name="sort_by" class="form-control input-sm">
                        <option value="">&laquo; Select One &raquo;</option>
                        % for (v, t) in sort_choices:
                            <option value="{{ v }}" {{! selected2(q.sort_by, v) }}> {{ t }} </option>
                        % end
                    </select>
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Then By</div>
                <div class="col-md-7">
                    <select name="then_by" class="form-control input-sm">
                        <option value="">&laquo; Select One &raquo;</option>
                        % for (v, t) in sort_choices:
                            <option value="{{ v }}" {{! selected2(q.then_by, v) }}> {{ t }} </option>
                        % end
                    </select>
                </div>
            </div>
            <div class="divider"></div>
            
            <div class="row m-t-10">
                <div class="col-md-12">
                    <button type="submit" class="btn btn-default" name="filter">Apply</button>
                    <button type="reset" class="btn btn-default" name="reset">Clear</button>
                </div>
            </div>
        </div>
    </div>
</form>