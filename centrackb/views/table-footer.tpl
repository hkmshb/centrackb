<div class="pagination-packed">
    <div class="summary">
        <span>
            {{ p.start_index() }} - {{ p.end_index() }} of {{ p.paginator.count }} items @
            {{ p.current_page_size }} per page
        </span>
    </div>
                                   
    <div class="controls">
        <span name="first" class="btn btn-default glyphicon glyphicon-fast-backward"></span>
        <span name="prev" class="btn btn-default glyphicon glyphicon-step-backward"></span>
        <input type="number" class="form-control" name="page" min="1" max="{{ p.paginator.num_pages }}" value="{{ p.number }}" />
            / {{ p.paginator.num_pages }} 
        <span name="next" class="btn btn-default glyphicon glyphicon-step-forward"></span>
        <span name="last" class="btn btn-default glyphicon glyphicon-fast-forward"></span>
    </div>
</div> 