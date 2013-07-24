%rebase layout app=app, user=user, helper=helper, refresh=False, title='Shinken.io Achievements'


<div id="achievements">
  <h1>Achievements</h1>
  
  <ul class='achivemements'>
    %for a in achievements:
    %name = a['name']
    %how  = a['how']
    %sub  = a['sub']
    <li class='achievement'>
      <table>
	<tr>
	  <th>
	    <a href='/achievements/{{name}}'><img src='http://static.shinken.io/img/achievements/{{name}}.png' height='96px' width='96px' />
	    </a>
	  </th>
	  <td colspan="2">
	    <h2><a href='/achievements/{{name}}'>{{name}}</a></h2>
	    <p class='sub'> {{sub}}</p>
	  </td>
	</tr>
	<tr>
	  <th></th>
	  <th>How to get it:</th>
	  <td>	{{!how}}
	  </td>
	</tr>
      </table>
    </li>
    %end
  </ul>

  <i>Got an idea about a cool achievement to add? Just <a href="https://github.com/naparuba/shinken.io">submit it</a> :)</i>
</div>
