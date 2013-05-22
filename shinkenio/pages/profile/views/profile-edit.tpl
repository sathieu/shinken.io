%rebase layout app=app, user=user, helper=helper, title='Edit profile', refresh=False, js=['profile/profile.js']

%name = user['_id']
%full_name = user['full_name']
%email = user['email']
%github = user['github']
%twitter = user['twitter']
%homepage = user['homepage']

<h1>Edit your Profile</h1>

<p id="profile_err" style="display:none;" class="error"></p>

<form method="post" action="/profile-edit" id="profile">
  <input type="hidden" name="name" value="{{name}}">

  <fieldset>
    <label for="fullname">Full Name</label>
    <input id="fullname" name="fullname" value="{{full_name}}">
  </fieldset>
  
  <fieldset>
    <label for="email">Email</label>
    <input id="email" name="email" value="{{email}}">
  </fieldset>
  
  <fieldset>
    <label for="github">Github</label>
    <input id="github" name="github" value="{{github}}">
  </fieldset>
  
  <fieldset>
    <label for="twitter">Twitter</label>
    <input id="twitter" name="twitter" value="{{twitter}}">
  </fieldset>
  
  <fieldset>
    <label for="homepage">Homepage</label>
    <input id="homepage" name="homepage" value="{{homepage}}">
  </fieldset>
  
  <fieldset class="buttons">
    <button class="btn" type="submit">Save</button>
  </fieldset>
</form>
