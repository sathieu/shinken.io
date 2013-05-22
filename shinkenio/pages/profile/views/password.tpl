%rebase layout app=app, user=user, helper=helper, title='Edit profile', refresh=False, js=['profile/password.js']

%name = user['_id']
%full_name = user['full_name']
%email = user['email']
%github = user['github']
%twitter = user['twitter']
%homepage = user['homepage']

<h1>Edit your Profile</h1>

<p id="password_err" style="display:none;" class="error"></p>


<form method="post" id="password">
  <fieldset>
    <label for="current">Current Password</label>
    <input id="current" name="current" type="password">
  </fieldset>
  
  <fieldset>
    <label for="new">New Password</label>
    <input id="password" name="password" type="password">
    <p class="form-help">Please choose something long and memorable</p>
  </fieldset>
  
  <fieldset>
    <label for="verify">Verify Password</label>
    <input id="verify" name="verify" type="password">
  </fieldset>
  
  <fieldset class="buttons">
    <button class="btn" type="submit">Make it so.</button>
  </fieldset>
  
</form>
