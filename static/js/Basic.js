$(document).ready(function(){
    var host = "http://localhost:";
	var port="8080";
	var webservice="/BooksOnline/rest";
	var loginservice="/login";
	var bookservice="/books";
	var bookAdservice = "/bookAd";
	var STATUS = "status";
	var ERRMSG = "errmsg";


    function handleSuccess(data, status)
	{
		alert("In success callback");
	}
	function handleFail(data, status)
	{
		alert("In fail callback");
	}
	function doAjaxGet(params)
	{
		console.log("called doAjaxget");
		var url = params['url'];
		console.log("url:"+url);
		console.log("data:"+params['data']);
		var successCallback = params['successCallbackFunction'];
		var failureCallback = params['failureCallbackFunction'];
		jQuery.ajax({
			type: 'get',
			url: url,
			success: successCallback,
			error: failureCallback
		});
	}
    function doAjaxPost(params)
	{
		console.log("called doAjaxPost");
		var url = params['url'];
		var data=params['data'];
		var successCallback = params['successCallbackFunction'];
		var failureCallback = params['failureCallbackFunction'];

		jQuery.ajax({
		    url: params['url'],
		    type: 'post',
		    //headers: {"Authentication": "Bearer " + localStorage.getItem("token") , "x-auth": localStorage.getItem("x-auth")},
		    data: params['data'],
		    dataType: 'json',
		    contentType: "application/json; charset=utf-8",
		    success:successCallback,
		    error:failureCallback
		});
	}
    $("#loginformsubmitbutton").click(function() {
        var ans = $('#qna input:radio:checked').val();
        alert("sss:"+ana);
        var que = 1;
        var data = JSON.stringify({
            "QNo": que,
            "Ans": ans,
        });

       var params = {};
        params['url'] = host + port + webservice + loginservice + "/validate";
        params['data'] = data;
        params['successCallbackFunction'] = handleSuccess;
        params['failureCallbackFunction'] = handleFail;
        doAjaxGet(params);
    });
});