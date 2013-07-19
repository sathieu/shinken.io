%rebase layout app=app, user=user, helper=helper, title=package['_id'], refresh=False

%pname = package['_id']
%description = package['description']
%uname = package['user_id']
%user = app.get_user(uname)
%gravatar = app.get_gravatar(user)
%version = package['version']
%keywords = package['keywords']
%repository = package['repository']
%homepage = package['homepage']
%starred  = package['starred']


<div id="package">
  <h1>{{pname}}</h1>

  <p class="description">{{description}}</p>
  
  <pre class="sh sh_sourceCode"><code>shinken install {{pname}}</code></pre>
  
  <table class="downloads">
    <!--
    <tbody><tr><td>20 642</td><td> downloads in the last day</td></tr>
      <tr><td>126 421</td><td> downloads in the last week</td></tr>
      <tr><td>462 194</td><td> downloads in the last month</td></tr>
      -->
  </tbody></table>



  <table class="metadata">
    
    <tbody><tr>
        <th>Maintainer</th>
        <td>
          
          <div class="user">
            <a class="username" href="/~{{uname}}"><img src="{{gravatar}}?s=50&amp;d=retro" class="avatar">
              {{uname}}</a>
          </div>
          
        </td>
      </tr>
      
      <tr>
        <th>Version</th>
        <td>
          <b>
            {{version}}
          </b>
          
          last updated {{helper.print_duration(package['updated'], just_duration=True, x_elts=1)}} ago
          
        </td>
      </tr>
      
      
      <tr>
        <th>Keywords</th>
        <td>
	  %""" Why not use a ','.join? Because the bottle will stip the <a>, but we can avoid it with !, but can be dangerous, so no"""
	  %i = 0
	  %for keyword in keywords:
	    %if i >= 1:
	    ,
	    %end
	    %i += 1
	    <a href="/browse/keyword/{{keyword}}">{{keyword}}</a>
	  %end
	</td>
      </tr>
      
      
      <tr>
        <th>Repository
        </th><td>
          <a href="{{repository}}">
		   {{repository}}</a>
        </td>
      </tr>
      
      
      <tr>
        <th>Homepage
        </th><td>
          <a href="{{homepage}}">{{homepage}}</a>
        </td>
      </tr>
      
      <!--
      <tr>
        
        <th>Dependencies</th>
        <td>
          None
        </td>
      </tr>
      
      <tr>
        <th>Dependents (1000)</th>
        <td>
	  <br>and 980 more
        </td>
      </tr>
      -->
      

      
      <tr>
        <th>Starred by ({{len(starred)}})</th>
        <td>
	  %""" remember before? ok same here"""
	  %i=0
	  %for star in starred:
	  %if i >= 1:
	  ,
	  %end
	  <a href="/~{{star}}">{{star}}</a>
	  %end
	  <!--<br><a href="/browse/star/underscore">and
            21 more</a>
	    -->
        </td>
      </tr>
      
  </tbody></table>

  <div class="details">
    %if readme:
    <section id='readme'>
    {{!readme}}
    </section>
    %else:
    None
    %end
  </div>
</div>
