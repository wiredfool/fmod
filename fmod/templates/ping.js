<script type='text/javascript'>
var pingQueue = new Array();
var inPing = false;
var timeoutId=0;

function addClickHandlers(){
	$('#d_pings').find('a.mod').live('click',
	function(e){
		e.preventDefault();
		var effect_container = $(this).parent().parent();
		var err_container = $(this).parent();
		$.post($(this).attr('href'), {moderation:'mod'}, function(resp){
			   if (resp=='Success') {
				   effect_container.hide("slow", check_empty_pings )
				   getNextPing()
			   } else {
				   err_container.append("<br />There was an error: "+resp)
			   }
		})
	})
}

function check_empty_pings(){
	if ($('#d_pings .d_ping_image:visible').length) {
		if (timeoutId) {
			window.clearTimeout(timeoutId);
		}
		if ($('#d_nopings:visible').length) {
			$('#d_nopings').hide()
			$('#d_addpings').show()
		}
	} else {
		if ($('#d_addpings:visible').length) {
			$('#d_addpings').hide()
			$('#d_nopings').show()
		}
	}
}

function refresh_pings() {
	timeoutId = window.setTimeout("getNextPing()",60000);
}

/*// find last child of #d_pings
 // post its id to /ping/more/id
 // append that to the #d_pings div
 */
function getOnePing(pid){
	if (inPing) {
		pingQueue.push(getNextPing);
		return;
	} else {
		inPing=true;
	}
	$.get("/${request.path.split('/')[1]}/more/"+pid,"",
		  function(data,status){
			  if (data=='' && status=='success') {
				  pingQueue = new Array();
				  inPing=false;
				  check_empty_pings();
				  if ($('#d_pings .d_ping_image:visible').length < 3) {
					  refresh_pings();
				  }
			  } else {
				  $('#d_pings').append(data);
				  check_empty_pings();
				  inPing=false;
				  if (pingQueue.length) {
					  pingQueue.shift()();
				  } else {
					  if ($('#d_pings .d_ping_image:visible').length < 3) {
						  getNextPing();
					  }
				  }
			  }
		  })
}

function getNextPing() {
	getOnePing($('#d_pings div.d_ping_image:last').attr('id'))
}

function onMorePings() {
	pingQueue.push(getNextPing);
	pingQueue.push(getNextPing);
	pingQueue.push(getNextPing);
	pingQueue.push(getNextPing);
	getNextPing();
}

$(document).ready(addClickHandlers);
$(document).ready(getNextPing);


</script>