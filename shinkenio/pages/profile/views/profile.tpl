%rebase layout app=app, user=user, helper=helper, title=profile['_id'], refresh=False, js=['profile/profile.js']

%name = profile['_id']
%full_name = profile['full_name']
%email = profile['email']
%github = profile['github']
%twitter = profile['twitter']
%homepage = profile['homepage']
%api_key  = profile['api_key']

<div id="profile">
  
  <a href="http://en.gravatar.com/emails/" title="edit avatar at gravatar.com">
    %gravatar = app.get_gravatar(profile)
    <img src="{{gravatar}}?s=496&amp;d=retro" class="avatar-large" height="248" width="248" alt="">
  </a>
  

  <h1>{{name}}</h1>

  %if is_me:
    <p><a href="/profile-edit">Edit Profile</a> -
      <a href="/password">Change Password</a> -
      <a href="http://gravatar.com/emails/">Change Picture</a>
    </p>
  %end
    

  <table class="metadata">
    <tbody>
      %if full_name:
      <tr>
        <th>Full Name</th>
        <td>{{full_name}}</td>
      </tr>
      %end
      <tr>
        <th>Email</th>
        <td><a href="mailto:{{email}}">{{email}}</a></td>
      </tr>
      %if github:
      <tr>
        <th>Github</th>
        <td><a rel="me" href="https://github.com/{{github}}">{{github}}</a></td>
      </tr>
      %end
      %if twitter:
      <tr>
        <th>Twitter</th>
        <td><a rel="me" href="http://twitter.com/{{twitter}}">{{twitter}}</a></td>
      </tr>
      %end
      %if homepage:
      <tr>
        <th>Homepage</th>
        <td><a rel="me" href="{{homepage}}">{{homepage}}</a></td>
      </tr>
      %end
      <tr>
        <th>Api Key</th>
        <td>{{api_key}}</td>
      </tr>

      
    </tbody>
  </table>

  


  

  
    <a href="/logout">log out</a>
    
</div>
