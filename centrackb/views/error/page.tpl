<div class="row">
    <div class="col-md-offset-2 col-md-8 content">
        <h1>{{ header }}</h1>
        <p>
            {{ message }}
        </p>
    </div>
</div>

%rebase('error/base.tpl', title=title, year=year)
