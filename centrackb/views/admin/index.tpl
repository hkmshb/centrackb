<div class="row">
    <div class="col-md-3">
        <div class="stat-card stat-green">
            <div class="fig">{{ stat.count_projects }}</div>
            <div class="txt">Project(s)</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card stat-green">
            <div class="fig">{{ stat.count_xforms }}</div>
            <div class="txt">XForm(s)</div>
        </div>
    </div>
</div>

% rebase('admin/base.tpl', title=title, year=year)