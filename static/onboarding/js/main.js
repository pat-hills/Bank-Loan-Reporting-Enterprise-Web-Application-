
$(document).ready(function() {
  $("input[name$='financialSituation']").click(function() {
      var financialValue = $(this).val();
      if(financialValue == 'Yes') {
           $('.debtAmountCustomer').show();           
      }

      else {
           $('.debtAmountCustomer').hide();   
      }
  });
});