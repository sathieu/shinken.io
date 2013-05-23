%rebase layout locals(), title='Shinken.io', refresh=False, js=['login/login.js']


<h1>Login, please</h1>

<p id="login_err" style="display:none;" class="error"></p>

<form action="/login" method="post" class="form" id="login">
  <fieldset>
    <label for="name">Username</label>
    <input name="name" id="name">
  </fieldset>
  <fieldset>
    <label for="password">Password</label>
    <input type="password" name="password" id="password">
  </fieldset>
  <fieldset class="buttons">
    <button class="btn" type="submit">Login!</button>
    <a href="/forgot">Forgot password?</a>
  </fieldset>
</form>

<p>Don't have an account? <a href="/signup">Sign up.</a>
</p>


