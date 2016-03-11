<form method="post">
    <div class="panel panel-default">
        <div class="panel-heading">
            <b>Feeders</b>
            <div class="pull-right">
                <div style="margin-top: -5px;">
                    <a href="/admin/feeders/create" class="btn btn-default">Add</a>
                    <button type="submit" name="del" class="btn btn-danger">Delete</button>
                </div>
            </div>
        </div>
        <div class="panel-body">
            <table class="table panel-table">
                <thead>
                    <tr><th style="width:150px;">Code</th>
                        <th style="width:150px;">Voltage</th>
                        <th style="width:45%;">Name</th>
                        <th style="width:150px">Stations</th>
                        <th style="width:150px">Captures</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                % if records:
                    % for r in records:
                    <tr><td style="white-space:nowrap;"><a href="/admin/feeders/{{ r.code.lower() }}/">{{ r.code }}</a></td>
                        <td>{{ r.voltage }}KV</td>
                        <td>{{ r.name }}</td>
                        <td>{{ get_station_count(r.code) }}</td>
                        <td>{{ get_capture_count(r.code.lower() + "_cf_KN") }}</td>
                        <td>
                            <a href="{{ '/admin/feeders/%s/edit' % r.code.lower() }}">
                                <i class="glyphicon glyphicon-edit"></i>
                            </a>
                        </td>
                    </tr>
                    % end
                % else:
                    <tr><td colspan="6">No data available.</td></tr>
                % end
                </tbody>
            </table>
        </div>
    </div>
</form>
% rebase('admin/base.tpl', title=title, year=year)