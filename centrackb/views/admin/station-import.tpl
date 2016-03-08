<div class="panel panel-default">
    <div class="panel-heading">
        <b>{{ title }}</b>
    </div>
    <div class="panel-body">
        <form method="post" enctype="multipart/form-data">
            <table class="narrow-labels">
                <tbody>
                    <tr><td><label for="id_impfile">CSV File: </label></td>
                        <td><input type="file" id="id_impfile" name="impfile" required="" /></td>
                    </tr>
                    <tr><td>&nbsp;</td>
                        <td><button type="submit" class="btn btn-default">Import</button></td>
                    </tr>
                </tbody>
            </table>
        </form>
    </div>
</div>
%rebase('admin/base.tpl', title=title, year=year)