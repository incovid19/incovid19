$(document).ready(function () {
  var loaderDash = '<div class="text-center" style="padding-top:10px;"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>';
  // stateSummary();
  // districtwiseTotalVaccine('Health');
  districtwiseVaccine('Total')
  // vaccineCumulatedSummary('Health');
  // vaccineCumulatedSummaryCitizen('Citizen')
});

  var loaderDash = '<div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>';
var loader = '<div class="h-100 d-flex align-items-center justify-content-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>';

$.ajaxSetup({
  headers: {
    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
  }
});

function stateSummary() {
  var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';

  $("#statewiseVaccineStatus").html(loader);
  $.ajax({
    url: "vaccine-ajax/stateSummary",
    method: 'get',
    data: {},
    success: function (result) {
      $("#statewiseVaccineStatus").html(result);
    }
  });
}

function districtwiseVaccine(type) {
  // var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';
  $(".statewideVaccinationCoverageTable").html(loader);
  $("#mapVaccineDataType").val(type);
  $("#vac-Dose0-tab").click();
  $("#vaccineTotalDose").html(loaderDash);
  $("#vaccineFirstDose").html(loaderDash);
  $("#vaccineSecondDose").html(loaderDash);
  vaccineMapData('intTotalDose');
  $.ajax({
    url: "vaccine-ajax/districtwiseVaccine",
    method: 'get',
    data: { 'type': type },
    success: function (result) {
      $(".statewideVaccinationCoverageTable").html(result);
    }
  });
}
function districtwiseTotalVaccine(type) {
  var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';
  $(".districtwiseTotalVaccine").html(loader);
  $.ajax({
    url: "vaccine-ajax/districtwiseTotalVaccine",
    method: 'get',
    data: { 'type': type },
    success: function (result) {
      $(".districtwiseTotalVaccine").html(result);
    }
  });
}

/**
 * Function for Get Vaccination Summary Cumulative Graph for Health
 */
function vaccineCumulatedSummary(type) {
  var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';
  $(".vaccineCumulatedSummary").html(loader);
  $.ajax({
    url: "vaccine-ajax/vaccineCumulatedSummary",
    method: 'get',
    data: { 'type': type },
    success: function (result) {
      $(".vaccineCumulatedSummary").html(result);
    }
  });
}


/**
 * Function for Get Vaccination Summary Cumulative Graph for Health
 */
function vaccineCumulatedSummaryCitizen(type){
  var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';
  $(".vaccineCumulatedSummaryCitizen").html(loader);
  $.ajax({
    url: "vaccine-ajax/vaccineCumulatedSummary",
    method: 'get',
    data: { 'type': type },
    success: function (result) {
      $(".vaccineCumulatedSummaryCitizen").html(result);
    }
  });
}