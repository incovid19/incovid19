(function ($) {
  // Store the original beforeSerialize, as we want to continue using
  // it after we've overridden it.
  Drupal.ajax.prototype.originalBeforeSerialize = Drupal.ajax.prototype.beforeSerialize;

  /**
   * Override core's beforeSerialize.
   *
   * We switch to using GET if this is for an ajax View.
   * We also avoid adding ajax_html_id and ajax_page_state.
   * (This happens in core's beforeSerialize).
   */
  Drupal.ajax.prototype.beforeSerialize = function (element, options) {

    // @See Drupal.ajax.prototype.beforeSerialize
    if (this.form) {
      var settings = this.settings || Drupal.settings;
      Drupal.detachBehaviors(this.form, settings, 'serialize');
    }

    // If this is for a view, switch to GET.
    if (options.url &&
      options.url.indexOf('/views/ajax') !== -1 &&
      Drupal.settings.viewsAjaxGet &&
      $.inArray(options.data.view_name, Drupal.settings.viewsAjaxGet) !== -1) {
      options.type = 'GET';
      return;
    }

    return this.originalBeforeSerialize(element, options);
  };

})(jQuery);
