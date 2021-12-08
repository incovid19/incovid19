$( document ).ready(function() {
    var loaderDash = '<div class="text-center" style="padding-top:10px;"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>';
    $("#conformedGraph").html(loaderDash); 
    $("#activeGraph").html(loaderDash); 
    $("#recoveredGraph").html(loaderDash);  
    $("#deceasedGraph").html(loaderDash); 
    conformedGraph();
    deceasedGraph();
    recoveredGraph(); 
    activeGraph(); 
    setHelplineType(1);
    infectedDailySummary();
    mobileInfectedSection();
    hovertooltip('intActive');
    statewiseInfection();
    mobileInfectedMap();

    setTimeout(function(){
        sampleTestedGraph();      
        heatMapCareMain();
        // heatMapTmcMain();
        heatMapHospitalMain('Current');
    },1000);

    setTimeout(function(){
        // callReturnFrom();
        populationSummary(); 
        infectedAgeGroupSummary();
        // passengerByRoad('state');        
    },3000);

}); 

var loader = '<div class="h-100 d-flex align-items-center justify-content-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>';

$.ajaxSetup({
  headers: {
    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
  }
});

function showTmc(){
  // showDistrictWiseBed();
  heatMapTmcMain();
}

function showCare(){
  showDistrictWiseBed();
  heatMapHospitalMain();
}

function showHospital(str){
  showDistrictWiseBed(str);
  heatMapHospitalMain(str);
}

function showInfectionRatio() {
  $("#infectionTableDiv").removeClass("d-none");
   showInfectionRatioTable();
   showInfectionRatioMap();
}

function showInfectionRatioTable(){    
    $("#heat-map-table-view1").html(loader); 
    $.ajax({
      url: "ajax/showInfectionRatioTable",
      method: 'get',
      data: {},
      success: function(result){
         $("#heat-map-table-view1").html(result);           
    }});
}

function showInfectionRatioMap(){   
    $("#map_section").hide(); 
    $("#heatMapDiv").show(); 
    $("#heatMapDiv").html(loader);            
    $.ajax({
      url: "ajax/showInfectionRatioMap",
      method: 'get',
      data: {},
      success: function(result){
         $("#heatMapDiv").html(result);            
    }});
}

function mobileInfectedMap(){    
    // var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';
    $("#heat-map-table-view1").html(loader); 
    $.ajax({
      url: "ajax/mobileInfectedMap",
      method: 'get',
      data: {},
      success: function(result){
         $("#heat-map-table-view1").html(result);           
    }});
}

function setHelplineType(intType) {
  $("#helpline_type").val(intType);
  helpline();
}

function helpline(){    
    // var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';
    $("#helpdesk-portlet").html(loader); 
    var intType = $("#helpline_type").val();
    var distrct_id = $("#helpline_district").val();
    var vchName = $("#helpline_hospital").val();
    $.ajax({
      url: "ajax/helpline",
      method: 'get',
      data: {'intType':intType,'distrct_id':distrct_id,'vchName':vchName},
      success: function(result){
         $("#helpdesk-portlet").html(result);           
    }});
}

function districtSummary(){ 
  var loader = '<div class="card dashboard-card" style="min-height:200px;"><h4>District Summary</h4><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';

   $("#districtSummaryGraph").html(loader);  
    $.ajax({
      url: "ajax/districtSummary",
      method: 'get',
      data: {},
      success: function(result){
         $("#districtSummaryGraph").html(result);    
    }});
}

function statewiseInfection(){ 
  var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';

   $("#statewise-data").html(loader);  
    $.ajax({
      url: "ajax/statewiseInfection",
      method: 'get',
      data: {},
      success: function(result){
         $("#statewise-data").html(result);    
    }});
}

function populationSummary(){ 
  var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';

   $("#populationsRatioDiv").html(loader);  
    $.ajax({
      url: "ajax/populationSummary",
      method: 'get',
      data: {},
      success: function(result){
         $("#populationsRatioDiv").html(result);    
    }});
}

function infectedDailySummary(){    
  $("#infectiondaywise").html(loader);  
    $.ajax({
      url: "ajax/infectedDailySummary",
      method: 'get',
      data: {},
      success: function(result){
         $("#infectiondaywise").html(result);           
    }});
}

function infectedCumulatedSummary(){  
//   $("#infecionHeading").html("Infected Summary");  
   $("#infectionGraph").html(loader);  
    $.ajax({
      url: "ajax/infectedCumulatedSummary",
      method: 'get',
      data: {},
      success: function(result){
         $("#infectionGraph").html(result);            
    }});
}

function infectedTotalCumulatedSummary(){  
//   $("#infecionHeading").html("Infected Summary");  
   $("#infectionGraph").html(loader);  
    $.ajax({
      url: "ajax/infectedTotalCumulatedSummary",
      method: 'get',
      data: {},
      success: function(result){
         $("#infectionGraph").html(result);            
    }});
}

function outboundCallSummary(){   

    var loader = '<div class="col-md-12" ><div class="card dashboard-card" style="min-height:200px;">   <div class="card dashboard-card outbond-section">      <h4>Outbound Call Summary</h4></div><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div></div>';

    $("#outboundGraph").html(loader);  
    $.ajax({
      url: "ajax/outboundCallSummary",
      method: 'get',
      data: {},
      success: function(result){
         $("#outboundGraph").html(result);           
    }});
}

function inboundCallSummary(){    
   $("#inboundGraph").html(loader);  
    $.ajax({
      url: "ajax/inboundCallSummary",
      method: 'get',
      data: {},
      success: function(result){
         $("#inboundGraph").html(result);           
    }});
}

function heatMap(str){    
    var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';
    $("#heatMapDiv").html(loader);            
    $.ajax({
      url: "ajax/heatMapMain",
      method: 'get',
      data: {'data':str},
      success: function(result){
         $("#heatMapDiv").html(result);            
    }});
}

function heatBlockMap(str){    
    var loader = '<div class="card dashboard-card" style="min-height:200px;"><h4>Block Wise Heat Map</h4><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';
    $("#heatBlockMapDiv").html(loader);  
    $.ajax({
      url: "ajax/heatBlockMapMain",
      method: 'get',
      data: {'data':str},
      success: function(result){
         $("#heatBlockMapDiv").html(result);            
    }});
}

function conformedGraph(){    
   
    $.ajax({
      url: "ajax/conformedGraph",
      method: 'get',
      data: {},
      success: function(result){
         $("#conformedGraph").html(result);   
                
    }});
}

function activeGraph(){    
    $.ajax({
      url: "ajax/activeGraph",
      method: 'get',
      data: {},
      success: function(result){
         $("#activeGraph").html(result);          
    }});
}

function recoveredGraph(){    
    $.ajax({
      url: "ajax/recoveredGraph",
      method: 'get',
      data: {},
      success: function(result){
         $("#recoveredGraph").html(result); 

    }});
}

function deceasedGraph(){    
    $.ajax({
      url: "ajax/deceasedGraph",
      method: 'get',
      data: {},
      success: function(result){
         $("#deceasedGraph").html(result);   
           
    }});
}

function sampleTestedGraph(){    
    $.ajax({
      url: "ajax/sampleTestedGraph",
      method: 'get',
      data: {},
      success: function(result){
         $("#sampleTestedGraph").html(result);           
    }});
}

function quarantineRunning(){    
    $.ajax({
      url: "ajax/quarantineRunning",
      method: 'get',
      data: {},
      success: function(result){
         $("#actQurntGraph").html(result);           
    }});
}

function quarantineCompleted(){    
    $.ajax({
      url: "ajax/quarantineCompleted",
      method: 'get',
      data: {},
      success: function(result){
         $("#qurntOverGraph").html(result);           
    }});
}

function heatMapHospitalMain(type){    
    var loader = '<div class="card dashboard-card" style="min-height:200px;"><div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div>';
    if(type!='Current'){
         $("#heatMapHospitalUpcoming").html(loader);            
        }else{
          $("#heatMapHospital").html(loader); 
        }

    $.ajax({
      url: "ajax/heatMapHospitalMain",
      method: 'get',
      data: {'type':type},
      success: function(result){
        if(type!='Current'){
         $("#heatMapHospitalUpcoming").html(result);     
         $("#heatMapHospital").html("");       
        }else{
         $("#heatMapHospitalUpcoming").html("");     
         $("#heatMapHospital").html(result);            
        }
    }});
}

function blockInfectedMap(){    
      $("#blocktable-view-heat").html(loader); 
      $.ajax({
            url: "ajax/blockInfectedMap",
            method: 'get',
            data: {'intDistrictId':$('#mapBlockDistrictId').val()},
            success: function(result){
               $("#blocktable-view-heat").html(result);           
            }
      });
}

function heatMapCareMain(){    
    $("#heatCovidCare").html(loader);
    $.ajax({
      url: "ajax/heatMapCareMain",
      method: 'get',
      data: {},
      success: function(result){
         $("#heatCovidCare").html(result);     
    }});
}

function heatMapTmcMain(){    
    $("#heatCovidTmc").html(loader);
    $.ajax({
      url: "ajax/heatMapTmcMain",
      method: 'get',
      data: {},
      success: function(result){
         $("#heatCovidTmc").html(result);  
         showDistrictWiseTmcBed();   
    }});
}

function showDistrictWiseTmcBed(){
    $("#distwisetmcbed").html(loader);
    $.ajax({
      url: "ajax/showDistrictWiseTmcBed",
      method: 'get',
      data: {},
      success: function(result){
         $("#distwisetmcbed").html(result);     
    }});
}

function infectedGenderSummary(){    
//   $("#infecionHeading").html("Infected Summary");  
   $("#genderGroup").html(loader);  
    $.ajax({
      url: "ajax/infectedGenderSummary",
      method: 'get',
      data: {},
      success: function(result){
         $("#genderGroup").html(result);           
    }});
}

function infectedAgeGroupSummary(){    
//   $("#infecionHeading").html("Infected Summary");  
   $("#ageGroup").html(loader);  
    $.ajax({
      url: "ajax/infectedAgeGroupSummary",
      method: 'get',
      data: {},
      success: function(result){
         $("#ageGroup").html(result);           
    }});
}

function mobileInfectedSection(){    
//   $("#infecionHeading").html("Infected Summary");  
   $("#mobileInfectionData").html(loader); 
    $.ajax({
      url: "ajax/mobileInfectedSection",
      method: 'get',
      data: {},
      success: function(result){
         $("#mobileInfectionData").html(result);           
    }});
}

function updateFcmUser(fcmId){
    var deviceType = '';  
    if (window.matchMedia("(max-width: 767px)").matches)  
    { 
      var deviceType = 'Mobile';
    } else { 
        var deviceType = 'Web';
    } 
    $.ajax({
      url: "ajax/setNotificationUsers",
      method: 'post',
      dataType: "text",
      data: {
        "vchFcmid":fcmId,
        "vchType":deviceType,
        "vchTopic":"covidupdates"
      },
      success: function(result){
        if(result.trim()=='SUCC'){
          setTokenSentToServer(1);
        }        
    }});
}

function setTokenSentToServer(sent) {
  window.localStorage.setItem('sentToServer', sent ? '1' : '0');
}
function sendTokenToServer(currentToken) {
  if (!isTokenSentToServer()) {
    console.log('Sending token to server...');
  // TODO(developer): Send the current token to your server.
    setTokenSentToServer(true);
  } else {
    console.log('Token already sent to server so won\'t send it again ' +
      'unless it changes');
  }
}
function isTokenSentToServer() {
  return window.localStorage.getItem('sentToServer') === '1';
}

function subscribeTokenToTopic(token, topic) {
  fetch('https://iid.googleapis.com/iid/v1/'+token+'/rel/topics/'+topic, {
    method: 'POST',
    headers: new Headers({
      'Authorization': 'key=AAAAs9qRhUc:APA91bG5rHZuXxmXXn8Q3vDO3GL-23DZhvaYSF-dGNb621JtCutdmtaX2zlgyE3sfilAudmNym-3JVwnplvRd7rBL8RWkCIqTBrQ9ZT5QXpvFDzhZpmhjv71OtEmoQT6A6dzLbgAFA_l'
    })
  }).then(response => {
    if (response.status < 200 || response.status >= 400) {
      throw 'Error subscribing to topic: '+response.status + ' - ' + response.text();
    }
    console.log('Subscribed to "'+topic+'"');
    updateFcmUser(token);
  }).catch(error => {
    console.error(error);
  })
}

function callReturnFrom() {
  returnToOdisha('Flight');
  returnToOdishaTrain();
}

function returnToOdisha(str){   
    $("#returnBy"+str).html(loader);  
    $.ajax({
      url: "ajax/returnToOdisha",
      method: 'get',
      data: {'mode':str},
      success: function(result){
         $("#returnBy"+str).html(result);           
    }});
}

function returnToOdishaTrain(){   
    $("#returnToOdishaTrain").html(loader);  
    $.ajax({
      url: "ajax/returnToOdishaTrain",
      method: 'get',
      data: {'mode':'Train'},
      success: function(result){
         $("#returnByTrain").html(result);           
    }});
}

function passengerByRoad(str){   
  $(".statewise-roadreturnee").addClass('statewise-datashowhide');  
  $(".distwise-roadreturnee").addClass('distwise-datashowhide');   
    if(str=="state"){
    $(".statewise-roadreturnee").html(loader);  
        
    }else{          
     $(".distwise-roadreturnee").html(loader);   
             
    }

    $.ajax({
      url: "ajax/passengerByRoad",
      method: 'get',
      data: {'type':str},
      success: function(result){
        if(str=="state"){
         $(".statewise-roadreturnee").html(result); 
         $(".statewise-roadreturnee").removeClass('statewise-datashowhide');           
        }else{          
         $(".distwise-roadreturnee").html(result);  
         $(".distwise-roadreturnee").removeClass('distwise-datashowhide');         
        }
    }});
}

function showDistrict() {
  document.location = $("#base_url_id").val()+"/district/"+$("#dashboardDistrictsId option:selected").text();
}

function showDistrictMobile() {
  document.location = $("#base_url_id").val()+"/district/"+$("#dashboardDistrictsMobileId option:selected").text();
}

function showTesting(str) {
  if(str=='local'){
    $("#localOdishaTexting").show();
    $("#populationsRatioDiv").hide();
  }else{
    $("#localOdishaTexting").hide();
    $("#populationsRatioDiv").show();
    populationSummary();
  }
}