$.tts = function(data) {
    var lrm = data[0];
    var stats = data[1];
    $.each(['l','r'],function() {
        $("#d"+this).text(lrm[this]); $("#"+this).val(lrm[this]);
    });
    $.each(['correct','incorrect','answered'],function() {
        $("#"+this).text(stats[this]);
    });
    $("#msg").text(lrm.msg || "");
    $("#a").val("");
}
$.badRequest = function() {
	$("#msg").text("Please provide a numerical answer.")
	$("#a").val("");
}
$(document).ready(function(){
    $("form#t").submit(function() {
        var inputs = {};
        $.ajax({
            data: $(":input").serializeArray(),
            dataType: "json",
            type: 'POST',
            url: this.action,
            error: function(XMLHttpRequest,textStatus,errorThrown) {
				if(XMLHttpRequest.status == 400) {
					$.badRequest();
				}
            },
            success: function(data,statusText) {
                $.tts(data);
            }
        });
        return false;
    });
});

