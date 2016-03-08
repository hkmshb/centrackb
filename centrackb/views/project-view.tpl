% fmt = '<label class="item-title"><input type="checkbox" value="%s" />&nbsp; %s</label>'
<h1>{{ title }}</h1>
<div class="panel panel-default panel-xforms">
    <div class="panel-heading">
        &nbsp;
        <div class="pull-right" style="margin-top:-5px">
            <form method="post" action="sync">
                <button type="submit" name="sync" class="btn btn-primary" data-type="xforms">Sync Captures</button>
                <input type="hidden" name="project_id" value="{{ project.id }}" />
                <input type="hidden" name="project_xforms" value="" />
            </form>
        </div>    
    </div>
    <div class="panel-body">        
        % include('summary-table.tpl', records=xrecords, header="XForms", 
        %         get_url=lambda r:'#', get_title=lambda r: (fmt % (r.id, r.title[:9])))
    </div>
</div>
<div class="panel panel-default panel-uforms">
    <div class="panel-heading">
        &nbsp;
        <div class="pull-right" style="margin-top:-5px">
            <form method="post" action="sync">
                <button type="submit" name="sync" class="btn btn-primary" data-type="uforms">Sync Updates</button>
                <input type="hidden" name="project_id" value="{{ project.id }}" />
                <input type="hidden" name="project_uforms" value="" />
            </form>
        </div>
    </div>
    <div class="panel-body">
        % include('summary-table.tpl', records=urecords, header="UForms",
        %         get_url=lambda r:'#', get_title=lambda r: (fmt % (r.id, r.title[:9])))
    </div>
</div>
% def script():
<script type="text/javascript">
    (function($){
        $(function(){
            $('[name=sync]').on('click', function(){
                var $this = $(this)
                  , type = $this.data('type'), form_ids = []
                  , $panel = $('.panel-' + type)
                  , $selected = $panel.find('.item-title>input:checked');
                if ($selected.length <= 0) {
                    alert('At least one XForm needs to be selected.')
                    return false;
                }
                $selected.each(function() { form_ids.push(this.value); });
                $panel.find('[name=project_' + type + ']').val(form_ids.join(','));
                return true;
            });
        });
    })(jQuery);
</script>
% end
% rebase('layout-md-sm.tpl', title=title, year=year, extra_scripts=script)