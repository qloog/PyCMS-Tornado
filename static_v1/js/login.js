var gbks = gbks || {};

gbks.Login = function() { 
	
	this.init = function() {
    $('.wrapSignupForm input[name=email]').focus();
  };
	
}

$(document).ready(function() {
  var instance = new gbks.Login();
  instance.init();
});