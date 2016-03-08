<script type="text/ng-template" id="capture_snippet.html">
  <div class="wrapper">
    <form method="post" class="form-horizontal form-compressed">
        <div class="panel-group" id="accordion_:{ title }:">
            <div class="panel panel-default panel-compressed" ng-repeat="(title, meta) in _meta.fields">
                <div class="panel-heading" ng-if="title !== 'capture'">
                    <h4 class="panel-title">
                        <a role="button" data-toggle="collapse" data-parent="#accordion_:{ title }:" href="#collapse_:{ title }:">
                            :{ title }:
                        </a>
                    </h4>
                </div>
                <div id="collapse_:{ title }:" class="panel-collapse" ng-class="{'collapse': title !== 'capture'}">
                    <div class="panel-body">
                        <div class="form-group" ng-repeat="(field, label) in meta">
                            <label for="id_:{field}:" class="col-md-4 control-label">:{ label }:: </label>
                            
                            <div class="col-md-8" ng-if="field[0] == '_' || title == 'meta'">
                                <label ng-if="title != 'meta'" id="id_:{ field }:" name=":{ field }:" class="form-control-static">:{ capture[field.substr(1)] }:</label>
                                <label ng-if="title == 'meta'" id="id_:{ field }:" name=":{ field }:" class="form-control-static">:{ capture[field] }:</label>
                            </div>
                            
                            <div class="col-md-8" ng-if="_meta.widgets.select.indexOf(field) > -1">
                                <select id="id_:{ field }:" name=":{ field }:" class="form-control" >
                                    <option value="">&laquo; Select One &raquo;</option>
                                    <option ng-repeat="(value, text) in _choices[field]" value=":{ value }:"
                                            ng-selected="capture[field] == value">:{ text }:</option>
                                </select>
                            </div>
                            
                            <div class="col-md-8" ng-if="field[0] !== '_' && title !== 'meta' && _meta.widgets.select.indexOf(field) == -1">
                                <input type="text" id="id_:{ field }:" name=":{ field }:" class="form-control" ng-model="capture[field]"
                                       change-on-blur="listenForChange(newValue, oldValue)"
                                       ng-if="field === 'rseq'" />
                                <input type="text" id="id_:{ field }:" name=":{ field }:" class="form-control" ng-model="capture[field]"
                                       ng-if="field !== 'rseq'" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>
  </div>
</script>