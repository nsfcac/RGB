var j = jQuery_1_4_2


function displayClusterInfo(data){
  j("#result").text(JSON.stringify(data, undefined, 10));
        j(document).ready(function() {
          j('#result').each(function(i, e) {hljs.highlightBlock(e)});
       });
}


j(function() {
  j('a#get-cluster-data').bind('click', function() {
    j.getJSON('/show_data_center_info', function(data) {
        displayClusterInfo(data)
      });
      return false;
    });
  });


function ValidateIPaddress(inputText) {
  var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  if(inputText.value.match(ipformat)) {
    document.form1.text1.focus();
    return true;
  }
  else {
    alert("You have entered an invalid IP address!");
    document.form1.text1.focus();
    return false;
  }
}


j(function() {
  j('a#save').bind('click', function() {
    j.getJSON('/post_cluster_info', {
    device_name: j('input[name="device_name"]').val(),
    device_type: j('#device_type').find('option:selected').text(),
    ip: j('input[name="ip"]').val(),
    port: j('input[name="port"]').val(),
    mac_address: j('input[name="mac_address"]').val()
  }, function(data) {
    if(data == "ip error"){
      alert("Please enter a valid ip address")
    }else if(data == "mac error"){
      alert("Please enter a valid mac address")
    }else if(data == "port error"){
      alert("Please enter a valid port number")
    }else {
      $("#alert").css("display", "block");
      setTimeout("$('#alert').css('display', 'none');", 2000)
    }
  });
  return false;
  });
});