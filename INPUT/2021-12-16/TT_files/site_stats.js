/**
 * Renders Site Stats using AngularJS
 */
var json = {};
var app = angular.module('site_stats_display', [])
  .controller('SiteStatsDisplay', function ($scope, $http, $log) {
    // Set default values for our form fields.
    $scope.desc = 'sitedesc_stats_stats';
    $scope.site = 'site_stats_stats';

    $scope.change = function () {
      // Fetch the data from sites/default/files
      var url = Drupal.settings.basePath + 'sites/default/files/' + $scope.desc + '.json';
      $http.get(url).
        success(function (data, status, headers, config) {
          $scope.name1 = $scope.desc;
          $scope.meta = data.meta;
          $scope.main_data = data;

          //User Stats
          var users = nice_numbers(data.user.value, true);
          $scope.users = users.val;
          $scope.users_postfix = users.postfix;
          $scope.users_number = numberWithCommas(data.user.value);


          //Task Stats
          var submissions = nice_numbers(data.comment_do.value, true);
          $scope.submissions = submissions.val;
          $scope.submissions_postfix = submissions.postfix;
          $scope.submission_number = numberWithCommas(data.comment_do.value);

          var tasks = nice_numbers(data.do.value, true);
          $scope.tasks = tasks.val;
          $scope.tasks_postfix = tasks.postfix;

          //Discussions Stats
          var comments = nice_numbers(data.comment_discuss.value, true);
          $scope.comments = comments.val;
          $scope.comments_postfix = comments.postfix;
          $scope.comment_number = numberWithCommas(data.comment_discuss.value);

          var discussions = nice_numbers(data.discuss.value, true);
          $scope.discussions = discussions.val;
          $scope.discussions_postfix = discussions.postfix;

          //Poll Vote highlighted Stats
          var poll_survey_submission = nice_numbers(data.poll_votes.value, true);
          $scope.poll_survey_submission = poll_survey_submission.val;
          $scope.poll_survey_postfix = poll_survey_submission.postfix;

          //Poll Vote detail block
          var poll_counts = nice_numbers(data.poll_survey.value, true);
          $scope.poll_counts = poll_counts.val;
          $scope.vote_number = numberWithCommas(data.poll_votes.value);

          //Quiz Stats
          var participants = nice_numbers(data.quiz_counts.participation, true);
          $scope.participants = participants.val;
          $scope.participants_postfix = participants.postfix;
          $scope.participation_number = numberWithCommas(data.quiz_counts.participation);

          var quizes = nice_numbers(data.quiz_counts.quiz_live_count, true);
          $scope.quizes = quizes.val;
          $scope.quizes_postfix = quizes.postfix;

          //Pledge Stats
          var pledgestaken = nice_numbers(data.pledge_counts.pladge_taken, true);
          $scope.pledgestaken = pledgestaken.val;
          $scope.pledgestaken_postfix = pledgestaken.postfix;
          $scope.pledges_number = numberWithCommas(data.pledge_counts.pladge_taken);

          var pledges = nice_numbers(data.pledge_counts.total_pledge_count, true);
          $scope.pledges = pledges.val;
          $scope.pledges_postfix = pledges.postfix;

        }).
        error(function (data, status, headers, config) {
          // Log an error in the browser's console.
          $log.error('Could not retrieve data from ' + url);
        });
    };

    $scope.site_change = function () {
      // Fetch the data from sites/default/files
      var url = Drupal.settings.basePath + 'sites/default/files/' + $scope.site + '.json';
      $http.get(url).
        success(function (data, status, headers, config) {
          $scope.name2 = $scope.site;
          $scope.meta_site = data.meta;
          $scope.main_data_site = data;

          if ($scope.main_data_site.poll.latest_poll_nid == null) {
            $scope.show_poll_ticker = false;
          } else {
            $scope.show_poll_ticker = true;
          }

          var poll_choices = "";
          for (var item in $scope.main_data_site.poll.latest_poll_choices) {
            poll_choices += $scope.main_data_site.poll.latest_poll_choices[item].weight + ". " + $scope.main_data_site.poll.latest_poll_choices[item].chtext + ", ";
          }
          $scope.pollchoice = poll_choices;


          //Group Stats
          var groups = nice_numbers(data.group.value, true);
          $scope.groups = groups.val;
          $scope.groups_postfix = groups.postfix;

          //Do Stats
          var do_count = nice_numbers(data.do.value, true);
          $scope.do_count = do_count.val;
          $scope.do_extra_stats = data.do.extra_stats;
          $scope.do_count_postfix = do_count.postfix;

          //Discuss Stats
          var discuss_count = nice_numbers(data.discuss.value, true);
          $scope.discuss_count = discuss_count.val;
          $scope.discuss_extra_stats = data.discuss.extra_stats;
          $scope.discuss_count_postfix = discuss_count.postfix;

          //Blog Stats
          var blog_count = nice_numbers(data.blog.value, true);
          $scope.blog_count = blog_count.val;
          $scope.blog_count_postfix = data.blog.postfix;

          //Poll Stats
          var poll_count = nice_numbers(data.poll.value, true);
          $scope.poll_count = poll_count.val;
          $scope.poll_count_postfix = poll_count.postfix;

          //Talk Stats
          var talk_count = nice_numbers(data.talk.value, true);
          $scope.talk_count = talk_count.val;
          $scope.talk_extra_stats = data.talk.extra_stats;
          $scope.blog_count_postfix = blog_count.postfix;

          //User Stats
          var user_count = nice_numbers(data.user.value, true);
          $scope.user_count = user_count.val;
          $scope.user_count_postfix = user_count.postfix;
        }).
        error(function (data, status, headers, config) {
          // Log an error in the browser's console.
          $log.error('Could not retrieve data from ' + url);
        });
    };

    // Trigger form submission for first load.
    $scope.change();
    //$scope.site_change();

  });

function nice_numbers(num, format) {
  format = format || false;
  var postfix = '';
  // first strip any formatting;
  num = parseFloat(num.toString().replace(",", ""));

  // is this a number?
  if (isNaN(num)) return false;

  // now filter it;
  if (parseFloat(num) > parseFloat(1000000000000)) {
    output = (parseFloat(num) / 1000000000000).toFixed(2);
    $postfix = 'T';
  } else if (parseFloat(num) > parseFloat(1000000000)) {
    output = (parseFloat(num) / 1000000000).toFixed(2);
    postfix = 'B';
  }
  //else if(parseFloat(num)>parseFloat(1000000)) {
  //output = (parseFloat(num)/1000000).toFixed(2);
  //postfix = 'M';
  // } 
  else if (parseFloat(num) > parseFloat(100000)) {
    output = (parseFloat(num) / 100000).toFixed(2);
    var units = Drupal.t('Lakh');
    postfix = ' + ' + units;
  } else {
    output = parseFloat(num);
  }
  if (format) {
    json.postfix = postfix;
    json.val = output;
    //console.log('format'+json.val , output, postfix);
    return json;
  } else {
    return output;
  }
}

function numberWithCommas(x) {
  var parts = new Intl.NumberFormat('en-IN', { maximumSignificantDigits: 15 }).format(x);
  return parts;
}
