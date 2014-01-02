%rebase layout app=app, user=user, helper=helper, title='Shinken.io', refresh=False

<div id="index">
  
  <h1>Shinken Packages</h1>
  
  <p>Total Packages: {{app.get_number_of_packages()}}</p>
  
  <table class="downloads">
    <!--<tr><td>897 924</td><td> downloads in the last day</td></tr>
    <tr><td>10 485 607</td><td> downloads in the last week</td></tr>-->
  </table>
  <a href="http://github.com/naparuba/shinken.io">Patches welcome!</a>
  <p>Any package can be installed by using <a href="http://github.com/naparuba/shinken">shinken install</a></p>
  <p>Add your package to this index by using <a href="http://github.com/naparuba/shinken">shinken publish</a></p>
  
  <table>
    <tbody>
      <tr>
	<td>
	  <h2>Packs Updated</h2>
	  <ul>
	  %for package in app.get_recently_updated('pack'):
	    <li>{{helper.print_duration(package['updated'], just_duration=True, x_elts=1)}} <a href="/package/{{package['name']}}">{{package['name']}}</a></li>
	  %end
          <li><a href="/browse/packs/updated">More...</a></li>
	  </ul>
	</td>
	<td>
	  <h2>Modules Updated</h2>
	  <ul>
	  %for package in app.get_recently_updated('module'):
	    <li>{{helper.print_duration(package['updated'], just_duration=True, x_elts=1)}} <a href="/package/{{package['name']}}">{{package['name']}}</a></li>
	  %end
            <li><a href="/browse/modules/updated">More...</a></li>
	  </ul>
	</td>
      </tr>

      <tr>
	<td>
	  <h2>Most starred</h2>
	  <ul>
	  %for package in app.get_most_starred():
	    <li>{{package.get('starred_len',0)}} <a href="/package/{{package['name']}}">{{package['name']}}</a></li>
	  %end
            <!--<li><a href="/browse/updated">More...</a></li>-->
	  </ul>
	</td>
	<td>
	  <h2>Most prolific</h2>
	  <ul>
	  %for u in app.get_most_xp():
	    <li>{{u.get('xp',0)}} <a href="/~{{u['_id']}}">{{u['_id']}}</a></li>
	  %end
	  <!--<li><a href="/browse/updated">More...</a></li>-->
	  </ul>
	</td>
      </tr>
      
      <tr>
	<td>
	  <h2>Shinken.io Stuff</h2>
	  <ul>
            <li><a href="/doc/faq.html">FAQ</a></li>
            <li><a href="/achievements">Achievements</a></li>
            <li><a href="/doc/disputes.html">Handling Disputes</a></li>
            <li><a href="https://github.com/naparuba/shinken/issues">Shinken Bugs</a></li>
            <li><a href="https://github.com/naparuba/shinken.io/issues">Website Bugs</a></li>
            <li><a href="https://lists.sourceforge.net/lists/listinfo/shinken-devel">Mailing List</a></li>
            <li><a href="/about">More about this site</a></li>
	  </ul>
	</td>
	<td>
	  <h2>Profile Stuff</h2>
	  
	  <ul>
            <li><a href="/signup">Create a profile</a></li>
            <li><a href="/~">View your profile</a></li>
            <li><a href="/~naparuba">View someone else's profile</a></li>
            <li><a href="/profile-edit">Edit your profile</a></li>
            <li><a href="/password">Change your password</a></li>
            <li><a href="/forgot">Reset a forgotten password</a></li>
            <li><a href="/logout">Log out</a></li>
	  </ul>
	</td>
      </tr>

      
    </tbody>
  </table>




</div>
