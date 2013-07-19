%rebase layout app=app, user=user, helper=helper, refresh=False


<div id="search">
  <h1>Search Results</h1>
  
  %if len(results) == 0:
    No results!
  %else:
  <ul class='search-results'>
    %for p in results:
    %pname = p['_id']
    %uname = p['user_id']
    <li class='search-result package'>
      <h2><a href='/package/{{pname}}'>{{pname}}</a></h2>
      <p class='details'>
	{{p['version']}} by <a href='/~{{uname}}'>{{uname}}</a>
      </p>
      <p>{{p['description']}}</p>
      <ul class='keywords'>
	<li>
	  %for k in p['keywords']:
	  <a href='/browse/keywords/{{k}}'>{{k}}</a>
	  %end
	</li>
      </ul>
    </li>
    %end
  </ul>

  %end
</div>
