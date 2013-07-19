%rebase layout app=app, user=user, helper=helper, refresh=False


<div id="package">
  <h1>All modules (by updated date)</h1>
  
  %if len(results) == 0:
    No results!
  %else:
    %for p in results:
    %pname = p['_id']
    %uname = p['user_id']
    <div class='row'>
      <p><a href='/package/{{pname}}'>{{pname}}</a>
      {{p['description']}}</p>
    </div>
    %end

  %end
</div>
