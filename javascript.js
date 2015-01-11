$(document).ready(function() {
  var menuitems = ['#sunday','#monday','#tuesday','#wednesday','#thursday','#friday','#saturday'];
  var myUrlArray = ["sunday's Labour.html", "monday's Labour.html", "tuesday's Labour.html", "wednesday's Labour.html", "thursday's Labour.html", "friday's Labour.html", "saturday's Labour.html"];
  
  var iframe = function(element, arraynum){
    if(typeof interval != 'undefined'){ 
      clearInterval(interval)
    };
    $('#nav ul li').css({
      'color': ''
    });
    $(element).css({
     'color': 'green'
    });
    $("#header").hide()
    document.getElementById('maps').setAttribute('src',myUrlArray[arraynum]);  
  };

  $('#sunday').click(function(){
    iframe(this,0);
  });  
  $('#monday').click(function(){
    iframe(this,1);
  });
  $('#tuesday').click(function(){
    iframe(this,2);
  });
  $('#wednesday').click(function(){
    iframe(this,3);
  });
  $('#thursday').click(function(){
    iframe(this,4);
  });
  $('#friday').click(function(){
    iframe(this,5);
  });
  $('#saturday').click(function(){
    iframe(this,6);
  });

  $('#scroll').click(function(){
    $("#header").hide()
    $(this).css({
        'color': 'red'
        });
    var changeCSS = function(x, y){
      if(document.getElementById('maps').getAttribute('src') == y){
        $('#nav ul li').css({
          'color': ''
        });
        $('#scroll').css({
        'color': 'red'
        });
        $(x).css({
        'color': 'green'
        }); 
      };
    };
    var u = 0;
    interval = setInterval(function(){
    document.getElementById('maps').setAttribute('src',myUrlArray[u]);
    if(u < myUrlArray.length){
       ++u;
    }else{
       u = 0;
    }
    changeCSS('#sunday', "sunday's Labour.html");
    changeCSS('#monday', "monday's Labour.html");
    changeCSS('#tuesday', "tuesday's Labour.html");
    changeCSS('#wednesday', "wednesday's Labour.html");
    changeCSS('#thursday', "thursday's Labour.html");
    changeCSS('#friday', "friday's Labour.html");
    changeCSS('#saturday', "saturday's Labour.html");
    },15000);
  });
  //$('#sunday').trigger('click'); 
});



