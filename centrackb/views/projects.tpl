<div class="panel panel-default">
    <div class="panel-heading">
        {{ title }}
    </div>
    <div class="panel-body">
        % include('summary-table.tpl', records=records, header="Project",
        %         get_url=lambda r: "/projects/%s/" % r.id,
        %         get_title=lambda r: r.name)
    </div>
</div>

% rebase('layout-md-sm.tpl', title=title, year=year)