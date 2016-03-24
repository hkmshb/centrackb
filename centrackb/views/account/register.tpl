<div class="row">
    <div class="form-register col-md-4">
        <h3>Register To Use CENTrack</h3>
        <form method="post" class="form-stacked">
            <div class="form-group">
                <label for="id_username">Username</label>
                <input type="text" id="id_username" name="username" class="form-control"
                       value="{{ form.username or '' }}" required />
                <p class="text-danger"></p>
            </div>
            <div class="form-group">
                <label for="id_email">Email</label>
                <input type="email" id="id_email" name="email" class="form-control" 
                       value="{{ form.email or '' }}" required />
                <p class="text-danger"></p>
            </div>
            <div class="form-group">
                <label for="id_password">Password</label>
                <input type="password" id="id_password" name="password" class="form-control" required />
                <p class="text-danger"></p>
            </div>
            <div class="form-group">
                <label for="id_password_confirm">Confirm Password</label>
                <input type="password" id="id_password_confirm" name="confirm_password" class="form-control" required />
                <p class="text-danger"></p>
            </div>
            <div class="form-group">
                <button type="submit" class="btn btn-primary pull-right">Register</button>
            </div>
        </form>
    </div>
</div>
% rebase("layout.tpl", title=title, year=year)