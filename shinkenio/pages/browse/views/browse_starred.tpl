%rebase layout app=app, user=user, helper=helper, refresh=False


<div id="package">
  <h1>Most Starred Packages</h1>
  
  %for p in results:
  %pname = p['_id']
  %uname = p['user_id']
  <div class='row'>
    <p><a href='/package/{{pname}}'>{{pname}}</a>
      {{p['description']}} - {{p.get('starred_len', 0)}}</p>
  </div>
  %end

</div>
