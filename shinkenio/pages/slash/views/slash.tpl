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
	  <h2>Recently Updated</h2>
	  <ul>
	  %for package in app.get_recently_updated():
	    <li>{{helper.print_duration(package['updated'], just_duration=True, x_elts=1)}} <a href="/package/{{package['name']}}">{{package['name']}}</a></li>
	  %end
            <li><a href="/browse/updated">More...</a></li>
	  </ul>
	</td>
	<td>
	  <h2>Modules Updates</h2>
	  <ul>
            <li>1m <a href="/module/kd">livestatus</a></li>
            <li>3m <a href="/module/hstrap">webui</a></li>
            <li>6m <a href="/module/jsonspace-core">mongodb-retention</a></li>
            <li>14m <a href="/module/mux-demux">npcdmod</a></li>
            <li>19m <a href="/module/backpack-replicator">merlindb</a></li>
            <li>19m <a href="/module/mangouste">pickle-file</a></li>
            <li>19m <a href="/module/modjs">redis</a></li>
            <li>23m <a href="/module/github-cloner">hot_dependencies</a></li>
            <li>24m <a href="/module/appmaker">ec2</a></li>
            <li>25m <a href="/module/sioux-ui-navigation">file_tag</a></li>
            
            <li><a href="/browse/module/updated">More...</a></li>
	  </ul>
	</td>

      </tr>
    </tbody>
  </table>




</div>
