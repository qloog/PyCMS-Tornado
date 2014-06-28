var gbks = gbks || {};

/**
 * Interaction for polaroid-style display of images.
 */
gbks.Password = function() { 
  
  this.init = function() {
    this.form = $('#formPassword');
    this.form.submit($.proxy(this.onSubmitForm, this));
    
    console.log('stuff', this.form);
  };
  
  this.onSubmitForm = function(event) {
    var oldInput = $('input[name=currentpassword]', this.form);
    var newInput = $('input[name=newpassword]', this.form);
    var verifyInput = $('input[name=verifypassword]', this.form);
    
    var oldPass = oldInput.val();
    var newPass = newInput.val();
    var verifyPass = verifyInput.val();
    
    var minLength = 4;
    var isValid = (oldPass.length > minLength && newPass.length > minLength && verifyPass.length > minLength);
    isValid = (isValid && newPass == verifyPass);
    
    console.log('onSubmitForm', isValid);
    
    var container = $('#main .wrapSettingsForm');
    if(isValid) {
      container.removeClass('invalid');
    } else {
      container.addClass('invalid');
      
      event.preventDefault();
      event.stopPropagation();
    }
  };
	
}

var instance;
$(document).ready(new function(){
  instance = new gbks.Password();
  instance.init();
});
