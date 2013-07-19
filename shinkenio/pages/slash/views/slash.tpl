%rebase layout app=app, user=user, helper=helper, title='Shinken.io', refresh=False

<div id="index">
  
  <h1>Shinken Packages</h1>
  
  <p>Total Packages: {{app.get_number_of_packages()}}</p>
  
  <table class="downloads">
    <!--<tr><td>897 924</td><td> downloads in the last day</td></tr>
    <tr><td>10 485 607</td><td> downloads in the last week</td></tr>-->
  </table>

  <table>
    <tbody>
      <tr>
	<td>
	  <h2>Packs Updated</h2>
	  <ul>
	  %for package in app.get_recently_updated('pack'):
	    <li>{{helper.print_duration(package['updated'], just_duration=True, x_elts=1)}} <a href="/package/{{package['name']}}">{{package['name']}}</a></li>
	  %end
            <li><a href="/browse/updated">More...</a></li>
	  </ul>
	</td>
	<td>
	<td>
	  <h2>Modules Updated</h2>
	  <ul>
	  %for package in app.get_recently_updated('module'):
	    <li>{{helper.print_duration(package['updated'], just_duration=True, x_elts=1)}} <a href="/package/{{package['name']}}">{{package['name']}}</a></li>
	  %end
            <li><a href="/browse/updated">More...</a></li>
	  </ul>
	</td>
	</td>

      </tr>
    </tbody>
  </table>




</div>
