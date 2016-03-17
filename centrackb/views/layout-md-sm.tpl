<div class="row">
    <div class="col-md-9">
        {{!base}}
    </div>
    <div class="col-sm-3">
        % include('calendar.tpl', ref_date=ref_date())
        % if defined('pane_block'):
            % pane_block()
        % end
    </div>
</div>
% rebase('layout.tpl', title=title, year=year)