/**
 * Author: Justin Clayton
 */

'use strict';
(function() {
  $(document).ready(init);

  /** Initialize the JS to control page behavior */
  function init() {
    $('#pw_confirm').on('input', onCheckPW);
    $('#first_name, #last_name').on('input', onCheckName);
    $('#email').on('input', onCheckEmail);
  }

  /** Validate that pws match before sending to registration. */
  function onCheckPW() {
    if ($(this).val() === $('#pw').val()) {
      this.setCustomValidity('');
    } else {
      this.setCustomValidity('Passwords must match.');
    }
  }

  /** Validates name fields */
  function onCheckName() {
    let re = new RegExp('^[a-zA-Z]{2,45}')
    if (re.test($(this).val())) {
      this.setCustomValidity('')
    } else {
      this.setCustomValidity('Name must be between 2 and 45 characters.')
    }
  }

  /** Check if email is available */
  function onCheckEmail() {
    if ($(this).val().length > 0) {
      $.get(`/check_email/${$(this).val()}`)
      .done((data) => {
        $('#email-valid').removeClass('hidden');
        $('#email-valid').removeClass('text-success');
        $('#email-valid').removeClass('text-danger');
        if (data === 'available') {
          $('#email-valid').text('Email is available');
          $('#email-valid').addClass('text-success');
        } else {
          $('#email-valid').text('Email is unavailable');
          $('#email-valid').addClass('text-danger');
        }
      });
    }
  }
})();
