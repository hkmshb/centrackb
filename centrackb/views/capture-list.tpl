% f = lambda x: x or '-'
% enum = lambda x: '%s<b> / </b>%s' % (x[0], x[2:].title())
% addy = lambda x: '' if (x or '').upper() in ['NA','N/A'] else (x or '')
% shorten = lambda x: x if x=='-' or len(x) < 22 else x[:22]+'...'

<div class="form-search">
    <div class="row">
        <div class="col-md-8"><span class="h4">{{ title }}</span></div>
        <div class="col-md-4">
            <form class="form-inline" method="get">
                <div class="input-group pull-right" style="width:75%;">
                    <input type="text" name="q" class="form-control" placeholder="Quick Search"
                           value="{{ search_text or '' }}" />
                    <div class="input-group-btn">
                        <button type="submit" class="btn btn-default">
                            <i class="glyphicon glyphicon-search"></i>
                        </button>
                    </div>
                </div>
                <div class="pull-left">
                    <div class="btn-group">
                        <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                            Export <span class="caret"></span>
                        </button>
                        <ul class="dropdown-menu">
                            <li><a href="#" name="export_xls">
                                    <i class="glyphicon glyphicon-list"></i> &nbsp; Excel File (.xls)
                                </a></li>
                            <li><a href="#" name="export_csv">
                                    <i class="glyphicon glyphicon-file"></i> &nbsp; CSV File (.csv)
                                </a></li>
                        </ul>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>

<div class="panel panel-default capture-list">
    <div class="panel-body" style="padding-bottom:0;">
      <form data-bind="table" method="post" data-paging-numbers="{{ records.paging_numbers }}">
        <table class="table table-condensed table-hover table-striped" style="margin-bottom:0; padding-bottom:0;">
            <thead>
                <tr><th>Enum.ID</th>
                    <th>R.Seqence</th>
                    <th>Customer</th>
                    <th>Address</th>
                    <th>Mobile #</th>
                    <th>Acct. Status</th>
                    <th>Acct. #</th>
                    <th>Tariff</th>
                    <th>Meter</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            % if records:
                % for r in records:
                <tr class="{{ 'dropped' if r.dropped else 'updated' if r.last_updated else '' }}">
                    <td>{{! enum(r.enum_id) }}</td>
                    <td>
                    % if not defined('get_extra_info'):
                        <a href="{{ r._id }}/">{{ r.rseq }}</a>
                    % else:
                        % info = get_extra_info(r)
                        <a href="{{ r._id }}/" data-toggle="tooltip" title="{{ info }}">
                            {{ r.rseq }}
                        </a>
                    % end 
                    </td>
                    <td>{{ shorten(f(r.cust_name)).title() }}</td>
                    <td>{{ shorten("%s %s" % (addy(r.addr_no), addy(r.addr_street))).title() }}
                    <td>{{ f(r.cust_mobile1 or r.cust_mobile2) }}</td>
                    <td>{{ r.acct_status }}</td>
                    <td>{{ f(r.acct_no) }}</td>
                    <td>{{ f(r.tariff) }}</td>
                    <td>{{ f(r.meter_type) }}</td>
                    <td>
                        % if r.dropped:
                            <i class="glyphicon glyphicon-ban-circle"></i>
                        % elif r.last_updated:
                            <i class="glyphicon glyphicon-tag" title="Updated: {{ r.last_updated }}"></i>
                        % else:
                            % if not defined('has_updates'):
                                <i class="glyphicon glyphicon-none"></i>
                            % else:
                                % count = has_updates(r._id, r.rseq)
                                % if count == 0:
                                    <i class="glyphicon glyphicon-none"></i>
                                % else:
                                    <i class="glyphicon glyphicon-leaf" title="Available Updates: {{ count }}"></i>
                                % end
                            % end
                            % if not defined('has_duplicates'):
                                <i class="glyphicon glyphicon-none"></i>
                            % else:
                                % count = has_duplicates(r._id, r.rseq)
                                % if count == 0:
                                    <i class="glyphicon glyphicon-none"></i>
                                % else:
                                    <i class="glyphicon glyphicon-flag" title="Duplicates: {{count}}"></i>
                                % end
                            % end
                        % end
                    </td>
                </tr>
                % end
            % else:
                <tr><td colspan="10">No data available</td></tr>
            % end
            </tbody>
            <tfoot>
                <tr><td colspan="10">
                    % include('table-footer.tpl', p=records)
                    </td></tr>
            </tfoot>
        </table>
      </form>
    </div>
</div>
% include('filter-panel.tpl', q=filter_params)
% def scripts():
    <script type="text/javascript">
        App.filterCapture();
        App.exportCapture();
        $('.input-group.date').datepicker({
                format: "yyyy-mm-dd", clearBtn: true,
                autoclose: true, toggleActive: true,
                todayHighlight: true,           
            });
        $('[data-toggle="tooltip"]').tooltip();
    </script>
% end
% rebase('layout.tpl', title=title, year=year, extra_scripts=scripts)