%rebase layout app=app, user=user, helper=helper, refresh=False

%name = achievement['name']
%how  = achievement['how']
%sub  = achievement['sub']

<div id="achievement">
  

  

  <h1>{{name}}</h1>
  <img src="http://static.shinken.io/img/achievements/{{name}}.png" alt="{{name}}">
  <table class="metadata">
    <tbody>
      <tr>
        <th></th>
        <td>{{sub}}</td>
      </tr>
      
      <tr>
        <th>How to get it:</th>
        <td>{{!how}}</td>
      </tr>
    </tbody>
  </table>

    
</div>
