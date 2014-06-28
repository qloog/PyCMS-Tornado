var gbks = gbks || {};

gbks.Profile = function() { 
  
  this.init = function() {
    $('#formSettings input[name=slug]').focus($.proxy(this.onFocusSlugInput, this));
    $('#formSettings input[name=slug]').blur($.proxy(this.onBlurSlugInput, this));
    $('#formSettings').submit($.proxy(this.onSubmitForm, this));
    this.slugChangeMethod = $.proxy(this.checkProfileName, this);
    
    this.lastNameChecked = null;
    this.checkingName = false;
    this.nameValid = true;
  };
  
  this.onSubmitForm = function(event) {
    if(!this.nameValid) {
      event.preventDefault(); 
      event.stopPropagation();
    }
  };
  
  this.onFocusSlugInput = function(event) {
    event.preventDefault(); 
    event.stopPropagation();
    
    $(document).keyup(this.slugChangeMethod);
  };
  
  this.onBlurSlugInput = function(event) {
    event.preventDefault(); 
    event.stopPropagation();
    
    $(document).unbind('keyup', this.slugChangeMethod);
  };
  
  this.checkProfileName = function(event) {
      if(event) {
      event.preventDefault(); 
      event.stopPropagation();
    }
    
    var input = this.getSlugInput();
    var slug = input.replace(/[^a-z0-9_-]/g, '');
    
    $('#formSettings .slugdisplay .display').html(slug);
    
    var error = '';
    if(slug.length < 3) {
      error = 'Name needs to be at least 3 characters';
    } else if(slug.length > 50) {
      error = 'Name needs to be shorter than 50 characters';
    } else if(input != slug) {
      error = 'Only use numbers, letters, "-" and "_"';
    }
    var isValid = (error == '');
    
    if(isValid) {
      if(!this.checkingName && slug !== this.lastNameChecked) {
        this.checkingName = true;
        this.lastNameChecked = slug;
        this.showLoader('Checking name');
        $.ajax({
          url: '/settings/profile/checkslug',
          data: {slug:slug},
          type: 'POST',
          success: $.proxy(this.onCheckName, this)  
        });
      }  
      $('#formSettings .slugerror').slideUp();
    } else {
      $('#formSettings .slugerror').html(error);
      $('#formSettings .slugerror').slideDown();
    }
  };
  
  this.getSlugInput = function() {
    return $('#formSettings input[name=slug]').val();
  };
  
  this.onCheckName = function(data) {
    this.checkingName = false;
    this.hideLoader();
    var input = this.getSlugInput();
    if(input !== this.lastNameChecked) {
      this.checkProfileName(null);
    } else {
      this.nameValid = (data!=='1');
      if(this.nameValid) {
        $('#formSettings .slugerror').slideUp();
      } else {
        $('#formSettings .slugerror').html('This name is already taken');
        $('#formSettings .slugerror').slideDown();
      }
    }
  };
  
  this.showLoader = function(message) {
    if(!this.loader || this.loader.length == 0) {
      this.loader = $('#loader');
    }
    
    this.loader.stop();
    
    if(message && message.length > 0) {
      this.loader.html(message);
    } else {
      this.loader.html('');
    }
    
    this.loader.show();
    this.loader.animate({opacity:1}, 50);
  };
  
  this.hideLoader = function() {
    this.loader.stop();
    var callback = null;
    if(this.onHideLoader) {
      callback = $.proxy(this.onHideLoader, this);
    }
    this.loader.animate({opacity:0}, 250, callback);
  };
  
  this.onHideLoader = function(event) {
    this.loader.hide();
  };
  
}

var profile;
$(document).ready(function(){
  profile = new gbks.Profile();
  profile.init();
});
