%rebase layout title='Shinken.io', refresh=False, js=['signup/signup.js']


<h1>Sign all the way up</h1>

<p id="signup_err" style="display:none;" class="error"></p>


<form action="/signup" method="post" class="form" id="signup">
  <fieldset>
    <label for="name">Username</label>
    <input id="name" name="name" type="text">
    <p class="form-help">Must be all lower-case, and not have any non-urlsafe chars.</p>
  </fieldset>

  <fieldset>
    <label for="password">Password</label>
    <input id="password" name="password" type="password">
  </fieldset>

  <fieldset>
    <label for="verify">Verify Password</label>
    <input id="verify" name="verify" type="password">
  </fieldset>

  <fieldset>
    <label for="email">Email Address</label>
    <input id="email" name="email" type="email">
    <p class="form-help">Must be a valid email address.  It <strong>will</strong>
      be shown on the site, and on all packages you publish.</p>
    <p class="form-help">Accounts without valid email addresses may be deleted
      without notice.</p>
  </fieldset>

  <fieldset class="buttons">
    <button type="submit" class="btn">Make it so.</button>
  </fieldset>
</form>



