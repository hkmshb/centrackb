% def ex_scripts():
    <script type="text/javascript">
        (function($) {
            $(function() {
                $('#form-pwd').validate();
            });
        })(jQuery);
    </script>
% end
<div class="row">
    <div class="col-md-6">
        % include('admin/user-form-snippet.tpl', title=title, action_url="/profile")
    </div>
</div>
%rebase('layout.tpl', title=title, year=year, extra_scripts=ex_scripts)
