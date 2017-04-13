(function(){
  var jquery_version = '2.1.4';
  var site_url = 'http://127.0.0.1:8000/';
  var static_url = site_url + 'static/';
  // 爬取的图片的最小宽和高
  var min_width = 100;
  var min_height = 100;

  function bookmarklet(msg) {
    // 加载CSS文件 using a random number as parameter to avoid the browser's cache
    var css = jQuery('<link>');
    css.attr({
      rel: 'stylesheet',
      type: 'text/css',
      href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
    });
    jQuery('head').append(css);

    // 加载HTML
    box_html = '<div id="bookmarklet">' +
                  '<a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1>' +
                  '<div class="images"></div>' +
              '</div>';
    jQuery('body').append(box_html);

	  // 关闭bookmarklet
	  jQuery('#bookmarklet #close').click(function(){
      jQuery('#bookmarklet').remove();
	  });

    // each遍历每一张图片，符合宽高要求的图片加载到<div class="images"></div>中
    // img[src$="jpg"] selector 寻找网站中所有img标签，并且src属性的值以jpg结尾
    jQuery.each(jQuery('img[src$="jpg"]'), function(index, image) {
      if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height)
      {
        image_url = jQuery(image).attr('src');
        jQuery('#bookmarklet .images').append('<a href="#"><img src="'+ image_url +'" /></a>');
      }
    });

    // when an image is selected open URL with it
    jQuery('#bookmarklet .images a').click(function(e){
      selected_image = jQuery(this).children('img').attr('src');
      // hide bookmarklet
      jQuery('#bookmarklet').hide();
      // open new window to submit the image
      window.open(site_url +'image/create/?url='
                  + encodeURIComponent(selected_image)
                  + '&title=' + encodeURIComponent(jQuery('title').text()),
                  '_blank');
    });

  };
  // Check if jQuery is loaded
  if(typeof window.jQuery != 'undefined') {
    bookmarklet();
  } else {
    // Check for conflicts
    var conflict = typeof window.$ != 'undefined';
    // Create the script and point to Google API
    var script = document.createElement('script');
    script.setAttribute('src','http://ajax.googleapis.com/ajax/libs/jquery/' + jquery_version + '/jquery.min.js');
    // Add the script to the 'head' for processing
    document.getElementsByTagName('head')[0].appendChild(script);
    // Create a way to wait until script loading
    var attempts = 15;
    (function(){
      // Check again if jQuery is undefined
      if(typeof window.jQuery == 'undefined') {
        if(--attempts > 0) {
          // Calls himself in a few milliseconds
          window.setTimeout(arguments.callee, 250)
        } else {
          // Too much attempts to load, send error
          alert('An error ocurred while loading jQuery')
        }
      } else {
          bookmarklet();
      }
    })();
  }

})()
