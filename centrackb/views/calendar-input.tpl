% calendar_class = get('calendar_class', "")
<div class="calendar pull-right {{ calendar_class }}">
    <div class="pull-left">
        <a href="#" class="date-input">
            <i class="glyphicon glyphicon-calendar"></i>
        </a>
    </div>
    <div class="pull-right body">
        <span class="tdy">{{ ref_date.strftime('%a, %B %d, %Y') }}</span>
        <br/>
        <span class="wk">
            {{ weekdate_bounds[0].strftime('%b %d, %Y') }} - 
            {{ weekdate_bounds[1].strftime('%b %d, %Y') }}
        </span>
    </div>
</div>