% def ex_scripts():
    <script type="text/javascript">
        (function($) {
            $(function() {
                $('#form-pwd').validate();
            });
        })(jQuery);
    </script>
% end
% include('admin/user-form-snippet.tpl', title=title, action_url="change_password")
%rebase('admin/base.tpl', title=title, year=year, extra_scripts=ex_scripts)
