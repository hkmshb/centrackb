<div class="row">
    <div class="col-md-3">
        % include('admin/menu.tpl')
        % if defined('extra_menu'):
            % extra_menu()
        % end
    </div>
    <div class="col-md-9">
        {{!base}}
    </div>
</div>
% rebase('layout.tpl', title=title, year=year)