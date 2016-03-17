% calendar_class = get('calendar_class', "")
<div class="calendar pull-right {{ calendar_class }}">
    <div class="pull-left">
        <i class="glyphicon glyphicon-calendar"></i>
    </div>
    <div class="pull-right body">
        <span class="tdy">{{ ref_date.strftime('%a, %B %d, %Y') }}</span>
        <br/>
        %_weekdate_bounds = weekdate_bounds(ref_date)
        <span class="wk">
            {{ _weekdate_bounds[0].strftime('%b %d, %Y') }} - 
            {{ _weekdate_bounds[1].strftime('%b %d, %Y') }}
        </span>
    </div>
</div>