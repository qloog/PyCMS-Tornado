var gbks = gbks || {};

gbks.Signup = function() { 
	
	this.init = function() {
    //$('.wrapSignupForm input[name=name]').focus();
    
    var inputs = $('#maincontent input');
    inputs.focus($.proxy(this.onFocusInput, this));
    inputs.blur($.proxy(this.onBlurInput, this));
  };
  
  this.onFocusInput = function(event) {
    var field = $(event.currentTarget);
    var value = field.val();
    var placeholder = field.attr('placeholder');
    if(placeholder && placeholder.length > 0) {
      if(value == placeholder) {
        field.val('');
        if(placeholder.toLowerCase() == 'password') {
        }
        field.addClass('active');
      }
    }
    
    var name = field.attr('name');
    if(name == 'pastaDummy') {
      var parent = field.parent();
      parent.addClass('active');
      $('#maincontent input[type=password]').focus();
    }
  };
  
  this.onBlurInput = function(event) {
    var field = $(event.currentTarget);
    var value = field.val();
    var placeholder = field.attr('placeholder');
    if(placeholder && placeholder.length > 0) {
      if(value == '') {
        field.val(placeholder);
        field.removeClass('active');
      }
    }
    
    var type = field.attr('type');
    if(type == 'password' && value.length == 0) {
      var parent = field.parent();
      parent.removeClass('active');
    }
  };
	
}

$(document).ready(function() {
  var instance = new gbks.Signup();
  instance.init();
});