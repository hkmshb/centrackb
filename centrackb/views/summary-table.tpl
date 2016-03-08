<table class="table panel-table table-figures">
    <thead>
        <tr><th colspan="2">&nbsp;</th>
            <th colspan="2" class="lvsep col-shade">Duplicates</th>
            <th colspan="4" class="lvsep">Account Status</th>
            <th colspan="3" class="lvsep col-shade">Meter Type</th>
        </tr>
        <tr><th>{{ header }}</th>
            <th class="lvsep">Total</th>
            <th class="col-shade lvsep ">#RS</th>
            <th class="col-shade">#AC</th>
                    
            <th class="lvsep" title="# New">#.N</th>
            <th title="# Active">#.A</th>
            <th title="# Inactive">#.I</th>
            <th title="# Unknown">#.U</th>
                    
            <th class="col-shade lvsep" title="# Analogue">#.Alog</th>
            <th class="col-shade" title="# PPM">#.PPM</th>
            <th class="col-shade" title="# None">#.NA</th>
        </tr>
    </thead>
    <tbody>
    % if records:
        % for r in records:
        <tr><td><a href="{{ get_url(r) }}">{{! get_title(r) }}</a></td>
            <td class="lvsep">{{ r._total or '-' }}</td>
            <td class="col-shade lvsep">{{ r._rseq_duplicates or '-' }}</td>
            <td class="col-shade">{{ r._acctno_duplicates or '-' }}</td>
            <td class="lvsep">{{ r.new or '-' }}</td>
            <td>{{ r.active or '-' }}</td>
            <td>{{ r.inactive or '-' }}</td>
            <td>{{ r.unknown or '-' }}</td>
            <td class="lvsep col-shade">{{ r.analogue or '-' }}</td>
            <td class="col-shade">{{ r.ppm or '-' }}</td>
            <td class="col-shade">{{ r.none or '-' }}</td>
        </tr>
        % end
    % else:
        <tr><td colspan="11">No data available.</td></tr>
    % end
    </tbody>
</table>