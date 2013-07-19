<!DOCTYPE html>

%#Set default values
%if not 'js' in locals(): js = []
%if not 'title' in locals(): title = 'No title'
%if not 'css' in locals(): css = []
%if not 'print_menu' in locals(): print_menu = True
%if not 'print_header' in locals(): print_header = True
%if not 'print_footer' in locals(): print_footer = True
%if not 'refresh' in locals(): refresh = False
%if not 'user' in locals(): user = None
%if not 'app' in locals(): app = None

%if not 'layout_type' in globals():
%   layout_type=""
%end


%# For the menu selection
%if not 'menu_part' in locals(): menu_part = ''

<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{title or 'Shinken.io'}}</title>

    <!-- Le HTML5 shim, for IE6-8 support of HTML elements -->
    <!--[if lt IE 9]>
      <script src="http://static.shinken.io/js/html5.js"></script>
      <script src="http://static.shinken.io/js/json2.js"></script>
    <![endif]-->

    <!-- Le styles -->
    <link type="text/css" rel="stylesheet" media="all" href="http://static.shinken.io/css/normalize.css">
    <link type="text/css" rel="stylesheet" media="all" href="http://static.shinken.io/css/index.css">
    <link type="text/css" rel="stylesheet" media="all" href="http://static.shinken.io/css/sh.css">
    <link type="text/css" rel="stylesheet" media="all" href="http://static.shinken.io/css/codehilite.css">


    <!-- Source+Sans+Pro from google fonts -->
    <link href='http://fonts.googleapis.com/css?family=Lato:300,400,700,900,300italic,400italic,700italic,900italic' rel='stylesheet' type='text/css'>

    %# And now for css files
    %for p in css:
    <link rel="stylesheet" type="text/css" href="http://static.shinken.io/css/{{p}}">
    %end

    <!-- Javascript part -->
    <script src="http://static.shinken.io/js/jquery-1.8.3.js"></script>


    %# End of classic js import. Now call for specific ones
    %for p in js:
    <script type="text/javascript" src="http://static.shinken.io/js/{{p}}"></script>
    %end

  </head>

<body>

  %include header globals()


  %include

  </div></div></div>

  
  %include footer globals()


  <!-- The modal div that will be shown when we want, and after put in it the data we want -->
  <div class="modal fade" id="modal"></div>
</body>
</html>
