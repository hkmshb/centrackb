<table class="table table-condensed">
    <tbody>
        <tr style="border-bottom:solid 1px #ddd;">
            <td style="white-space:nowrap; width:100px;">
                <label class="control-label">Feeder: </lable>
            </td>
            <td style="width:100px;">{{ feeder.code }}</td>
            <td style="width:80%;">{{ feeder.voltage }}KV {{ feeder.name }}</td>
            <td><a href="{{ '/admin/feeders/%s/edit' % feeder.code.lower() }}">
                    <i class="glyphicon glyphicon-edit"></i>
                </a>
            </td>
        </tr>
    </tbody>
</table>
<form data-bind="table" method="post" data-paging-numbers="{{ stations.paging_numbers }}">    
    <div class="panel panel-default">    
        <div class="panel-heading">
            <b>Stations</b>
            <div class="pull-right">
                <div style="margin-top: -5px;">
                    <a href="{{ '/admin/feeders/%s/stations/create' % feeder.code.lower() }}" class="btn btn-default">Add</a>
                    <a href="{{ '/admin/feeders/%s/stations/import' % feeder.code.lower() }}" class="btn btn-default">Import</a>
                    <button type="submit" name="del" class="btn btn-danger">Delete</button>
                </div>
            </div>
        </div>
        <div class="panel-body panel-fitted">
            <table class="table table-condensed table-striped table-hover">
                <thead>
                    <tr>
                        <th>Code</th>
                        <th>Name</th>
                        <th>Rating</th>
                        <th>Captures</th>
                    </tr>
                </thead>
                <tbody>
                    % if stations:
                    % for s in stations:
                    <tr>
                        <td>
                            <a href="{{ '/admin/feeders/%s/stations/%s/' % (feeder.code.lower(), s.code.lower()) }}">{{ s.code }}</a>
                        </td>
                        <td>{{ s.name }}</td>
                        <td>{{ s.capacity }}KVA, {{ get_vratio_display(s.vratio) or ''}}</td>
                        <td>{{ get_capture_count(s.code) }}</td>
                    </tr>
                    % end
                    % else:
                    <tr>
                        <td colspan="5">No data available.</td>
                    </tr>
                    % end
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="5">
                            % include('table-footer.tpl', p=stations)
                        </td>
                    </tr>
                </tfoot>
            </table>
        </div>
    </div>
</form>    
%rebase('admin/base.tpl', title=title, year=year)