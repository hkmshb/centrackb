<div class="row" ng-controller="CaptureViewCtrl" style="min-height: 500px;">
    <div class="col-md-2 affix side-dash" style="padding-right: 30px">
        <h5 style="text-transform:uppercase; font-weight:bold;"> &nbsp; </h5>
        <div class="panel panel-default panel-compressed">
            <div class="panel-body identical-entries">
                <div class="panel-section section">
                    <ul class="duplicates">
                        <li class="item">
                            <label for="id_clear">
                                <input type="radio" id="id_clear" name="entry" value="" /> Clear Selection
                            </label>
                        </li>
                        <li><h6>Duplicates</h6></li>
                    % if duplicates:
                        % for d in duplicates:
                        <li class="item">
                            <label for="id_{{ d._id }}">
                                <input type="radio" id="id_{{ d._id }}" name="entry" data-type="duplicate" value="{{ d._id }}" /> {{ d.rseq }} 
                            </label>
                        </li>
                        % end
                    % else:
                        <li>None Found</li>
                    % end
                        
                        <li><h6>Updates</h6></li>
                    % if defined('updates') and updates:
                        % for u in updates:
                        <li class="item">
                            <label for="id_{{ u._id }}">
                                <input type="radio" id="id_{{ u._id }}" name="entry" data-type="update" value="{{ u._id }}" /> {{ u.rseq }}
                            </label>
                        </li>
                        % end
                    % else:
                        <li>None Found</li>
                    % end
                    </ul>
                </div>
            </div>
        </div>
    </div>
    
    <div class="section col-md-5 col-md-offset-2 l-view">
        &nbsp;
    </div>
    <div class="section col-md-5 compared-item r-view">
        &nbsp;
    </div>
</div>

% def scripts():
    <script src="/static/ng/angular.min.js"></script>
    <script src="/static/ng/app.js"></script>
    <script src="/static/ng/controllers.js"></script>
    <script src="/static/ng/directives.js"></script>
    
    <!-- script template -->
  <script type="text/ng-template" id="capture_snippet">
    <div class="capture-form">
        <div class="capture-ctrl clearfix">
            <h5 class="section-head pull-left">Entry</h5>
            <div class="control-btns full-right text-right">
                <label for="id_:{ prefix }:drop">
                    <input type="checkbox" id="id_:{ prefix }:drop" name="dropped" ng-model="capture['dropped']" />  <span>Dropped</span>
                </label>
                <a name="save" class="btn btn-default" title="Save"><i class="glyphicon glyphicon-floppy-disk"></i></a>
                <a name="expand" class="btn btn-default" title="Expand All"><i class="glyphicon glyphicon-resize-full"></i></a>
            </div>
        </div>
        <div class="capture-body">
            <form method="post" class="form-horizontal form-compressed">
                <div class="panel-group" id="accordion_:{ title }:">
                    <div class="panel panel-default panel-compressed" ng-repeat="(title, meta) in _meta.fields">
                        <div class="panel-heading" ng-if="title !== 'capture'">
                            <h4 class="panel-title">
                                <a role="button" data-toggle="collapse" data-parent="#accordion_:{ title }:" href=".collapse_:{ title }:"
                                   ng-click="toggle_pane(title)">
                                  :{ title }:
                                </a>
                            </h4>
                        </div>
                        <div class="collapse_:{ title }: panel-collapse" ng-class="{'collapse': title !== 'capture'}">
                            <div class="panel-body">
                                <div class="form-group" ng-repeat="(field, label) in meta">
                                    <label for="id_:{field}:" class="col-md-4 col-sm-4 control-label">:{ label }:: </label>
                                    
                                    <div class="col-md-8 col-sm-8" ng-if="field[0] == '_' || title == 'meta'">
                                        <label ng-if="title != 'meta'" id="id_:{ field }:" name=":{ field }:" class="form-control-static">:{ capture[field.substr(1)] }:</label>
                                        <label ng-if="title == 'meta' && field != 'snapshots'" id="id_:{ field }:" name=":{ field }:" class="form-control-static">:{ capture[field] }:</label>
                                        <textarea ng-if="title == 'meta' && field == 'snapshots'" id="id_:{ field }:" class="form-control snapshot-text" rows="20" readonly>:{ capture['snapshots']['original']['capture'] }:</textarea>
                                    </div>
                                    
                                    <div class="col-md-8 col-sm-8" ng-if="_meta.widgets.select.indexOf(field) > -1">
                                        <select id="id_:{ field }:" name=":{ field }:" class="form-control" ng-model="capture[field]"
                                                ng-if="!is_update_record">
                                            <option value="">&laquo; Select One &raquo;</option>
                                            <option ng-repeat="(value, text) in _choices[field]" value=":{ value }:">:{ text }:</option>
                                        </select>
                                        <select id="id_:{ field }:" name=":{ field }:" class="form-control" ng-model="capture[field]"
                                                ng-if="is_update_record" disabled="">
                                            <option value="">&laquo; Select One &raquo;</option>
                                            <option ng-repeat="(value, text) in _choices[field]" value=":{ value }:">:{ text }:</option>
                                        </select>
                                    </div>
                                  
                                    <div class="col-md-8 col-sm-8" ng-if="field[0] !== '_' && title !== 'meta' && _meta.widgets.select.indexOf(field) == -1">
                                        <input type="text" id="id_:{ field }:" name=":{ field }:" class="form-control" ng-model="capture[field]"
                                               change-on-blur="onRSeqChanged(newValue, oldValue)"
                                               ng-if="field === 'rseq' && !is_update_record" />
                                        <input type="text" id="id_:{ field }:" name=":{ field }:" class="form-control" ng-model="capture[field]"
                                               change-on-blur="onRSeqChanged(newValue, oldValue)"
                                               ng-if="field === 'rseq' && is_update_record" disabled="" />
                                        <input type="text" id="id_:{ field }:" name=":{ field }:" class="form-control" ng-model="capture[field]"
                                               ng-if="field !== 'rseq' && !is_update_record" />
                                        <input type="text" id="id_:{ field }:" name=":{ field }:" class="form-control" ng-model="capture[field]"
                                               ng-if="field !== 'rseq' && is_update_record" readonly="" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
  </script>
% end
% rebase('layout.tpl', title=title, year=year, extra_scripts=scripts)
