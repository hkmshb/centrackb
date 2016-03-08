<div class="row">
    <div class="col-md-5">
       <div class="panel panel-default panel-compressed">
            <div class="panel-heading">Export Result</div>
            <div class="panel-body">
                <b>Status</b>: {{ status }}<br/>
                <b>Filename</b>: {{ filename }} <br/>
               <b>Error Details:</b> {{ error }}<br/>
            </div>
        </div>
    </div>
</div>
% rebase('layout.tpl', title=title, year=year)