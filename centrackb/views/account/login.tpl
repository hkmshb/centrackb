<div class="form-signup">
    <h3>CENTrak</h3>
    <form method="post" class="form-stacked">
        <div class="form-group">
            <input type="text" name="username" class="form-control"
                   placeholder="Username" />
        </div>
        <div class="form-group">
            <input type="password" name="password" class="form-control"
                   placeholder="Password" />
        </div>
        <button type="submit" class="btn btn-primary btn-login">Log In</button>
    </form>
</div>

% def head():
    <style type="text/css">
        .form-signup {
            width: 300px;
            margin: 20px auto 100px;
        }
        h3 { text-align: center; }
        .btn-login { width: 100%; }
    </style>
% end
% rebase("layout.tpl", title=title, year=year, extra_head=head)